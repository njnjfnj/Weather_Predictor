import pandas as pd 
import pickle
from os import path
from csv import reader
from dotenv import load_dotenv, dotenv_values
load_dotenv()

def predict_city_weather(city_name):
    pass



def check_city_name(city_name):
    cities_path = path.join(path.dirname(__file__), dotenv_values['CITIES_DIR'])
    with open(cities_path, 'r') as cities_csv:
        cities = list(reader(cities_csv))
        name_index = cities[0].index('name')
        for i in range(1, len(cities)):
            if cities[i][name_index] == city_name:
                return True
    return False
    