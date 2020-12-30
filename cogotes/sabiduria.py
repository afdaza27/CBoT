import discord
from discord.ext import commands
import random

class Sabiduria(commands.Cog):

    def __init__(self, sapo):
        self.sapo = sapo
        self.adagios = ["Manchmal muss man machen, dass man machen muss.",
                        "I am but a tearful clown. Though I smile, I cry inside.",
                        "Bad times are just times that are bad.",
                        "Who wears armour today may wear armour tomorrow.",
                        "Sun Tzu dice: El verdadero arte de la guerra es vencer a tu enemigo sin enfrentarlo.",
                        "Sun Tzu dice: La invencibilidad se encuentra en la defensa, pero la posibilidad de la victoria está en el ataque.",
                        "It is no nation we inhabit, but a language. Make no mistake; our native tongue is our true fatherland.",
                        "Sun Tzu dice: Si el enemigo esta lejos, hágalo creer que está cerca.",
                        "Sun Tzu dice: En el caos yacen tambien oportunidades.",
                        "Sun Tzu dice: Al tomarse, se multiplican las oportunidades.",
                        "Sun Tzu dice: Estoy en la edad de la rana; hago lo que se me da la gana.",
                        "Ayúdenme, esto no es un meme. Me estan obligando a escribir estas babosadas y necesito ayuda.",
                        "Un sabio dijo: Es mejor saber aprender que saber.",
                        "Un sabio dijo: Ignora tus instintos bajo tu propio riesgo.",
                        "Un sabio dijo: Veo Sabados Felices los domingos.",
                        "Un sabio dijo: Sin honor la victoria es vacia.",
                        "Un sabio dijo: El equilibrio está en aquel que acepta su culpa.",
                        "Un sabio dijo: Las coronas se heredan, pero los reinos se ganan.",
                        "Un sabio dijo: El engaño es el arma de la avaricia.",
                        "Un sabio dijo: La sabiduría nace tanto en los tontos como en los sabios.",
                        "Sun Tzu dice: La búsqueda del honor lo hace a uno honorable.",
                        "Un sabio dijo: El que nunca arriesga se suele perder lo mejor.",
                        "Un sabio dijo: Cualquiera puede cocinar.",
                        "Un sabio dijo: Despeja tu área, o te haré llorar.",
                        "Un sabio dijo: Jueputa ya deje de preguntarme frases que no me se más.",
                        "Un sabio dijo: Un ogro es como una cebolla. Las cebollas tienen capas; los ogros tenemos capas.",
                        "¿Sabías que? 437 es el número más grande",
                        "There is no success without succ.",
                        "Un sabio dijo: Buenas tardes, busco teclado para PC.",
                        "¿Sabías que? Hay un restaurante en Nueva York.",
                        "A wise man from the east once said: Never ask anything from me ever again.",
                        "Un sabio dijo: Reclama taco de galletas Saltín por la compra de tu sim card TIGO o COMCEL.",
                        "A wise man from the west once said: Eat the glass bitch!",
                        "Hard times create real niggas. Real niggas create good times. Good times create bitch-ass niggas. Bitch-ass niggas create hard times.",
                        "Los límites de mi lenguaje significan los límites de mi mundo.",
                        "Tremendo pecho frio el Messi.\n Dale like si no sos gay.",
                        "The wicked flee when no one pursueth, but the righteous are as bold as a lion.",
                        "Lao-Tze said: He who knows that enough is enough will always have enough.",
                        "Shakespeare said: Nought's had, all's spent, where our desire is got without content.",
                        "Confucius said: The cautious seldom err.",
                        "A wise man once said: Friendly counsel cuts off many foes.",
                        "Confucius said: The superior man is modest in his speech but exceeds in his actions.",
                        "A wise man from the east once said: Rashness brings success to few and misfortune to many.",
                        "A proud man does not eat rotting meat even when hungry, nor steal water from another's well when he thirsts.",
                        "The snake, knowing itself, strikes swiftly.",
                        "Sometimes treasure is not hidden. It is only invisible.",
                        "He who stubs his toe is he who remembers his feet are there.",
                        "Breathing underwater is rather easy, assuming you have gills.",
                        "Power is often fleeting.","There are no shortcuts in life, except for when there are.",
                        "Your friends need you. They always need you. They will never stop.",
                        "He who believes he has a pure heart is probably just a beast in denial.",
                        "It always rains on your birthday, yet no one ever gives you an umbrella.",
                        "Those who slip are often given a chance to appreciate the ground.",
                        "He who looks from below sees a great deal.",
                        "When someone fakes a smile, don't get mad, for they are at least trying.",
                        "If you beat yourself up, that means you lost to yourself.",
                        "Cheese can never be milk again.",
                        "Sometimes it really do be like that.",
                        "3 stages of a real nigga: struggle, grind, SHINE.",
                        "Real niggas don't wash their hands after peeing.",
                        "Sun Tzu dice: Conoce a tu enemigo y conocete a ti mismo, y en 100 batallas nunca estaras en peligro.",
                        "Un sabio dijo: Para tener exito el deseo debe ser mayor que el miedo al fracaso.",
                        "Un sabio dijo: No cualquiera puede convertirse en un gran artista, pero un gran artista puede provenir de cualquier lado.",
                        "Un sabio dijo: Evita usar zapatos en la playa, pues se llenaran de arena.",
                        "Monitorias Exámenes finales Álgebra Lineal e Integral \n \n \n Recibe un cordial saludo, soy Christian Jerry:  \n \n En este correo, queremos confirmar nuestras ultimas monitorias de Integral y Álgebra lineal. \n \n La monitoria de integral del martes a sugerencia  de muchos la empezaremos a la 11:30am. Si tienes parcial de Álgebra Lineal o Fisica 2, podrias asistir. \n \n Metodología: Explicaremos los últimos temas del curso, haremos ejercicios de diferentes niveles, muchos de ellos, ejercicios viejos de parciales \n \n Inscríbete aquí vía whatsaap 3017578752 \n \n A continuación te presentamos la agenda: \n \n Álgebra Lineal: Examen final \n •	Opción 3: Domingo 2 de diciembre. 2:00pm-7:30pm. Hotel Interbogota Carrera 3 20-17. Frente a universidades. Integral con ecuaciones:  Examen final  \n •	Opción 2: Lunes 3 de diciembre. 2:00pm-7:30pm. Hotel Interbogota Carrera 3 20-17. Frente a universidades.\n •	Opción 3: Martes 4 de diciembre. 11:30am-5pm Hotel Interbogota Carrera 3 20-17. Frente a universidades.\n Valor de las monitorias: 50mil \n Promo: si asistes en grupos de a 3, recibe un descuento de 5mil, es decir, cada uno paga 45mil (avisando con antelación a la monitoria) \n \n \n Cupos limitados!! \n  Recuerda inscríbirte aquí vía whatsaap 3017578752 \n \n \n Te esperamos \n Atentamente \n \n Christian",
                        "Por donde camina el gentio no crece el matorral."]
        self.ego = 	"La vida de un crítico es sencilla en muchos aspectos, arriesgamos poco y tenemos poder sobre aquellos que ofrecen su trabajo \n  y su servicio a nuestro juicio. Prosperamos con las críticas negativas, divertidas de escribir y de leer, pero la triste verdad que \n debemos afrontar es que en el gran orden de las cosas, cualquier basura tiene más significado que lo que deja ver nuestra crítica. \n Pero en ocasiones el crítico si se arriesga cada vez que descubre y defiende algo nuevo, el mundo suele ser cruel con el \n nuevo talento; las nuevas creaciones, lo nuevo, necesita amigos. Anoche experimente algo nuevo; una extraordinaria cena de una \n fuente singular e inesperada. Decir solo que la comida y su creador han desafiado mis prejuicios sobre la buena cocina, \n subestimaría la realidad; me han tocado en lo más profundo. En el pasado jamás oculte mi desdén por el famoso lema del chef Gusteau: \n Cualquiera puede cocinar. Pero al fin me doy cuenta de lo que quiso decir en realidad; no cualquiera puede \n convertirse en un gran artista, pero un gran artista puede provenir de cualquier lado. Es difícil imaginar un origen más humilde que\n  el del genio que ahora cocina en el restaurante Gusteau´s y quien, en opinión de este critico, es nada menos que el \n mejor chef de Francia. ¡Pronto volveré a Gusteau´s hambriento!"

    @commands.Cog.listener()
    async def on_ready(self):
        print("Sun Tzu dice: buenas tardes.")

    @commands.command()
    async def ego(self, cbt):
        await cbt.send(self.ego)

    @commands.command()
    async def adagio(self, cbt):
        numericio = random.randint(0, len(self.adagios)-1)
        await cbt.send(self.adagios[numericio])



def setup(sapo):
    sapo.add_cog(Sabiduria(sapo))