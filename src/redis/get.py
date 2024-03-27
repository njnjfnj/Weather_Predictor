from json import dumps, loads
from redis import Redis

from utils.utils import construct_offsets, construct_result, construct_cities_count

hash_table_city_keys = ['country',
                'zip_code',
                'lon',
                'lat',
                'utc_time_difference']

def connect_to_redis(host, port):
    return Redis(host=host, port=port)

def construct_searchable_city_name(city_name):
    city_name = city_name.replace("_", " ")
    splitted = city_name.split(" ")
    prepared_name = ''
    for e in splitted:
        prepared_name += e.lower().capitalize() + " "
    
    return prepared_name.strip() + "*"


def get_city(city_name, page=0, limit=None):
    offsets, start, end = {}, 0, 0

    offsets = construct_offsets(page=page, limit=limit)
    start = int(offsets["start"])
    end = int(offsets["end"])

    redis_cnt = connect_to_redis(host="redis", port="6379")
    
    res = []

    prepared_name = construct_searchable_city_name(city_name)

    try:
        c, city_matches = list(redis_cnt.zscan(name="city_names", cursor=0, match=prepared_name))
        if len(city_matches) == 0:
            c, city_matches = list(redis_cnt.zscan(name="city_names", cursor=0, match=prepared_name[:-1]))
        if end >= len(city_matches):
            if start >= len(city_matches):
                total_pages = (len(city_matches) // limit) + (len(city_matches) % limit > 0)
                return construct_result([], f"Invalid pagination parameters: requested page ({page}) exceeds available data (total pages: {total_pages})")
            city_matches = city_matches[start:]
        elif (start != end):
            city_matches = city_matches[start:end] 
        
        for city, index in city_matches:
            arr = redis_cnt.hmget(name=city, keys=tuple(hash_table_city_keys))
        
            res.append({"name": city.decode("UTF-8")})
            for i in range(len(hash_table_city_keys)):
                res[-1][hash_table_city_keys[i]] = arr[i].decode("UTF-8")
        
        return construct_result(res)

    except Exception as e:
        return construct_result(res, e)
    
def get_all_cities(page, limit):
    offsets, start, end = {}, 0, 0

    offsets = construct_offsets(page=page, limit=limit)
    start = int(offsets["start"])
    end = int(offsets["end"])

    r = connect_to_redis(host="redis", port="6379")
    res = []
    try:
        c, keys = list(r.zscan(name="city_names", cursor=0, match="*"))
        if end >= len(keys):
            if start >= len(keys):
                total_pages = (len(keys) // limit) + (len(keys) % limit > 0)
                return construct_result([], f"Invalid pagination parameters: requested page ({page}) exceeds available data (total pages: {total_pages})")
            keys =  keys[start:-1]
        elif (start != end): keys = keys[start:end] 

        for key, index in keys:
            arr = r.hmget(name=key, keys=tuple(hash_table_city_keys))
            res.append({"name": key.decode("UTF-8")})
            for i in range(len(hash_table_city_keys)):
                res[-1][hash_table_city_keys[i]] = arr[i].decode("UTF-8")
            
        return construct_result(res)
    
    except Exception as e:
        return construct_result(res, e)


def get_number_of_cities(city_name):
    r = connect_to_redis(host="redis", port="6379")
    city_name = city_name.replace("_", " ")
    splitted = city_name.split(" ")
    prepared_name = ''
    for e in splitted:
        prepared_name += e.lower().capitalize() + " "
    res = 0
    prepared_name = prepared_name.strip() + "*"
    try:
        c, keys = list(r.zscan(name="city_names", cursor=0, match=prepared_name))
        if len(keys) == 0:
            c, keys = list(r.zscan(name="city_names", cursor=0, match=prepared_name[:-1]))
        return construct_cities_count(len(keys))
    except Exception as e:
        return construct_cities_count(res, e)
    


def check_city_name(city_name):
    match = get_city(city_name)
    match = loads(match)["result"][0]["name"]
    if match:
        if match.lower() == city_name.lower(): 
            return True
    return False

from datetime import datetime
from math import ceil

def match_time_difference(city_name, model_last_index):
    match = get_city(city_name)
    match = loads(match)["result"][0]
    time_difference = match["utc_time_difference"]
    curr_city_time = datetime.now(datetime.UTC)

    if time_difference[0] == '-':
        time_difference = int(time_difference[1:]) * -1
    else: time_difference = int(time_difference)

    return (int(ceil(((curr_city_time - model_last_index).total_seconds() / 3600))) + time_difference)
