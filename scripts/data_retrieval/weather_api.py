import csv
from dotenv import load_dotenv, dotenv_values
from datetime import datetime, timedelta
from os import path,curdir
from load.load import update_city_info


cities_filepath = path.join(curdir, "../../data/cities/cities.csv")
cities_weather_data_dir = path.join(curdir, "../../data/datasets/")


datetime_format = '%Y-%m-%d:%H'

START_DATE = datetime.strptime('2015-08-09:00', datetime_format)
END_DATE = datetime.strptime('2024-03-01:00', datetime_format) 
print(START_DATE, END_DATE)
CITY_WEATHER_COLUMNS = ['timestamp','temp','feels_like','pressure','humidity','temp_min','temp_max','wind_speed','wind_deg','clouds_coverage', 'weather_category','weather_description']

with open(cities_filepath, 'r') as cities_file:
    cities = list(csv.reader(cities_file, delimiter=',', quotechar='"'))
    cities_columns =  cities[0]
    for i in range(1, len(cities)):
        update_city_info(START_DATE, END_DATE, cities[i], cities_columns,cities_weather_data_dir)
        