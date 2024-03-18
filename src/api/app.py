import flask
from json import loads
from flask import make_response, jsonify, request
from ..scripts.model_prediction.model_prediction import predict_hourly_city_weather, predict_daily_city_weather
from ..redis.get import get_city, get_all_cities, get_number_of_cities
from flask_cors import CORS
app = flask.Flask(__name__)
CORS(app)

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
def predict_hourly_weather(city_name, prediction_hours):
    json_data = predict_hourly_city_weather(city_name=city_name, prediction_hours=prediction_hours)
    headers = {
        'Content-Type': 'application/json'
    }
    return construct_response(json_data, headers)
    
@app.route("/predict/<city_name>/days/<prediction_daily>")
def predict_daily_weather(city_name, prediction_daily):
    json_data = predict_daily_city_weather(city_name=city_name, prediction_days=prediction_daily)
    headers = {
        'Content-Type': 'application/json'
    }
    return construct_response(json_data, headers)



@app.route("/cities/total/", defaults={"city_name": ""})
@app.route("/cities/total/<city_name>")
def get_total_cities_count(city_name):
    city_data = loads(get_number_of_cities(city_name))
    headers = {
        'Content-Type': 'application/json'
    }
    return construct_response(city_data, headers)



@app.route("/cities/<city_name>")
def get_city_info(city_name):
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 6))
    city_data = loads(get_city(city_name, page, limit))
    headers = {
        'Content-Type': 'application/json'
    }
    return construct_response(city_data, headers)


@app.route("/cities/")
def get_cities_info():
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 6))
    cities_data = loads(get_all_cities(page=page, limit=limit))
    headers = {
        'Content-Type': 'application/json'
    }
    return construct_response(cities_data, headers)

