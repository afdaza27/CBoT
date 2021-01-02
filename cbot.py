import discord
from discord.ext import commands
import os
from discord.ext.commands import CommandNotFound
from os import environ
import datetime
import shutil

sapo = commands.Bot(command_prefix=">")
BOT_KEY = environ["BOT_KEY"]

async def check_mod(cbt):
    return "Bigga Nigga" in [y.name for y in cbt.author.roles] or "Bigger Nigger" in [y.name for y in cbt.author.roles] or "Biggest Niggest" in [y.name for y in cbt.author.roles]

@sapo.event
async def on_command_error(cbt, error):
    if isinstance(error, CommandNotFound):
        await cbt.send("No sé de qué habla, retrasado")
    raise error

@sapo.event
async def on_ready():
    print("Ready to torture some cock and balls")

@sapo.command()
async def load(cbt, cogote):
    if await check_mod(cbt):
        sapo.load_extension(f'cogotes.{cogote}')
    else:
        await cbt.send("No tiene permiso")

@sapo.command()
async def unload(cbt, cogote):
    if await check_mod(cbt):
        sapo.unload_extension(f'cogotes.{cogote}')
    else:
        await cbt.send("No tiene permiso")

@sapo.command()
async def guardar_datos(cbt):
    if await check_mod(cbt):
        now = datetime.datetime.now()
        current_time = now.strftime("%Y-%B-%a%d_%H-%M-%S")
        shutil.make_archive('CBoT_Datos_'+current_time, 'zip', './data')
        await cbt.send(file=discord.File(r'./CBoT_Datos_'+current_time+'.zip'))
    else:
        await cbt.send("No tiene permiso")


for sapito in os.listdir("./cogotes"):
    if sapito.endswith(".py"):
        sapo.load_extension(f'cogotes.{sapito[:-3]}')

sapo.run(BOT_KEY)