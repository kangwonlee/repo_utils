import os
import re
import subprocess
import sys


def main(argv):
    assert argv

    folder = argv[0]

    tags_list = get_tags_list(folder)

    remotes_list = get_remotes_list(folder)

    branch = get_current_branch(folder)

    for old_tag in filter_date_tags(tags_list):
        new_tag = convert_date_tag(old_tag)

        git_tag(folder, old_tag, new_tag, tags_list, remotes_list)

    switch_to_branch(folder, branch)
    subprocess.check_call(['git', 'push', 'origin', '--tags'], cwd=folder)


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
        join_this.append(tag[6:].strip('_').strip('-').strip(sep))

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
    main(sys.argv[1:])
