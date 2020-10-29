# bot.py
import os
import random
import discord
import re

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

@bot.command(name= 'color_me', help='adds user to role of hex code color')
async def color_me(ctx, color_req: str):
    try: 
        color = discord.Color(value=int(color_req,16))
    except:
        await ctx.send(f'You\'re not allowed to be {color_req}.')
        return
    if color.value == 0:
        await ctx.send('Invalid color.')
        return

    guild = ctx.guild
    member = ctx.message.author

    print(f'Running color_me')
    for role in member.roles:
        print(f'{role.name}')
        if re.match('#[\dabcdef]{6}', role.name):
            print(f'Removing user from color role: {role.name}')
            await member.remove_roles(role)
    existing_color = discord.utils.get(guild.roles, color=color)
    if not existing_color:
        print(f'User created new color role: {color}')
        await guild.create_role(reason='bot color add', name=str(color),color=color)
        existing_color = discord.utils.get(guild.roles, color=color)
    print(f'Adding user to color role: {color}')
    await member.add_roles(existing_color)

@bot.command(name = 'color_cleanup', help='removes empty colors from role list')
async def color_cleanup(ctx):
    guild = ctx.guild
    print(f'Running color role cleanup')
    for role in guild.roles:
        if re.match('#[\dabcdef]{6}', role.name) and len(role.members) == 0:
            print(f'Deleting {role.name}, members: {len(role.members)}')
            await role.delete()
    print(f'Cleanup done')

bot.run(TOKEN)