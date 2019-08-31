import os
import sys

import pytest

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
)


import date_tag as dt


def test_get_tags_list():
    result = dt.get_tags_list(os.path.dirname(__file__))
    assert isinstance(result, list)


if "__main__" == __name__:
    pytest.main()
