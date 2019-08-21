import os
import sys
import tempfile

import pytest

sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
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


if "__main__" == __name__:
    pytest.main()
