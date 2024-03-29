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


@pytest.fixture(scope="session")
def umbrella(tmpdir_factory):
    folder = tmpdir_factory.mktemp("umbrella")

    assert os.path.exists(folder)

    # prepare a test folder tree
    # https://doc.pytest.org/en/latest/tmpdir.html#the-tmpdir-factory-fixture

    sub_folder_00 = os.path.join(folder, 'sub_00')
    sub_folder_01 = os.path.join(folder, 'sub_01')
    sub_folder_git_00 = os.path.join(folder, 'repo_00')
    sub_folder_git_01 = os.path.join(folder, 'repo_01')

    os.mkdir(sub_folder_00)
    os.mkdir(sub_folder_01)
    os.mkdir(sub_folder_git_00)
    os.mkdir(sub_folder_git_01)

    assert os.path.exists(sub_folder_00), sub_folder_00
    assert os.path.exists(sub_folder_01), sub_folder_01
    assert os.path.exists(sub_folder_git_00), sub_folder_git_00
    assert os.path.exists(sub_folder_git_01), sub_folder_git_01

    assert os.path.isdir(sub_folder_00), sub_folder_00
    assert os.path.isdir(sub_folder_01), sub_folder_01
    assert os.path.isdir(sub_folder_git_00), sub_folder_git_00
    assert os.path.isdir(sub_folder_git_01), sub_folder_git_01

    subprocess.check_call(['git', 'init'], cwd=sub_folder_git_00)
    subprocess.check_call(['git', 'init'], cwd=sub_folder_git_01)

    temp_file_00 = os.path.join(folder, 'tmp_00')
    temp_file_01 = os.path.join(folder, 'tmp_01')

    with open(temp_file_00, 'w') as tf_00:
        tf_00.write("")
    with open(temp_file_01, 'w') as tf_01:
        tf_01.write("")

    assert os.path.exists(temp_file_00), temp_file_00
    assert os.path.exists(temp_file_01), temp_file_01

    return {
        "top": folder,
        "folder": (
            sub_folder_00,
            sub_folder_01,
            sub_folder_git_00,
            sub_folder_git_01,
        ),
        "repos": (
            sub_folder_git_00,
            sub_folder_git_01,
        ),
        "files": (
            temp_file_00,
            temp_file_01,
        )
    }


def test_umbrella(umbrella):
    assert os.path.exists(umbrella["top"])
    assert umbrella['folder']
    assert umbrella['repos']
    assert os.path.exists(umbrella['repos'][0])

    for folder in umbrella['folder']:
        assert os.path.exists(folder), folder

    for folder in umbrella['repos']:
        assert os.path.exists(folder), folder
        assert os.path.exists(
            os.path.join(folder, '.git', 'config')
        ), folder


def test_gen_item_full_path(umbrella):
    assert umbrella['repos']
    assert os.path.exists(umbrella['repos'][0])

    result = fetch.gen_item_full_path(umbrella['top'])

    expected_list = list(umbrella['folder'] + umbrella['files'])

    assert expected_list

    for item in result:
        assert os.path.exists(item), item
        expected_list.remove(item)

    assert not expected_list


def test_gen_folder(umbrella):
    assert umbrella['repos']
    assert os.path.exists(umbrella['repos'][0])

    result = fetch.gen_folder(umbrella['top'])

    expected_list = list(umbrella['folder'])

    assert expected_list

    for item in result:
        assert os.path.isdir(item), item
        expected_list.remove(item)

    assert not expected_list


def test_gen_git_repo(umbrella):
    assert umbrella['repos']
    assert os.path.exists(umbrella['repos'][0])

    result = fetch.gen_git_repo(umbrella['top'])

    expected_list = list(umbrella['repos'])

    assert expected_list

    for item in result:
        assert os.path.isdir(item), item
        expected_list.remove(item)

    assert not expected_list


def test_is_git_repo(umbrella):
    assert umbrella['repos'], umbrella
    assert os.path.exists(umbrella['repos'][0])

    for item in umbrella['repos']:
        assert fetch.is_git_repo(item)


def test_get_git_config_path(umbrella):
    result = fetch.get_git_config_path(umbrella['repos'][0])
    assert os.path.exists(result), result


if "__main__" == __name__:
    pytest.main()
