import pandas as pd 
from os import path
from csv import reader
from dotenv import load_dotenv, dotenv_values
from sklearn.tree import DecisionTreeClassifier
from ..model_training.utils.utils import load_model, load_sklearn_model
load_dotenv()


TARGET_PARAMETERS = ['temp', 'humidity', 'wind_speed', 'pressure', 'temp_min', 'temp_max', 'weather_category']
# CITIES_WEATHER_MODELS_DIR = dotenv_values()['CITIES_WEATHER_MODELS_DIR']
# ROOT_DIR = dotenv_values()['ROOT_DIR']

def predict_city_weather(city_name, time_period_hours):
    time_period_hours = int(time_period_hours)
    checked_city = check_city_name(city_name)
    if checked_city:
        result = False
        models = open_weather_models(city_name)
        for param in TARGET_PARAMETERS:
            m = models[param]
            try:
                if param != 'weather_category':
                    future = m.make_future_dataframe(periods=time_period_hours, freq='h')
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
        
        return result.to_csv(sep=',')
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

def open_weather_models(city_name):
    res = {}
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
    return res