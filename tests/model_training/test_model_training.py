import pytest

from unittest import TestCase
from unittest.mock import Mock, patch

import pandas as pd
import numpy as np

from pandas.testing import assert_frame_equal

from random import uniform, randint

from src.scripts.model_training.model_training import (create_basic_prophet_model,
    create_products_models, create_pressure_model, create_weather_description_model,
    create_wind_speed_model)


# Tests for create_basic_prophet_model 
@pytest.fixture
def valid_prophet_df():
    return pd.DataFrame({'ds': pd.date_range(start='2012-01-01', end='2012-02-01'), 'y': range(0, 32)})

def test_create_basic_prophet_model_success(valid_prophet_df, tmp_path):
    model_filename = tmp_path / "test.json"
    create_basic_prophet_model(valid_prophet_df, model_filename)

def test_prophet_model_filename_error(valid_prophet_df, tmp_path):
    model_filename = tmp_path / "/test.json"
    with pytest.raises(PermissionError):
        create_basic_prophet_model(valid_prophet_df, model_filename)
    model_filename = tmp_path / "/abc/bca/test.json"
    with pytest.raises(FileNotFoundError):
        create_basic_prophet_model(valid_prophet_df, model_filename)

def test_prophet_model_inconsistent_df(tmp_path):
    filename = tmp_path / "test.json"
    df = pd.DataFrame({'ds': pd.date_range(start='2012-01-01', end='2012-02-01'), 'temp': range(0, 32)})
    with pytest.raises(AttributeError):
        create_basic_prophet_model(df, filename)
    
    df.rename(columns={"temp": "y"}, inplace=True)
    
    df.loc[14 ,"ds"] = np.NAN
    df.loc[12 ,"ds"] = np.NaN
    
    with pytest.raises(Exception):
        create_basic_prophet_model(df, filename)
    
    df = "df" 
    with pytest.raises(ValueError):
        create_basic_prophet_model(df, filename)


# Tests for create_products_models

PRODUCTS = {
    'humidity': create_basic_prophet_model,
    'pressure': create_pressure_model,
    'temp': create_basic_prophet_model,
    'wind_speed': create_wind_speed_model,
    'feels_like': create_basic_prophet_model,
    'clouds_percentage': create_basic_prophet_model,
    'sun_horison_angle': create_basic_prophet_model,
    'precipitation': create_basic_prophet_model,
    'wind_direction': create_basic_prophet_model,
    'weather_description': create_weather_description_model
}

@pytest.fixture
def create_valid_df():
    weather_categories = ["Rain", "Sun", "Clouds", "Snow"]
    df = pd.DataFrame({
        "ds": pd.to_datetime(pd.date_range(start='2012-01-01', end='2012-02-01', unit="s", freq="H"), unit="s"),
        "temp": round(number=uniform(14.56, 28.54), ndigits=2),
        "feels_like": round(number=uniform(16.56, 29.54), ndigits=2),
        "clouds_percentage": randint(0, 100),
        "sun_horison_angle": round(number=uniform(0, 180), ndigits=2),
        "precipitation": round(number=uniform(0, 10), ndigits=2),
        "pressure": round(number=uniform(0, 1100), ndigits=2),
        "humidity": round(number=uniform(0, 100), ndigits=2),
        "wind_speed": round(number=uniform(0, 100), ndigits=2),
        "wind_direction": randint(0, 360),
        "weather_description": weather_categories[randint(0, len(weather_categories)-1)]
    })
    return df

# Note:
    # For testing purposes while tested create_products_models()
    # I wrote tests with external argument(product), and commented create_model(df, filename) line
    # instead of it added return df, also i deleted for loop in that time
    # (talking above about changes in def create_products_models(city_name) )

@patch("pandas.read_csv")
def test_create_products_models(mock_read_df, create_valid_df):
    mock_df = Mock()
    response_df = create_valid_df
    for product in PRODUCTS:
        response_df.rename(columns={product: "y"}, inplace=True)
        
        passed_df = response_df.rename(columns={"y": product, "ds": "timestamp"})
        passed_df["timestamp"] = pd.to_datetime(passed_df["timestamp"], origin="unix")
        
        mock_df.configure_mock(return_value=passed_df)
        mock_df.columns = passed_df.columns
        mock_df.rename = passed_df.rename
        mock_read_df.return_value = mock_df
        
        returned_df = create_products_models("miami", product)
        assert_frame_equal(returned_df, response_df)
