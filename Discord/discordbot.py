import os # used with dotenv to load tokens from .env
from dotenv import load_dotenv # used with os to load tokens from .env
from asyncio import sleep # 
import requests # for API calls to OpenWeather
import json # for working with API responses
import discord 
from discord.ext import commands # Import the bot from the discord.ext.commands module

# Load tokens from .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
API = os.getenv('WEATHER_API')

# Change the default help command heading
category_heading = commands.DefaultHelpCommand(
    no_category = 'WeatherBot Commands'
)

# Initiate the bot using a command prefix
bot = commands.Bot(command_prefix='%', help_command = category_heading)

# Print to the console that the bot is connected
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected Discord!')

# Emoji selection
def get_emoji(resp):
    switcher = {
        "Thunderstorm": " :thunder_cloud_rain:",
        "Drizzle": " :cloud_rain:",
        "Rain": " :cloud_rain:",
        "Snow": " :snowflake:",
        "Clear": "",
        "Tornado": " :cloud_tornado:",
        "Clouds": " :cloud:"       
    }
    return switcher.get(resp.json()['weather'][0]['main'], "")

# "zip" command for looking up weather based on ZIP code
@bot.command(name="zip", help='Display the weather for the ZIP code you specify. Takes a ZIP code as the argument.')
async def zip(ctx, arg):
    response = requests.get("http://api.openweathermap.org/data/2.5/weather?zip={},us&appid={}&units=imperial".format(arg, API))
    
    temperature = round(response.json()['main']["temp"])
    location = response.json()['name']
    description = response.json()['weather'][0]['description']

    await ctx.send("It is currently {}° F in {} with {}{}.".format(temperature, location, description, get_emoji(response)))
    print(f'{bot.user.name} sent the weather by ZIP code.')

# "city" command for looking up weather based on city name
@bot.command(name="city", help='''Display the weather for the city you specify. Takes a city name as the argument. 
If your city\'s name is comprised of more than one word, it must be wrapped in quotations (e.g. "San Francisco").''')
async def city(ctx, arg):
    response = requests.get("http://api.openweathermap.org/data/2.5/weather?q={},us&appid={}&units=imperial".format(arg, API))
    
    temperature = round(response.json()['main']["temp"])
    location = response.json()['name']
    description = response.json()['weather'][0]['description']

    await ctx.send("It is currently {}° F in {} with {}{}.".format(temperature, location, description, get_emoji(response)))
    print(f'{bot.user.name} sent the weather by city name.')

bot.run(TOKEN)
