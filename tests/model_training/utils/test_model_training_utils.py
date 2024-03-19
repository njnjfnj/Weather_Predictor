import pandas as pd

import pytest

from prophet import Prophet
from prophet.serialize import model_from_json, model_to_json

from src.scripts.model_training.utils.utils import (
    save_prophet_model, load_prophet_model, save_sklearn_model, load_sklearn_model)

from json import dump, JSONDecodeError

from sklearn.tree import DecisionTreeClassifier
from random import choice

from pickle import UnpicklingError

@pytest.fixture
def prophet_model():
    model = Prophet()
    model.fit(pd.DataFrame({'ds': pd.date_range(start='2012-01-01', end='2012-02-01'), 'y': range(0, 32)}))
    return model
   
@pytest.fixture
def sklearn_model():
    x = pd.DataFrame({"wind_speed": range(20), "temp": range(20)})
    y = pd.DataFrame({"y": [choice(["Clouds", "Sun", "Rain"]) for _ in range(20)]})
    model = DecisionTreeClassifier(random_state=0)
    model.fit(x, y)
    return model

@pytest.fixture
def get_model_by_type(prophet_model, sklearn_model):
    def _get_model_by_type(name):
        if name == "Prophet": return prophet_model
        else: return sklearn_model
    return _get_model_by_type

@pytest.mark.parametrize(
    ("model_type", "save_function", "load_function", "filename"),
    [
        ("Prophet", save_prophet_model, load_prophet_model, "test.json"),
        ("Sklearn", save_sklearn_model, load_sklearn_model, "test.pkl"),
    ],
)
def test_save_model_success(model_type ,save_function, load_function,
                             filename, tmp_path, get_model_by_type):
    filename = tmp_path / filename
    model = get_model_by_type(model_type)
    save_function(model, str(filename))
    m = load_function(str(filename))
    assert m is not None

@pytest.mark.parametrize(("model_type", "save_function", "filename"),
                         [("Prophet", save_prophet_model, "test.json"),
                         ("Sklearn", save_sklearn_model, "test.pkl")])
def test_save_model_filepath_error(model_type, save_function, filename,
                             tmp_path, get_model_by_type):
    model = get_model_by_type(model_type)
    filename = "/" + filename 
    filename = tmp_path / filename
    with pytest.raises(PermissionError):
        save_function(model, str(filename))
        
    filename = tmp_path / "/abc/dea/test.json" if model_type == "Prophet" else "/abc/dea/test.pkl"

    with pytest.raises(FileNotFoundError):
        save_function(model, str(filename))


@pytest.mark.parametrize(("model_type", "save_function", "filename"),
                         [("Sklearn", save_sklearn_model, "test.pkl"),
                          ("Prophet", save_prophet_model , "test.json")
                         ])
def test_save_model_convertion_error(model_type, save_function,
                             filename, tmp_path):
    model =  Prophet() if model_type == "Prophet" else DecisionTreeClassifier()
    filename = tmp_path / filename
    err = AttributeError if model_type == "Sklearn" else ValueError
    with pytest.raises(err):
        save_function(model, str(filename))

    model = None
    err = AttributeError if model_type == "Sklearn" else AttributeError
    with pytest.raises(err):
        save_function(model, str(filename))

@pytest.mark.parametrize(("model_type", "save_function", "load_function", "filename"), 
                         [("Prophet", save_prophet_model, load_prophet_model, "test.json"),
                         ("Sklearn",  save_sklearn_model, load_sklearn_model, "test.pkl")])
def test_load_model_success(model_type, save_function, load_function, filename,
                             tmp_path, get_model_by_type):
    filename = tmp_path / filename
    model = get_model_by_type(model_type)
    save_function(model, filename)
    m = load_function(filename)
    assert m

@pytest.mark.parametrize(("model_type", "save_function", "load_function", "filename", "open_extension"), 
                         [("Prophet", save_prophet_model, load_prophet_model, "test.json", "r+"),
                         ("Sklearn",  save_sklearn_model, load_sklearn_model, "test.pkl", "rb+")])
def test_load_model_conversion_error(model_type, save_function, load_function, filename,
                                     open_extension,  tmp_path, get_model_by_type):
    filename = tmp_path / filename
    model = get_model_by_type(model_type)
    save_function(model, filename)
    with open(filename, open_extension) as f:
        f.truncate(0)
    err = (UnpicklingError, EOFError) if model_type == "Sklearn" else JSONDecodeError
    with pytest.raises(err):
        load_function(str(filename))


@pytest.mark.parametrize(("model_type", "save_function", "load_function", "filename"),
                         [("Prophet", save_prophet_model,load_prophet_model , "test.json"),
                         ("Sklearn",  save_sklearn_model, load_sklearn_model, "test.pkl")])
def test_load_model_filepath_error(model_type, save_function, load_function, 
                                   filename, tmp_path, get_model_by_type):
    filename = tmp_path / filename
    model = get_model_by_type(model_type)
    save_function(model, filename)

    filename = "/test.json" if model_type == "Prophet" else "/test.pkl"

    with pytest.raises(FileNotFoundError):
        load_function(str(filename))

    filename = "/abc/dea/test.json" if model_type == "Prophet" else "/abc/dea/test.pkl"

    with pytest.raises(FileNotFoundError):
        load_function(str(filename))
