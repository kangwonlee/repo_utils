"""
Fetch from subfolders

What it does:
Fetches git repositores under current working directory.
First level only.

How to use:
$ cd <to a folder containing multiple repositories>
$ python fetch.py
"""


import os
import subprocess
import sys


def main(argv):
    folder_gen = filter(os.path.isdir, os.listdir(os.getcwd()))

    git_repo_gen = filter(
        lambda folder: os.path.exists(os.path.join(os.path.join(folder), '.git', 'config')),
        folder_gen
    )

    list(
        map(
            lambda repo: subprocess.check_call(
                ['git', 'fetch', '--all']
                ,cwd=repo
            ),
            git_repo_gen
        )
    )


if "__main__" == __name__:
    main(sys.argv[1:])
