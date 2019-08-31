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


@pytest.fixture(scope='module')
def samples_input():
    return (
        "18/02/12/package/00", "18/05/23/package/00", "18/08/12/01", 
        "18/09/04/01_chapter_order", "18102501", "18103001", "18110501", 
        "181121_q", "181130/repair_direction_field", "now", "test_matrix", 
        "181201/posix_nt__each_file", "19040901", "19041001", "19060901", 
        "19081701", "2nd_int_bug", "2nd_order_int", "60-linalg2/181125/01", 
        "build/195", "build/249", "cantilever_test", "float_limit", "issue#7", 
        "issue_#11", "nmisp-20-181201", "nmisp-50-181201", "readme", 
        "nmisp-50/relative_error", "nmisp/19060901", "nmisp/actions", 
        "nmisp/badge-workflows", "nmisp/release/test02", "request", 
        "nmisp/requirements-2019-07", "nmisp/update-workflows-19083101", 
        "travis", "try_these", "wk00",
    )


@pytest.fixture(scope='module')
def samples_output():
    return (
        "18102501", "18103001", "18110501", "181121_q", 
        "181130/repair_direction_field",
        "181201/posix_nt__each_file", "19040901", "19041001", "19060901", 
        "19081701",
    )


def test_filter_date_tags(samples_input, samples_output):
    result = dt.filter_date_tags(samples_input)

    assert set(result) == set(samples_output)


if "__main__" == __name__:
    pytest.main()
