from git import Repo
import os
import re


class BeatricaDiffTracker:
    def __init__(self, repo_path=None, base_branch='main', head_branch="HEAD"):
        if repo_path is None:
            repo_path = os.getcwd()
        self.repo = Repo(repo_path)
        self.base_branch = base_branch
        self.head_branch = head_branch
        self.commit_changes = {}

    def get_file_content_from_commit(self, commit, file_path):
        try:
            blob = commit.tree / file_path
            return blob.data_stream.read().decode('utf-8').splitlines()
        except KeyError:
            return []

    def get_commits_between(self):
        return list(self.repo.iter_commits(f"{self.base_branch}..{self.head_branch}"))

    def parse_diff(self, diff_bytes):
        diff = diff_bytes.decode('utf-8')
        old_lines = []
        new_lines = []
        old_line_num = None
        new_line_num = None

        for line in diff.split('\n'):
            if line.startswith('@@'):
                m = re.match(r'@@ -(\d+),?\d* \+(\d+),?\d* @@', line)
                if m:
                    old_line_num = int(m.group(1))
                    new_line_num = int(m.group(2))
            elif line.startswith('-') and not line.startswith('---'):
                old_lines.append({"line number": old_line_num, "line content": line[1:]}) if old_line_num is not None else None
                old_line_num += 1 if old_line_num is not None else None
            elif line.startswith('+') and not line.startswith('+++'):
                new_lines.append({"line number": new_line_num, "line content": line[1:]}) if new_line_num is not None else None
                new_line_num += 1 if new_line_num is not None else None
            else:
                old_line_num += 1 if old_line_num is not None else 0
                new_line_num += 1 if new_line_num is not None else 0

        return old_lines, new_lines

    def analyze_commits(self):
        commits = self.get_commits_between()

        for commit in commits:
            diff_index = commit.parents[0].diff(commit, create_patch=True) if commit.parents else []
            for diff_item in diff_index:
                change_detail = self.process_diff_item(commit, diff_item)

                if commit.hexsha not in self.commit_changes:
                    self.commit_changes[commit.hexsha] = {
                        "commit_message": commit.message.strip(),
                        "changes": []
                    }

                self.commit_changes[commit.hexsha]["changes"].append(change_detail)

    def process_diff_item(self, commit, diff_item):
        change_detail = {
            "commit_hash": commit.hexsha,
            "commit_message": commit.message.strip(),
            "file_path": diff_item.b_path or diff_item.a_path,
            "file_name": os.path.basename(diff_item.b_path or diff_item.a_path),
            "old_file_path": "",
            "change_type": "",
            "old_lines": [],
            "new_lines": [],
        }

        if diff_item.new_file:
            lines = self.handle_new_file(diff_item, commit)
            change_detail["new_lines"] = [{"line number": i + 1, "line content": line.strip()} for i, line in enumerate(lines)]
            change_detail["change_type"] = "A"
        elif diff_item.deleted_file:
            change_detail["change_type"] = "D"
        elif diff_item.renamed_file:
            change_detail["change_type"] = "R"
            change_detail["old_file_path"] = diff_item.rename_from
            change_detail["file_path"] = diff_item.rename_to
        else:
            old_lines, new_lines = self.parse_diff(diff_item.diff)
            change_detail["old_lines"] = old_lines
            change_detail["new_lines"] = new_lines
            change_detail["change_type"] = "M"
        return change_detail

    def handle_new_file(self, diff_item, commit):
        try:
            with open(diff_item.b_path, 'r') as f:
                lines = f.readlines()
        except FileNotFoundError:
            lines = self.get_file_content_from_commit(commit.parents[0] if commit.parents else commit,
                                                      diff_item.a_path or diff_item.b_path)
        return lines

