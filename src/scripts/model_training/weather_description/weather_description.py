import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier

from src.scripts.model_training.utils.utils import save_sklearn_model
from src.scripts.model_training.utils.utils import handle_error


PRODUCT_KEYS =  ['ds',
    'humidity',
    'pressure',
    'temp',
    'wind_speed',
    'feels_like',
    'clouds_percentage',
    'sun_horison_angle',
    'precipitation',
    'wind_direction',
    'y']

def create_weather_description_model(df, model_filename):
    if not isinstance(df, pd.DataFrame):
        handle_error("Failed to convert: df argument must be the instance of pd.DataFrame", ValueError)
    
    df_columns = df.columns
    for column in df_columns:
        if df[column].isnull().any():
            handle_error("Failed to convert: all values in df must me not null", ValueError)
    
    
    x, y = None, None
    if all(x in df_columns for x in PRODUCT_KEYS):
        x = df.drop(columns=["y", "ds"])
        y = df['y']
    else:
        err_str = "Failed to convert: Columns: " + " ".join(PRODUCT_KEYS) + " and 'y' must be in df"
        handle_error(err_str, AttributeError)
    
    model = DecisionTreeClassifier(random_state=0)

    model.fit(x, y)
    print("yahoo")
    save_sklearn_model(model, model_filename)


