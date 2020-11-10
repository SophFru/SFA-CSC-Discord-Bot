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

@bot.command(name= 'ping', help='Tests if bot is responding')
async def pingpong(ctx):
    await ctx.send('pong')

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

#Poll Commands

class poll:
    isReady = False
    isActive = False
    question = ''
    emojiOptions = []
    tally = []

@bot.event
async def on_reaction_add(reaction, user):
    if poll.isActive and not user.bot:
        for emoji in poll.emojiOptions:
            if reaction.emoji == emoji:
                index = poll.emojiOptions.index(emoji)
                poll.tally[index] += 1

@bot.command(name='pollCustom', help='creates a poll with custom reactions')
async def setPoll(ctx, question, *choices):
    if not poll.isReady:
        await ctx.send('New poll has been created. Type !pollStart to launch poll.')
        poll.isReady = True
        poll.question = question
        poll.emojiOptions = choices
    else:
        await ctx.send('Error: there is already a poll ready to launch')
        
@bot.command(name='pollYesNo', help='creates a yes/no poll')
async def setPoll(ctx, question):
    if not poll.isReady:
        await ctx.send('New poll has been created. Type !pollStart to launch poll.')
        poll.isReady = True
        poll.question = question
        poll.emojiOptions = ['\U0001F44D', '\U0001F44E', '\U0001F937']
    else:
        await ctx.send('Error: there is already a poll ready to launch')

@bot.command(name='pollStart', help='launches poll created by \'poll\'')
async def startPoll(ctx):
    if poll.isReady:
        poll.isActive = True
        message = await ctx.send(poll.question)
        for emoji in poll.emojiOptions:
            await message.add_reaction(emoji)
            poll.tally.append(0)
    else:
        await ctx.send('Error: no poll to launch')

@bot.command(name='pollEnd', help='Ends poll and declares a winner')
async def endPoll(ctx):
    if poll.isActive:
        poll.isActive = False
        poll.isReady = False
        isTie = False
        highestNum = 1
        for num in poll.tally:
            if num > highestNum:
                highestNum = num
        amount = 0
        for num in poll.tally:
            if highestNum == num:
                amount += 1
        print(highestNum)
        if amount > 1:
            isTie = True
        index = poll.tally.index(highestNum)
        if isTie:
            await ctx.send("poll has ended, it's a tie")
        else:
            await ctx.send("poll has ended, the winner is " + poll.emojiOptions[index])
        poll.tally.clear()
    else:
        await ctx.send("Error: there are no active polls")

bot.run(TOKEN)
