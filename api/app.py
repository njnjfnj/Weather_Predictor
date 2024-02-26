import flask
from flask import make_response, jsonify
from ..scripts.model_prediction.model_prediction import predict_city_weather
from ..redis_scripts.get import get_city
app = flask.Flask(__name__)

@app.route("/predict/<city_name>/<prediction_hours>")
def predict_weather(city_name, prediction_hours):
    json_data = predict_city_weather(city_name=city_name, prediction_hours=prediction_hours)
    meta = {
        'status': 'success',
        'message': 'Data retrieved successfully'
    }
    response = {
        'data': json_data,
        'meta': meta
    }
    headers = {
        'Content-Type': 'application/json'
    }
    return make_response(jsonify(response), 200, headers)
     
@app.route("/cities/<city_name>")
def get_city_info(city_name):
    return get_city(city_name)

