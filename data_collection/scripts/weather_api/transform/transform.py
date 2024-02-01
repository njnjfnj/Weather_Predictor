def transform_weather_json(json_str):
    info = json_str['list'][0]
    timestamp = info['dt']
    temp = float(info['main']['temp']) - 273.15 
    feels_like = float(info['main']['feels_like']) - 273.15
    pressure = info['main']['pressure']
    humidity = info['main']['humidity']
    temp_min = float(info['main']['temp_min']) - 273.15
    temp_max = float(info['main']['temp_max']) - 273.15
    wind_speed = info['wind']['speed'] * 3.6
    wind_deg = info['wind']['deg']
    clouds_coverage = info['clouds']['all']
    weather_category = info['weather'][0]['main']
    weather_description = info['weather'][0]['main']

    arr = [timestamp, temp, feels_like, pressure, humidity, temp_min, temp_max, wind_speed, wind_deg, clouds_coverage, weather_category, weather_description]
    
    return arr