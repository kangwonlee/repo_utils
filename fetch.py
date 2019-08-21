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

    working_folder = get_working_folder(argv)

    gen_folder = filter(lambda item: os.path.isdir(item), gen_item_full_path(working_folder))

    git_repo_list = list(
        filter(
            lambda folder: os.path.exists(os.path.join(os.path.join(folder), '.git', 'config')),
            gen_folder
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


def gen_item_full_path(working_folder):
    return map(lambda item: os.path.join(working_folder, item), os.listdir(working_folder))


def get_working_folder(argv):
    if not argv:
        argv = [os.getcwd()]

    working_folder = os.path.abspath(argv[0])

    assert os.path.exists(working_folder)
    return working_folder


def repeat_this(repo, cmd=['git', 'fetch', '--all'], b_verbose=True):
    if b_verbose:
        print(f"{repo} ".ljust(75, '='))

    return subprocess.check_call(cmd, cwd=repo)


if "__main__" == __name__:
    main(sys.argv[1:])
