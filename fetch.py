import os
import random
import subprocess


def main():
    folders = [item for item in os.listdir(os.curdir) if (
                os.path.isdir(item) and os.path.exists(os.path.join(item, '.git'))
            )]
    random.shuffle(folders)

    for folder in folders:

        print(f"{folder} ".ljust(60, '='))
        subprocess.check_call(['git', 'fetch', '--all'], cwd=folder)


if "__main__" == __name__:
    main()
