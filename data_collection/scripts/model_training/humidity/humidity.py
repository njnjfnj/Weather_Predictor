from prophet import Prophet
from ..utils.utils import save_model 
def create_humidity_model(df, test_size, model_filename):
    train = df.iloc[:-test_size]
    
    model = Prophet(
    yearly_seasonality=False,  
    weekly_seasonality=False  
    )
    model.add_seasonality(name='monthly', period=30.5, fourier_order=5)  
    
    model.fit(train)

    save_model(model, model_filename)

    # model.add_regressor('wind_speed')
    # model.add_regressor('pressure') 

    # future = model.make_future_dataframe(periods=prediction_hours, freq='H')
    # future_len = future.shape[0]  

    # future['wind_speed'] = df['wind_speed'].values[:future_len]
    # future['pressure'] = df['pressure'].values[:future_len]

    # forecast = model.predict(future)

    # return forecast
