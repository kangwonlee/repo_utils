"""
Fetch subfolders

What it does:
Fetches git repositores of the given folder or the current working directory.

How to use 00 :
$ cd <to a folder containing multiple repositories>
$ python fetch.py

How to use 01 "
$ python fetch.py <folder containing git repositories>

"""


import multiprocessing
import os
import random
import subprocess
import sys


def main(argv):

    working_folder = get_working_folder(argv)

    git_repo_list = list(gen_git_repo(working_folder))

    assert git_repo_list

    random.shuffle(git_repo_list)

    assert all(list(map(os.path.exists, git_repo_list)))

    pool = multiprocessing.Pool(multiprocessing.cpu_count())

    print(f"fetching {len(git_repo_list)} repos with {multiprocessing.cpu_count()} processes")

    result = all(
        pool.map(
            repeat_this,
            git_repo_list,
        )
    )

    print(f"finished fetching {len(git_repo_list)} repos with {multiprocessing.cpu_count()} processes")

    pool.close()
    pool.join()

    return result


def gen_git_repo(working_folder):
    return filter(
        lambda folder: is_git_repo(folder),
        gen_folder(working_folder)
    )


def is_git_repo(folder):
    return os.path.exists(get_git_config_path(folder))


def get_git_config_path(folder):
    return os.path.join(folder, '.git', 'config')


def gen_folder(working_folder):
    return filter(lambda item: os.path.isdir(item), gen_item_full_path(working_folder))


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
