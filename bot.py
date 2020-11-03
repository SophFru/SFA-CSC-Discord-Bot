# bot.py
import os
import random
import discord

from discord.ext import commands
from dotenv import load_dotenv
from apiclient.discovery import build

load_dotenv()

# Keys and IDs
KEY = os.getenv('API_KEY')
CSE_ID = os.getenv('CUSTOM_SEARCH_ID')
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name= 'ping', help='tests if bot is responding')
async def pingpong(ctx):
	await ctx.send('pong')

# Custom Image Search
resource = build("customsearch", 'v1', developerKey=KEY).cse()
@bot.command(name='image', help='Gets an image from Google')
async def getImage(ctx, query:str):
    result = resource.list(q=query, cx=CSE_ID, searchType='image').execute()
    firstLink = result['items'][0]['link']
    await ctx.send(firstLink)


bot.run(TOKEN)
