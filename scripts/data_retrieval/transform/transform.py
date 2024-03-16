from csv import DictWriter,DictReader ,reader
from json import loads
from os import path, mkdir

def transform_into_raw(dct, raw_weather_data_dir, prepared_weather_data_dir, city_name):
    try:
        data_for_csv = []
        for item in dct['data']:
            item['weather_description'] = item['weather']['description']
            del item['weather']
            data_for_csv.append(item)

        keys = list(data_for_csv[0].keys())

        if path.isdir(raw_weather_data_dir):
            raw_city_data_dir = path.join(raw_weather_data_dir, city_name)
            if not path.isdir(raw_city_data_dir):
                mkdir(raw_city_data_dir)

            raw_city_data_filename = path.join(raw_city_data_dir, city_name+ '.csv')
            existing_data = {}
            file_empty = True
            try:
                if not path.getsize(raw_city_data_filename) == 0:
                    file_empty = False
                    
            except FileNotFoundError:
                file_empty = True

            if file_empty:
                with open(raw_city_data_filename, 'w') as output_file:
                    dict_writer = DictWriter(output_file, keys)
                    dict_writer.writeheader()
                    dict_writer.writerows(data_for_csv)
            else:
                with open(raw_city_data_filename, 'a') as output_file:
                    dict_writer = DictWriter(output_file, keys)
                    dict_writer.writerows(data_for_csv)
    except KeyError as e:
        raise KeyError(e)


       


        
import pandas as pd
import numpy as np

def transform_raw_to_prepared(dataset_path, output_path, existed=False):
    df = pd.read_csv(dataset_path)
    df.rename(columns={"ts": "timestamp"}, inplace=True)
    df.rename(columns={"app_temp": "feels_like",
                    "clouds": "clouds_percentage", "elev_angle": "sun_horison_angle",
                    "precip": "precipitation", "pres": "pressure",
                    "rh": "humidity", "snow": "snow_level",
                    "vis": "visibility", "wind_spd": "wind_speed",
                    "wind_dir": "wind_direction"}, inplace=True)
    
    df = df[['timestamp', 'temp', 'feels_like', 'clouds_percentage', 'sun_horison_angle',
            'precipitation', 'pressure', 'humidity', 'snow_level', 'visibility',
            'wind_speed', 'wind_direction', 'weather_description']]
    
    min_timestamp = df['timestamp'].min()
    df['from_0_ts'] = df['timestamp'] - min_timestamp
    
    num_s_day = 60*60*24
    num_s_year = 365.2425* num_s_day
    
    df["day_sin"] = np.sin(df['from_0_ts'] * (2 * np.pi / num_s_day))
    df["day_cos"] = np.cos(df['from_0_ts'] * (2 * np.pi / num_s_day))

    df["year_sin"] = np.sin(df['from_0_ts'] * (2 * np.pi / num_s_year))
    df["year_cos"] = np.cos(df['from_0_ts'] * (2 * np.pi / num_s_year))

    df.drop(columns=['from_0_ts'], inplace=True)
    df.drop(columns=['snow_level'], inplace=True)
    df.drop(columns=['visibility'], inplace=True)
    df.index = df['timestamp']


    if existed:
        existing_df = pd.read_csv(output_path)
        resulting_df = pd.concat([existing_df, df]).drop_duplicates(subset=['timestamp'])
        resulting_df.to_csv(output_path, index=False)
    else:
        df.to_csv(output_path, index=False)