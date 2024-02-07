import flask
from ..scripts.model_prediction.model_prediction import predict_city_weather

app = flask.Flask(__name__)

@app.route("/predict/<city_name>/<prediction_hours>")
def predict_weather(city_name, prediction_hours):
    return predict_city_weather(city_name=city_name, prediction_hours=prediction_hours)

