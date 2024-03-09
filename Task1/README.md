## Weather API requests

* Weather API:
    * http://openweathermap.org/api
	
* Description
    * Display the current weather, temperature and humidity in five random world cities.
    * Display the average temperature and the most colder city from these five.
    * Display the current weather, tempetarure and humidiby for inserted city. 

* Logical steps
    * Get excel file with all available cities in openweathermap.org and save in current directory
    * Get random five cities from all available and display temperature, humidity and weather
    * It's possible to insert city and get information about the weather.

* Used library
    * requests - to get data from API
    * os.path - to check if excel file is already downloaded
    * pandas - to read excel file 
    * functools - to use reduce function for determination the coldest city and the average temperature

* Way to use like .exe application
    * In function get_city_weather change the value for attribute API_KEY with your key
    * Open PowerShell in directory where the main.py file is (cd "./your_directory")
	* Install the Virtual evniroment library like py -m pip install virtualenv
	* Create virtual enviroment py -m virtualenv venv (Where venv is the virtual enviroment name)
	* Activate the virtual enviroment (venv/scripts/activate)
	* Install all the external libraries (requests and pandas)
	* Create one file exe (PyInstaller --onefile main.py)
	* Close the virtual enviroment (deactivate)
	* The exe file is in folder dist
	
* The menu options:
	1: "Search city by name" - Search the weather by city name
    2: "Refresh" - Get the weather information about 5 random cities
    0: "Exit" - close the program
	