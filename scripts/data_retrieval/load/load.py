import requests
import csv
from os import path, mkdir
from dotenv import load_dotenv, dotenv_values
from datetime import date, datetime, timedelta
from time import sleep, mktime

from transform.transform import transform_into_raw, transform_raw_to_prepared

def load_api_key():
    load_dotenv()
    return dotenv_values()['API_KEY']

API_KEY = load_api_key()

datetime_format = '%Y-%m-%d:%H'

def update_city_info(start_date, end_date, city_row, cities_columns, 
                     raw_weather_data_dir, prepared_weather_data_dir):        
    name_index = cities_columns.index('name')
    lat_index = cities_columns.index('lat')
    lon_index = cities_columns.index('lon')
    
    city_name = city_row[name_index].lower()

    city_time_diff_index = cities_columns.index('utc_time_difference')
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
        next_date = start_date + timedelta(days=13)
        url = f'https://api.weatherbit.io/v2.0/history/hourly?lat={city_row[lat_index]}&lon={city_row[lon_index]}&start_date={start_date.strftime("%Y-%m-%d:%H")}&end_date={next_date.strftime("%Y-%m-%d:%H")}&tz=utc&key={API_KEY}'
        
        start_date = next_date
        unix_start = mktime(start_date.timetuple())

        try:
            res = requests.get(url=url).json()
            transform_into_raw(res, raw_weather_data_dir, prepared_weather_data_dir, city_name)
        except Exception as e:
            print(e)
            break
        sleep(1)

    raw_city_data_dir = path.join(raw_weather_data_dir, city_name)
    if not path.isdir(raw_city_data_dir):
        mkdir(raw_city_data_dir)

    raw_city_data_filename = path.join(raw_city_data_dir, city_name+ '.csv')

    prepared_city_data_dir = path.join(prepared_weather_data_dir, city_name)
    if not path.isdir(prepared_city_data_dir):
        mkdir(prepared_city_data_dir)

    prepared_city_data_filename = path.join(prepared_city_data_dir, city_name+ '.csv')
    
    if not path.isfile(raw_city_data_filename):
        transform_raw_to_prepared(raw_city_data_filename,
                                    prepared_city_data_filename, existed=False)
    else:
        transform_raw_to_prepared(raw_city_data_filename,
                                    prepared_city_data_filename, existed=True)
    

        
        
