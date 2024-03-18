import csv
from dotenv import load_dotenv, dotenv_values
from datetime import datetime, timedelta
from os import path, curdir, mkdir
from load.load import update_city_info


cities_filepath = path.join(curdir, "../../data/cities/cities.csv")
raw_weather_data_dir = path.join(curdir, "../../data/datasets/raw_data/")
prepared_weather_data_dir = path.join(curdir, "../../data/datasets/")

if not path.isdir(raw_weather_data_dir):
    mkdir(raw_weather_data_dir)

if not path.isdir(prepared_weather_data_dir):
    mkdir(prepared_weather_data_dir)

datetime_format = '%Y-%m-%d:%H'

START_DATE = datetime.strptime('2023-04-30:00', datetime_format)
END_DATE = datetime.strptime('2024-03-01:00', datetime_format) 
print(START_DATE, END_DATE)

with open(cities_filepath, 'r') as cities_file:
    cities = list(csv.reader(cities_file, delimiter=',', quotechar='"'))
    cities_columns =  cities[0]
    for i in range(1, len(cities)):
        update_city_info(START_DATE, END_DATE, cities[i], cities_columns, raw_weather_data_dir,
                         prepared_weather_data_dir)
