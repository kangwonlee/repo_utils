import os
import subprocess
import sys


def main(argv):

    assert argv
    assert os.path.exists(argv[0])

    tags = subprocess.check_output(['git', 'tag'], cwd=argv[0], encoding='utf-8')
    tags_list = tags.splitlines()

    print(tags_list)


if "__main__" == __name__:
    main(sys.argv[1:])
