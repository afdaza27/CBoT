import discord
from discord.ext import commands
import os
import cbot
import datetime
import random
from modulos.insultos import Insultos


class YanLukas(commands.Cog):

    def __init__(self, sapo):
        self.sapo = sapo
        self.cogote = "<:cogote:755197902049116201>"
        self.greed = "<:greed:339595362551595009>"
        self.janpueblo = {}
        self.Insultos = Insultos()
        self.Insultos.cargar_insultos()
        # Big play funciona como el estado de la apuesta
        # 0 - No hay apuesta
        # 1 - Se aceptan apuestas
        # 2 - Apuesta en juego
        self.bigplay = 0
        # Las apuestas c guardan en una diccionario en un diccionario, bajo la llave "o", y bajo la segunda llave del id de la opción
        # tambien tiene la llaves "u", "t", "prompt" y "pirobo"
        # cada opción de apuesta tiene otro triplehijueputa diccionario, con:
        # prompt de la opción, cantidad de xhanglukas en total, tasa de retorno
        self.bets = {"u": [],  # Lista de tuplas de usuarios que apostaron (id, opcion, cantidad)
                     "o": {},
                     "t": 0,  # total de yanlvkinhas en la bolsa
                     "prompt": "",  # prompt de la apuesta
                     "pirobo": None  # el hijueputa que invocó la apuesta
                     }
        # ACA SE CARGA EL ÍNDICE DE GENTE REGISTRADA CON JANLUCAS
        # Es un DICCIONARIO porque así se me ocurrió
        # hijueputa
        # print(os.path.exists("./data/sapos"))
        for sapito in os.listdir("./data/sapos"):
            if sapito.endswith(".doge"):
                gianluk = f'{sapito[:-5]}'
                janluc = open('./data/sapos/' + gianluk + '.doge', 'r')
                yanlucc = int(janluc.readlines()[0].strip())
                self.janpueblo[gianluk] = yanlucc
                janluc.close()

    async def actualizar_insultos(self):
        self.Insultos.cargar_insultos()

    # A ESTA FUNCIÓN SE LE PASA UN CAMBIO DE VALOR POR PARÁMETRO
    # ES DECIR, SI SE LE VAN A AGREGAR 10 YANLUCAS A ALGUIEN, SE LE PASA balor = 10
    # SI SE VAN A RESTAR, SE PASA balor = -10
    # DEFAULT = 50
    def persistir(self, sapillo, balor=50):
        sapillo = sapillo + ".doge"
        if sapillo in os.listdir("./data/sapos"):
            if self.janpueblo[sapillo[:-5]] + balor < 0:
                balor = 0
                self.janpueblo[sapillo[:-5]] = balor
            else:
                self.janpueblo[sapillo[:-5]] += balor
                balor = self.janpueblo[sapillo[:-5]]
            janarchibo = open('./data/sapos/' + sapillo, 'r')
            janlineas = janarchibo.readlines()
            janarchibo.close()
            janlineas[0] = str(balor) + "\n"
            with open('./data/sapos/' + sapillo, 'w') as janarchibo:
                janarchibo.writelines(janlineas)
                janarchibo.close()
        else:
            # Sólo se pueden registrar usuarios con valores POSITIVOS
            if balor > 0:
                janarchibo = open('./data/sapos/' + sapillo, 'x')
                self.janpueblo[sapillo[:-5]] = 0 + balor
                janarchibo.write(str(balor) + "\n")
                janarchibo.close()

    @commands.Cog.listener()
    async def on_ready(self):
        print("Módulo de ¥anLukas cargado.")

    @commands.command(brief="Otorga ¥anLukas a un usuario",
                      description="Otorga una cierta cantidad de ¥anLukas a uno o más usuarios. La estructura del comando es >otorgar cantidad @usuario(s). Si el usuario no está registrado en el YanBanco se registra con la cantidad otorgada")
    async def otorgar(self, cbt, q="0", sapoides=None):
        if await cbot.check_mod(cbt):
            if '@' in q:
                await cbt.send("La estructura del comando es >otorgar cantidad usuario(s), bobo")
            elif "." in q or "," in q:
                await cbt.send("No hay ¥anCentavos, gran imbécil")
            elif int(q) < 0:
                await cbt.send("No le puede otorgar una cantidad negativa a alguien bobo hijueputa")
                await cbt.send("Use el comando >impuesto para eso")
            elif int(q) == 0:
                await cbt.send("No le puede otorgar 0 a alguien, bobazo")
            elif sapoides is None or not sapoides.startswith('<@'):
                print(sapoides)
                await cbt.send("Tiene que otorgarle las ¥ a alguien, baboso")
            else:
                q = int(q)
                beggars = cbt.message.mentions
                for nigga in beggars:
                    if str(nigga.id) not in self.janpueblo.keys():
                        await cbt.send(
                            nigga.display_name + " no tiene registro de GIANLUKAS; nuevo registro creado con ¥" + str(
                                q))
                    self.persistir(str(nigga.id), q)
                await cbt.send("¥" + str(q * len(beggars)) + " dadas.")
            # user = await self.sapo.fetch_user(cbt.author.id)
            # jajaja mennnnntiras
        else:
            await cbt.send("Nadie le dio permiso de eso, pirobo bobo")

    @commands.command(brief="Cobra un impuesto en Xhanlucas",
                      description="Cobra un impuesto en Janlucas a uno o más usuarios. La estructura del comando es >impuesto cantidad @usuario(s)")
    async def impuesto(self, cbt, q="0", sapoides=None):
        if await cbot.check_mod(cbt):
            if '@' in q:
                await cbt.send("La estructura del comando es >impuesto cantidad usuario(s), bobo")
            elif "." in q or "," in q:
                await cbt.send("No hay ¥anCentavos, gran imbécil")
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
                        await cbt.send(
                            nigga.display_name + " no tiene registro de GIANLUKAS; no se le va a cobrar el impuesto.")
                    else:
                        self.persistir(str(nigga.id), -q)
                await cbt.send("Impuesto cobrado, dentro de lo posible.")
        else:
            await cbt.send("Nadie le dio permiso de eso, pirobo bobo")

    @commands.command(brief="Consultar el saldo de gianluks",
                      description="Consultar el saldo de gianluks de un usuario. Si no se ingresa un usuario específico se consulta el saldo de quien escribió el comando")
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

    @commands.command(brief="Registrarse en el ¥anBanco",
                      description="Registra al invocador del comando en el ¥anBanco y se le otorga una cantidad de LlanLucas predeterminada")
    async def registrar(self, cbt):
        if str(cbt.author.id) in self.janpueblo.keys():
            await cbt.send("¿Para que se registra al ¥anBanco si ya está registrado? Malparido bobo")
        else:
            self.persistir(str(cbt.author.id))
            await cbt.send("Registro de JanLukas completo. Su saldo inicial es de ¥50.")

    @commands.command(brief="Realiza un pago a un usuario",
                      description="Realiza una transferencia entre dos usuarios. La estructura del comando es >pagar cantidad @usuario")
    async def pagar(self, cbt, q="0", sapinho=None):

        if '@' in q:
            await cbt.send("La estructura del comando es >pagar cantidad usuario, bobo magnánimo")
        elif "." in q or "," in q:
            await cbt.send("No hay ¥anCentavos, gran imbécil")
        elif int(q) < 0:
            await cbt.send("No le puede pagar una cantidad negativa a alguien bobo hijueputa")
        elif int(q) == 0:
            await cbt.send("No le puede pagar 0 a alguien, bobazo")
        elif sapinho is None or not sapinho.startswith('<@'):
            await cbt.send("Tiene que pagarle las ¥ a alguien, baboso")
        elif str(cbt.message.mentions[0].id) not in self.janpueblo.keys():
            await cbt.send(cbt.message.mentions[0].display_name + " no tiene registro de GIANLUKAS " + self.cogote)
        elif str(cbt.author.id) not in self.janpueblo.keys():
            await cbt.send("USTED no tiene registro de GIANLUKAS, bobo carepulgar " + self.cogote)
        else:
            q = int(q)
            if q > self.janpueblo[str(cbt.author.id)]:
                q = self.janpueblo[str(cbt.author.id)]
            self.persistir(str(cbt.author.id), -q)
            self.persistir(str(cbt.message.mentions[0].id), q)
            await cbt.send("Transferencia de ¥" + str(q) + " realizada. " + self.greed)
            await cbt.send(
                "Saldos actuales: \n" + cbt.author.display_name + ": ¥" + str(self.janpueblo[str(cbt.author.id)]))
            sapaso = cbt.message.mentions[0]
            sapeiro = sapaso.display_name
            await cbt.send(sapeiro + ": ¥" + str(self.janpueblo[str(cbt.message.mentions[0].id)]))

    @commands.command(brief="Muestra los mayores Yanburgueses de la mazmorra CBT",
                      description="Muestra el top 5 de Yanburgueses del servidor")
    async def yanking(self, cbt):
        listoix = list(self.janpueblo.keys())

        def key(item):
            return self.janpueblo[item]

        listoix = sorted(listoix, key=key, reverse=True)
        max = 5
        if len(listoix) < max:
            max = len(listoix)
        if not len(listoix):
            await cbt.send("No hay nadie con registro de GIANLUCAS, bobo puto")
        else:
            corotinho = "Top " + str(max) + " de yanburgueses: \n"
            # print(listoix)
            for niggy in range(0, max):
                c = listoix[niggy]
                # print(c)
                # print(self.janpueblo[c])
                # print(self.sapo.get_user(int(c)))
                sapaso = await self.sapo.fetch_user(int(c))
                sapeiro = sapaso.display_name
                corotinho += str(niggy + 1) + ": " + sapeiro + ": ¥" + str(self.janpueblo[c]) + "\n"
            await cbt.send(corotinho)

    @commands.command(brief="Invocar y avanzar una apuesta",
                      description="Comando multiuso. En su primera invocación, su estructura es >moneyman prompt opcion1 opcion2 ... opciónN. Es importante que cada uno de los argumentos del comando estén entre comillas. Una vez invocado así, se abren las apuestas, y la estructura del comando cambia a >moneyman (sin argumentos) para cerrar las apuestas. Durante este periodo, se puede apostar con >apostar. Finalmente, el comando >moneyman idOpcionGanadora reparte las hhanlux a los ganadores, y revierte el estado del comando al inicial.")
    async def moneyman(self, cbt, *args):
        if self.bigplay == 0:
            # C abren apuestas
            if args is None or len(args) < 1:
                await cbt.send("Debe basar la apuesta en algo, " + self.Insultos.insultar())
            elif len(args) < 3:
                await cbt.send("Incluya por lo menos 2 opciones para apostar más bien, " + self.Insultos.insultar())
            else:
                self.bets["prompt"] = args[0]
                self.bets["pirobo"] = cbt.author.id
                self.bigplay = 1
                cogote = "APUESTA DECLARADA \n" + args[0]
                for sapito in range(1, len(args)):
                    self.bets["o"][str(sapito)] = {
                        "prompt": args[sapito],
                        "total": 0,
                        "r": 1
                    }
                    cogote += "\n" + str(sapito) + ": " + args[sapito]
                cogote += "\n Diga [>apostar opción cantidad] para entrar a la apuesta"
                await cbt.send(cogote)
        elif self.bigplay == 1 and self.bets["pirobo"] == cbt.author.id:
            # C cierran apuestas
            if len(self.bets["u"]) == 0:
                await cbt.send(
                    "Nadie ha apostado aun, " + self.Insultos.insultar() + "\n Si va a cancelar, use >refund")
            else:
                self.bigplay = 2
                corote = "Apuestas cerradas: \n"
                for sapillo in self.bets["o"].keys():
                    corote += sapillo + " - " + self.bets["o"][sapillo]["prompt"] + ": ¥" + str(
                        self.bets["o"][sapillo]["total"]) + ", retorno de " + str(self.bets["o"][sapillo]["r"]) + "\n"
                await cbt.send(corote + " Esperando resultados.")
        elif self.bigplay == 2 and self.bets["pirobo"] == cbt.author.id:
            # C acaba la apuesta
            if args is None or len(args) < 1:
                await cbt.send("Debe declarar un resultado como ganador, " + self.Insultos.insultar())
            else:
                vic = args[0]
                if vic not in self.bets["o"].keys():
                    await cbt.send("Esa opción es inválida, " + self.Insultos.insultar())
                else:
                    r = float(self.bets["o"][vic]["r"])
                    robo = 0
                    for niggy in self.bets["u"]:
                        if niggy[1] == vic:
                            q = int(niggy[2] * r)
                            robo += q
                            self.persistir(str(niggy[0]), q)
                    await cbt.send(
                        "¥" + str(robo) + " repartidas a la opción " + vic + ": " + self.bets["o"][vic]["prompt"])
                    robo = abs(self.bets["t"] - robo)
                    self.persistir(str(self.sapo.user.id), robo)
                    self.bets = {"u": [],  # Lista de tuplas de usuarios que apostaron (id, opcion, cantidad)
                                 "o": {},
                                 "t": 0,
                                 "prompt": "",
                                 "pirobo": None
                                 }
                    self.bigplay = 0
        else:
            await cbt.send("Ya hay una apuesta en juego, " + self.Insultos.insultar())

    @commands.command(brief="Lo que el nombre implica",
                      description="Apostar en una apuesta abierta. La estructura del comando es >apostar idOpcion cantidad. Apuesta la cantidad de Yanlucas determinada a la opción dada como identificador. El comando sólo se puede utilizar si hay una apuesta abierta.")
    async def apostar(self, cbt, *args):
        if self.bigplay == 0:
            await cbt.send("No hay una apuesta en juego, " + self.Insultos.insultar())
        elif self.bigplay == 2:
            await cbt.send("Ya se cerraron apuestas, " + self.Insultos.insultar())
        elif cbt.author.id == self.bets["pirobo"]:
            await cbt.send("No puede apostar en su propia apuesta, " + self.Insultos.insultar())
        elif cbt.author.id in self.ludopatas():
            await cbt.send("Usted ya apostó, " + self.Insultos.insultar())
        elif str(cbt.author.id) not in self.janpueblo.keys():
            await cbt.send("USTED no tiene registro de GIANLUKAS, bobo carepulgar " + self.cogote)
        elif self.janpueblo[str(cbt.author.id)] == 0:
            await cbt.send("USTED no tiene GIANLUKAS, bobo pobre " + self.cogote)
        elif args is None or len(args) < 2:
            await cbt.send(
                "Use el comando completo " + self.Insultos.insultar() + "\n La estructura del comando es >apostar opción cantidad")
        elif args[0] not in self.bets["o"].keys():
            await cbt.send("Opción invalida " + self.Insultos.insultar())
        elif int(args[1]) <= 0:
            await cbt.send("Tan chistosito, " + self.Insultos.insultar())
        else:
            q = int(args[1])
            corote = ""
            if q >= self.janpueblo[str(cbt.author.id)]:
                q = self.janpueblo[str(cbt.author.id)]
                corote = "Si señores, ALL IN \n"
            self.persistir(str(cbt.author.id), -q)
            self.bets["u"].append(
                (cbt.author.id, args[0], q)
            )
            self.bets["t"] += q
            self.bets["o"][args[0]]["total"] += q
            # self.bets["o"][args[0]]["r"] = self.bets["t"]/self.bets["o"][args[0]]["total"]
            for sapillo in self.bets["o"].keys():
                if self.bets["o"][sapillo]["total"] != 0:
                    self.bets["o"][sapillo]["r"] = self.bets["t"] / self.bets["o"][sapillo]["total"]
            corote += "¥" + str(q) + " apostadas a la opción " + args[0] + ": " + self.bets["o"][args[0]]["prompt"]
            await cbt.send(corote)

    @commands.command(brief="Cancela una apuesta",
                      description="Cancelar una apuesta abierta. La estructura del comando es >refund. Sólo se puede llamar por el que invocó la apuesta o un moderador.")
    async def refund(self, cbt):
        jannies = await cbot.check_mod(cbt)
        if self.bigplay == 0:
            await cbt.send("¿Refund de que? " + self.Insultos.insultar())
        elif cbt.author.id != self.bets["pirobo"] and not jannies:
            await cbt.send("Nadie le dio permiso de eso, " + self.Insultos.insultar())
        else:
            for amiguinho in self.bets["u"]:
                self.persistir(str(amiguinho[0]), amiguinho[2])
            self.bets = {"u": [],  # Lista de tuplas de usuarios que apostaron (id, opcion, cantidad)
                         "o": {},
                         "t": 0,
                         "prompt": "",
                         "pirobo": None
                         }
            self.bigplay = 0
            await cbt.send("Apuesta cancelada, yanlucas restauradas.")

    @commands.command(brief="Reclamar",
                      description="Reclamar una cantidad de Yanlukas aleatoria cada 24 horas.")
    async def daily(self, cbt):
        sapillo = str(cbt.author.id)
        if sapillo in self.janpueblo.keys():
            numero_gracioso = random.randint(0,100)
            yanlukas = 0
            if numero_gracioso <= 85:
                yanlukas = random.randint(2,5)
            elif 85 < numero_gracioso <= 95:
                yanlukas = random.randint(6,10)
            elif 95 < numero_gracioso <= 98:
                yanlukas = random.randint(-4, -2)
            else:
                yanlukas = 15
            now = datetime.datetime.now()
            current_time = now.strftime('%Y-%m-%d %H:%M:%S.%f')
            janarchibo = open('./data/sapos/' + sapillo + ".doge", 'r')
            janlineas = janarchibo.readlines()
            janarchibo.close()
            if len(janlineas) < 2:
                if yanlukas == 15:
                    await cbt.send("JACKPOT!\n"+cbt.author.display_name + " ha reclamado " + str(yanlukas) + " Yanlucas. Presione ALT+F4 para reclamar sus Yanluks diarias.")

                elif yanlukas < 0:
                    await cbt.send(str(abs(yanlukas)) + " Yanlukas fueron incineradas lmao")
                else:
                    await cbt.send(
                        cbt.author.display_name + " ha reclamado " + str(yanlukas) + " Yanlucas. Presione ALT+F4 para reclamar sus Yanluks diarias.")
                self.persistir(sapillo, yanlukas)
                with open('./data/sapos/' + sapillo + ".doge", 'a+') as janarchibo:
                    janarchibo.write(current_time+"\n")
                    janarchibo.close()
            else:
                fecha_anterior_str = janlineas[1].strip()
                fecha_anterior = datetime.datetime.strptime(fecha_anterior_str, '%Y-%m-%d %H:%M:%S.%f')
                diferencia_fechas = now - fecha_anterior
                if diferencia_fechas.days >= 1:
                    janlineas[1] = current_time+"\n"
                    if yanlukas == 15:
                        await cbt.send( "JACKPOT!\n" + cbt.author.display_name + " ha reclamado " + str(yanlukas) + " Yanlucas. Presione ALT+F4 para reclamar sus Yanluks diarias.")
                    elif yanlukas < 0:
                        await cbt.send(str(abs(yanlukas)) + " Yanlukas fueron incineradas lmao")
                    else:
                        await cbt.send(
                            cbt.author.display_name + " ha reclamado " + str(yanlukas) + " Yanlucas. Presione ALT+F4 para reclamar sus Yanluks diarias.")
                    with open('./data/sapos/' + sapillo + ".doge", 'w') as janarchibo:
                        janarchibo.writelines(janlineas)
                        janarchibo.close()
                    self.persistir(sapillo, yanlukas)
                else:
                    await cbt.send("No sea codicioso, " + self.Insultos.insultar())
        else:
            await cbt.send("A dónde le consigno, " + self.Insultos.insultar())

    def ludopatas(self):
        niggas = []
        for niggy in self.bets["u"]:
            niggas.append(niggy[0])
        return niggas


def setup(sapo):
    sapo.add_cog(YanLukas(sapo))
