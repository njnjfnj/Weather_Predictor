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

def get_city(city_name):
    r = connect_to_redis(host="redis", port="6379")
    city_name = city_name.lower().capitalize() + "*"
    res = []
    c, keys = list(r.zscan(name="city_names", cursor=0, match=city_name))  
    for key, index in keys:
        arr = r.hmget(name=key, keys=tuple(hash_table_keys))
        res.append([key.decode("UTF-8")])
        res[-1] = res[-1] + [e.decode("UTF-8") for e in arr]
    try:
        if res:
            return dumps({"match": res})
        else:
            return dumps({"error": "No matching cities found"})
    except Exception as e:
        print(f"Error during get request: {e}")
        return dumps({"error": "An error occurred"})
