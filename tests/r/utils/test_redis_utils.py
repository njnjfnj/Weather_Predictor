import pytest
from src.redis.utils.utils import (construct_result, construct_offsets,
                                   construct_cities_count)

from json import loads

@pytest.mark.parametrize(('passed_array', 'passed_error', 'expected_result'),
                         [([], str("No cities found"), {"result": [], "status": "error", "message": str("No cities found")}),
                        ([{"name": "Los Angeles", "country": "US"}], '', {"result": [{"name": "Los Angeles","country": "US"}], "status": "success"})])
def test_construct_result(passed_array, passed_error, expected_result):
    res = construct_result(passed_array, passed_error)
    assert expected_result == loads(res)

@pytest.mark.parametrize(('page', 'limit', 'expected_result', "success"),
                         [(0, 1, {"start": 0, "end": 1}, 1),
                        (3, 12, {"start": 24, "end": 36}, 1),
                        (2, 0, "'limit' must an integer value > 0", 0),
                        (-1, 0, "'page' must an integer value >= 0", 0)])
def test_construct_offsets(page, limit, expected_result, success):
    if not success:
        with pytest.raises(Exception) as e_info:
            construct_offsets(page, limit)
        assert expected_result in str(e_info.value)
    else:
        res = construct_offsets(page, limit)
        assert res == expected_result
        

@pytest.mark.parametrize(
    "amount, expected_status, expected_message",
    [
        (10, "success", None),
        (0, "error", "No matching cities found"),
        (0, "error", "Custom Error Message"),
    ],
)
def test_construct_cities_count(amount, expected_status, expected_message):
    output = construct_cities_count(amount, e=expected_message if expected_message else "")
    output_dict = loads(output)

    assert output_dict["status"] == expected_status
    if expected_message:
        assert output_dict["message"] == expected_message
    else:
        assert "message" not in output_dict

def test_construct_cities_count_invalid_input():
    with pytest.raises(TypeError):
        construct_cities_count("invalid")