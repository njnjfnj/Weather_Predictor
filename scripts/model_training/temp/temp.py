from prophet import Prophet
from ..utils.utils import save_model
 
def create_temp_model(df, model_filename):


    model = Prophet(
    yearly_seasonality=False,  
    weekly_seasonality=False,  
    )
    model.add_seasonality(name='monthly', period=30.5, fourier_order=5)  

    # model.add_regressor('wind_speed')
    # model.add_regressor('temp_min')
    # model.add_regressor('temp_max')
    # model.add_regressor('pressure') 

    model.fit(df)

    save_model(model, model_filename)

    # future = model.make_future_dataframe(periods=prediction_hours, freq='H')
    # future_len = future.shape[0]  

    # future['wind_speed'] = df['wind_speed'].values[:future_len]
    # future['temp_max'] = df['temp_max'].values[:future_len]
    # future['temp_min'] = df['temp_min'].values[:future_len]
    # future['pressure'] = df['pressure'].values[:future_len]

    # forecast = model.predict(future)

    # return forecast

def create_temp_min_model(df, model_filename):


    model = Prophet(
    yearly_seasonality=False,  
    weekly_seasonality=False
    )
    model.add_seasonality(name='monthly', period=30.5, fourier_order=5)  

    model.fit(df)

    save_model(model, model_filename)

    # future = model.make_future_dataframe(periods=prediction_hours, freq='H')

    # forecast = model.predict(future)

    # return forecast

def create_temp_max_model(df, model_filename):


    model = Prophet(
    yearly_seasonality=False,  
    weekly_seasonality=False
    )

    model.add_seasonality(name='monthly', period=30.5, fourier_order=5)  
    # model.add_regressor('temp_min')

    model.fit(df)

    save_model(model, model_filename)

    # future = model.make_future_dataframe(periods=prediction_hours, freq='H')
    # future_len = future.shape[0]  
    
    
    # future['temp_min'] = df['temp_min'].values[:future_len]
    # forecast = model.predict(future)

    # return forecast