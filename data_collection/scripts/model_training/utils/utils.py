from prophet.serialize import model_to_json, model_from_json

def save_model(model, filename):
    with open(filename, 'w') as fout:
        fout.write(model_to_json(model)) 
        
def load_model(filename):
    with open(filename, 'r') as fin:
        return model_from_json(fin.read())