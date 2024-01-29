import requests
import csv
from os import path, mkdir
from dotenv import load_dotenv, dotenv_values
from datetime import date, datetime, timedelta
from time import sleep, mktime
import json
load_dotenv()

def to_gmt(dt):
    if dt.utcoffset() is not None:
        return dt - timedelta(seconds=dt.utcoffset().total_seconds())
    else: return dt

API_KEY = dotenv_values()['API_KEY']
CITY_DATA_DIR='./city_weather_datasets/'

datetime_format = '%Y-%m-%d %H:%M:%S'
START_DATE = datetime.strptime('2023-01-30 00:00:00', datetime_format)
END_DATE = to_gmt(datetime.strptime('2023-02-2 00:00:00', datetime_format))


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
            print(res)
            arr.append(res)
            sleep(0.5)


        
        if path.isdir(CITY_DATA_DIR):
            city_directory = path.join(CITY_DATA_DIR, city[name_index].lower())
            if not path.isdir(city_directory):
                mkdir(city_directory)

            filename = path.join(city_directory, city[name_index].lower() + '.json')
            
            with open(filename, 'a+') as city_file:
                city_file.seek(0)
                content = city_file.read()
                if content:
                    content += ','
                    content += '\n'
                for i in range(0, len(arr)):
                    json_str = json.dumps(arr[i])
                    if i == (len(arr) - 1):
                        city_file.write(content + json_str)
                    else:
                        city_file.write(content + json_str + ',' + '\n')

