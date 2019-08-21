import os
import subprocess
import sys
import tempfile

import pytest

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
)

import fetch


def test_get_working_folder_no_arg():
    result = fetch.get_working_folder([])

    assert isinstance(result, (str, os.PathLike))
    assert os.getcwd() == result, result


def test_get_working_folder_file():
    result = fetch.get_working_folder([os.path.dirname(__file__)])

    assert isinstance(result, (str, os.PathLike))
    assert os.path.dirname(__file__) == result, result


@pytest.fixture(scope="module")
def umbrella():
    with tempfile.TemporaryDirectory() as folder:

        assert os.path.exists(folder)

        # prepare a test folder
        sub_folder_00 = tempfile.TemporaryDirectory(dir=folder)
        sub_folder_01 = tempfile.TemporaryDirectory(dir=folder)
        sub_folder_git_00 = tempfile.TemporaryDirectory(dir=folder)
        sub_folder_git_01 = tempfile.TemporaryDirectory(dir=folder)

        temp_file_00 = tempfile.TemporaryFile(dir=folder)
        temp_file_01 = tempfile.TemporaryFile(dir=folder)

        subprocess.check_call(['git', 'init'], cwd=sub_folder_git_00.name)
        subprocess.check_call(['git', 'init'], cwd=sub_folder_git_01.name)

        # let test use the temp folder
        yield {
            "top": folder, 
            "folder": [
                sub_folder_00.name,
                sub_folder_01.name,
                sub_folder_git_00.name,
                sub_folder_git_01.name,
            ],
            "repos": [
                sub_folder_git_00.name,
                sub_folder_git_01.name,
            ],
            "files": [
                temp_file_00,
                temp_file_01,
            ]
        }

        del sub_folder_git_01
        del sub_folder_git_00
        del sub_folder_01
        del sub_folder_00

        # after use, the folder is expected to be removed

    assert not os.path.exists(folder)


        # after use, remove the folder
        folder.cleanup()


if "__main__" == __name__:
    pytest.main()
