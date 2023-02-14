import discord
from discord import Colour, Embed, Guild, Interaction, Member, Message, Spotify
from discord.ext import commands, tasks

class fun(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('Fun cog is ready!')   
    
    @commands.command()
    async def imitate(self, ctx, *args):
        await ctx.channel.purge(limit = 1);
        await ctx.send("{}".format(" ".join(args)));
        
    @commands.command()
    async def ping(self, ctx):
        ping_ms = round(ctx.client.latency * 1000)
        embed = Embed(title = "Pong!", color = Colour.random())
        embed.add_field(name = "Latency: ", value = "{} ms".format(ping_ms))
        await ctx.send(embed = embed)
        
async def setup(client):
    await client.add_cog(fun(client))