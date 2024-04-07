[![PyPI version](https://badge.fury.io/py/beatrica-git.svg)](https://badge.fury.io/py/beatrica-git)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://static.pepy.tech/badge/beatrica-git)](https://pepy.tech/project/beatrica-git)

# Beatrica Git

`beatrica-git` is a Python package designed for analyzing git differences between branches in a local repository. It helps developers and project managers to easily track and visualize changes, fostering better understanding and collaboration within teams.

## Installation

To install `beatrica-git`, use pip:

```bash
pip install beatrica-git
```

## Usage

`beatrica-git` is straightforward to use. Below are examples demonstrating how to analyze and retrieve recent commit changes between branches.

### Analyzing Commit Changes

```python
from beatrica_git.recent_change_inspector import BeatricaDiffTracker

# Initialize the analyzer for a specific repository path (optional) and branch
beatrica_diff_tracker = BeatricaDiffTracker(base_branch='master')

# Perform the analysis
beatrica_diff_tracker.analyze_commits()

# Retrieve and print the commit changes
commit_changes = beatrica_diff_tracker.commit_changes
print(commit_changes)
```

This example shows how to instantiate the `BeatricaDiffTracker` and analyze commit changes between the `master` branch and the `HEAD`. It's possible to specify a repository path; otherwise, the current working directory is used.

## Features

- Easy retrieval and analysis of commit differences between two branches.
- Support for analyzing changes in local git repositories.
- Detailed breakdown of additions, deletions, and modifications in each commit.
- Customizable for different base and head branches.
- Simplified API for easy integration into development workflows and tools.

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/chigwell/beatrica-git/issues).

## License

This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).
