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
import random
import subprocess
import sys


def main(argv):

    if not argv:
        argv = [os.getcwd()]

    working_folder = os.path.abspath(argv[0])

    assert os.path.exists(working_folder)

    item_full_path_list = list(map(lambda item: os.path.join(working_folder, item), os.listdir(working_folder)))

    folder_list = list(
        filter(
            lambda item: os.path.isdir(item),
            item_full_path_list
        )
    )

    git_repo_list = list(
        filter(
            lambda folder: os.path.exists(os.path.join(os.path.join(folder), '.git', 'config')),
            folder_list
        )
    )

    assert git_repo_list

    random.shuffle(git_repo_list)

    assert all(map(os.path.exists, git_repo_list))

    return all(
        list(
            map(
                repeat_this,
                git_repo_list,
            )
        )
    )


def repeat_this(repo, cmd=['git', 'fetch', '--all'], b_verbose=True):
    if b_verbose:
        print(f"{repo} ".ljust(75, '='))

    return subprocess.check_call(cmd, cwd=repo)


if "__main__" == __name__:
    main(sys.argv[1:])
