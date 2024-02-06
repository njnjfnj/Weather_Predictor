from os import path 

with open('.env', 'a') as env:
    env.write(f'\nROOT_DIR={path.dirname(path.abspath(__file__))}')

from scripts.model_training.model_training import create_products_models
from scripts.model_prediction.model_prediction import predict_city_weather

create_products_models('miami', 240)
predict_city_weather('miami', 240)