import os
import sys

import pytest


sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
)

import fetch


if "__main__" == __name__:
    pytest.main()
