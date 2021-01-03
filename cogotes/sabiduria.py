import discord
from discord.ext import commands
import random
import cbot
from modulos.insultos import Insultos

class Sabiduria(commands.Cog):

    def __init__(self, sapo):
        self.Insultos = Insultos()
        self.Insultos.cargar_insultos()
        self.sapo = sapo
        self.adagios = self.cargar_adagios()
        self.ego = "La vida de un crítico es sencilla en muchos aspectos, arriesgamos poco y tenemos poder sobre aquellos que ofrecen su trabajo \n  y su servicio a nuestro juicio. Prosperamos con las críticas negativas, divertidas de escribir y de leer, pero la triste verdad que \n debemos afrontar es que en el gran orden de las cosas, cualquier basura tiene más significado que lo que deja ver nuestra crítica. \n Pero en ocasiones el crítico si se arriesga cada vez que descubre y defiende algo nuevo, el mundo suele ser cruel con el \n nuevo talento; las nuevas creaciones, lo nuevo, necesita amigos. Anoche experimente algo nuevo; una extraordinaria cena de una \n fuente singular e inesperada. Decir solo que la comida y su creador han desafiado mis prejuicios sobre la buena cocina, \n subestimaría la realidad; me han tocado en lo más profundo. En el pasado jamás oculte mi desdén por el famoso lema del chef Gusteau: \n Cualquiera puede cocinar. Pero al fin me doy cuenta de lo que quiso decir en realidad; no cualquiera puede \n convertirse en un gran artista, pero un gran artista puede provenir de cualquier lado. Es difícil imaginar un origen más humilde que\n  el del genio que ahora cocina en el restaurante Gusteau´s y quien, en opinión de este critico, es nada menos que el \n mejor chef de Francia. ¡Pronto volveré a Gusteau´s hambriento!"


    async def actualizar_insultos(self):
        self.Insultos.cargar_insultos()

    def cargar_adagios(self):
        ruta_archivo = "./data/adagios.txt"
        archivo_adagios = open(ruta_archivo, "r", encoding="utf-8")
        adagios = []
        for adagio in archivo_adagios:
            adagio = adagio.strip()
            adagios.append(adagio)
        archivo_adagios.close()
        return adagios

    @commands.Cog.listener()
    async def on_ready(self):
        print("Sun Tzu dice: buenas tardes.")

    @commands.command(brief="Reseña del crítico Anton", description="Reseña del crítico Anton")
    async def ego(self, cbt):
        await cbt.send(self.ego)

    @commands.command(brief="Una migaja de sabiduría", description="Una migaja de sabiduría")
    async def adagio(self, cbt):
        numericio = random.randint(0, len(self.adagios)-1)
        await cbt.send(self.adagios[numericio])

    @commands.command(brief="Agrega un nuevo adagio", description="Agrega un nuevo adagio, este debe estar entre comillas.")
    async def agregar_adagio(self, cbt, nuevo_adagio):
        if await cbot.check_mod(cbt):
            if nuevo_adagio not in self.adagios:
                ruta_archivo = "./data/adagios.txt"
                archivo_adagios = open(ruta_archivo, "r", encoding="utf-8")
                lineas = archivo_adagios.readlines()
                archivo_adagios.close()
                lineas.append("\n" + nuevo_adagio)
                self.adagios.append(nuevo_adagio)
                with open('./data/adagios.txt', 'w', encoding="utf-8") as janarchibo:
                    janarchibo.writelines(lineas)
                    janarchibo.close()
                await cbt.send("Adagio agregado con éxito")
            else:
                await cbt.send("El adagio ya está registrado, "+self.Insultos.insultar())
        else:
            await cbt.send("Y a USTED quién le dió permiso?? "+self.Insultos.insultar())


def setup(sapo):
    sapo.add_cog(Sabiduria(sapo))