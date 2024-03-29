import pytest

from unittest.mock import patch, Mock, call

from src.redis.get.get import (construct_searchable_city_names,
                               get_city, get_all_cities, 
                               get_number_of_cities, check_city_name,
                               match_time_difference)

from json import loads, dumps

@pytest.mark.parametrize(('name', 'expected_result'),
                         [
                             ("New_York", ["New York*", "New York"]),
                             ("new jersey", ["New Jersey*", "New Jersey"]),
                             ("miami", ["Miami*", "Miami"])
                         ])
def test_construct_searchable_city_names(name, expected_result):
    assert tuple(expected_result) == construct_searchable_city_names(name)


@pytest.fixture
def get_city_result():
    return [
        {
            "name": "New York City",
            "country": "USA",
            "zip_code": "10001",  
            "lon": "-74.0060",
            "lat": "40.7128",
            "utc_time_difference": "-5"  
        },
        {
            "name": "Nashville",
            "country": "USA",
            "zip_code": "37201",  
            "lon": "-86.7816",
            "lat": "36.1627",
            "utc_time_difference": "-6" 
        },
        {
            "name": "New Orleans",
            "country": "USA",
            "zip_code": "70112",  
            "lon": "-90.0715",
            "lat": "29.9511",
            "utc_time_difference": "-6"  
        }
    ]



@pytest.mark.parametrize(("city_name", "page", "limit", "zcan_result", "hmget_result"),
    [("N", 0, 3, (0, [(el.encode("UTF-8"), c) for el, c in [("New York City", 0), ("Nashville", 0), ("New Orleans", 0)]]),
    [
        [ el.encode("UTF-8") for el in ["USA", "10001", "-74.0060", "40.7128", "-5"]],
        [ el.encode("UTF-8") for el in ["USA", "37201", "-86.7816", "36.1627", "-6"]],
        [ el.encode("UTF-8") for el in ["USA", "70112", "-90.0715", "29.9511", "-6"]]
    ])]    
    )
@patch("src.redis.get.get.connect_to_redis")
def test_get_city(redis_cnt, city_name, page, limit, zcan_result, hmget_result, get_city_result):
    redis_mock = Mock()
    redis_cnt.return_value = redis_mock

    redis_mock.zscan.return_value = zcan_result
    redis_mock.hmget.side_effect = [el for el in hmget_result]

    result = get_city(city_name, page, limit)

    assert loads(result)["result"] == get_city_result

@pytest.fixture
def get_all_cities_result(get_city_result):
    return get_city_result + [{
                                "name": "Los Angeles",
                                "country": "USA",
                                "zip_code": "90001",  
                                "lon": "-118.2437",
                                "lat": "34.0522",
                                "utc_time_difference": "-8"  
                            },
                            {
                                "name": "Chicago",
                                "country": "USA",
                                "zip_code": "60601",  
                                "lon": "-87.6298",
                                "lat": "41.8781",
                                "utc_time_difference": "-6"  
                            }]



@pytest.mark.parametrize(("page", "limit", "zcan_result", "hmget_result"),
    [(0, 5, (0, [(el.encode("UTF-8"), c) for el, c in [("New York City", 0), ("Nashville", 0), ("New Orleans", 0), ("Los Angeles", 0), ("Chicago", 0)]]),
    [
        [ el.encode("UTF-8") for el in ["USA", "10001", "-74.0060", "40.7128", "-5"]],
        [ el.encode("UTF-8") for el in ["USA", "37201", "-86.7816", "36.1627", "-6"]],
        [ el.encode("UTF-8") for el in ["USA", "70112", "-90.0715", "29.9511", "-6"]],
        [ el.encode("UTF-8") for el in ["USA", "90001", "-118.2437", "34.0522", "-8"]],
        [ el.encode("UTF-8") for el in ["USA", "60601", "-87.6298", "41.8781", "-6"]]
    ])]    
)
@patch("src.redis.get.get.connect_to_redis")
def test_get_all_cities(redis_cnt, page, limit, zcan_result, hmget_result, get_all_cities_result):
    redis_mock = Mock()
    redis_cnt.return_value = redis_mock

    redis_mock.zscan.return_value = zcan_result
    redis_mock.hmget.side_effect = [el for el in hmget_result]

    result = get_all_cities(page, limit)

    assert loads(result)["result"] == get_all_cities_result
    


@pytest.mark.parametrize(("city_name", "zcan_result", "expected_result"),
    [("N", (0, [(el.encode("UTF-8"), c) for el, c in [("New York City", 0), ("Nashville", 0), ("New Orleans", 0)]]), 3)]    
    )
@patch("src.redis.get.get.connect_to_redis")
def test_get_number_of_cities(redis_cnt, city_name, zcan_result, expected_result):
    redis_mock = Mock()
    redis_cnt.return_value = redis_mock

    redis_mock.zscan.return_value = zcan_result

    result = get_number_of_cities(city_name)

    assert loads(result)["result"] == expected_result



@pytest.mark.parametrize(("city_name", "get_city_return_value", "expected_result"),
                         [
                            ("Nashville", 
                            {"result": [{
                                "name": "Nashville",
                                "country": "USA",
                                "zip_code": "37201",  
                                "lon": "-86.7816",
                                "lat": "36.1627",
                                "utc_time_difference": "-6" 
                            }], "status": "success"},
                            True
                            )
                         ])
@patch("src.redis.get.get.get_city")
def test_check_city_name(get_city, city_name, get_city_return_value, expected_result):
    
    get_city.return_value = dumps(get_city_return_value)

    assert check_city_name(city_name) == expected_result


from time import time 
from math import ceil


@pytest.mark.parametrize(('city_name', 'model_last_index', 'expected_result', 'get_city_return_value'),
                         [
                             ("Nashville", '2024-03-28 00:00:00', ceil((time() - 1711584000) / 3600) + (-6), 
                                {"result": [{
                                    "name": "Nashville",
                                    "country": "USA",
                                    "zip_code": "37201",  
                                    "lon": "-86.7816",
                                    "lat": "36.1627",
                                    "utc_time_difference": "-6" 
                                }], "status": "success"}
                            )
                         ])
@patch("src.redis.get.get.get_city")
def test_match_time_difference(get_city, city_name, model_last_index, expected_result, get_city_return_value):
    get_city.return_value = dumps(get_city_return_value)
    assert match_time_difference(city_name, model_last_index) == expected_result