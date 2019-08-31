import os
import re
import subprocess
import sys


def main(argv):

    assert argv

    tags = subprocess.check_output(['git', 'tag'], cwd=argv[0], encoding='utf-8')
    tags_list = tags.splitlines()

    print(tags_list)


def get_tags_list(folder):
    assert os.path.exists(folder)
    assert os.path.isdir(folder)

    tags = subprocess.check_output(['git', 'tag'], cwd=folder, encoding='utf-8')
    return tags.splitlines()


def filter_date_tags(tags_list):
    result = []

    for tag in tags_list:
        if tag.startswith("18") or tag.startswith("19"):
            if '/' != tag[2]:
                result.append(tag)

    return result


def convert_date_tag(tag):

    sep = '/'

    assert 6 > len(tag)

    join_this = [tag[:2], tag[2:4], tag[4:6],]

    if 6 < len(tag):
        join_this.append(tag[6:].strip('_').strip('-').strip(sep))

    return sep.join(join_this)


def get_remotes_list(folder):
    assert os.path.exists(folder)
    assert os.path.isdir(folder)

    remotes = subprocess.check_output(['git', 'remote'], cwd=folder, encoding='utf-8')
    return remotes.splitlines()


def git_tag(folder, old_tag, new_tag, remotes_list=[]):
    subprocess.check_call(['git', 'checkout', old_tag], cwd=folder)
    subprocess.check_call(['git', 'tag', new_tag], cwd=folder)
    subprocess.check_call(['git', 'tag', '--delete', old_tag], cwd=folder)
    subprocess.check_call(['git', 'tag', '--delete', old_tag], cwd=folder)

    for remote in remotes_list:
        subprocess.check_call(['git', 'push', remote, '--delete', old_tag])


if "__main__" == __name__:
    main(sys.argv[1:])
