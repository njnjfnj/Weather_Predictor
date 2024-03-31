import pandas as pd 
from os import path
from csv import reader
from dotenv import load_dotenv, dotenv_values
from sklearn.tree import DecisionTreeClassifier
from ..model_training.utils.utils import load_prophet_model, load_sklearn_model
from json import loads, dumps
from ...redis.get.get import get_city, check_city_name, match_time_difference

load_dotenv()


TARGET_PARAMETERS = {
    'humidity',
    'pressure',
    'temp',
    'wind_speed',
    'feels_like',
    'clouds_percentage',
    'sun_horison_angle',
    'precipitation',
    'wind_direction',
    'weather_description'
}

def predict_hourly_city_weather(city_name, prediction_hours, target_params=TARGET_PARAMETERS):

    city_name = city_name.lower()

    if check_city_name(city_name):
        result = False
        models_and_time_diff = open_weather_models(city_name, prediction_hours, target_params=target_params)
        models = models_and_time_diff['models']
        new_prediction_hours = int(models_and_time_diff['prediction_hours'])
        
        for param in target_params:
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
            
        result["timestamp"] = pd.to_datetime(result["timestamp"], unit="s")
        data_list = result[-int(prediction_hours):].to_dict(orient='records')
        for row in data_list:
            row["timestamp"] = row["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
        json_objects = [dumps(row) for row in data_list]
        
        return {"result": json_objects, "status": "success"}
    else: return {"result": [], "status": "error"}
    
def predict_daily_city_weather(city_name, prediction_days):
    hours = prediction_days * 24
    return predict_hourly_city_weather(city_name, prediction_hours=hours, 
                                       target_params=['temp_min', 'temp_max', 'weather_category'])


from time import mktime, time


def open_weather_models(city_name, prediction_hours, target_params=TARGET_PARAMETERS):
    res = {}
    model_last_index = None
    for param in target_params:
        filepath = path.join(path.dirname(path.realpath(__file__)), '../../../data/models/', city_name, param)
        if param == 'weather_description':
            filepath += '.pkl'
        else:
            filepath += '.json'

        if path.isfile(filepath):
            if param == 'weather_description':
                res[param] = load_sklearn_model(filepath)
            else:
                res[param] = load_prophet_model(filepath)
                model_last_index = res[param].history.tail(1)['ds'].iloc[0]

    prediction_hours = prediction_hours + match_time_difference(city_name=city_name, 
                                             model_last_index=model_last_index)
    return {'models': res, 'prediction_hours': prediction_hours}



