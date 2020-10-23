# bot.py
import os
import random
import discord

from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

#enable intents
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name= 'ping', help='tests if bot is responding')
async def pingpong(ctx):
	await ctx.send('pong')

#dm's new members when they join
@bot.event
async def on_member_join(member):
    await member.create_dm()
    
	#Welcome Message
	msg = f'Hi {member.name}, welcome to the Computer Science Club Discord Server!/n'
	msg += 'Be sure to change your nickname to your first name so we know who is who!/n/n'
	msg += 'Follow our social media!/n'
	msg += 'Instagram: sfacompsci /n'
	msg += 'Twitter: sfaCompSci /n'
	msg += 'facebook: sfaCompSci'
	
	await member.dm_channel.send(msg)
    
bot.run(TOKEN)
