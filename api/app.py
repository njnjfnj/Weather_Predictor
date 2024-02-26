import flask
from json import loads
from flask import make_response, jsonify
from ..scripts.model_prediction.model_prediction import predict_city_weather
from ..redis_scripts.get import get_city, get_all_cities
app = flask.Flask(__name__)

def construct_response(data, headers):
    if_message = ''
    if "message" in data.keys():
        if_message = data["message"]
    response = {
        'data': data["result"],
        'meta': data["status"],
        'message': if_message
    }
    status_code = 200 if response['meta'] == "success" else 404
    return make_response(jsonify(response), status_code, headers)


@app.route("/predict/<city_name>/<prediction_hours>")
def predict_weather(city_name, prediction_hours):
    json_data = predict_city_weather(city_name=city_name, prediction_hours=prediction_hours)
    headers = {
        'Content-Type': 'application/json'
    }
    return construct_response(json_data, headers)
    
     
@app.route("/cities/<city_name>")
def get_city_info(city_name):
    city_data = loads(get_city(city_name))
    headers = {
        'Content-Type': 'application/json'
    }
    return construct_response(city_data, headers)


@app.route("/cities/")
def get_cities_info():
    cities_data = loads(get_all_cities())
    headers = {
        'Content-Type': 'application/json'
    }
    return construct_response(cities_data, headers)

