import pandas as pd 
from os import path
from csv import reader
from dotenv import load_dotenv, dotenv_values
from sklearn.tree import DecisionTreeClassifier
from ..model_training.utils.utils import load_model, load_sklearn_model
load_dotenv()


TARGET_PARAMETERS = ['temp', 'humidity', 'wind_speed', 'pressure', 'temp_min', 'temp_max', 'weather_description']
# CITIES_WEATHER_MODELS_DIR = dotenv_values()['CITIES_WEATHER_MODELS_DIR']
# ROOT_DIR = dotenv_values()['ROOT_DIR']


def predict_city_weather(city_name, prediction_hours):
    checked_city = check_city_name(city_name)
    if checked_city:
        result = False
        models_and_time_diff = open_weather_models(city_name, prediction_hours)
        models = models_and_time_diff['models']
        new_prediction_hours = models_and_time_diff['prediction_hours']
        
        for param in TARGET_PARAMETERS:
            m = models[param]
            try:
                if param != 'weather_description':
                    future = m.make_future_dataframe(periods=new_prediction_hours, freq='h')
                    forecast = m.predict(future)

                    forecast = pd.DataFrame(data=forecast)

                    forecast = forecast[['ds', 'yhat']].rename(columns={'yhat': param, 'ds': 'timestamp'})

                    forecast['timestamp'] = pd.to_datetime(forecast['timestamp'])

                    forecast.set_index('timestamp')
                    
                    if not isinstance(result, pd.DataFrame):
                        result = forecast
                    else:
                        result = pd.merge(result, forecast, on='timestamp', how='left')
                else:
                    if isinstance(result, pd.DataFrame):
                        weather_description = m.predict(result[TARGET_PARAMETERS[:-1]])
                        result['weather_description'] = weather_description
                        
            except AttributeError as e:
                return e
        
        print(result[-prediction_hours:].to_csv(sep=','))
    else: return ""




def check_city_name(city_name):
    cities_path = path.join(path.dirname(path.realpath(__file__)), '../../data/cities/cities.csv')
    if path.isfile(cities_path):
        with open(cities_path, 'r') as cities_csv:
            cities = list(reader(cities_csv))
            name_index = cities[0].index('name')
            for i in range(1, len(cities)):
                if str(cities[i][name_index]).lower() == city_name:
                    return True
    return False

from time import mktime, time


def open_weather_models(city_name, prediction_hours):
    res = {}
    model_last_index = None
    for param in TARGET_PARAMETERS:
        filepath = path.join(path.dirname(path.realpath(__file__)), '../../data/models/', city_name, param)
        if param == 'weather_description':
            filepath += '.pkl'
        else:
            filepath += '.json'

        if path.isfile(filepath):
            if param == 'weather_description':
                res[param] = load_sklearn_model(filepath)
            else:
                res[param] = load_model(filepath)
                model_last_index = res[param].history.tail(1)['ds'].iloc[0]
    print(model_last_index)
    prediction_hours = match_time_difference(city_name=city_name, 
                                             prediction_hours=prediction_hours, 
                                             model_last_index=model_last_index)
    return {'models': res, 'prediction_hours': prediction_hours}

import csv
from datetime import datetime, timezone
from math import ceil

def match_time_difference(city_name, prediction_hours, model_last_index):
    CITIES_DIR = "data/cities/cities.csv"
    
    with open(CITIES_DIR, 'r') as cities_csv:
        cities = list(csv.reader(cities_csv))
        name_index = cities[0].index('name')
        time_difference_index = cities[0].index('time_difference')
        curr_city_time = datetime.utcnow()
        for row in cities:
            if city_name == row[name_index].lower():
                print("sa")
                time_difference = row[time_difference_index][0]
                if row[time_difference_index][0] == '-':
                    time_difference = int(time_difference[1:]) * -1
                else: time_difference = int(time_difference)

                return (int(ceil(((curr_city_time - model_last_index).total_seconds() / 3600))) + time_difference)
