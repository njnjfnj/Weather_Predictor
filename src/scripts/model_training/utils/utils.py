from prophet.serialize import model_to_json, model_from_json
from pickle import dump, load, dumps, UnpicklingError

from os import path, makedirs
from json import JSONDecodeError

import logging

def save_prophet_model(model, filename):
    try:
        with open_file(filename, 'w') as fout:
            fout.write(model_to_json(model))
    except (ValueError, AttributeError) as e:
        handle_error("Failed to convert Prophet model to json:", e)
        
def load_prophet_model(filename):
    try:
        with open_file(filename, 'r') as fin:
            return model_from_json(fin.read())
    except JSONDecodeError as e:
        handle_error("Failed to decode Prophet model from json:", e)

def save_sklearn_model(model, filename):
    if hasattr(model, 'classes_') and hasattr(model, 'tree_'):
        try:
            with open_file(filename, 'wb') as f:
                dump(model, f)    
        except (ValueError, TypeError, AttributeError) as e:
            handle_error("Failed to convert scikit-learn model to .pkl", e)
    else:
        raise AttributeError("Failed to convert, model must be fit first (invalid model object)")

def load_sklearn_model(filename):
    try:
        with open_file(filename, 'rb') as f:
            return load(f)        
    except (UnpicklingError, EOFError) as e:
        handle_error("Failed to decode scikit-learn model from .pkl", e)

def open_file(filename, mode):
    try:
        return open(filename, mode)
    except (FileNotFoundError, PermissionError) as e: 
        handle_error(f"Failed to open file '{filename}' with mode '{mode}':", e)

def handle_error(message, error):
    logging.error(message)
    raise error
