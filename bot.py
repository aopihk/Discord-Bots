"""
    Discord Bot, requires python > 3
"""

from datetime import datetime, timedelta
import discord

import requests

BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
DEGREE_SIGN = "\N{DEGREE SIGN}"
OPEN_WEATHER_KEY = ""

#discord configuration w/ API
#this requires a valid discord token that is provided when you register the bot with Discord
TOKEN = ''
SERVER = 'BotTestingGround'

client = discord.Client()
discord.Intents(members=True)

# no recommend to use global variables at the module level
user_spam = {}


def _get_server():
    for server in client.guilds:
        if server.name == SERVER:
            return server
    raise Exception(f'{SERVER} not found.')


CONNECTED_SERVER = _get_server()


@client.event
async def on_ready():
    """
        Find correct server and set instance variable
    """
    print(f'{client.user} is connected to the following guild:\n'
          f'{CONNECTED_SERVER.name}(id: {CONNECTED_SERVER.id})')


# this code triggers when a message is sent
@client.event
async def on_message(message):
    """
        Processes message events
    """
    # dont trigger on bot-sent messages
    if message.author == client.user:
        return

    # dont trigger in defined channels
    if message.channel.name == 'demo-channel':  #or (message.channel.name == 'test-channel'):
        return

    # !weather CITYNAME triggers the bot to print a basic weather report of the inputted city
    if '!weather' in message.content.lower():
        await process_weather_msg(message)

    #!changenickname / targetuser / targetnickname
    #this code allows a user to change the nickname of another user
    #(if the bot has permission configured on the server)
    if '!changenickname' in message.content.lower():
        await process_name_change(message)

    # if "dead cord" is printed in a channel, the bot will respond with "ironic"
    # this can obviously be easily reconfigured to reply to any message with any other text
    # most of the code is implementing a basic "timeout" - if the bot sends 5
    # messages within 5 minutes
    # it will stop responding until another 5 minutes has passed
    if 'hello bot' in message.content.lower():
        await process_hello_bot(message)


async def process_weather_msg(message):
    """
        get city name from second part of argument string and build URL request
        w/ OpenWeatherMap developer API key
    """
    city = str(message.content)[9:]
    response = requests.get(BASE_URL + "q=" + city + "&units=imperial" +
                            "&appid=" + OPEN_WEATHER_KEY,
                            timeout=30)
    if response.status_code == 200:
        data = response.json()

        #store weather information from json payload
        primary_weather_data_dict = data['main']
        temperature = primary_weather_data_dict['temp']
        humidity = primary_weather_data_dict['humidity']
        weather_desc_dict = data['weather']
        city_name = data['name']

        #build formatted string to print information in the discord text channel
        weather_string = f"""Weather Report for: {city_name}\n The current temperature is
        {str(temperature) + DEGREE_SIGN} F\n The current humidity is {str(humidity)}%\n 
        Other information: {weather_desc_dict[0]['description']}"""
        await message.channel.send(weather_string)
    else:
        print("ERROR - API KEY LIKELY BROKEN")


async def process_name_change(message):
    """
        get current "nickname" and "nickname" to update to and set
    """
    change_nickname_msg_list = message.content.split('/')
    target_user_nickname = change_nickname_msg_list[1]
    target_nickname = change_nickname_msg_list[2]
    list_of_users = await CONNECTED_SERVER.query_members(target_user_nickname)
    for user in list_of_users:
        await user.edit(nick=target_nickname)
    return


async def process_hello_bot(message):
    """
        Process hello bot with spame detection
    """
    current_time = datetime.now()
    if message.author not in user_spam:
        # last cooldown, msg count, first msg date
        user_spam[message.auther] = [datetime.now(), 0, datetime.now()]
    else:
        spam_filter = user_spam.get(message.auther)
        if spam_filter[0] + timedelta(minutes=5) >= current_time:
            return
        if (spam_filter[1] == 5) & (spam_filter[2] + timedelta(minutes=5) >=
                                    current_time):
            spam_filter[0] = datetime.now()
            spam_filter[1] = 0
            return
        if spam_filter[2] + timedelta(minutes=5) <= current_time:
            spam_filter[1] = 0
        spam_filter[1] += 1
    await message.channel.send(f'hi {message.author}')


client.run(TOKEN)
