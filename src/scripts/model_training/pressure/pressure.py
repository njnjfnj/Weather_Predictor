from prophet import Prophet
import pandas as pd

from ..utils.utils import save_prophet_model, handle_error 

def create_pressure_model(df, model_filename):
    if not isinstance(df, pd.DataFrame):
        handle_error("df argument must be the instance of pd.DataFrame", ValueError)
    if 'ds' not in df.columns or 'y' not in df.columns:
        handle_error("df argument must have columns ds and y", AttributeError)
    try:
        model = Prophet(
        yearly_seasonality=False,  
        weekly_seasonality=False  
        )
        model.add_seasonality(name='monthly', period=30, fourier_order=25)  
        
        model.fit(df)
        save_prophet_model(model, model_filename)
    except Exception as e:
        handle_error("Failed to create and save model, exception occured: ", AttributeError)
