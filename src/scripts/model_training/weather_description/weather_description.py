import pandas as pd

from sklearn.tree import DecisionTreeClassifier

from ..utils.utils import save_sklearn_model ,handle_error

PRODUCT_KEYS =  ['humidity',
    'pressure',
    'temp',
    'wind_speed',
    'feels_like',
    'clouds_percentage'
    'sun_horison_angle',
    'precipitation',
    'wind_direction',
    'weather_description']

def create_weather_description_model(df, model_filename):
    if not isinstance(df, pd.DataFrame):
        handle_error("Failed to convert: df argument must be the instance of pd.DataFrame", ValueError)
    if df.isnull().any():
        handle_error("Failed to convert: all values in df must me not null", ValueError)
    df_columns = df.columns
    if PRODUCT_KEYS in df.columns and "y" in df_columns:
        x = df[[el for el in PRODUCT_KEYS if el != 'weather_description']]
        y = df['y']
    else:
        err_str = "Failed to convert: Columns: " + PRODUCT_KEYS + " and 'y' must be in df"
        handle_error(err_str, AttributeError)
    
    model = DecisionTreeClassifier(random_state=0)
    return {x: "x", y: "y" }    
    model.fit(x, y)
    # save_sklearn_model(model, model_filename)


