import discord
from discord.ext import commands
import os
import cbot
import datetime
import random
import deck
from modulos.insultos import Insultos
from cogotes.yanlukas import YanLukas

class Casino(commands.Cog):

    def __init__(self, sapo):
        self.sapo = sapo
        self.glyphs = {
            "eggman": ["<:EggMan:755200831623790631>",-4],
            "dedede": ["<:dedede1:339595423109087232>",-2],
            "mongo": ["🍄", 1],
            "formiga": ["🐜", 2],
            "pan": ["🍞", 3],
            "leche": ["🥛", 4],
            "crab": ["🦀", 5],
            "sapo": ["🐸", 7],
            "100": ["💯", 10],
            "flavio": ["<:flavio:339595337356410883>", 12],
            "cogote": ["<:cogote:755197902049116201>", 15],
            "dababy": ["<:DaBaby:819615780282302485>", 17],
            "greed": ["<:greed:339595362551595009>", 20]

        }
        self.defaultR = ["mongo"]*5 + ["formiga"]*5 + ["pan"]*4 + ["leche"]*4 + ["crab"]*3 + ["sapo"]*3 + ["100"]*2 + ["flavio"]*2 + ["cogote"]*2 + ["dababy"] + ["greed"]
        self.db = cbot.get_db()
        self.Insultos = Insultos(self.db, cbot.user)
        self.Insultos.cargar_insultos()


    async def actualizar_insultos(self):
        user = cbot.sign_in()
        self.Insultos.refrescar_usuario(user)
        self.Insultos.cargar_insultos()

    @commands.Cog.listener()
    async def on_ready(self):
        print("Casino abierto.")

    @commands.command(brief="Máquina tragamonedas",
                      description="")
    async def slots(self, cbt, s="5"):
        bid = int(s)
        yanlukas = self.sapo.get_cog("YanLukas")
        yanking = await yanlukas.syncYanking()
        if bid<5:
            await cbt.send("La apuesta mínima es de 5 ¥anLukas, "+ self.Insultos.insultar()+".\nLas perdió por bobo")
            yanlukas.persistir(cbt.author, -bid)
        elif str(cbt.author.id) not in yanking:
            await cbt.send("USTED no tiene registro de GIANLUKAS, bobo carepulgar " + self.cogote)
        elif yanlukas.janpueblo[str(cbt.author.id)] < 5:
            await cbt.send("USTED no tiene suficientes GIANLUKAS, bobo pobre " + self.cogote)
        else:
            if bid >= yanlukas.janpueblo[str(cbt.author.id)]:
                bid = yanlukas.janpueblo[str(cbt.author.id)]
                await cbt.send("Si señores, ALL IN")
            yanlukas.persistir(cbt.author, -bid)
            #Aquí se riggea la máquina lmao
            implying = yanking.index(str(cbt.author.id))
            rigged = int(((len(yanking)-implying)/5) + 1)
            # pranked
            locR = self.defaultR + ["eggman"]*(rigged//2) + ["dedede"]*rigged
            s1 = locR[random.randint(0, len(locR) - 1)]
            s2 = locR[random.randint(0, len(locR) - 1)]
            s3 = locR[random.randint(0, len(locR) - 1)]
            r = "|=============|\n| [{p1}] [{p2}] [{p3}] |\n|=====|¥L|=====|\n\n".format(p1=self.glyphs[s1][0],p2=self.glyphs[s2][0],p3=self.glyphs[s3][0])
            amogus=""
            if s1==s2 and s2==s3:
                yl = bid*self.glyphs[s1][1]
                yanlukas.persistir(cbt.author, yl)
                if(yl<0):
                    r+="Perdió, lmao\n{yan} ¥anlukas fueron incineradas".format(yan = -yl)
                else:
                    if s1=="greed":
                        r+="¡¡¡JACKPOT!!!\n"
                    elif s1=="mongo":
                        lista_mongos = os.listdir("./AMOGUS")
                        amogus = lista_mongos[random.randint(0, len(lista_mongos)-1)]
                    r += "¡Ganó {yan} ¥anlukas!".format(yan = yl)
            await cbt.send(r)
            if amogus != "":
                await cbt.send(file=discord.File("./AMOGUS/"+amogus))


def setup(sapo):
    sapo.add_cog(Casino(sapo))