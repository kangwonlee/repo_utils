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


@pytest.fixture(scope='module')
def converted_output():
    return (
        "18/10/25/01", 
        "18/10/30/01", 
        "18/11/05/01", 
        "18/11/21/q", 
        "18/11/30/repair_direction_field",
        "18/12/01/posix_nt__each_file", 
        "19/04/09/01", 
        "19/04/10/01", 
        "19/06/09/01", 
        "19/08/17/01",
    )


def test_convert_date_tag(samples_output, converted_output):
    for sample_input_tag, expected_output_tag in zip(samples_output, converted_output):
        assert sample_input_tag[:2] == expected_output_tag[:2]
        assert sample_input_tag[2:4] == expected_output_tag[3:5]
        assert sample_input_tag[4:6] == expected_output_tag[6:8]
        result = dt.convert_date_tag(sample_input_tag)
        assert result == expected_output_tag


if "__main__" == __name__:
    pytest.main()
