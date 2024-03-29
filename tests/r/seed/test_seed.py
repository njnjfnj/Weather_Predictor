import pytest

from unittest.mock import mock_open, Mock, patch, call

from src.redis.seed.seed import seed_cities, connect_to_redis

@pytest.mark.parametrize(('hset_call_args', 'zadd_call_args'), [
    (
        (
            ('Chicago', {'country': 'USA', 'zip_code': '60601', 'lon': '-87.6298', 'lat': '41.8781', 'utc_time_difference': '-6'}),
            ('Los Angeles', {'country': 'USA', 'zip_code': '90001', 'lon': '-118.2437', 'lat': '34.0522', 'utc_time_difference': '-8'}),
            ('Miami', {'country': 'USA', 'zip_code': '33101', 'lon': '-80.1918', 'lat': '25.7617', 'utc_time_difference': '-5'})
        ),
        (
            ("city_names", {'Chicago': 0}),
            ("city_names", {'Los Angeles': 0}),
            ("city_names", {'Miami': 0})
        )
    )
])
@patch('builtins.open', new_callable=mock_open, read_data='name,country,zip_code,lon,lat,utc_time_difference\nChicago,USA,60601,-87.6298,41.8781,-6\nLos Angeles,USA,90001,-118.2437,34.0522,-8\nMiami,USA,33101,-80.1918,25.7617,-5')
@patch("src.redis.seed.seed.connect_to_redis")
def test_seed_function(r_cnt, mock_open, hset_call_args, zadd_call_args):
    r_mock = Mock()
    r_cnt.return_value = r_mock

    seed_cities()
    
    r_mock.hset.assert_has_calls([call(name, mapping=mapping) for name, mapping in hset_call_args], any_order=True)
    r_mock.zadd.assert_has_calls([call(name, mapping) for name, mapping in zadd_call_args], any_order=True)




