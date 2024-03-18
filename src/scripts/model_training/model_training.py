import pandas as pd
from prophet import Prophet
from dotenv import load_dotenv, dotenv_values
from .utils.utils import save_model 
from .humidity.humidity import create_humidity_model
from .wind_speed.wind_speed import create_wind_speed_model
from .pressure.pressure import create_pressure_model
from .temp.temp import create_temp_model
from .weather_description.weather_description import create_weather_description_model

load_dotenv()
CITIES_WEATHER_DATA_DIR = 'data/datasets'
CITIES_WEATHER_MODELS_DIR = 'data/models'

def create_basic_model(df, model_filename): 
    model = Prophet(
    yearly_seasonality=False,  
    weekly_seasonality=False  
    )
    model.add_seasonality(name='monthly', period=30.5, fourier_order=5)  
    
    model.fit(df)

    save_model(model, model_filename)

PRODUCTS = ['humidity', 'pressure', 'temp', 'wind_speed','feels_like', 'sun_horison_angle', 'precipitation', 'wind_direction' ,'weather_description']

def create_products_models(city_name):
    df = pd.read_csv(f'{CITIES_WEATHER_DATA_DIR}/{city_name}/{city_name}.csv')

    for product in PRODUCTS:

        df = df.rename(columns={'timestamp': 'ds', product: 'y'})
        df['ds'] = pd.to_datetime(df['ds'], unit='s')

        filename = f'{CITIES_WEATHER_MODELS_DIR}/{city_name}/{product}.json'

        if product == 'weather_description':
            filename = f'{CITIES_WEATHER_MODELS_DIR}/{city_name}/{product}.pkl'

        match product:
            case 'humidity':
                create_humidity_model(df, filename)
            case 'wind_speed':
                create_wind_speed_model(df, filename)
            case 'pressure':
                create_pressure_model(df, filename)
            case 'temp':
                create_temp_model(df, filename)
            case 'feels_like':
                create_basic_model(df, filename)
            case 'sun_horison_angle':
                create_basic_model(df, filename)
            case 'wind_direction':
                create_basic_model(df, filename)
            case 'precipitation':
                create_basic_model(df, filename) 
            case 'weather_description':
                create_weather_description_model(df, filename)
        
        df = df.rename(columns={'timestamp': 'ds', 'y': product})


