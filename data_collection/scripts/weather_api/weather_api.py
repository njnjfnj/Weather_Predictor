import requests
from datetime import timedelta
from time import mktime

def get_city_weather_data(city, start_date, next_datetime, api_key):
    time_difference = int(city['time_difference'][1:]) if city['time_difference'][0] == '-' else int(city['time_difference'])
    adjusted_start_date = start_date - timedelta(hours=time_difference)
    hour = int(next_datetime.strftime('%H')) + time_difference
    url = f'https://history.openweathermap.org/data/2.5/history/city?lat={city["lat"]}&lon={city["lon"]}&type=hour&start={(mktime(adjusted_start_date.timetuple()))}&end={(mktime(next_datetime.timetuple()))}&appid={api_key}'
    return requests.get(url=url).json()