import requests
import csv
from os import path, mkdir
from dotenv import load_dotenv, dotenv_values
from datetime import date, datetime, timedelta
from time import sleep, mktime
load_dotenv()

def to_gmt(dt):
    if dt.utcoffset() is not None:
        return dt - timedelta(seconds=dt.utcoffset().total_seconds())
    else: return dt

API_KEY = dotenv_values()['API_KEY']
CITY_DATA_DIR='./city_weather_datasets/'

datetime_format = '%Y-%m-%d %H:%M:%S'
START_DATE = datetime.strptime('2023-01-02 00:00:00', datetime_format)
END_DATE = to_gmt(datetime.strptime('2023-04-02 00:00:00', datetime_format))
 
CITY_WEATHER_COLUMNS = ['timestamp','temp','feels_like','pressure','humidity','temp_min','temp_max','wind_speed','wind_deg','clouds_coverage', 'weather_category','weather_description']

def transform_weather_json(json_str):
    info = json_str['list'][0]
    timestamp = info['dt']
    temp = float(info['main']['temp']) - 273.15 
    feels_like = float(info['main']['feels_like']) - 273.15
    pressure = info['main']['pressure']
    humidity = info['main']['humidity']
    temp_min = float(info['main']['temp_min']) - 273.15
    temp_max = float(info['main']['temp_max']) - 273.15
    wind_speed = info['wind']['speed'] * 3.6
    wind_deg = info['wind']['deg']
    clouds_coverage = info['clouds']['all']
    weather_category = info['weather'][0]['main']
    weather_description = info['weather'][0]['main']

    arr = [timestamp, temp, feels_like, pressure, humidity, temp_min, temp_max, wind_speed, wind_deg, clouds_coverage, weather_category, weather_description]
    
    return arr



with open('cities/cities.csv', 'r') as cities_csv:
    cities = list(csv.reader(cities_csv, delimiter=',', quotechar='"'))
    header = cities[0]
    id_index = header.index('id')
    name_index = header.index('name')
    lat_index = header.index('lat')
    lon_index = header.index('lon')
    for i in range(1, len(cities)):
        arr = []
        city = cities[i]
        
        while START_DATE != END_DATE:
            START_DATE = to_gmt(START_DATE)
            NEXT_DATETIME = to_gmt(START_DATE + timedelta(hours=8))
            url = f'https://history.openweathermap.org/data/2.5/history/city?lat={city[lat_index]}&lon={city[lon_index]}&type=hour&start={(mktime(START_DATE.timetuple()))}&end={(mktime(NEXT_DATETIME.timetuple()))}&appid={API_KEY}'
            START_DATE = NEXT_DATETIME

            res = requests.get(url=url).json()
            transofmed_weather = transform_weather_json(res)

            arr.append(transofmed_weather)

        
        if path.isdir(CITY_DATA_DIR):
            city_directory = path.join(CITY_DATA_DIR, city[name_index].lower())
            if not path.isdir(city_directory):
                mkdir(city_directory)

            filename = path.join(city_directory, city[name_index].lower() + '.csv')
            existing_data = []
            
            try:
                with open(filename, 'r') as city_file:
                    reader = csv.reader(city_file)
                    existing_data = list(reader)
            except FileNotFoundError:
                existing_data = []

            if not existing_data[0] == CITY_WEATHER_COLUMNS:
                                existing_data.insert(0, CITY_WEATHER_COLUMNS)

            existing_data.extend(arr)

            with open(filename, 'w', newline='') as city_file:
                writer = csv.writer(city_file)
                writer.writerows(existing_data)

