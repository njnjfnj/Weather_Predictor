import pandas as pd

from sklearn.tree import DecisionTreeClassifier

from ..utils.utils import save_sklearn_model ,handle_error
from ..model_training import PRODUCTS

def create_weather_description_model(df, model_filename):
    if not isinstance(df, pd.DataFrame):
        handle_error("Failed to convert: df argument must be the instance of pd.DataFrame", ValueError)
    if df.isnull().any():
        handle_error("Failed to convert: all values in df must me not null", ValueError)
    df_columns = df.columns
    products_keys = products_keys
    if products_keys in df.columns and "y" in df_columns:
        x = df[[el for el in products_keys if el != 'weather_description']]
        y = df['y']
    else:
        err_str = "Failed to convert: Columns: " + products_keys + " and 'y' must be in df"
        handle_error(err_str, AttributeError)
    
    model = DecisionTreeClassifier(random_state=0)
    model.fit(x, y)    
    save_sklearn_model(model, model_filename)


