from csv import DictWriter,DictReader ,reader
from json import loads
from os import path, mkdir

def transform_load_weather_json(dct, city_data_dir, city_name):
    
    data_for_csv = []
    for item in dct['data']:
        item['weather_description'] = item['weather']['description']
        del item['weather']
        data_for_csv.append(item)

    keys = list(data_for_csv[0].keys())

    if path.isdir(city_data_dir):
        city_directory = path.join(city_data_dir, city_name)
        if not path.isdir(city_directory):
            mkdir(city_directory)

        filename = path.join(city_directory, city_name+ '.csv')
        existing_data = {}
        file_empty = False
        try:
            with open(filename, 'r') as city_file:
                reader = DictReader(city_file)
                file_empty = not bool(list(reader))
                
        except FileNotFoundError:
            file_empty = False

        if file_empty:
            with open(filename, 'w') as output_file:
                dict_writer = DictWriter(output_file, keys)
                dict_writer.writeheader()
                dict_writer.writerows(data_for_csv)
        else:
            with open(filename, 'a') as output_file:
                dict_writer = DictWriter(output_file, keys)
                dict_writer.writerows(data_for_csv)
        