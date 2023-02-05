import discord, logging, typing, os, asyncio, webbrowser, requests, time, random, json, aiohttp
from discord import Activity, ActivityType, async_, Embed, Guild, Intents, Member, Role, Spotify, TextChannel, Webhook
from discord.ext import commands, tasks
from discord.utils import get
from dotenv import load_dotenv

#Get token from a .env file
load_dotenv();
token = os.getenv("token");

#Setting up intents
intents = Intents.all();

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Additional functions


#Prefix of the bot
bot_prefix = "*";

class bot_class(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix = bot_prefix, help_command = None, description = "A bot developed by Fake Life#0697", intents = intents);
        self.synced = False;
    
    async def on_ready(self):
        await self.wait_until_ready();
        if not self.synced:
            self.synced = True;
        await self.change_presence(activity = Activity(type = ActivityType.listening, name = "A"));
        print(f"The bot has been logged in as {bot.user}\n");
        print("Running on {0} {1}\n".format(len(bot.guilds), "server" if len(bot.guilds) == 1 else "servers"));
        
     
bot = bot_class();

@bot.command()
async def say(ctx, *args):
    await ctx.channel.purge(limit = 1);
    await ctx.send("{}".format(" ".join(args)));

bot.run(token)