import pytest 

from unittest.mock import patch, Mock, MagicMock

from src.scripts.model_prediction.model_prediction import (load_prophet_model, load_sklearn_model)

from src.scripts.model_prediction.model_prediction import (
    predict_hourly_city_weather, open_weather_models
)

import pandas as pd 



@pytest.fixture
def get_model_target_params():
    return {
        'humidity',
        'pressure',
        'temp',
        'wind_speed',
        'feels_like',
        'clouds_percentage',
        'sun_horison_angle',
        'precipitation',
        'wind_direction',
        'weather_description'
    }


@pytest.mark.parametrize(("city_name", "prediction_hours", "expected_filepaths", "expected_prediction_hours"),
                         [
                             ("New Jersey", 240, 
                             [
                                 "/home/soloclimb/code/projects/Weather_Predictor/src/scripts/model_prediction/../../../data/models/New Jersey/humidity.json",
                                 "/home/soloclimb/code/projects/Weather_Predictor/src/scripts/model_prediction/../../../data/models/New Jersey/pressure.json",
                                 "/home/soloclimb/code/projects/Weather_Predictor/src/scripts/model_prediction/../../../data/models/New Jersey/temp.json",
                                 "/home/soloclimb/code/projects/Weather_Predictor/src/scripts/model_prediction/../../../data/models/New Jersey/wind_speed.json",
                                 "/home/soloclimb/code/projects/Weather_Predictor/src/scripts/model_prediction/../../../data/models/New Jersey/feels_like.json",
                                 "/home/soloclimb/code/projects/Weather_Predictor/src/scripts/model_prediction/../../../data/models/New Jersey/clouds_percentage.json",
                                 "/home/soloclimb/code/projects/Weather_Predictor/src/scripts/model_prediction/../../../data/models/New Jersey/sun_horison_angle.json",
                                 "/home/soloclimb/code/projects/Weather_Predictor/src/scripts/model_prediction/../../../data/models/New Jersey/precipitation.json",
                                 "/home/soloclimb/code/projects/Weather_Predictor/src/scripts/model_prediction/../../../data/models/New Jersey/wind_direction.json",
                                 "/home/soloclimb/code/projects/Weather_Predictor/src/scripts/model_prediction/../../../data/models/New Jersey/weather_description.pkl",
                            ], 240)
                         ])
@patch('src.scripts.model_prediction.model_prediction.match_time_difference')
@patch('os.path.isfile')
@patch('src.scripts.model_prediction.model_prediction.load_prophet_model')
@patch('src.scripts.model_prediction.model_prediction.load_sklearn_model')
def test_open_weather_models(load_sklearn, load_prophet, is_file, 
                             match_time_difference, city_name, 
                             prediction_hours, expected_filepaths,
                             expected_prediction_hours, get_model_target_params):
    
    load_prophet_mock = Mock()
    load_prophet_mock.history.tail = MagicMock()
    
    ds_mock = Mock()
    ds_mock.iloc = [0]

    load_prophet_mock.history.tail.return_value = {"ds": ds_mock}

    load_sklearn_mock = Mock()


    load_prophet.return_value = load_prophet_mock
    load_sklearn.return_value = load_sklearn_mock
    
    match_time_difference.return_value = 0
    
    is_file_mock = Mock()
    is_file.return_value = is_file_mock
    
    result = open_weather_models(city_name, prediction_hours, get_model_target_params)
    
    is_file_calls = is_file.call_args_list

    # for i in range(len(is_file_calls)):
    #     args, kwargs = is_file_calls[i]
    #     assert args[0] == expected_filepaths[i]
        
    assert set(result.keys()) == {'models', 'prediction_hours'}
    
    assert set(result['models'].keys()) == get_model_target_params
    
    assert result['prediction_hours'] == expected_prediction_hours


from random import uniform, randint

@pytest.fixture(params=[49])
def future_prophet_df(request):
    hours = request.param
    return pd.DataFrame({"ds": pd.date_range(start="2024-03-29 00:00:00", end="2024-03-31 00:00:00", freq="h"),
                            "yhat": [uniform(0, 30) for i in range(hours)]})

@pytest.fixture(params=[49])
def sklearn_DTC_predict(request):
    hours = request.param
    return [["Sun", "Rain", "Fog", "Snow"][randint(0, 3)] for i in range(hours)]

def model_predict_side_effect(value):
    return value


@pytest.fixture(params=[['humidity', 'pressure', 'temp','weather_description']])
def models_dict(request, future_prophet_df, sklearn_DTC_predict):
    result = {}
    features = request.param
    for feature in features:
        result[feature] = Mock()
        if feature != 'weather_description':
            result[feature].make_future_dataframe.return_value = future_prophet_df
            result[feature].predict.side_effect = model_predict_side_effect
        else:
            result[feature].predict.return_value = sklearn_DTC_predict 
    return result



@pytest.mark.parametrize(('city_name', 'prediction_hours', 'target_params'),
                         [("Miami", 240, ['humidity','pressure','temp','weather_description'])]
                        )
@patch('src.scripts.model_prediction.model_prediction.check_city_name')
@patch('src.scripts.model_prediction.model_prediction.open_weather_models')
def test_predict_hourly_city_weather(open_weather_models_patched, check_city_name, city_name, prediction_hours,
                                     target_params, models_dict):
    open_weather_models_patched.return_value = {"models": models_dict, "prediction_hours": prediction_hours}
    check_city_name.return_value =  True
    
    result = predict_hourly_city_weather(city_name=city_name,
                                         prediction_hours=prediction_hours,
                                         target_params=target_params)
    
    assert result["status"] == "success"