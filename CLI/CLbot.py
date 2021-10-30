import argparse # for parsing arguments put into the command line
import requests # for API calls to OpenWeather
import json # for working with API responses
import os # used with dotenv to load tokens from .env
from dotenv import load_dotenv # used with os to load tokens from .env

# Load tokens from .env
load_dotenv()
API = os.getenv('WEATHER_API')

# Command-line argument parser
parser = argparse.ArgumentParser(description="Look up the weather for your location.")

# ZIP code and city name arguments
parser.add_argument('--zipcode', metavar='Z', type=int, nargs=1, help='Your zip for looking up the weather in your zip code.')
parser.add_argument('--city', metavar='C', type=str, nargs='*', help='Your city name for looking up the weather in your city.')

# Arguments in object returned from parser.parse_args() should be accessed via properties
args = parser.parse_args()

# Emoji selection
def get_Emoji(resp):
    switcher = {
        "Thunderstorm": " \U000026C8",
        "Drizzle": " \U0001F327",
        "Rain": " \U0001F327",
        "Snow": " \U00002744",
        "Clear": "",
        "Tornado": " \U0001F32A",
        "Clouds": " \U00002601"      
    }
    return switcher.get(resp.json()['weather'][0]['main'], "")


# For debug purposes
# Print JSON with indentations for readability
def printjson(j):
    readable = json.dumps(j, sort_keys=True, indent=4)
    print(readable)

# If a zipcode is present in args, request the weather and display it
if (args.zipcode):
    try:
        # Get weather by ZIP code API call
        response = requests.get("http://api.openweathermap.org/data/2.5/weather?zip={},us&appid={}&units=imperial".format(args.zipcode[0], API))
        
        # Weather variables
        temperature = round(response.json()['main']["temp"])
        location = response.json()['name']
        description = response.json()['weather'][0]['description']

        # Print out the current weather
        print(get_Emoji(response))
        print("It is currently {}° F in {} with {}.".format(temperature, location, description))
    except:
        print("An error occured.")

# If a city name is present in args, request the weather and display it
if (args.city):
    try:
        # Get weather by city API call
        response = requests.get("http://api.openweathermap.org/data/2.5/weather?q={},us&appid={}&units=imperial".format(' '.join(args.city), API))

        # Weather variables
        temperature = round(response.json()['main']["temp"])
        location = response.json()['name']
        description = response.json()['weather'][0]['description']

        # Print out the current weather
        print(get_Emoji(response))
        print("It is currently {}° F in {} with {}.".format(temperature, location, description))
    except:
        print("An error occured.")