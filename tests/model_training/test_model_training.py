from prophet import Prophet
from prophet.serialize import model_from_json
from ...scripts.model_training.utils.utils import save_model
import pytest as pt

from json import JSONDecodeError

def test_save_model():
    model = Prophet()
    filename = "test.json"

    save_model(model, filename)

    with pt.raises(JSONDecodeError):
        with open(filename, 'r') as fin:
            return model_from_json(fin.read())
