import csv
from dotenv import load_dotenv, dotenv_values
from datetime import datetime, timedelta
from os import path
from load.load import update_city_info

def load_api_key():
    load_dotenv()
    return dotenv_values()['API_KEY']

API_KEY = load_api_key()
cities_filepath = path.join(path.dirname(__file__), dotenv_values()['CITIES_DIR'])
cities_weather_data_dir = path.join(path.dirname(__file__), dotenv_values()['CITIES_WEATHER_DATA_DIR'])


datetime_format = '%Y-%m-%d %H:%M:%S'

START_DATE = datetime.strptime('2018-02-11:00', datetime_format)
END_DATE = datetime.strptime('2024-03-01:00', datetime_format) 
print(START_DATE, END_DATE)
CITY_WEATHER_COLUMNS = ['timestamp','temp','feels_like','pressure','humidity','temp_min','temp_max','wind_speed','wind_deg','clouds_coverage', 'weather_category','weather_description']

with open(cities_filepath, 'r') as cities_file:
    cities = list(csv.reader(cities_file, delimiter=',', quotechar='"'))
    cities_columns =  cities[0]
    for i in range(1, len(cities)):
        update_city_info(START_DATE, END_DATE, cities[i], cities_columns,cities_weather_data_dir)
        
