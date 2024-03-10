import requests
import random
from flask import Flask, render_template

from utils.all_cities import cities

app = Flask(__name__)

def get_city_data(city):
        API_KEY = "f68e81d7220e100810fc7350499502e9"
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric")
        return response.json()

def get_weather_cities():
    cities_list = []
    print(random.sample(cities, 5))
    for city in random.sample(cities, 5):
        city_data = get_city_data(city)
        cities_list.append({
            'city': city,
            'temp': city_data["main"]["temp"],
            'humidity': city_data["main"]["humidity"]
        })
    return cities_list

@app.route('/')

def home():
    cities_weather = get_weather_cities()
    return render_template('index.html', cities_weather=cities_weather)

app.run()