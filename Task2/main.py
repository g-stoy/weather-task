import sys
import os.path
import requests
import pandas
import random
import functools
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit


class WeatherApp(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather App")
        self.layout = QVBoxLayout()
        self.cities_data = []
        self.city_labels = []
        self.create_city_labels()
        self.setLayout(self.layout)
        self.average_temp_label = QLabel()
        self.layout.addWidget(self.average_temp_label)
        self.coldest_city_label = QLabel()
        self.layout.addWidget(self.coldest_city_label)
        self.get_weather_data()
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.get_weather_data)
        self.layout.addWidget(self.refresh_button)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter city name...")
        self.layout.addWidget(self.search_input)
        self.search_buton = QPushButton('Search')
        self.search_buton.clicked.connect(self.search_city_weather)
        self.layout.addWidget(self.search_buton)
        self.search_city = QLabel()
        self.layout.addWidget(self.search_city)

    def create_city_labels(self):
        for _ in range(5):
            city_label = QLabel()
            self.city_labels.append(city_label)
            self.layout.addWidget(city_label)


    def api_connection(self, city):
        API_KEY = "f68e81d7220e100810fc7350499502e9"
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric")
        return response.json()


    def get_average_temp(self):
        return sum([i['temp'] for i in self.cities_data])/5  
    
    def get_coldest_city(self):
        return functools.reduce(lambda a, b: a if a['temp'] < b['temp'] else b, self.cities_data)['city']
    

    def get_weather_data(self):
        cities = random.sample(self.get_all_cities(), 5)

        for i, city in enumerate(cities):
            data = self.api_connection(city)
            temperature = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            self.cities_data.append({'city': city, 'temp': temperature})
            self.city_labels[i].setText(f"<b>{city}</b>: Temperature : {temperature}°C, Humidity : {humidity}%")

        self.average_temp_label.setText(f'The average temperature for these 5 cities: <b> {round(self.get_average_temp(), 2)}°C</b>')
        self.coldest_city_label.setText(f'The coldest city of these 5 is: <b>{self.get_coldest_city()}</b>')


    def get_all_cities(self)-> list:
        if not os.path.isfile('cities_list.xlsx'):
            all_cities_url = 'https://openweathermap.org/storage/app/media/cities_list.xlsx'
            data = requests.get(all_cities_url)
        
            with open('cities_list.xlsx', 'wb') as output:
                output.write(data.content)

        excel_data_df = pandas.read_excel('cities_list.xlsx')

        return excel_data_df['name'].to_list()
    
    def search_city_weather(self):
        all_cities = self.get_all_cities()
        city_name = self.search_input.text().capitalize()
        if city_name:
            if city_name in all_cities:
                data = self.api_connection(city_name)
                temperature = data["main"]["temp"]
                humidity = data["main"]["humidity"]
                self.search_city.setStyleSheet("color: black;")
                self.search_city.setText(f"{city_name}: Temperature : {temperature}°C, Humidity : {humidity}%")
            else:
                self.search_city.setStyleSheet("color: red;")
                self.search_city.setText(f"The {city_name} is not found!")
            self.search_input.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec())
