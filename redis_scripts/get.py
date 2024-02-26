from json import dumps
from redis import Redis

hash_table_keys = ['country',
                'zip_code',
                'lon',
                'lat',
                'utc_time_difference']

def connect_to_redis(host, port):
    return Redis(host=host, port=port)

cursor = 0

def construct_result(arr, e=''):
    if arr:
        return dumps({"result": arr, "status": "success"})
    else:
        message = e if e != '' else "No matching cities found"
        return dumps({"result": arr, "status": "error", "message": message})


def get_city(city_name):
    r = connect_to_redis(host="redis", port="6379")
    city_name = city_name.replace("_", " ")
    splitted = city_name.split(" ")
    prepared_name = ''
    for e in splitted:
        prepared_name += e.lower().capitalize() + " "
    res = []
    prepared_name = prepared_name.strip() + "*"
    try:
        c, keys = list(r.zscan(name="city_names", cursor=0, match=prepared_name))  
        for key, index in keys:
            arr = r.hmget(name=key, keys=tuple(hash_table_keys))
        
            res.append([key.decode("UTF-8")])
            res[-1] = res[-1] + [e.decode("UTF-8") for e in arr]
        
        return construct_result(res)

    except Exception as e:
        return construct_result(res, e)
    
def get_all_cities():
    r = connect_to_redis(host="redis", port="6379")
    res = []
    try:
        c, keys = list(r.zscan(name="city_names", cursor=0, match="*"))  
        for key, index in keys:
            arr = r.hmget(name=key, keys=tuple(hash_table_keys))
            res.append([key.decode("UTF-8")])
            res[-1] = res[-1] + [e.decode("UTF-8") for e in arr]
            
        return construct_result(res)
    
    except Exception as e:
        return construct_result(res, e)
