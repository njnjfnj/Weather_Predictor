import pytest
import pandas as pd
import numpy as np
from src.scripts.model_training.model_training import create_basic_prophet_model
from src.scripts.model_training.model_training import PRODUCTS 

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
