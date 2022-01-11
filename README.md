# Discord-Bots
A repository of different discord bot functionality I have implemented for servers I use with friends.

Development notes:
Can restrict bot response condition using Discord API by username (don't reply to user X), channel name (don't reply in channel Y), etc.
Latency is a problem. If too many triggers are received by the code at the same time from Discord it can cause unintended functionality.

Planned Experimental Features:
Ability to record voice communication and then process w/ open source software into text. This would allow for some cool data visualization of language used in different online communities. Words more often said in different servers, different voice channels, by different people could be calculated.

TO RUN:
1. Follow discord instructions to add bot to server at https://discordpy.readthedocs.io/en/stable/discord.html
2. Enter token from discord in line 6 empty string
3. Replace server name "BotTestingGround" with the server name the bot is invited to on line 7
4. Run !
