import os
import sys

import discord
from dotenv import load_dotenv
import pickle
import asyncio

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

PREFIX = "?"

client = discord.Client()
permissions = discord.Permissions()

try:
    with open('channels.txt', 'rb') as f:
        channels = pickle.load(f)
except:
    channels = {}

@client.event
async def on_ready():
    print(
        f'{client.user} is connected to the following guild:\n')
    for guild in client.guilds:
        if guild.id not in channels.keys():
            channels[guild.id] = set()
        

   
        print(f'{guild.name}(id: {guild.id})\n')
        await guild.get_member(825113715464208404).edit(nick="Connor")

@client.event
async def on_message(message):
    cmd = message.content.split()
    guild_channels = channels[message.guild.id]
    guild = message.guild

    if f'<@!{client.user.id}>' in message.content:
        if guild.name == "FREN 101":
            await message.channel.send(f"Bonjour <@!{message.author.id}>. Je m'appelle Connor. Je suis l'androïde envoyé par Cyberlife.\nMa mission est de réussir mes examens. Et j'accomplis toujours ma mission.")
        else:
            await message.channel.send(f'Hello <@!{message.author.id}>. My name is Connor. I\'m the android sent by Cyberlife.\nMy mission is to pass my exams. And I always accomplish my mission.')
            #await message.channel.send(f"你好 <@!{message.author.id}>。我叫 Connor。我是Cyberlife送来的机器人。\n我的任务是通过考试。而且，我的任务每次成功。")
            #await message.channel.send(f"Salve <@!{message.author.id}>. Meum nomen est Connor. Android sum missus a Cyberlife.\nMy missionem is to pass my probationes. Et semper missionem meam perficio.")

    if message.author == client.user:
        return


    if cmd[0][0] != PREFIX: return

    cc = cmd[0].strip(PREFIX)

    if not message.channel.permissions_for(message.author).manage_channels:
        print('%s attempted to run:\n%s' % (message.author, message.content))

        await message.channel.send("Manage channel permissions required to execute this command!")
        return

    print('%s:\n%s' % (message.author, message.content))


    if cc == "add":
        await message.channel.send('Added the following:')
        for channel in message.raw_channel_mentions:
            guild_channels.add(channel)
            await message.channel.send(f'<#{channel}>')
    

    elif cc == "remove":
        await message.channel.send('Removed the following:')
        for channel in message.raw_channel_mentions:
            if channel in guild_channels:
                guild_channels.remove(channel)
                await message.channel.send(f'<#{channel}>')

    elif cc == "lockdown":
        await message.channel.send('Locking:')
        for channel in guild_channels:
            await client.get_channel(channel).set_permissions(message.guild.default_role, send_messages=False)
            await message.channel.send(f'Locked down <#{channel}>')

    elif cc == "lift":
        await message.channel.send('Unlocking:')
        for channel in guild_channels:
            await client.get_channel(channel).set_permissions(message.guild.default_role, send_messages=None)
            await message.channel.send(f'Unlocked <#{channel}>')

    elif cc == "list":
        await message.channel.send('Channels added to unlocking for %s:' % message.guild)
        for channel in guild_channels:
            await message.channel.send('<#%s>' % channel)

    elif cc == "all":
        await message.channel.send('All servers:')
        for guild in channels.keys():
            await message.channel.send("%s:" % guild)
            for channel in channels[guild]:
                await message.channel.send(f'<#{channel}>')

    elif cc == "clear":
        await message.channel.send('Clearing lockdowns for %s...' % message.guild.name)
        channels[message.guild.id] = set()

    elif cc == 'exit':
        await message.add_reaction('\U0001f44b')
        sys.exit()

    elif cc == 'file':
        await message.delete()
        try:
            await message.channel.send(file=discord.File(' '.join(cmd[1:])))
        except FileNotFoundError as e:
            print(e)

    elif cc == 'temp':
        '''messages = await message.channel.history(limit=1000).flatten()
        for m in messages:
            print('Deleted %s' % m.content)
            await m.delete()'''
        '''for i in range(101, 114):
            await guild.create_role(name="Section %s" % i)'''
        for role in guild.roles:
            if role.name.startswith("Lab"):
                print(role.name)
                await role.delete()

    else:
        contents = message.content
        await message.delete()
        await message.channel.send(contents.strip(PREFIX))

    save('channels.txt')
            
def save(file):
    with open(file, 'wb') as f:
        pickle.dump(channels, f)
    
client.run(TOKEN)
