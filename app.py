import discord

from discord.ext import commands

from discord import app_commands

# Create bot instance

intents = discord.Intents.default()

intents.members = True  # To access user info

intents.presences = True  # To access member presence

bot = commands.Bot(command_prefix="!", intents=intents)

# Sync slash commands

@bot.event

async def on_ready():

    await bot.tree.sync()

    print(f'Logged in as {bot.user}')

# /userinfo command

@bot.tree.command(name="userinfo", description="Display information about a user")

async def userinfo(interaction: discord.Interaction, user: discord.User = None):

    user = user or interaction.user

    embed = discord.Embed(title=f"User Info - {user.name}", color=discord.Color.blue())

    embed.set_thumbnail(url=user.avatar.url)

    embed.add_field(name="Username", value=user.name, inline=True)

    embed.add_field(name="Discriminator", value=user.discriminator, inline=True)

    embed.add_field(name="ID", value=user.id, inline=True)

    embed.add_field(name="Account Created", value=user.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)

    

    member = interaction.guild.get_member(user.id)

    if member:

        embed.add_field(name="Joined Server", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)

    else:

        embed.add_field(name="Joined Server", value="User is not a member of this server.", inline=False)

    

    await interaction.response.send_message(embed=embed)

# /serverinfo command

@bot.tree.command(name="serverinfo", description="Display information about the server")

async def serverinfo(interaction: discord.Interaction):

    guild = interaction.guild

    embed = discord.Embed(title=f"Server Info - {guild.name}", color=discord.Color.green())

    

    if guild.icon:

        embed.set_thumbnail(url=guild.icon.url)

    

    embed.add_field(name="Server Name", value=guild.name, inline=True)

    embed.add_field(name="Server ID", value=guild.id, inline=True)

    embed.add_field(name="Owner", value=guild.owner, inline=False)

    embed.add_field(name="Member Count", value=guild.member_count, inline=True)

    embed.add_field(name="Roles", value=len(guild.roles), inline=True)

    embed.add_field(name="Channels", value=len(guild.channels), inline=True)

    embed.add_field(name="Created At", value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)

    await interaction.response.send_message(embed=embed)

# /firstmessage command

@bot.tree.command(name="firstmessage", description="Get the first message of a specified channel")

async def firstmessage(interaction: discord.Interaction, channel: discord.TextChannel):

    first_message = None

    

    async for message in channel.history(limit=1, oldest_first=True):

        first_message = message

    

    if first_message:

        message_link = f"https://discord.com/channels/{interaction.guild.id}/{channel.id}/{first_message.id}"

        

        embed = discord.Embed(title="First Message", description=first_message.content, color=discord.Color.purple())

        embed.set_author(name=first_message.author.name, icon_url=first_message.author.avatar.url)

        embed.set_footer(text=f"Sent on {first_message.created_at.strftime('%Y-%m-%d %H:%M:%S')}")

        embed.add_field(name="Message Link", value=message_link, inline=False)

        

        await interaction.response.send_message(embed=embed)

    else:

        await interaction.response.send_message("No messages found in this channel.")

# /roleinfo command

@bot.tree.command(name="roleinfo", description="Display information about a specific role")

async def roleinfo(interaction: discord.Interaction, role: discord.Role):

    embed = discord.Embed(title=f"Role Info - {role.name}", color=role.color)

    embed.add_field(name="Role ID", value=role.id, inline=True)

    embed.add_field(name="Color", value=str(role.color), inline=True)

    embed.add_field(name="Position", value=role.position, inline=True)

    embed.add_field(name="Created At", value=role.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)

    embed.add_field(name="Members", value=len(role.members), inline=True)

    

    await interaction.response.send_message(embed=embed)

# /botinfo command

@bot.tree.command(name="botinfo", description="Provide information about the bot")

async def botinfo(interaction: discord.Interaction):

    embed = discord.Embed(title="Bot Info", color=discord.Color.gold())

    embed.add_field(name="Name", value=bot.user.name, inline=True)

    embed.add_field(name="ID", value=bot.user.id, inline=True)

    embed.add_field(name="Created At", value=bot.user.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)

    

    await interaction.response.send_message(embed=embed)

# /channelinfo command

@bot.tree.command(name="channelinfo", description="Display information about a specific channel")

async def channelinfo(interaction: discord.Interaction, channel: discord.TextChannel):

    embed = discord.Embed(title=f"Channel Info - {channel.name}", color=discord.Color.orange())

    embed.add_field(name="Channel ID", value=channel.id, inline=True)

    embed.add_field(name="Channel Type", value=channel.type, inline=True)

    embed.add_field(name="Created At", value=channel.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)

    embed.add_field(name="Position", value=channel.position, inline=True)

    

    await interaction.response.send_message(embed=embed)

# /serverstats command

@bot.tree.command(name="serverstats", description="Show general server statistics")

async def serverstats(interaction: discord.Interaction):

    guild = interaction.guild

    embed = discord.Embed(title=f"Server Statistics - {guild.name}", color=discord.Color.blue())

    embed.add_field(name="Total Members", value=guild.member_count, inline=True)

    embed.add_field(name="Total Roles", value=len(guild.roles), inline=True)

    embed.add_field(name="Total Channels", value=len(guild.channels), inline=True)

    

    await interaction.response.send_message(embed=embed)

# /recentmessages command

@bot.tree.command(name="recentmessages", description="Retrieve the last few messages from a specified channel")

async def recentmessages(interaction: discord.Interaction, channel: discord.TextChannel, limit: int = 5):

    messages = [message async for message in channel.history(limit=limit)]

    

    if messages:

        embed = discord.Embed(title=f"Recent Messages in {channel.name}", color=discord.Color.purple())

        for message in messages:

            embed.add_field(name=f"{message.author.name}:", value=message.content or "No content", inline=False)

        await interaction.response.send_message(embed=embed)

    else:

        await interaction.response.send_message("No messages found in this channel.")

# /userroles command

@bot.tree.command(name="userroles", description="List all roles assigned to a specific user")

async def userroles(interaction: discord.Interaction, user: discord.User):

    member = interaction.guild.get_member(user.id)

    if member:

        roles = [role.name for role in member.roles if role.name != "@everyone"]

        embed = discord.Embed(title=f"Roles for {user.name}", color=discord.Color.blue())

        embed.add_field(name="Roles", value=", ".join(roles) if roles else "No roles assigned", inline=False)

        await interaction.response.send_message(embed=embed)

    else:

        await interaction.response.send_message("User is not a member of this server.")

# /guildemojis command

@bot.tree.command(name="guildemojis", description="Display all custom emojis in the server")

async def guildemojis(interaction: discord.Interaction):

    emojis = interaction.guild.emojis

    if emojis:

        embed = discord.Embed(title="Custom Emojis", color=discord.Color.green())

        emoji_list = " ".join([str(emoji) for emoji in emojis])

        embed.add_field(name="Emojis", value=emoji_list, inline=False)

        await interaction.response.send_message(embed=embed)

    else:

        await interaction.response.send_message("No custom emojis found in this server.")

# /membercount command

@bot.tree.command(name="membercount", description="Show the count of online and offline members")

async def membercount(interaction: discord.Interaction):

    online_members = sum(1 for member in interaction.guild.members if member.status != discord.Status.offline)

    offline_members = interaction.guild.member_count - online_members

    

    embed = discord.Embed(title=f"Member Count for {interaction.guild.name}", color=discord.Color.blue())

    embed.add_field(name="Online Members", value=online_members, inline=True)

    embed.add_field(name="Offline Members", value=offline_members, inline=True)

    

    await interaction.response.send_message(embed=embed)

bot.run("TOKEN")
