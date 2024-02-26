from os import path 
from scripts.model_training.model_training import create_products_models
from scripts.model_prediction.model_prediction import predict_city_weather

# create_products_models('miami', 240)
res = predict_city_weather('miami', 240)
print(res)