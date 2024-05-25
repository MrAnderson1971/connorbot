import os
import sys
import discord
from discord.ext import commands
from dotenv import load_dotenv
import pickle
import asyncio

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# Command prefix
PREFIX = "?"

# Initialize the bot with command prefix
bot = commands.Bot(command_prefix=PREFIX)

# Load or initialize channels data
def load_channels(filename='channels.txt'):
    try:
        with open(filename, 'rb') as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError):
        return {}

def save_channels(channels, filename='channels.txt'):
    with open(filename, 'wb') as f:
        pickle.dump(channels, f)

channels = load_channels()

# Event when the bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user} is connected to the following guilds:')
    for guild in bot.guilds:
        if guild.id not in channels:
            channels[guild.id] = set()
        print(f'{guild.name} (id: {guild.id})')
        member = guild.get_member(825113715464208404)
        if member:
            await member.edit(nick="Connor")

# Command: add channels to the list
@bot.command(name='add')
@commands.has_permissions(manage_channels=True)
async def add_channels(ctx, *channel_mentions):
    guild_channels = channels[ctx.guild.id]
    for channel in ctx.message.channel_mentions:
        guild_channels.add(channel.id)
        await ctx.send(f'Added: <#{channel.id}>')
    save_channels(channels)

# Command: remove channels from the list
@bot.command(name='remove')
@commands.has_permissions(manage_channels=True)
async def remove_channels(ctx, *channel_mentions):
    guild_channels = channels[ctx.guild.id]
    for channel in ctx.message.channel_mentions:
        if channel.id in guild_channels:
            guild_channels.remove(channel.id)
            await ctx.send(f'Removed: <#{channel.id}>')
    save_channels(channels)

# Command: lockdown channels
@bot.command(name='lockdown')
@commands.has_permissions(manage_channels=True)
async def lockdown_channels(ctx):
    guild_channels = channels[ctx.guild.id]
    for channel_id in guild_channels:
        channel = bot.get_channel(channel_id)
        if channel:
            await channel.set_permissions(ctx.guild.default_role, send_messages=False)
            await ctx.send(f'Locked down: <#{channel_id}>')

# Command: lift lockdown on channels
@bot.command(name='lift')
@commands.has_permissions(manage_channels=True)
async def lift_lockdown(ctx):
    guild_channels = channels[ctx.guild.id]
    for channel_id in guild_channels:
        channel = bot.get_channel(channel_id)
        if channel:
            await channel.set_permissions(ctx.guild.default_role, send_messages=None)
            await ctx.send(f'Unlocked: <#{channel_id}>')

# Command: list added channels
@bot.command(name='list')
@commands.has_permissions(manage_channels=True)
async def list_channels(ctx):
    guild_channels = channels[ctx.guild.id]
    await ctx.send(f'Channels added for unlocking in {ctx.guild.name}:')
    for channel_id in guild_channels:
        await ctx.send(f'<#{channel_id}>')

# Command: clear all channels from the list
@bot.command(name='clear')
@commands.has_permissions(manage_channels=True)
async def clear_channels(ctx):
    channels[ctx.guild.id] = set()
    await ctx.send(f'Cleared all channels for {ctx.guild.name}')
    save_channels(channels)

# Command: send a file
@bot.command(name='file')
async def send_file(ctx, filename: str):
    await ctx.message.delete()
    try:
        await ctx.send(file=discord.File(filename))
    except FileNotFoundError:
        await ctx.send(f'File not found: {filename}')

# Command: exit the bot
@bot.command(name='exit')
@commands.is_owner()
async def exit_bot(ctx):
    await ctx.message.add_reaction('\U0001f44b')
    await ctx.bot.close()
    sys.exit()

# Custom reply based on guild name
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if f'<@!{bot.user.id}>' in message.content:
        if message.guild.name == "FREN 101":
            await message.channel.send(f"Bonjour <@!{message.author.id}>. Je m'appelle Connor. Je suis l'androïde envoyé par Cyberlife.\nMa mission est de réussir mes examens. Et j'accomplis toujours ma mission.")
        else:
            await message.channel.send(f'Hello <@!{message.author.id}>. My name is Connor. I\'m the android sent by Cyberlife.\nMy mission is to pass my exams. And I always accomplish my mission.')

    # Process commands
    await bot.process_commands(message)

    # Default case: repeat the message if it doesn't match any command
    if message.content.startswith(PREFIX) and not any(cmd.name in message.content for cmd in bot.commands):
        contents = message.content
        await message.delete()
        await message.channel.send(contents.strip(PREFIX))

# Run the bot
bot.run(TOKEN)
