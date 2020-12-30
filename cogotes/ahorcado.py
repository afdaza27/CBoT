import discord
from discord.ext import commands
import asyncio
import random

class Ahorcado(commands.Cog):

    def __init__(self, sapo):
        self.sapo = sapo
        self.prompt = ""
        self.prompt_state = ""
        self.letters_juiced = []
        self.state = 0
        self.condenando = False
        self.emojis = {"cogote":"<:cogote:755197902049116201>"}
        self.state_list = ["|--------|\n|             |\n|\n|\n|\n|\n-------------------------",
                           "|--------|\n|             |\n|           <:cogote:755197902049116201>\n|\n|\n|\n-------------------------",
                           "|--------|\n|             |\n|           <:cogote:755197902049116201>\n|           🥋\n|\n|\n-------------------------",
                           "|--------|\n|             |\n|           <:cogote:755197902049116201>\n|           🥋\n|           👖\n|\n-------------------------",
                           "|--------|\n|             |\n|           <:cogote:755197902049116201>\n|    💪🏼 🥋👎🏼 \n|           👖\n|\n-------------------------\nBAD ENDING.",
                           "|           <:cogote:755197902049116201> \n|    💪🏼 🥋👍🏼\n|           👖\nGOOD ENDING."]

    @commands.Cog.listener()
    async def on_ready(self):
        print("Cogote listo para ser ahorcado.")

    @commands.command()
    async def condenar(self, cbt):
        if(not self.condenando):
            self.condenando = True
            retard_timeout = ["Se demoró mucho, retrasado", "Hasta el mundial de tejo o que hijueputas", "Pirobo tan lento",
                              "Era pa ayer, pues", "Más lento que tortuga coja", "Parece Max cepillándose los dientes"]
            user = await self.sapo.fetch_user(cbt.author.id)
            await user.send("Para iniciar el juego escriba su palabra o frase. Procure no usar tildes ni caracteres graciosos. Tiene un minuto.")
            await cbt.send("Se esta generando la condena.")
            msg = "Se pospone la condena, el retrasado no supo escribir a tiempo."
            def check(msg):
                return msg.author == cbt.author and msg.channel == user.dm_channel
            try:
                msg = await self.sapo.wait_for("message", check=check, timeout=60)
            except asyncio.TimeoutError:
                await user.send(retard_timeout[random.randint(0, len(retard_timeout)-1)])
                self.condenando = False
            if msg != "Se pospone la condena, el retrasado no supo escribir a tiempo.":
                self.prompt = msg.content.lower()
                self.prompt_state = ""
                for i in range(0, len(self.prompt)):
                    if self.prompt[i] != " ":
                        self.prompt_state += "?"
                    else:
                        self.prompt_state += " "
                self.state = 0
                self.letters_juiced.clear()
                await cbt.send(self.state_list[self.state])
                await cbt.send(self.prompt_state)
            else:
                await cbt.send(msg)
        else:
            await cbt.send("ESPÉRESE. Ya hay una condena en progreso.")

    @commands.command()
    async def perdonar(self, cbt):
        if self.condenando:
            self.state = 0
            self.prompt = ""
            self.prompt_state = ""
            self.letters_juiced.clear()
            self.condenando = False
            await cbt.send("El cogote fue perdonado, finaliza el juego. "+self.emojis["cogote"])
        else:
            await cbt.send("¿Perdonar a quién?, bobooo")

    @commands.command()
    async def objecion(self, cbt, letra):
        letra = letra.lower()
        if self.condenando:
            if len(letra) != 1:
                await cbt.send("UNA letra, bobo")
                self.state += 1
            elif letra in self.letters_juiced:
                await cbt.send("Esa ya salió, ponga atención bruto")
                self.state += 1
            elif letra in self.prompt:
                prompt_state_list = []
                for char in self.prompt_state:
                    prompt_state_list.append(char)
                for i in range(0, len(prompt_state_list)):
                    if self.prompt[i] == letra:
                        prompt_state_list[i] = letra
                self.prompt_state = ""
                for i in range(0, len(prompt_state_list)):
                    self.prompt_state+=prompt_state_list[i]
            else:
                self.state +=1
            if letra not in self.letters_juiced:
                self.letters_juiced.append(letra)
            if "?" not in self.prompt_state:
                self.state = 5
                self.condenando = False

            if self.state == 4:
                self.condenando = False
                await cbt.send(self.state_list[self.state])
                await cbt.send(self.prompt)
            if self.state != 4:
                await cbt.send(self.state_list[self.state])
                await cbt.send(self.prompt_state)
        else:
            await cbt.send("De qué putas habla, gran marika")


    @commands.command()
    async def absolver(self, cbt, *args):
        intento = ""
        for i in range(0, len(args)):
            intento += args[i]
            intento += " "
        intento = intento.rstrip()
        if self.condenando:
            if intento == self.prompt:
                self.state = 5
                self.condenando = False
                await cbt.send(self.state_list[self.state])
                await cbt.send(self.prompt)
            else:
                self.state = 4
                self.condenando = False
                await cbt.send(self.state_list[self.state])
                await cbt.send(self.prompt)
        else:
            await cbt.send("A qué juega, imbécil")

def setup(sapo):
    sapo.add_cog(Ahorcado(sapo))