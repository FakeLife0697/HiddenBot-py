import discord, os
from discord import Activity, ActivityType, Intents
from discord.ext import commands

#Setting up intents
intents = Intents.all();

class bot_class(commands.Bot):
    def __init__(self, command_prefix):
        super().__init__(command_prefix, help_command = None, description = "A bot developed by Fake Life#0697", intents = intents);
        self.synced = False;
        
        for file in os.listdir("C:/Coding/Test/HiddenBot-py/cogs"):
            if file.endswith(".py"):
                try:
                    self.load_extension(f"cogs.{file[:-3]}")
                except Exception as e:
                    print(f"Failed to load cog {file[:-3]}: {e}")
                    raise e
                
    @commands.command()
    async def load(self, ctx, extension):
        await self.load_extension(f"cogs.{extension}")
        await ctx.send("Extensions loaded successfully")

    @commands.command()
    async def unload(self, ctx, extension):
        await self.unload_extension(f"cogs.{extension}")
        await ctx.send("Extensions unloaded successfully")
    
    @commands.command()
    async def reload(self, ctx, extension):
        await self.unload_extension(f"cogs.{extension}")
        await self.load_extension(f"cogs.{extension}")
        await ctx.send("Extensions reloaded successfully")
    
    async def on_ready(self):
        await self.wait_until_ready();
        if not self.synced:
            self.synced = True;
            await self.change_presence(activity = Activity(type = ActivityType.listening, name = "小喋日和"));
            await self.tree.sync()
        print(f"The bot has been logged in as {self.user}\n");
        print("Running on {0} {1}\n".format(len(self.guilds), "server" if len(self.guilds) == 1 else "servers"));