# bot.py
import os
import random
import discord

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name= 'ping', help='tests if bot is responding')
async def pingpong(ctx):
	await ctx.send('pong')

@bot.command(name= 'new_color', help='adds hex code color to role list')
async def new_color(ctx, color_name: str, color_req: discord.Color):
    guild = ctx.guild
    existing_color = discord.utils.get(guild.roles, color=color_req)
    if not existing_color:
        print(f'Creating new Role: {color_req}')
        await guild.create_role(name(color_name),color(color_req),reason='bot color add')

bot.run(TOKEN)