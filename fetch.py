import os
import random
import subprocess


def main():
    folders = get_folders()

    for folder in folders:

        print(f"{folder} ".ljust(60, '='))
        subprocess.check_call(['git', 'fetch', '--all'], cwd=folder)


def get_folders():
        folders = [item for item in os.listdir(os.curdir) if (
                    os.path.isdir(item) and is_git_repository(item)
                )]
        random.shuffle(folders)
        return folders


def is_git_repository(folder):
        local_repo = os.path.join(folder, '.git')
        return os.path.exists(local_repo) and os.path.isdir(local_repo)


if "__main__" == __name__:
    main()
