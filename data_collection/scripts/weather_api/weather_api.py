import csv
from dotenv import load_dotenv, dotenv_values
from datetime import datetime, timedelta

from load.load import update_city_info

def load_api_key():
    load_dotenv()
    return dotenv_values()['API_KEY']

API_KEY = load_api_key()
CITY_DATA_DIR='./city_weather_datasets/'

datetime_format = '%Y-%m-%d %H:%M:%S'

UTC_NOW = datetime.utcnow()
LOCAL_NOW = datetime.now()
TIME_DIFFERENCE = int((LOCAL_NOW - UTC_NOW).total_seconds() / 3600)

START_DATE = datetime.strptime('2023-07-28 00:00:00', datetime_format) + timedelta(hours=TIME_DIFFERENCE)
END_DATE = datetime.strptime('2023-12-31 00:00:00', datetime_format) 
 
CITY_WEATHER_COLUMNS = ['timestamp','temp','feels_like','pressure','humidity','temp_min','temp_max','wind_speed','wind_deg','clouds_coverage', 'weather_category','weather_description']

with open('cities/cities.csv', 'r') as cities_file:
    cities = list(csv.reader(cities_file, delimiter=',', quotechar='"'))
    cities_columns =  cities[0]
    for i in range(1, len(cities)):
        update_city_info(START_DATE, END_DATE, cities[i], cities_columns, CITY_WEATHER_COLUMNS)
