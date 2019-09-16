import argparse
import os
import re
import subprocess
import sys


def main(argv=sys.argv):
    p = get_argparse()
    ns = p.parse_args(argv[1:])

    tags_list = get_tags_list(ns.folder)

    remotes_list = get_remotes_list(ns.folder)

    branch = get_current_branch(ns.folder)

    for old_tag in filter_date_tags(tags_list):
        new_tag = convert_date_tag(old_tag)

        git_tag(ns.folder, old_tag, new_tag, tags_list, remotes_list)

    switch_to_branch(ns.folder, branch)
    subprocess.check_call(['git', 'push', 'origin', '--tags'], cwd=ns.folder)


def get_argparse() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="add /s in date tag",
    )

    p.add_argument('folder', type=str, help="local repository folder")
    p.add_argument('--dry-run', action='store_true', default=False)

    return p


def get_current_branch(folder):
    return subprocess.check_output(['git', 'branch', '--show-current'], cwd=folder, encoding='utf-8').strip()


def switch_to_branch(folder, new_branch):
    return subprocess.check_output(['git', 'switch', new_branch], cwd=folder, encoding='utf-8')


def get_tags_list(folder):
    assert os.path.exists(folder)
    assert os.path.isdir(folder)

    tags = subprocess.check_output(['git', 'tag'], cwd=folder, encoding='utf-8')
    return tags.splitlines()


def filter_date_tags(tags_list):
    result = []

    for tag in tags_list:
        if tag.startswith("18") or tag.startswith("19") or tag.startswith("17"):
            if '/' != tag[2]:
                result.append(tag)

    return result


def convert_date_tag(tag):

    sep = '/'

    assert 6 <= len(tag), tag

    join_this = [tag[:2], tag[2:4], tag[4:6],]

    if 6 < len(tag):
        join_this.append(tag[6:].strip('_').strip('-').strip('.').strip(sep))

    return sep.join(join_this)


def get_remotes_list(folder):
    assert os.path.exists(folder)
    assert os.path.isdir(folder)

    remotes = subprocess.check_output(['git', 'remote'], cwd=folder, encoding='utf-8')
    return remotes.splitlines()


def git_tag(folder, old_tag, new_tag, tags_list, remotes_list=[]):
    print(' '.join(['git', 'checkout', old_tag]))
    subprocess.check_call(['git', 'checkout', old_tag], cwd=folder)
    if new_tag not in tags_list:
        print(' '.join(['git', 'tag', new_tag]))
        subprocess.check_call(['git', 'tag', new_tag], cwd=folder)
    print(' '.join(['git', 'tag', '--delete', old_tag]))
    subprocess.check_call(['git', 'tag', '--delete', old_tag], cwd=folder)

    for remote in remotes_list:
        print(' '.join(['git', 'push', '--delete', remote, old_tag]))
        subprocess.run(['git', 'push', '--delete', remote, old_tag], cwd=folder)


if "__main__" == __name__:
    main(sys.argv)
