import discord
from discord.ext import commands
import os
from discord.ext.commands import CommandNotFound
from os import environ
import datetime
import shutil
from modulos.insultos import Insultos

sapo = commands.Bot(command_prefix=">")
BOT_KEY = "NzkzOTAyMzk2OTA3NTg1NTg2.X-zBOQ.gQyJkwrZPjeDxSycbKbPoQ92n94"  # environ["BOT_KEY"]


async def check_mod(cbt):
    return "Bigga Nigga" in [y.name for y in cbt.author.roles] or "Bigger Nigger" in [y.name for y in
                                                                                      cbt.author.roles] or "Biggest Niggest" in [
               y.name for y in cbt.author.roles]


async def actualizar_insultos():
    await sapo.get_cog("Ahorcado").actualizar_insultos()
    await sapo.get_cog("YanLukas").actualizar_insultos()
    await sapo.get_cog("Sabiduria").actualizar_insultos()


@sapo.event
async def on_command_error(cbt, error):
    insultos = Insultos()
    insultos.cargar_insultos()
    if isinstance(error, CommandNotFound):
        await cbt.send("No sé de qué habla, "+insultos.insultar())
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
        shutil.make_archive('CBoT_Datos_' + current_time, 'zip', './data')
        await cbt.send(file=discord.File(r'./CBoT_Datos_' + current_time + '.zip'))
    else:
        await cbt.send("No tiene permiso")


@sapo.command()
async def agregar_insulto(cbt, insulto_nuevo):
    insultos = Insultos()
    lista_insultos = insultos.cargar_insultos()
    if await check_mod(cbt):
        if insulto_nuevo in lista_insultos:
            await cbt.send("Ese insulto ya está, " + insultos.insultar())
        else:
            insultos.agregar_insulto(insulto_nuevo)
            await actualizar_insultos()
            await cbt.send(insulto_nuevo + " fue agregado a los insultos")
    else:
        await cbt.send("Literalmente quién le dio permiso, " + insultos.insultar())


for sapito in os.listdir("./cogotes"):
    if sapito.endswith(".py"):
        sapo.load_extension(f'cogotes.{sapito[:-3]}')

sapo.run(BOT_KEY)
