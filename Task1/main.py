import requests
import os.path
import pandas
import functools



#get list with weather type, temperature and himidity by lat and lot
def get_city_weather(lat, lon, API_KEY = 'f68e81d7220e100810fc7350499502e9') -> list:
    r = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={API_KEY}')
    content = r.json()

    return [content['weather'][0]['main'], content['main']['temp'], content['main']['humidity']] #[weather type, temperature, humidity]


def get_all_cities()-> None:
    if not os.path.isfile('cities_list.xlsx'):
        all_cities_url = 'https://openweathermap.org/storage/app/media/cities_list.xlsx'
        data = requests.get(all_cities_url)
        
        with open('cities_list.xlsx', 'wb') as output:
            output.write(data.content)


def read_excel(file_name='cities_list.xlsx'):
    excel_data_df = pandas.read_excel(file_name)
    cities = excel_data_df.to_json(orient='records')

    return pandas.read_json(cities)


def get_five_cities(list_data:list) -> dict:
    return list_data.sample(n=5).to_dict('records')


def prepate_city_data():
    cities_list = []
    coldest_city = ''
    average_temp = float

    get_all_cities()
    five_cities_list = get_five_cities(read_excel())
    
    for i in five_cities_list:
        data = get_city_weather(i['lat'], i['lon'])

        cities_list.append(
            {'city': i['name'], 
            'country':i['country'],
            'weather': data[0],
            'temp': float(data[1]),
            'humidity': float(data[2])})

    coldest_city = functools.reduce(lambda a, b: a if a['temp'] < b['temp'] else b, cities_list)['city']
    average_temp = round(sum([i['temp'] for i in cities_list])/ len(cities_list), 2)

    print(coldest_city, average_temp)


prepate_city_data()