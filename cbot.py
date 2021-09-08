import discord
from discord.ext import commands
import os
from discord.ext.commands import CommandNotFound
from os import environ
import datetime
from modulos.insultos import Insultos
import pyrebase

sapo = commands.Bot(command_prefix=">")
BOT_KEY = environ["BOT_KEY"]
FIREBASE_KEY = environ["FIREBASE_KEY"]
EMAIL = environ["EMAIL"]
PASSWORD = environ["PASSWORD"]

firebaseConfig = {
    "apiKey": FIREBASE_KEY,
    "authDomain": "cbot-23554.firebaseapp.com",
    "databaseURL": "https://cbot-23554-default-rtdb.firebaseio.com",
    "projectId": "cbot-23554",
    "storageBucket": "cbot-23554.appspot.com",
    "messagingSenderId": "721323806712",
    "appId": "1:721323806712:web:137aac9c386f0a3e29100d"
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
auth = firebase.auth()


def sign_in():
    return auth.sign_in_with_email_and_password(EMAIL, PASSWORD)


user = sign_in()


def get_db():
    return db


async def check_mod(cbt):
    return "Bigga Nigga" in [y.name for y in cbt.author.roles] or "Bigger Nigger" in [y.name for y in
                                                                                      cbt.author.roles] or "Biggest Niggest" in [
               y.name for y in cbt.author.roles]


async def actualizar_insultos():
    await sapo.get_cog("Ahorcado").actualizar_insultos()
    await sapo.get_cog("YanLukas").actualizar_insultos()
    await sapo.get_cog("Sabiduria").actualizar_insultos()
    await sapo.get_cog("Casino").actualizar_insultos()
    await sapo.get_cog("Bich").actualizar_insultos()


@sapo.event
async def on_command_error(cbt, error):
    error_user = sign_in()
    insultos = Insultos(get_db(), error_user)
    insultos.cargar_insultos()
    if isinstance(error, CommandNotFound):
        await cbt.send("No sé de qué habla, " + insultos.insultar())
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
async def agregar_insulto(cbt, insulto_nuevo):
    user_bruh = sign_in()
    insultos = Insultos(get_db(), user_bruh)
    lista_insultos = insultos.cargar_insultos()
    if await check_mod(cbt):
        if insulto_nuevo in lista_insultos:
            await cbt.send("Ese insulto ya está, " + insultos.insultar())
        else:
            insultos.agregar_insulto(insulto_nuevo, user_bruh)
            await actualizar_insultos()
            await cbt.send(insulto_nuevo + " fue agregado a los insultos")
    else:
        await cbt.send("Literalmente quién le dio permiso, " + insultos.insultar())


for sapito in os.listdir("./cogotes"):
    if sapito.endswith(".py"):
        sapo.load_extension(f'cogotes.{sapito[:-3]}')

sapo.run(BOT_KEY)
