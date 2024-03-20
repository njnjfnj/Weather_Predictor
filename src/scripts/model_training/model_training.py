import pandas as pd

from prophet import Prophet

from .utils.utils import save_prophet_model, handle_error 
from .wind_speed.wind_speed import create_wind_speed_model
from .pressure.pressure import create_pressure_model
from .weather_description.weather_description import create_weather_description_model

from os.path import isdir, isfile, exists
from os import mkdir

CITIES_WEATHER_DATA_DIR = 'data/datasets'
CITIES_WEATHER_MODELS_DIR = 'data/models'

def create_basic_prophet_model(df, model_filename):
    if not isinstance(df, pd.DataFrame):
        handle_error("df argument must be the instance of pd.DataFrame", ValueError)
    if 'ds' not in df.columns or 'y' not in df.columns:
        handle_error("df argument must have columns ds and y", AttributeError)
    try:
        model = Prophet(
        yearly_seasonality=False,  
        weekly_seasonality=False  
        )
        model.add_seasonality(name='monthly', period=30.5, fourier_order=5)  
        
        model.fit(df)
        save_prophet_model(model, model_filename)
    except Exception as e:
        handle_error("Failed to create and save model, exception occured: ", AttributeError)



PRODUCTS = {
    'humidity': create_basic_prophet_model,
    'pressure': create_pressure_model,
    'temp': create_basic_prophet_model,
    'wind_speed': create_wind_speed_model,
    'feels_like': create_basic_prophet_model,
    'sun_horison_angle': create_basic_prophet_model,
    'precipitation': create_basic_prophet_model,
    'wind_direction': create_basic_prophet_model,
    'weather_description': create_weather_description_model
}


def create_products_models(city_name):
    df = None
    filename = f'{CITIES_WEATHER_DATA_DIR}/{city_name}/{city_name}.csv'
    if exists(CITIES_WEATHER_DATA_DIR):
        if exists(filename):
            df = pd.read_csv(f'{CITIES_WEATHER_DATA_DIR}/{city_name}/{city_name}.csv')
        else:
            handle_error("Failed to read: data file for provided city does not exist", FileNotFoundError)
    else: 
        handle_error("Failed to read: directory for cities data does not exist", FileNotFoundError)
    
    for product, create_model in PRODUCTS.items():
        df_columns = df.columns
        if product in df_columns:
            if "timestamp" in df_columns:
                df = df.rename(columns={'timestamp': 'ds', product: 'y'})
                df['ds'] = pd.to_datetime(df['ds'], unit='s')
            else:
                handle_error("Failed to transform: Derired column timestamp is not in df", AttributeError)
        else:
            error_str = "Derired column: '" + product + "' is not in provided df"
            handle_error(error_str, AttributeError)

        filename = f'{CITIES_WEATHER_MODELS_DIR}/{city_name}/{product}.json'

        if product == 'weather_description':
            filename = f'{CITIES_WEATHER_MODELS_DIR}/{city_name}/{product}.pkl'

        create_model(df, filename)


