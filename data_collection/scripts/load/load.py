import requests
import csv
from os import path, mkdir
from dotenv import load_dotenv, dotenv_values
from datetime import date, datetime, timedelta
from time import sleep, mktime

from scripts.transform.transform import transform_weather_json


def update_city_info(start_date, end_date, city_row, cities_columns, city_data_dir, city_weather_columns):        
    name_index = cities_columns.index('name')
    lat_index = cities_columns.index('lat')
    lon_index = cities_columns.index('lon')
    
    city_time_difference = cities_columns.index('time_difference')
        

    time_difference = None
    
    while start_date <= end_date:

        next_date = start_date + timedelta(hours=1) 
        if not time_difference:
            time_difference = int(city_row[city_time_difference][1:]) * -1 if city_row[city_time_difference][0] == '-' else int(city_row[city_time_difference])
            start_date = start_date - timedelta(hours=time_difference)
            next_date = start_date + timedelta(hours=1)
        
        url = f'https://history.openweathermap.org/data/2.5/history/city?lat={city_row[lat_index]}&lon={city_row[lon_index]}&type=hour&start={(mktime(start_date.timetuple()))}&end={(mktime(next_date.timetuple()))}&appid={API_KEY}'
        
        start_date = next_date

        res = requests.get(url=url).json()

        print(res['list'][0]['dt'])

        transofmed_weather = transform_weather_json(res)
        arr = [transofmed_weather]
        
        if path.isdir(city_data_dir):
            city_directory = path.join(city_data_dir, city_row[name_index].lower())
            if not path.isdir(city_directory):
                mkdir(city_directory)

            filename = path.join(city_directory, city_row[name_index].lower() + '.csv')
            existing_data = []
            
            try:
                with open(filename, 'r') as city_file:
                    reader = csv.reader(city_file)
                    existing_data = list(reader)
            except FileNotFoundError:
                existing_data = []

            if not existing_data or not existing_data[0] == city_weather_columns:
                existing_data.insert(0, city_weather_columns)

            existing_data.extend(arr)

            with open(filename, 'w', newline='') as city_file:
                writer = csv.writer(city_file)
                writer.writerows(existing_data)
