import discord
import requests, json
from datetime import datetime, timedelta

BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
degreeSign = u"\N{DEGREE SIGN}"
OpenWeatherKey = "30d8c43f0d2614036e2957739678963a"

#discord configuration w/ API
#this requires a valid discord token that is provided when you register the bot with Discord
TOKEN = 'OTQxMDM2NzM1ODY4MDQzMzE1.YgQGwQ.Yb-_W8DSw533XjwoWflrF8fs6Nw'
SERVER = 'BotTestingGround'

client = discord.Client()
discord.Intents(members=True)

global serverConnected

#variables to protect from bot spam
global msgCount
global currentTime
global firstMsgDate
global lastCooldownDate
firstMsgDate = datetime(2000, 1, 1)
lastCooldownDate = datetime(2000, 1, 1)


@client.event
async def on_ready():
    global serverConnected
    for server in client.guilds:
        if server.name == SERVER:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{server.name}(id: {server.id})'
    )
    serverConnected = server
    global msgCount
    msgCount = 0


#this code triggers when a message is sent
@client.event
async def on_message(message):
    global msgCount
    global lastCooldownDate
    global currentTime
    global firstMsgDate

    global serverConnected

    #dont trigger on bot-sent messages
    if message.author == client.user:
        return

    #dont trigger in defined channels
    if (message.channel.name == 'demo-channel'): #or (message.channel.name == 'test-channel'):
        return

    #!weather CITYNAME triggers the bot to print a basic weather report of the inputted city
    if ('!weather' in message.content.lower()):

        #get city name from second part of argument string and build URL request w/ OpenWeatherMap developer API key
        CITY = str(message.content)[9:]
        URL = BASE_URL + "q=" + CITY + "&units=imperial" + "&appid=" + OpenWeatherKey

        response = requests.get(URL)
        if response.status_code == 200:

            data = response.json()

            #store weather information from json payload
            primaryWeatherDataDict = data['main']
            temperature = primaryWeatherDataDict['temp']
            humidity = primaryWeatherDataDict['humidity']
            weatherDescriptionDict = data['weather']
            cityName = data['name']

            #build formatted string to print information in the discord text channel
            stringToPrint = "Weather Report for: " + cityName + "\n The current temperature is " + str(temperature) + degreeSign + "F" + "\n The current humidity is " + str(humidity) + "%" + "\n Other information: " + weatherDescriptionDict[0]['description']
            await message.channel.send(stringToPrint)

        else:
            print("ERROR - API KEY LIKELY BROKEN")

    #!changenickname / targetuser / targetnickname
    #this code allows a user to change the nickname of another user (if the bot has permission configured on the server)
    if'!changenickname' in message.content.lower():
        changeNicknameMsgList = message.content.split('/')
        #get current "nickname" and "nickname" to update to and set
        targetUserNickname = changeNicknameMsgList[1]
        targetNickname = changeNicknameMsgList[2]
        listOfUsers = await serverConnected.query_members(targetUserNickname)
        for user in listOfUsers:
            await user.edit(nick=targetNickname)
        return

    #if "dead cord" is printed in a channel, the bot will respond with "ironic"
    #this can obviously be easily reconfigured to reply to any message with any other text
    #most of the code is implementing a basic "timeout" - if the bot sends 5 messages within 5 minutes
    #it will stop responding until another 5 minutes has passed

    if 'hello bot' in message.content.lower():
        currentTime = datetime.now()
        if lastCooldownDate + timedelta(minutes=5) >= currentTime:
            return
        if (msgCount == 5) & (firstMsgDate + timedelta(minutes=5) >= currentTime):
            lastCooldownDate = datetime.now()
            msgCount = 0
            return
        if firstMsgDate + timedelta(minutes=5) <= currentTime:
            msgCount = 0
        if msgCount == 0:
            firstMsgDate = datetime.now()
        msgCount = msgCount + 1
        await message.channel.send('hi alek')


client.run(TOKEN)
