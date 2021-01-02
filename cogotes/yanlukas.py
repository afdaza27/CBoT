import discord
from discord.ext import commands
import os
import cbot

class YanLukas(commands.Cog):

    def __init__(self, sapo):
        self.sapo = sapo
        self.cogote = "<:cogote:755197902049116201>"
        self.greed = "<:greed:339595362551595009>"
        self.janpueblo = {}
        # ACA SE CARGA EL ÍNDICE DE GENTE REGISTRADA CON JANLUCAS
        # Es un DICCIONARIO porque así se me ocurrió
        # hijueputa
        #print(os.path.exists("./data/sapos"))
        for sapito in os.listdir("./data/sapos"):
            if sapito.endswith(".doge"):
                gianluk = f'{sapito[:-5]}'
                janluc = open('./data/sapos/'+gianluk+'.doge', 'r')
                yanlucc = int(janluc.readlines()[0].strip())
                self.janpueblo[gianluk] = yanlucc
                janluc.close()

    #A ESTA FUNCIÓN SE LE PASA UN CAMBIO DE VALOR POR PARÁMETRO
    #ES DECIR, SI SE LE VAN A AGREGAR 10 YANLUCAS A ALGUIEN, SE LE PASA balor = 10
    #SI SE VAN A RESTAR, SE PASA balor = -10
    #DEFAULT = 50
    def persistir(self, sapillo, balor=50):
        sapillo = sapillo + ".doge"
        if sapillo in os.listdir("./data/sapos"):
            if self.janpueblo[sapillo[:-5]]+balor<0:
                balor = 0
                self.janpueblo[sapillo[:-5]] = balor
            else:
                self.janpueblo[sapillo[:-5]] += balor
                balor = self.janpueblo[sapillo[:-5]]
            janarchibo = open('./data/sapos/'+sapillo, 'r')
            janlineas = janarchibo.readlines()
            janarchibo.close()
            janlineas[0] = str(balor)
            with open('./data/sapos/'+sapillo, 'w') as janarchibo:
                janarchibo.writelines(janlineas)
                janarchibo.close()
        else:
            #Sólo se pueden registrar usuarios con valores POSITIVOS
            if balor>0:
                janarchibo = open('./data/sapos/'+sapillo, 'x')
                self.janpueblo[sapillo[:-5]] = 0 + balor
                janarchibo.write(str(balor))
                janarchibo.close()


    @commands.Cog.listener()
    async def on_ready(self):
        print("Módulo de ¥anLukas cargado.")

    @commands.command()
    async def otorgar(self, cbt, q="0", sapoides=None):
        if await cbot.check_mod(cbt):
            if '@' in q:
                await cbt.send("La estructura del comando es >otorgar cantidad usuario(s), bobo")
            elif int(q)<0:
                await cbt.send("No le puede otorgar una cantidad negativa a alguien bobo hijueputa")
                await cbt.send("Use el comando >impuesto para eso")
            elif int(q)==0:
                await cbt.send("No le puede otorgar 0 a alguien, bobazo")
            elif sapoides is None or not sapoides.startswith('<@'):
                print(sapoides)
                await cbt.send("Tiene que otorgarle las ¥ a alguien, baboso")
            else:
                q = int(q)
                beggars = cbt.message.mentions
                for nigga in beggars:
                    if str(nigga.id) not in self.janpueblo.keys():
                        await cbt.send(nigga.display_name +" no tiene registro de GIANLUKAS; nuevo registro creado con ¥" + str(q))
                    self.persistir(str(nigga.id), q)
                await cbt.send("¥"+str(q*len(beggars))+ " dadas.")
            #user = await self.sapo.fetch_user(cbt.author.id)
            #jajaja mennnnntiras
        else:
            await cbt.send("Nadie le dio permiso de eso, pirobo bobo")

    @commands.command()
    async def impuesto(self, cbt, q = "0", sapoides=None):
        if  await cbot.check_mod(cbt):
            if '@' in q:
                await cbt.send("La estructura del comando es >impuesto cantidad usuario(s), bobo")
            elif int(q) < 0:
                await cbt.send("No le puede cobrar una cantidad negativa a alguien bobo hijueputa")
                await cbt.send("Use el comando >otorgar para eso")
            elif int(q) == 0:
                await cbt.send("No le puede cobrar 0 a alguien, bobazo")
            elif sapoides is None or not sapoides.startswith('<@'):
                await cbt.send("Tiene que cobrarle las ¥ a alguien, baboso")
            else:
                q = int(q)
                beggars = cbt.message.mentions
                for nigga in beggars:
                    if str(nigga.id) not in self.janpueblo.keys():
                        await cbt.send(nigga.display_name + " no tiene registro de GIANLUKAS; no se le va a cobrar el impuesto.")
                    else:
                        self.persistir(str(nigga.id), -q)
                await cbt.send("Impuesto cobrado, dentro de lo posible.")
        else:
            await cbt.send("Nadie le dio permiso de eso, pirobo bobo")

    @commands.command()
    async def saldo(self, cbt, sapillo=None):
        dato = cbt.message.mentions
        if sapillo is None or not dato:
            sapillo = cbt.author
        else:
            sapillo = dato[0]
        if str(sapillo.id) not in self.janpueblo.keys():
            await cbt.send(sapillo.display_name + " no se encuentra en los registros del ¥anBanco Central.")
        else:
            await cbt.send(sapillo.display_name + ": ¥" + str(self.janpueblo[str(sapillo.id)]))

    @commands.command()
    async def registrar(self, cbt):
        if str(cbt.author.id) in self.janpueblo.keys():
            await cbt.send("¿Para que se registra al ¥anBanco si ya está registrado? Malparido bobo")
        else:
            self.persistir(str(cbt.author.id))
            await cbt.send("Registro de JanLukas completo. Su saldo inicial es de ¥50.")

    @commands.command()
    async def pagar(self, cbt, q="0", sapinho = None):

        if '@' in q:
            await cbt.send("La estructura del comando es >pagar cantidad usuario, bobo magnánimo")
        elif int(q) < 0:
            await cbt.send("No le puede pagar una cantidad negativa a alguien bobo hijueputa")
        elif int(q) == 0:
            await cbt.send("No le puede pagar 0 a alguien, bobazo")
        elif sapinho is None or not sapinho.startswith('<@'):
            await cbt.send("Tiene que pagarle las ¥ a alguien, baboso")
        elif str(cbt.message.mentions[0].id) not in self.janpueblo.keys():
            await cbt.send(cbt.message.mentions[0].display_name + " no tiene registro de GIANLUKAS "+ self.cogote)
        elif str(cbt.author.id) not in self.janpueblo.keys():
            await cbt.send("USTED no tiene registro de GIANLUKAS, bobo carepulgar " + self.cogote)
        else:
            q = int(q)
            if q > self.janpueblo[str(cbt.author.id)]:
                q = self.janpueblo[str(cbt.author.id)]
            self.persistir(str(cbt.author.id), -q)
            self.persistir(str(cbt.message.mentions[0].id), q)
            await cbt.send("Transferencia de ¥"+ str(q) +" realizada. "+self.greed)
            await cbt.send("Saldos actuales: \n"+cbt.author.nick + ": ¥" + str(self.janpueblo[str(cbt.author.id)]))
            await cbt.send(cbt.message.mentions[0].nick + ": ¥" + str(self.janpueblo[str(cbt.message.mentions[0].id)]))

    @commands.command()
    async def yanking(self, cbt):
        listoix = list(self.janpueblo.keys())
        def key(item):
            return self.janpueblo[item]
        listoix = sorted(listoix, key=key, reverse=True)
        max = 5
        if len(listoix)<max:
            max = len(listoix)
        if not len(listoix):
            await cbt.send("No hay nadie con registro de GIANLUCAS, bobo puto")
        else:
            corotinho = "Top " + str(max) + " de yanburgueses: \n"
            #print(listoix)
            for niggy in range(0,max):
                c = listoix[niggy]
                #print(c)
                #print(self.janpueblo[c])
                #print(self.sapo.get_user(int(c)))
                sapaso = await self.sapo.fetch_user(int(c))
                sapeiro = sapaso.display_name
                corotinho += str(niggy+1) + ": " + sapeiro + ": ¥" + str(self.janpueblo[c])+"\n"
            await cbt.send(corotinho)

def setup(sapo):
    sapo.add_cog(YanLukas(sapo))

