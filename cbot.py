import discord
from discord.ext import commands
import os

sapo = commands.Bot(command_prefix=">")

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

sapo.run("NzkzOTAyMzk2OTA3NTg1NTg2.X-zBOQ.bzS_KgeWr4WKhwP57DGKc9Howk8")