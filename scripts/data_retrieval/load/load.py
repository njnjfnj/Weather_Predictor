import requests
import csv
from os import path, mkdir
from dotenv import load_dotenv, dotenv_values
from datetime import date, datetime, timedelta
from time import sleep, mktime

from transform.transform import transform_load_weather_json

def load_api_key():
    load_dotenv()
    return dotenv_values()['API_KEY']

API_KEY = load_api_key()

datetime_format = '%Y-%m-%d:%H'

def update_city_info(start_date, end_date, city_row, cities_columns, city_data_dir):        
    name_index = cities_columns.index('name')
    lat_index = cities_columns.index('lat')
    lon_index = cities_columns.index('lon')
    
    city_time_diff_index = cities_columns.index('time_difference')
    city_time_diff = city_row[city_time_diff_index]

    # if city_time_diff[0] == "-":
    #     city_time_diff = int(city_time_diff[1:])
    #     start_date = start_date - timedelta(hours=city_time_diff)
    #     end_date = end_date - timedelta(hours=city_time_diff)
    # else: 
    #     city_time_diff = int(city_time_diff)
    #     start_date = start_date + timedelta(hours=city_time_diff)
    #     end_date = end_date + timedelta(hours=city_time_diff)
    
    unix_start = mktime(start_date.timetuple())
    unix_end = mktime(end_date.timetuple())

    while unix_start < unix_end:
        next_date = start_date + timedelta(days=14)
        url = f'https://api.weatherbit.io/v2.0/history/hourly?lat={city_row[lat_index]}&lon={city_row[lon_index]}&start_date={start_date.strftime("%Y-%m-%d:%H")}&end_date={next_date.strftime("%Y-%m-%d:%H")}&tz=utc&key={API_KEY}'
        
        start_date = next_date
        unix_start = mktime(start_date.timetuple())

        res = requests.get(url=url).json()
        print(res)
        # transform_load_weather_json(res, city_data_dir, city_row[name_index].lower())
        
        sleep(2)
        
    
        
        
