import discord
from discord.ext import commands
import os
from os import environ

sapo = commands.Bot(command_prefix=">")
BOT_KEY = environ["BOT_KEY"]

@sapo.event
async def on_ready():
    print("Ready to torture some cock and balls")

@sapo.command()
async def load(cbt, cogote):
    sapo.load_extension(f'cogotes.{cogote}')

@sapo.command()
async def unload(cbt, cogote):
    sapo.unload_extension(f'cogotes.{cogote}')



for sapito in os.listdir("./cogotes"):
    if sapito.endswith(".py"):
        sapo.load_extension(f'cogotes.{sapito[:-3]}')

sapo.run(BOT_KEY)