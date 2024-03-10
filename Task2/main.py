import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
import requests

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather App")
        self.layout = QVBoxLayout()
        self.city_labels = []
        self.create_city_labels()
        self.setLayout(self.layout)
        self.get_weather_data()

    def create_city_labels(self):
        for _ in range(5):
            city_label = QLabel()
            self.city_labels.append(city_label)
            self.layout.addWidget(city_label)

    def get_weather_data(self):
        cities = ["London", "Paris", "Berlin", "New York", "Tokyo"]
        API_KEY = "f68e81d7220e100810fc7350499502e9"
        for i, city in enumerate(cities):
            response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric")
            data = response.json()
            temperature = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            self.city_labels[i].setText(f"{city}: Temperature - {temperature}°C, Humidity - {humidity}%")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec())
