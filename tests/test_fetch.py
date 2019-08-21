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


@pytest.fixture(scope="module")
def umbrella():
    with tempfile.TemporaryDirectory() as folder:

        # let test use the temp folder
        yield folder.name

        # after use, remove the folder
        folder.cleanup()


if "__main__" == __name__:
    pytest.main()
