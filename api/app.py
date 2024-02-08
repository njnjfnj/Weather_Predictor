import flask
from flask import Response
from ..scripts.model_prediction.model_prediction import predict_city_weather    
app = flask.Flask(__name__)

@app.route("/predict/<city_name>/<prediction_hours>")
def predict_weather(city_name, prediction_hours):
    # csv_data = predict_city_weather(city_name=city_name, prediction_hours=prediction_hours)
    response = Response(f"{city_name},{prediction_hours}", content_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=weather.csv"
    return response
     

