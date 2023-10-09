import requests
from config import WEATHER_API_KEY


# change this key in config.py file of base directory
api_key = WEATHER_API_KEY

# Function to fetch weather data by coordinates
def fetch_weather(lat, lon):
    base_url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {
        'lat': lat,
        'lon': lon,
        'appid': api_key,
        'units': 'metric',  # you can use 'imperial' for Fahrenheit
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        temperature = data['main']['temp']
        return temperature
    else:
        return None
