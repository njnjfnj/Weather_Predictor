import pandas as pd
from dotenv import load_dotenv, dotenv_values
from .humidity.humidity import create_humidity_model
from .wind_speed.wind_speed import create_wind_speed_model
from .pressure.pressure import create_pressure_model
from .temp.temp import create_temp_min_model
from .temp.temp import create_temp_max_model
from .temp.temp import create_temp_model
from .weather_category.weather_category import create_weather_category_model

load_dotenv()
CITIES_WEATHER_DATA_DIR = dotenv_values()['CITIES_WEATHER_DATA_DIR']
CITIES_WEATHER_MODELS_DIR = dotenv_values()['CITIES_WEATHER_MODELS_DIR']

PRODUCTS = ['humidity', 'pressure', 'temp', 'temp_min', 'temp_max', 'wind_speed', 'weather_category']

def create_products_models(city_name, test_size):
    df = pd.read_csv(f'{CITIES_WEATHER_DATA_DIR}/{city_name}/{city_name}.csv')

    for product in PRODUCTS:

        df = df.rename(columns={'timestamp': 'ds', product: 'y'})
        df['ds'] = pd.to_datetime(df['ds'], unit='s')

        filename = f'{CITIES_WEATHER_MODELS_DIR}/{city_name}/{product}.json'

        if product == 'weather_category':
            filename = f'{CITIES_WEATHER_MODELS_DIR}/{city_name}/{product}.pkl'

        match product:
            case 'humidity':
                create_humidity_model(df, test_size, filename)
            case 'wind_speed':
                create_wind_speed_model(df, test_size, filename)
            case 'pressure':
                create_pressure_model(df, test_size, filename)
            case 'temp_min':
                create_temp_min_model(df, test_size, filename)
            case 'temp_max':
                create_temp_max_model(df, test_size, filename)
            case 'temp':
                create_temp_model(df, test_size, filename) 
            case 'weather_category':
                create_weather_category_model(df, filename)
        
        df = df.rename(columns={'timestamp': 'ds', 'y': product})


