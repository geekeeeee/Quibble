from typing import Final
import os 
from dotenv import load_dotenv
from random import randint
import requests, json, discord

load_dotenv()
weather_token : Final[str] = os.getenv('WEATHER')

def weath(location : str) :
    weather_url = f'https://api.weatherapi.com/v1/current.json?q={location}&key={weather_token}'
    response = requests.get(weather_url)
    response_json = json.loads(response.text)
    if response.status_code == 200:
        condition_text = response_json['current']['condition']['text']
        temp_celsius = response_json['current']['temp_c']
        title = condition_text + " \nTemp: " + str(temp_celsius) + " Cel"
        img = response_json['current']['condition']['icon']
        embedd= discord.Embed(title=title, description='', color=0xff69b4)

        if img.startswith("//"):  # Check for valid URL format
            embedd.set_thumbnail(url= 'https:' + img)
        return embedd

    return discord.Embed(title="City not found", description='', color=0xff69b4)

def embedded(message):
  title = message
  description = ""

  embed = discord.Embed(title=title, description=description, color=0xff69b4)

  return embed

def get_response (uinput: str):
    uinput = uinput.lower()
    response = ''
    if(uinput == '') : 
        response = 'Hello are you there?'
    elif 'hello' in uinput : 
        response = 'Hello mate !'
    elif 'how are you' in uinput : 
        response = 'Great Day, Cheers mate'
    elif 'bye' in uinput :
        response = 'See ya!'
    elif uinput.startswith('weather ') :
        return weath(uinput[8:])
    elif 'roll dice' in uinput :
        ran = randint(0,5)
        dice = ""
        if(ran == 0) :
            dice = "1 ⚀"
        elif(ran == 1) :
            dice = "2 ⚁"
        elif(ran == 2) :
            dice = "3 ⚂"
        elif(ran == 3) :
            dice = "4 ⚃"
        elif(ran == 4) :
            dice = "5 ⚄"
        elif(ran == 5) :
            dice = "6 ⚅"
        
        response = f'You rolled a {dice} '
    else: 
        response = 'Please rephrase that, mate!'
    return embedded(response)
