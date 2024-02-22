from csv import DictReader
from redis import Redis

def connect_to_redis(host, port):
    return Redis(host=host, port=port)

def seed_cities():
    r = connect_to_redis(host="localhost", port="6379")
    with open("../data/cities/cities.csv", "r") as csv_f:
        lines = list(DictReader(csv_f))
        for row in lines:
            name = row['name']
            country = row['country']
            zip_code = row['zip_code']
            lon = row['lon']
            lat = row['lat']
            utc_time_difference = row['utc_time_difference']

            r.hset(name, mapping={
                'country': country,
                'zip_code': zip_code,
                'lon': lon,
                'lat': lat,
                'utc_time_difference': utc_time_difference
            })

            r.zadd('city_names', {name: 0}) 

seed_cities()