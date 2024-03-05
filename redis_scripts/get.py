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

def construct_offsets(page, limit):
    start = (page*limit - 1) - (limit - 1)
    end_non_inclusive = page*limit
    return {"start": start, "end": end_non_inclusive}

def get_city(city_name, page=0, limit=None):
    offsets, start, end = {}, 0, 0
    if limit and limit > 0:
        offsets = construct_offsets(page=page, limit=limit)
        start = int(offsets["start"])
        end = int(offsets["end"])

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
        if len(keys) == 0:
            c, keys = list(r.zscan(name="city_names", cursor=0, match=prepared_name[:-1]))
        if end >= len(keys):
            if start >= len(keys):
                total_pages = (len(keys) // limit) + (len(keys) % limit > 0)
                return construct_result([], f"Invalid pagination parameters: requested page ({page}) exceeds available data (total pages: {total_pages})")
            keys = keys[start:]
        elif (start != end):
            keys = keys[start:end] 
        

        for key, index in keys:
            arr = r.hmget(name=key, keys=tuple(hash_table_keys))
        
            res.append({"name": key.decode("UTF-8")})
            for i in range(len(hash_table_keys)):
                res[-1][hash_table_keys[i]] = arr[i].decode("UTF-8")
        
        return construct_result(res)

    except Exception as e:
        return construct_result(res, e)
    
def get_all_cities(page, limit):
    offsets, start, end = {}, 0, 0
    if limit and limit > 0:
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
            arr = r.hmget(name=key, keys=tuple(hash_table_keys))
            res.append({"name": key.decode("UTF-8")})
            for i in range(len(hash_table_keys)):
                res[-1][hash_table_keys[i]] = arr[i].decode("UTF-8")
            
        return construct_result(res)
    
    except Exception as e:
        return construct_result(res, e)
