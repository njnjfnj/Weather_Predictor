from json import dumps
from redis import Redis

def connect_to_redis(host, port):
    return Redis(host=host, port=port)

def get_city(city_name):
    r = connect_to_redis(host="localhost", port="6379")
    city_name = city_name.lower().encode("utf-8")
    res = r.zrangebylex("city_names", min=city_name, max=city_name + b'\xff')
    try:
        if res: return dumps({"match": res})
        else: return dumps({"error": "No matching cities found"})
    except Exception as e:
        print(f"Error during get request: {e}")
        return dumps({"error": "An error occurred"})
    
print(get_city("Los"))