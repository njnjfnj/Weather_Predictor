import pytest 

from unittest.mock import patch, Mock, MagicMock

from src.scripts.model_prediction.model_prediction import (load_prophet_model, load_sklearn_model)

from src.scripts.model_prediction.model_prediction import (
    predict_hourly_city_weather, predict_daily_city_weather, open_weather_models
)


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