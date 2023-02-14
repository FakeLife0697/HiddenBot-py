import discord
from discord import Embed, Guild, Interaction, Member, Message, Spotify
from discord.ext import commands, tasks

class mod(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Mod cog is ready')
    
    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def purge(self, ctx, limit1: int = 0):
        await ctx.channel.purge(limit = limit1 + 1 if limit1 <= 99 and limit1 >= 1 else 100);
        
async def setup(client):
    await client.add_cog(mod(client))