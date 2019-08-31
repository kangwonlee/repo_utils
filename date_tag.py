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


if "__main__" == __name__:
    main(sys.argv[1:])
