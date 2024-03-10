import requests
import random
import functools
from flask import Flask, render_template, request

from utils.all_cities import cities

app = Flask(__name__)

def get_city_data(city):
        API_KEY = "f68e81d7220e100810fc7350499502e9"
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric")
        return response.json()


def get_weather_cities():
    cities_list = []

    for city in random.sample(cities, 5):
        city_data = get_city_data(city)
        cities_list.append({
            'city': city,
            'weather': city_data["weather"][0]["main"],
            'temp': city_data["main"]["temp"],
            'humidity': city_data["main"]["humidity"]
        })
    return cities_list


def get_average_temp(cities_data):
    return sum([city['temp'] for city in cities_data])/5  
    
    
def get_coldest_city(cities_data):
    return functools.reduce(lambda a, b: a if a['temp'] < b['temp'] else b, cities_data)['city']


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        city = request.form["city"].capitalize()
        city_data = get_city_data(city)

        return render_template("index.html", city=city, temperature=city_data["main"]["temp"], humidity=city_data["main"]["humidity"], weather=city_data["weather"][0]["main"])
    
    else:
        cities_weather = get_weather_cities()
        coldest_city = get_coldest_city(cities_weather)
        average_temp = round(get_average_temp(cities_weather),2)
        
        return render_template('index.html', cities_weather=cities_weather, coldest_city=coldest_city, average_temp=average_temp)

app.run()