import pandas as pd 
from os import path
from csv import reader
from dotenv import load_dotenv, dotenv_values
from sklearn.tree import DecisionTreeClassifier
from ..model_training.utils.utils import load_model, load_sklearn_model
from json import loads, dumps
from ...redis_scripts.get import get_city

load_dotenv()



TARGET_PARAMETERS = ['temp', 'humidity', 'wind_speed', 'pressure', 'temp_min', 'temp_max', 'weather_category']

def predict_city_weather(city_name, prediction_hours):
    city_name = city_name.lower()
    print(city_name)
    checked_city = check_city_name(city_name)
    if checked_city:
        result = False
        models_and_time_diff = open_weather_models(city_name, prediction_hours)
        models = models_and_time_diff['models']
        new_prediction_hours = int(models_and_time_diff['prediction_hours'])
        
        for param in TARGET_PARAMETERS:
            m = models[param]
            try:
                if param != 'weather_category':
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
                        weather_category = m.predict(result[TARGET_PARAMETERS[:-1]])
                        result['weather_category'] = weather_category
                        
            except AttributeError as e:
                return e
            
        result["timestamp"] = pd.to_datetime(result["timestamp"], unit="s")
        data_list = result[-int(prediction_hours):].to_dict(orient='records')
        for row in data_list:
            row["timestamp"] = row["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
        json_objects = [dumps(row) for row in data_list]
        
        return {"result": json_objects, "status": "success"}
    else: return {"result": [], "status": "error"
}



def check_city_name(city_name):
    match = get_city(city_name)
    match = loads(match)["result"][0]["name"]
    if match:
        if match.lower() == city_name.lower(): 
            return True
    return False

from time import mktime, time


def open_weather_models(city_name, prediction_hours):
    res = {}
    model_last_index = None
    for param in TARGET_PARAMETERS:
        filepath = path.join(path.dirname(path.realpath(__file__)), '../../data/models/', city_name, param)
        if param == 'weather_category':
            filepath += '.pkl'
        else:
            filepath += '.json'

        if path.isfile(filepath):
            if param == 'weather_category':
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
    match = get_city(city_name)
    match = loads(match)["result"][0]
    time_difference = match["utc_time_difference"]
    curr_city_time = datetime.utcnow()

    if time_difference[0] == '-':
        time_difference = int(time_difference[1:]) * -1
    else: time_difference = int(time_difference)

    return (int(ceil(((curr_city_time - model_last_index).total_seconds() / 3600))) + time_difference)

