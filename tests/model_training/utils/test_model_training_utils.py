from prophet import Prophet
from prophet.serialize import model_from_json, model_to_json
from src.scripts.model_training.utils.utils import save_model, load_model
import pytest as pt
from unittest.mock import patch
import pandas as pd

from json import JSONDecodeError

def test_save_model_success():
    model = Prophet()
    model.fit(pd.DataFrame({'ds': pd.date_range(start='2012-01-01', end='2012-02-01'), 'y': range(0, 32)}))
    filename ="test.json"
    save_model(model, str(filename))
    with open(filename, 'r') as m:
        m = model_from_json(m.read())
    assert m;

def test_save_model_file_error():
    model = Prophet()
    model.fit(pd.DataFrame({'ds': pd.date_range(start='2012-01-01', end='2012-02-01'), 'y': range(0, 32)}))
    filename ="/test.json"

    with pt.raises(PermissionError):
        save_model(model, str(filename))
        
    filename ="/abc/dea/test.json"

    with pt.raises(FileNotFoundError):
        save_model(model, str(filename))

def test_save_model_convertion_error():
    model = Prophet()
    filename = "test.json"
    with pt.raises(ValueError):
        save_model(model, str(filename))

    model = None
    filename = "test.json"
    with pt.raises(AttributeError):
        save_model(model, str(filename))


    model = Prophet()
    model.fit(pd.DataFrame({'ds': pd.date_range(start='2012-01-01', end='2012-02-01'), 'y': range(0, 32)}))
    save_model(model, str(filename))

def load_test_model(filename):    
    model = Prophet()
    model.fit(pd.DataFrame({'ds': pd.date_range(start='2012-01-01', end='2012-02-01'), 'y': range(0, 32)}))
    with open(filename, 'w') as fout:
        fout.write(model_to_json(model))

def test_load_model_success():
    filename = 'test.json'
    load_test_model(filename)
    m = load_model(filename)
    assert m;

def test_load_model_convertion_error():
    filename = 'test.json'
    load_test_model(filename)
    with open(filename, "r+") as f:
        f.truncate()
    with pt.raises(JSONDecodeError):
        m = load_model(filename)
    
def test_load_model_filepath_error():
    filename = 'test.json'
    load_test_model(filename)
    filename = '/test.json'

    with pt.raises(FileNotFoundError):
        m = load_model(str(filename))
        
    filename ="/abc/dea/test.json"

    with pt.raises(FileNotFoundError):
        m = load_model(str(filename))