#Hidden Bot alpha ver 0.1.2 (Python)
#6 months into the work now
import discord, logging, typing, os, asyncio, webbrowser, requests, time, random, json, aiohttp, datetime
from discord import Activity, ActivityType, Embed, Guild, Intents, Interaction, Member, Role, Spotify, TextChannel, Webhook, app_commands
from discord.ext import commands, tasks
from discord.utils import get
from dotenv import load_dotenv

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
        await self.change_presence(activity = Activity(type = ActivityType.listening, name = "小喋日和"));
        await self.tree.sync()
        print(f"The bot has been logged in as {bot.user}\n");
        print("Running on {0} {1}\n".format(len(bot.guilds), "server" if len(bot.guilds) == 1 else "servers"));
        
     
bot = bot_class();

# @bot.event
# async def on_member_join(member):
#     role = discord.utils.get(member.guild.roles, name = "Member")
#     await bot.add_roles(member, role)

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Slash commands
#Get user's information
@bot.tree.command(name = "userinfo", description = "Reply with user info!")
async def slash_userinfo(interaction: Interaction, member: Member = None):
    member = member if member != None else interaction.guild.get_member(interaction.user.id);
    role_list = [];
    for role in member.roles:
        if role.name != "@everyone":
            role_list.append(role.mention);
    roles = ', '.join(role_list);
    embed = Embed(colour = member.top_role.color, timestamp = interaction.created_at);
    embed.set_author(name = f"Username: {member}");
    embed.set_thumbnail(url = member.avatar);
    embed.set_footer(text = f"Requested by {interaction.user}", icon_url = interaction.user.avatar);
    embed.add_field(name = "ID: ", value = member.id, inline = False);
    embed.add_field(name = "Name: ", value = member.display_name, inline = False);
    embed.add_field(name = "Account created at: ", value = member.created_at, inline = False);
    embed.add_field(name = "Joined server at: ", value = member.joined_at, inline = False);
    embed.add_field(name = f"Roles ({len(role_list)}): ", value = ''.join([roles]), inline = False);
    embed.add_field(name = "Top role: ", value = member.top_role.mention, inline = False);
    embed.add_field(name = "Bot: ", value = member.bot, inline = False);
    await interaction.response.send_message(embed = embed)
    
#Get server's information
@bot.tree.command(name = "serverinfo", description = "Reply with server info!")
async def slash_serverinfo(interaction: Interaction):
    embed = Embed(colour = interaction.guild.owner.top_role.color, timestamp = interaction.created_at);
    embed.set_author(name = f"Server: {interaction.guild.name}");
    embed.set_thumbnail(url = interaction.guild.icon);
    embed.set_footer(text = f"Requested by {interaction.user}", icon_url = interaction.user.avatar);
    embed.add_field(name = "Server ID: ", value = interaction.guild_id, inline = False);
    embed.add_field(name = "Owner: ", value = interaction.guild.owner, inline = False);
    embed.add_field(name = "Server created at: ", value = interaction.guild.created_at, inline = False);
    embed.add_field(name = "Text channels: ", value = len(interaction.guild.text_channels), inline = False);
    embed.add_field(name = "Voice channels: ", value = len(interaction.guild.voice_channels), inline = False);
    embed.add_field(name = "Threads: ", value = len(interaction.guild.threads), inline = False);
    embed.add_field(name = "Members till now: ", value = interaction.guild.member_count, inline = False);
    embed.add_field(name = "Verification Level: ", value = interaction.guild.verification_level, inline = False);
    await interaction.response.send_message(embed = embed)    

#Display user's current Spotify info
@bot.tree.command(name = "stfinfo", description = "Reply with user's current spotify info!")
async def slash_stfinfo(interaction: Interaction, member: Member = None):
    listen = False;
    member = member if member != None else interaction.guild.get_member(interaction.user.id);
    embed = Embed(colour = member.top_role.color, timestamp = interaction.created_at);
    embed.set_author(name = f"{member}'s spotify info:");
    embed.set_thumbnail(url = member.avatar);
    embed.set_footer(text = f"Requested by {interaction.user}", icon_url = interaction.user.avatar);
    for activity in member.activities:
        if isinstance(activity, Spotify):
            embed.add_field(name = "Song: ", value = activity.title, inline = False);
            embed.add_field(name = "Artist: ", value = ", ".join(activity.artists), inline = False);
            embed.add_field(name = "Duration: ", value = activity.duration, inline = False);
            embed.add_field(name = "Started at: ", value = activity.start, inline = False);
            listen = True;
    if not listen:
        embed.add_field(name = "No playing songs", value = "No songs are being listened.", inline = False);
    await interaction.response.send_message(embed = embed)

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Bot commands

#Purge messages
@bot.command()
@commands.has_permissions(manage_messages = True)
async def purge(ctx, limit1: int = 0):
    await ctx.channel.purge(limit = limit1 + 1 if limit1 <= 99 and limit1 >= 1 else 100);

#Duplicate user's messages, then delete user's command
@bot.command()
async def imitate(ctx, *args):
    await ctx.channel.purge(limit = 1);
    await ctx.send("{}".format(" ".join(args)));

#Display user's current Spotify info
@bot.command()
async def stfinfo(ctx, member: Member = None):
    listen = False;
    member = member if member != None else ctx.author;
    embed = Embed(colour = member.top_role.color, timestamp = ctx.message.created_at);
    embed.set_author(name = f"{member}'s spotify info:");
    embed.set_thumbnail(url = member.avatar);
    embed.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.avatar);
    for activity in member.activities:
        if isinstance(activity, Spotify):
            embed.add_field(name = "Song: ", value = activity.title, inline = False);
            embed.add_field(name = "Artist: ", value = ", ".join(activity.artists), inline = False);
            embed.add_field(name = "Duration: ", value = activity.duration, inline = False);
            embed.add_field(name = "Started at: ", value = activity.start, inline = False);
            listen = True;
    if not listen:
        embed.add_field(name = "No playing songs", value = "No songs are being listened.", inline = False);
    await ctx.send(embed = embed)

#Get user's information
@bot.command()
async def userinfo(ctx, member: Member = None):
    member = member if member != None else ctx.author;
    role_list = [];
    for role in member.roles:
        if role.name != "@everyone":
            role_list.append(role.mention);
    roles = ', '.join(role_list);
    embed = Embed(colour = member.top_role.color, timestamp = ctx.message.created_at);
    embed.set_author(name = f"Username: {member}");
    embed.set_thumbnail(url = member.avatar);
    embed.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.avatar);
    embed.add_field(name = "ID: ", value = member.id, inline = False);
    embed.add_field(name = "Name: ", value = member.display_name, inline = False);
    embed.add_field(name = "Account created at: ", value = member.created_at, inline = False);
    embed.add_field(name = "Joined server at: ", value = member.joined_at, inline = False);
    embed.add_field(name = f"Roles ({len(role_list)}): ", value = ''.join([roles]), inline = False);
    embed.add_field(name = "Top role: ", value = member.top_role.mention, inline = False);
    embed.add_field(name = "Bot: ", value = member.bot, inline = False);
    await ctx.send(embed = embed)

@bot.command()
async def whois(ctx, member: Member = None):
    member = member if member != None else ctx.author;
    role_list = [];
    for role in member.roles:
        if role.name != "@everyone":
            role_list.append(role.mention)
    roles = ', '.join(role_list);
    
    embed = Embed(colour = member.top_role.color, timestamp = ctx.message.created_at);
    embed.set_author(name = f"Username: {member}");
    embed.set_thumbnail(url = member.avatar);
    embed.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.avatar);
    embed.add_field(name = "ID: ", value = member.id, inline = False);
    embed.add_field(name = "Name: ", value = member.display_name, inline = False);
    embed.add_field(name = "Account created at: ", value = member.created_at, inline = False);
    embed.add_field(name = "Joined server at: ", value = member.joined_at, inline = False);
    embed.add_field(name = f"Roles ({len(role_list)}): ", value = ''.join([roles]), inline = False);
    embed.add_field(name = "Top role: ", value = member.top_role.mention, inline = False);
    embed.add_field(name = "Bot: ", value = member.bot, inline = False);
    await ctx.send(embed = embed)
    
#Get server's information    
@bot.command()
async def serverinfo(ctx):
    embed = Embed(colour = ctx.guild.owner.top_role.color, timestamp = ctx.message.created_at);
    embed.set_author(name = f"Server: {ctx.guild.name}");
    embed.set_thumbnail(url = ctx.guild.icon);
    embed.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.avatar);
    embed.add_field(name = "Server ID: ", value = ctx.guild.id, inline = False);
    embed.add_field(name = "Owner: ", value = ctx.guild.owner, inline = False);
    embed.add_field(name = "Server created at: ", value = ctx.guild.created_at, inline = False);
    embed.add_field(name = "Text channels: ", value = len(ctx.guild.text_channels), inline = False);
    embed.add_field(name = "Voice channels: ", value = len(ctx.guild.voice_channels), inline = False);
    embed.add_field(name = "Threads: ", value = len(ctx.guild.threads), inline = False);
    embed.add_field(name = "Members till now: ", value = ctx.guild.member_count, inline = False);
    embed.add_field(name = "Verification Level: ", value = ctx.guild.verification_level, inline = False);
    await ctx.send(embed = embed)

#Add roles
@bot.command()
@commands.has_permissions(manage_roles = True)
async def addrole(ctx, member: Member = None, role: Role = None):
    embed = Embed(colour = ctx.guild.owner.top_role.color, timestamp = ctx.message.created_at);
    embed.set_footer(text = f"Modified by {ctx.author}", icon_url = ctx.author.avatar);
    if member == None:
        embed.add_field(name = "Invalid user.", value = "Please type a valid user", inline = False);
    elif role == None:
        embed.add_field(name = "Invalid role.", value = "Please type a valid role", inline = False);
    else:
        #Check if the role mentioned is exist or not
        temp_list = []
        for tempRole in ctx.guild.roles:
            if tempRole != "@everyone":
                temp_list.append(tempRole)
        for check in temp_list:
            if role == check:
                exist = True;
                break;
            else:
                exist = False;
        
        #Check if the member has already had the role or not
        
        if exist:
            embed = Embed(colour = role.color, timestamp = ctx.message.created_at);
            embed.set_author(name = f"{member}:");
            embed.set_thumbnail(url = member.avatar);
            temp = get(ctx.guild.roles, name = role.name)  
            embed.add_field(name = "Role added", value = f"Added role {role} to {member}", inline = False);
            await member.add_roles(temp)
        else:
            embed.add_field(name = "Invalid role", value = "Please type a valid role", inline = False);
    await ctx.send(embed = embed)
        
#Remove roles
@bot.command()
@commands.has_permissions(manage_roles = True)
async def removerole(ctx, member: Member = None, role: Role = None):
    embed = Embed(colour = ctx.guild.owner.top_role.color, timestamp = ctx.message.created_at);
    embed.set_footer(text = f"Modified by {ctx.author}", icon_url = ctx.author.avatar);
    if member == None:
        embed.add_field(name = "Invalid user", value = "Please type a valid user", inline = False);
    elif role == None:
        embed.add_field(name = "Invalid role", value = "Please type a valid role", inline = False);
    else:
        #Check if the role mentioned is exist or not
        temp_list = []
        for tempRole in ctx.guild.roles:
            if tempRole != "@everyone":
                temp_list.append(tempRole)
        for check in temp_list:
            if role == check:
                exist = True;
                break;
            else:
                exist = False;
             
        #Check if the member has already had the role or not   
        
        if exist:
            embed.set_author(name = f"{member}:");
            embed.set_thumbnail(url = member.avatar);
            temp = get(ctx.guild.roles, name = role.name)  
            embed.add_field(name = "Role removed", value = f"Removed role {role} from {member}", inline = False);
            await member.remove_roles(temp)
        else:
             embed.add_field(name = "Invalid role", value = "Please type a valid role", inline = False);
    await ctx.send(embed = embed)
    
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Too lazy to continue developing
    
# #Timeout user
# @bot.command()
# @commands.has_permissions(timeout_members = True)
# async def timeout(ctx, member: Member, reason: str, time: int = 0):
#     await ctx.channel.purge(limit = 1);
#     embed = Embed(colour = member.color, timestamp = ctx.message.created_at);
#     embed.set_footer(text = f"By {ctx.author}", icon_url = ctx.author.avatar);
#     if member == None:
#         embed.add_field(name = "Invalid user", inline = False);
#     elif time == 0:
#         embed.add_field(name = "Please provide valid time", inline = False);
#     else:
#         embed.set_author(name = f"Timeout user {member.display_name}");
#         embed.set_thumbnail(url = member.avatar);
#         embed.add_field(name = "Reason: ", value = reason if reason != "" else "No reasons given", inline = False);
#     await ctx.send(embed = embed);

# #Kick user
# @bot.command()
# @commands.has_permissions(kick_members = True)
# async def kick(ctx, member: Member, reason: str):
#     await ctx.channel.purge(limit = 1);
#     embed = Embed(colour = member.color, timestamp = ctx.message.created_at);
#     embed.set_footer(text = f"By {ctx.author}", icon_url = ctx.author.avatar);
#     if member == None:
#         embed.add_field(name = "Invalid user", inline = False);
#     else:
#         embed.set_author(name = f"Kicked user {member.display_name}");
#         embed.set_thumbnail(url = member.avatar);
#         embed.add_field(name = "Reason: ", value = reason if reason != "" else "No reasons given", inline = False);
#     await ctx.send(embed = embed);

# #Ban user
# @bot.command()
# @commands.has_permissions(ban_members = True)
# async def ban(ctx, member: Member, reason: str):
#     await ctx.channel.purge(limit = 1);
#     embed = Embed(colour = member.color, timestamp = ctx.message.created_at);
#     embed.set_footer(text = f"By {ctx.author}", icon_url = ctx.author.avatar);
#     if member == None:
#         embed.add_field(name = "Invalid user", inline = False);
#     else:
#         embed.set_author(name = f"Banned user {member.display_name}");
#         embed.set_thumbnail(url = member.avatar);
#         embed.add_field(name = "Reason: ", value = reason if reason != "" else "No reasons given", inline = False);
#         await ctx();
#     await ctx.send(embed = embed);
    
#Fetch webhooks
# @bot.command()
# @commands.has_permissions(manage_webhooks = True)
# async def webhook(ctx):
#     
#     await ctx.send()
    
#
# @bot.command()
# @commands.has_permissions(manage_server = True)
# async def (ctx):
#     await ctx.send("")
    
# #Help information
# @bot.command()
# async def help(ctx):
#     embed = discord.Embed(colour = ctx.author.color)
#     embed.set_author(name = "Help Information")
#     embed.add_field(name = "", value = None, inline = False)
#     await ctx.send(embed = embed)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Log in with the bot token
bot.run(token)