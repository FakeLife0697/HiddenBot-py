import discord, asyncio, os
from discord import Activity, ActivityType, Colour, Embed, Guild, Intents, Interaction, Member, Role, Spotify, TextChannel, Webhook, app_commands
from discord.ext import commands, tasks
from discord.utils import get

class slash_commands(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('Slash_commands cog is ready')
    
    @app_commands.command(name = "ping", description = "Pong!")
    async def slash_ping(self, interaction: Interaction):
        ping_ms = round(self.client.latency * 1000)
        embed = Embed(title = "Pong!", color = Colour.random())
        embed.add_field(name = "Latency: ", value = "{} ms".format(ping_ms))
        await interaction.response.send_message(embed = embed)
    
    @app_commands.command(name = "userinfo", description = "Reply with user info!")    
    async def slash_userinfo(self, interaction: Interaction, member: Member = None):
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
       
    @app_commands.command(name = "serverinfo", description = "Reply with server info!")    
    async def slash_serverinfo(self, interaction: Interaction):
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
    
    @app_commands.command(name = "stfinfo", description = "Reply with user's current spotify info!")    
    async def slash_stfinfo(self, interaction: Interaction, member: Member = None):
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
        
async def setup(client):
    await client.add_cog(slash_commands(client))