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
    get_all_cities()
    excel_data_df = pandas.read_excel(file_name)
    cities = excel_data_df.to_json(orient='records')

    return pandas.read_json(cities)


def get_five_cities(list_data:list) -> dict:
    return list_data.sample(n=5).to_dict('records')


def prepare_city_data(cities_data=get_five_cities(read_excel()) )-> list:
    cities_list = []


    for i in cities_data:

        data = get_city_weather(i['lat'], i['lon'])

        cities_list.append(
            {'city': i['name'], 
            'country':i['country'],
            'weather': data[0],
            'temp': float(data[1]),
            'humidity': float(data[2])})
        
    return cities_list

def get_city_by_name(city):

    all_cities= read_excel()
    searching_city = all_cities[all_cities["name"].str.contains(city.capitalize())==True].to_dict('list')

    if len(searching_city['name']) > 1:
        print('\nFind is more by one city: '+ ', '.join(searching_city['name']) + '. Choose one.\n')
    
    elif len(searching_city['name']) == 0:
        print(f'\nThe {city} is not found\n')
    
    else:
        city_data = [{i:searching_city[i][0] for i in searching_city}]
        result = prepare_city_data(city_data)
        [city, country, weather, temp, humidity] = result[0].values()

        print(f'\nThe weather in {city}/{country} is {weather} with current temperature {temp} Celsium and humidity {humidity}%.\n')

def visualise_data(data = prepare_city_data()):
    #Get random 5 cities {city, country, weather, temp, humidity}    

    for city_data in data:
        [city, country, weather, temp, humidity] = city_data.values()
        print(f'The weather in {city}/{country} is {weather} with current temperature {temp} Celsium and humidity {humidity}%.')
    
    print('-'*100)

    coldest_city = functools.reduce(lambda a, b: a if a['temp'] < b['temp'] else b, data)['city']
    average_temp = round(sum([i['temp'] for i in data])/ len(data), 2)

    print(f'The coldest city: {coldest_city}\n')
    print(f'The average temperature: {average_temp} Celsium\n')
    print('-'*100)


#interface menu
menu_options = {
    1: "Search city by name",
    2: "Refresh",
    0: 'Exit'
}

def print_menu():
    for key in menu_options.keys():
        print (key, '--', menu_options[key] )



if __name__=='__main__':
    get_all_cities()
    #visualize data for 5 random cities and write info about coldest city and average temperature
    visualise_data()

    while(True):
        print_menu()
        option = ''
        try:
            option = int(input('Choose the option: '))
        except:
            print('Wrong option. Choose correct option ..')

        if option == 1:
           city_name = input('Insert city name: ')
           get_city_by_name(city_name)
        elif option == 2:
            visualise_data()
        elif option == 0:
            print('The window is closing.')
            exit()

