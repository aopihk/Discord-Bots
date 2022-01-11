import discord
from datetime import datetime, timedelta

#discord configuration w/ API
#this requires a valid discord token that is provided when you register the bot with Discord
TOKEN = ''
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
    if (message.channel.name == 'bot-feature-requests') or (message.channel.name == 'dj-booth'):
        return

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

    if 'dead cord' in message.content.lower():
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
        await message.channel.send('ironic')


client.run(TOKEN)
