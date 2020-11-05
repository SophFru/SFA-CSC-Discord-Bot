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

#enable intents
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name= 'ping', help='Tests if bot is responding')
async def pingpong(ctx):
	await ctx.send('pong')

#dm's new members when they join
@bot.event
async def on_member_join(member):
    await member.create_dm()
    
    #Welcome Message
    msg = f'Hi {member.name}, welcome to the Computer Science Club Discord Server!\n'
    msg += 'Be sure to change your nickname to your first name so we know who is who!\n\n'
    msg += 'Follow our social media!\n'
    msg += 'Instagram: sfacompsci \n'
    msg += 'Twitter: sfaCompSci \n'
    msg += 'facebook: sfaCompSci'
    await member.dm_channel.send(msg)
    
# Custom Image Search
resource = build("customsearch", 'v1', developerKey=KEY).cse()
@bot.command(name='image', help='Gets an image from Google')
async def getImage(ctx, query:str):
    result = resource.list(q=query, cx=CSE_ID, searchType='image').execute()
    firstLink = result['items'][0]['link']
    await ctx.send(firstLink)

@bot.command(name='8Ball', help='Prints a Magic 8 Ball message')
async def magic8Ball(ctx):
    someResponses = [
        'As I see it, yes.',
        'Ask again later.',
        'Better not tell you now.',
        'Cannot predict now.',
        'Concentrate and ask again.',
        'Don’t count on it.',
        'It is certain.',
        'It is decidedly so.',
        'Most likely.',
        'My reply is no.',
        'My sources say no.',
        'Outlook not so good.',
        'Outlook good.',
        'Reply hazy, try again.',
        'Signs point to yes.',
        'Very doubtful.',
        'Without a doubt.',
        'Yes.',
        'Yes – definitely.',
        'You may rely on it.'
    ]

    response = random.choice(someResponses)
    await ctx.send(response)

bot.run(TOKEN)
