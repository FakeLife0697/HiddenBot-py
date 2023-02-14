#Hidden Bot alpha ver 0.2.1 (Python)
#7 months into the work now
import discord, logging, os, asyncio
from discord import Activity, ActivityType, Embed, Guild, Intents, Interaction, Member, Role, Spotify, TextChannel, Webhook, app_commands
from discord.ext import commands, tasks
from discord.utils import get
from dotenv import load_dotenv
import define_bot

#Get token from a .env file
load_dotenv();
token = os.getenv("token");

#Setting up logging
logger = logging.getLogger("discord");
logger.setLevel(logging.DEBUG);
handler = logging.FileHandler(filename = "HiddenBot.log", encoding = "utf-8", mode = "w");
handler.setFormatter(logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s'));
logger.addHandler(handler);

#Setting up intents
intents = Intents.all();

bot = define_bot.bot_class(command_prefix = "*");
# @bot.event
# async def on_member_join(member):
#     role = discord.utils.get(member.guild.roles, name = "Member")
#     await bot.add_roles(member, role)

#Load cogs
async def load(bot):
    for file in os.listdir("C:/Coding/Test/HiddenBot-py/cogs"):
        if file.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{file[:-3]}")
            except Exception as e:
                print(f"Failed to load cog {file[:-3]}: {e}")
                raise e

#Log in with the bot token
async def main():
    await load(bot)
    await bot.start(token)

if __name__ == "__main__":
    asyncio.run(main())