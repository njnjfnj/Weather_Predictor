from prophet.serialize import model_to_json, model_from_json
from pickle import dump, load, dumps

from os import path, makedirs
from json import JSONDecodeError

import logging

def save_model(model, filename):
    try:
        with open(filename, 'w') as fout:
            try:
                fout.write(model_to_json(model))
            except (ValueError, AttributeError) as e:
                logging.error("Failed to convert Prophet model to json: ")
                raise e
                
    except (FileNotFoundError, PermissionError) as e: 
        logging.error("Failed to save model for specified path: ")
        raise e

def load_model(filename):
    try:
        with open(filename, 'r') as fin:
            try:
                return model_from_json(fin.read())
            except (JSONDecodeError) as e:
                logging.error("Failed to decode Prophet model from json:")
                raise e
    except (FileNotFoundError, PermissionError) as e: 
        logging.error("Failed to load model for specified path: ")
        raise e

def save_sklearn_model(model, filename):
    with open(filename, 'wb') as f:
        dump(model, f)
        
def load_sklearn_model(filename):
    with open(filename, 'rb') as f:
        return load(f)        