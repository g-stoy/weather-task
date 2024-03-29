import functools
import requests
import random

from django.shortcuts import render
from django.http import JsonResponse

from weather.models import City, all_cities


def home(request):
    cities = get_weather_cities()
    average_temp = round(get_average_temp(cities), 2)
    coldest_city = get_coldest_city(cities)
    return render(request, "index.html", {'cities':cities, 'average_temp': average_temp, 'coldest_city': coldest_city })


def get_city_data(city):
        API_KEY = "f68e81d7220e100810fc7350499502e9"
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric")
        return response.json()


def get_weather_cities():
    cities_list = []
    cities = list(all_cities.objects.all().values())

    for city in random.sample(cities, 5):
        city_data = get_city_data(city['city_name'])
        cities_list.append({
            'city': city_data['name'],
            'weather': city_data["weather"][0]["main"],
            'temp': city_data["main"]["temp"],
            'humidity': city_data["main"]["humidity"]
        })
        city_instance = all_cities.objects.get(id =city['id'])
        City.objects.create(city_id=city_instance, weather=city_data["weather"][0]["main"], 
                            temp=city_data["main"]["temp"], humidity=city_data["main"]["humidity"])
    return cities_list


def get_average_temp(cities_data):
    return sum([city['temp'] for city in cities_data])/5  
    
    
def get_coldest_city(cities_data):
    return functools.reduce(lambda a, b: a if a['temp'] < b['temp'] else b, cities_data)['city']

def get_current_city(request):
    city = request.GET.get('city')

    data = get_city_data(city)
    city_instance = all_cities.objects.get(city_name = data["name"])
    City.objects.create(city_id=city_instance, weather=data["weather"][0]["main"], 
                            temp=data["main"]["temp"], humidity=data["main"]["humidity"])

    return JsonResponse({'city': data["name"],
            'weather': data["weather"][0]["main"],
            'temp': data["main"]["temp"],
            'humidity': data["main"]["humidity"]})

def refresh(request):
    weathers = get_weather_cities()
    average_temp = round(get_average_temp(weathers), 2),
    coldest_city = get_coldest_city(weathers)
    return JsonResponse({'cities':weathers, 'average_temp': average_temp, 'coldest_city': coldest_city }, safe=False)

def last_ten_records(request, category):
    comparison_data = []
    last_10_cities = City.objects.all()[:10]
    for city in last_10_cities:
        if category == 'weather':
            comparison_data.append({'city':city.city_id.city_name, 'category': city.weather})
        elif category == 'temperature':
            comparison_data.append({'city':city.city_id.city_name, 'category':city.temp})
        elif category == 'humidity':
            comparison_data.append({'city':city.city_id.city_name, 'category':city.humidity})

    return JsonResponse({'data':comparison_data})