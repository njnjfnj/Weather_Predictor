import pandas as pd

import pytest
from random import uniform, randint
from unittest.mock import Mock, MagicMock, patch, create_autospec

from sklearn.tree import DecisionTreeClassifier

from src.scripts.model_training.weather_description.weather_description import create_weather_description_model
from src.scripts.model_training.weather_description.weather_description import save_sklearn_model

@pytest.fixture
def create_valid_df():
    weather_categories = ["Rain", "Sun", "Clouds", "Snow"]
    dates = pd.to_datetime(pd.date_range(start='2012-01-01', end='2012-01-03', unit="s", freq="H"), unit="s").tolist()
    df = pd.DataFrame({
        "ds": [date.strftime("%Y-%m-%d %H:%M:%S") for date in dates[:-1]],
        "temp": [round(number=uniform(14.56, 28.54), ndigits=2) for i in range(48)],
        "feels_like": [round(number=uniform(16.56, 29.54), ndigits=2) for i in range(48)],
        "clouds_percentage": [randint(0, 100) for i in range(48)],
        "sun_horison_angle": [round(number=uniform(0, 180), ndigits=2) for i in range(48)],
        "precipitation": [round(number=uniform(0, 10), ndigits=2) for i in range(48)],
        "pressure": [round(number=uniform(0, 1100), ndigits=2) for i in range(48)],
        "humidity": [round(number=uniform(0, 100), ndigits=2) for i in range(48)],
        "wind_speed": [round(number=uniform(0, 100), ndigits=2) for i in range(48)],
        "wind_direction": [randint(0, 360) for i in range(48)],
        "y": [weather_categories[randint(0, len(weather_categories)-1)] for i in range(48)]
    })
    return df

@patch("sklearn.tree.DecisionTreeClassifier")
@patch("src.scripts.model_training.weather_description.weather_description.save_sklearn_model")
def test_create_weather_description_model(mock_save_sklearn_model, mock_sklearn_model, create_valid_df):
    df = create_valid_df
    real_x = df.drop(columns=["y", "ds"])
    real_y = df['y']

    mock_sklearn_model.fit = MagicMock(name='fit')
    mock_sklearn_model.fit(real_x, real_y)
    
    mock_save_sklearn_model.return_value = None
     
    create_weather_description_model(df, "model.pkl")

    mock_sklearn_model.fit.assert_called_once_with(real_x, real_y)
    mock_save_sklearn_model.assert_called_once()