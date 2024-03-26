import pytest
from src.redis.utils.utils import construct_result

from json import loads

@pytest.mark.parametrize(('passed_array', 'passed_error', 'expected_result'),
                         [([], str("No cities found"), {"result": [], "status": "error", "message": str("No cities found")}),
                        ([{"name": "Los Angeles", "country": "US"}], '', {"result": [{"name": "Los Angeles","country": "US"}], "status": "success"})])
def test_construct_result(passed_array, passed_error, expected_result):
    res = construct_result(passed_array, passed_error)
    assert expected_result == loads(res)