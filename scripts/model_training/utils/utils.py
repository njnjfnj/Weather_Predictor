from prophet.serialize import model_to_json, model_from_json
from pickle import dump, load, dumps

from os import path, makedirs
from json import JSONDecodeError

def save_model(model, filename):
    makedirs(path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as fout:
        fout.write(model_to_json(model)) 
        
def load_model(filename):
    try:
        with open(filename, 'r') as fin:
            return model_from_json(fin.read())
    except JSONDecodeError as e:
        print(e)

def save_sklearn_model(model, filename):
    with open(filename, 'wb') as f:
        dump(model, f)
        
def load_sklearn_model(filename):
    with open(filename, 'rb') as f:
        return load(f)        