# created by seifer for Kiddie Crew SMP discord
# discord : chipsnice#8514

import os
import mysql.connector
import discord
from discord.ext import commands

TOKEN = 'NzcyODE0ODA5NzQ0OTMyODg0.X6AJ4A.tKrWYi54iwYWoxp6QPy81dQix5U'
PREFIX = '.'


bot = commands.Bot(command_prefix=PREFIX, help_command=None)

db = mysql.connector.connect(
    host = 'sql12.freesqldatabase.com',
    username = 'sql12374029',
    password = '73dFLd2GPZ',
    database = 'sql12374029'
)
cursor = db.cursor()

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name='UR MOM'))
    print('IM READY')

@bot.command(name="help", description="Returns all commands", aliases=['commands'])
async def help(ctx):
    embed = discord.Embed(
        title = "🔎 Commands 🔎",
        description = '_Here are all the commands!_',
        colour = discord.Color.orange()
    )

    for command in bot.commands:
        embed.add_field(name=command.name, value=f'‣ {command.description}', inline=False)
        
    await ctx.send(embed=embed)

@bot.command(name="add", description="Adds new marker with given coordinates", aliases=['new', 'create'])
async def add(ctx, name, x: int, y: int, z: int):
    if check_duplicate(name):
        await ctx.send(f'🤔 **WAIT!** _*{name}*_ is already added! Do **{PREFIX}update** to change the coordinates! 🤔')
        return

    query = f'INSERT INTO coords (name, x, y, z) VALUES (%s, %s, %s, %s)'
    val = (name, x, y, z)
    cursor.execute(query, val)

    await ctx.send(f"""
    📡 **Added new location** 📡
    ➡ ***{name}***  [{x}, {y}, {z}]
    """)
    db.commit()

@bot.command(name="delete", description="Deletes marker with given name", aliases=['del', 'remove', 'rem'])
async def delete(ctx, name):
    if not check_duplicate(name):
        await ctx.send(f'🤔 WAIT! _*{name}*_ not found! **{PREFIX}add** to add the marker! 🤔')
        return

    query = 'DELETE FROM coords WHERE name = %s'
    val = (name, )
    cursor.execute(query, val)

    await ctx.send(f"""
    🗑 **Removed {name} !** 🗑
    """)
    db.commit()

@bot.command(name='list', description="Returns all markers", aliases=['all'])
async def list(ctx):
    query = 'SELECT * FROM coords'
    cursor.execute(query)
    coordinates = cursor.fetchall()
    embed = None

    if len(coordinates) > 0:
        embed = discord.Embed(
            title = '📃 All markers 📃',
            colour = discord.Color.blue()
        )
        for coordinate in coordinates:
            embed.add_field(name=coordinate[0], value=f'_X:_ **{coordinate[1]}** _Y:_ **{coordinate[2]}** _Z:_ **{coordinate[3]}**', inline=False)
    else:
        embed = discord.Embed(
            title = '🤔 No markers added! 🤔',
            colour = discord.Color.red()
        )
        
    await ctx.send(embed=embed)

def check_duplicate(markerName):
    query = 'SELECT * FROM coords WHERE name = %s'
    val = (markerName, )
    cursor.execute(query, val)

    result = cursor.fetchall()
    return len(result) > 0

bot.run(TOKEN)