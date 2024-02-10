from prophet import Prophet
from ..utils.utils import save_model 
def create_pressure_model(df, test_size, model_filename):
    train = df.iloc[:-test_size]
    
    model = Prophet(
    yearly_seasonality=False,  
    weekly_seasonality=False, 
    )
    
    model.add_seasonality(name='monthly', period=30, fourier_order=25)  
    
    model.fit(train)

    save_model(model, model_filename)

    # future = model.make_future_dataframe(periods=prediction_hours, freq='H')

    # forecast = model.predict(future)

    # return forecast