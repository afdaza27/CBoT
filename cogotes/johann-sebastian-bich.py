import discord
from discord.ext import commands

from youtube_dl import YoutubeDL

import cbot
from modulos.insultos import Insultos

import random
import asyncio
import itertools
import sys
import traceback
from async_timeout import timeout
from functools import partial
import youtube_dl

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

ytdlopts = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn',
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
}

ytdl = YoutubeDL(ytdlopts)


class VoiceConnectionError(commands.CommandError):
    """Custom Exception class for connection errors."""


class InvalidVoiceChannel(VoiceConnectionError):
    """Exception for cases of invalid Voice Channels."""


class YTDLSource(discord.PCMVolumeTransformer):

    def __init__(self, source, *, data, requester):
        super().__init__(source)
        self.requester = requester

        self.title = data.get('title')
        self.web_url = data.get('webpage_url')
        self.duration = data.get('duration')

        # YTDL info dicts (data) have other useful information you might want
        # https://github.com/rg3/youtube-dl/blob/master/README.md

    def __getitem__(self, item: str):
        """Allows us to access attributes similar to a dict.
        This is only useful when you are NOT downloading.
        """
        return self.__getattribute__(item)

    @classmethod
    async def create_source(cls, ctx, search: str, *, loop, download=False):
        loop = loop or asyncio.get_event_loop()

        to_run = partial(ytdl.extract_info, url=search, download=download)
        data = await loop.run_in_executor(None, to_run)

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        embed = discord.Embed(title="",
                              description=f"Queued [{data['title']}]({data['webpage_url']}) [{ctx.author.mention}]",
                              color=discord.Color.green())
        await ctx.send(embed=embed)

        if download:
            source = ytdl.prepare_filename(data)
        else:
            return {'webpage_url': data['webpage_url'], 'requester': ctx.author, 'title': data['title']}

        return cls(discord.FFmpegPCMAudio(source), data=data, requester=ctx.author)

    @classmethod
    async def regather_stream(cls, data, *, loop):
        """Used for preparing a stream, instead of downloading.
        Since Youtube Streaming links expire."""
        loop = loop or asyncio.get_event_loop()
        requester = data['requester']

        to_run = partial(ytdl.extract_info, url=data['webpage_url'], download=False)
        data = await loop.run_in_executor(None, to_run)

        return cls(discord.FFmpegPCMAudio(data['url']), data=data, requester=requester)


class MusicPlayer:
    """A class which is assigned to each guild using the bot for Music.
    This class implements a queue and loop, which allows for different guilds to listen to different playlists
    simultaneously.
    When the bot disconnects from the Voice it's instance will be destroyed.
    """

    __slots__ = ('bot', '_guild', '_channel', '_cog', 'queue', 'next', 'current', 'np', 'volume')

    def __init__(self, ctx):
        self.bot = ctx.bot
        self._guild = ctx.guild
        self._channel = ctx.channel
        self._cog = ctx.cog

        self.queue = asyncio.Queue()
        self.next = asyncio.Event()

        self.np = None  # Now playing message
        self.volume = .5
        self.current = None

        ctx.bot.loop.create_task(self.player_loop())

    async def player_loop(self):
        """Our main player loop."""
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            self.next.clear()

            try:
                # Wait for the next song. If we timeout cancel the player and disconnect...
                async with timeout(300):  # 5 minutes...
                    source = await self.queue.get()
            except asyncio.TimeoutError:
                return self.destroy(self._guild)

            if not isinstance(source, YTDLSource):
                # Source was probably a stream (not downloaded)
                # So we should regather to prevent stream expiration
                try:
                    source = await YTDLSource.regather_stream(source, loop=self.bot.loop)
                except Exception as e:
                    await self._channel.send(f'There was an error processing your song.\n'
                                             f'```css\n[{e}]\n```')
                    continue

            source.volume = self.volume
            self.current = source

            self._guild.voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
            embed = discord.Embed(title="Now playing",
                                  description=f"[{source.title}]({source.web_url}) [{source.requester.mention}]",
                                  color=discord.Color.green())
            self.np = await self._channel.send(embed=embed)
            await self.next.wait()

            # Make sure the FFmpeg process is cleaned up.
            source.cleanup()
            self.current = None

    def destroy(self, guild):
        """Disconnect and cleanup the player."""
        return self.bot.loop.create_task(self._cog.cleanup(guild))


class bich(commands.Cog):
    """Music related commands."""

    __slots__ = ('bot', 'players')

    def __init__(self, bot):
        self.bot = bot
        self.players = {}

    async def cleanup(self, guild):
        try:
            await guild.voice_client.disconnect()
        except AttributeError:
            pass

        try:
            del self.players[guild.id]
        except KeyError:
            pass

    async def __local_check(self, ctx):
        """A local check which applies to all commands in this cog."""
        if not ctx.guild:
            raise commands.NoPrivateMessage
        return True

    async def __error(self, ctx, error):
        """A local error handler for all errors arising from commands in this cog."""
        if isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.send('This command can not be used in Private Messages.')
            except discord.HTTPException:
                pass
        elif isinstance(error, InvalidVoiceChannel):
            await ctx.send('Error connecting to Voice Channel. '
                           'Please make sure you are in a valid channel or provide me with one')

        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    def get_player(self, ctx):
        """Retrieve the guild player, or generate one."""
        try:
            player = self.players[ctx.guild.id]
        except KeyError:
            player = MusicPlayer(ctx)
            self.players[ctx.guild.id] = player

        return player

    @commands.Cog.listener()
    async def on_ready(self):
        print("MANOS EN EL PIANO")

    @commands.command(name='caiga', aliases=['connect', 'j','join'], description="connects to voice")
    async def connect_(self, ctx, *, channel: discord.VoiceChannel = None):
        """Connect to voice.
        Parameters
        ------------
        channel: discord.VoiceChannel [Optional]
            The channel to connect to. If a channel is not specified, an attempt to join the voice channel you are in
            will be made.
        This command also handles moving the bot to different channels.
        """
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                embed = discord.Embed(title="",
                                      description="No channel to join. Please call `,join` from a voice channel.",
                                      color=discord.Color.green())
                await ctx.send(embed=embed)
                raise InvalidVoiceChannel('No channel to join. Please either specify a valid channel or join one.')

        vc = ctx.voice_client

        if vc:
            if vc.channel.id == channel.id:
                return
            try:
                await vc.move_to(channel)
            except asyncio.TimeoutError:
                raise VoiceConnectionError(f'Moving to channel: <{channel}> timed out.')
        else:
            try:
                await channel.connect()
            except asyncio.TimeoutError:
                raise VoiceConnectionError(f'Connecting to channel: <{channel}> timed out.')
        if (random.randint(0, 1) == 0):
            await ctx.message.add_reaction('👍')
        await ctx.send(f'**Joined `{channel}`**')

    @commands.command(name='play', aliases=['sing', 'p'], description="streams music")
    async def play_(self, ctx, *, search: str):
        """Request a song and add it to the queue.
        This command attempts to join a valid voice channel if the bot is not already in one.
        Uses YTDL to automatically search and retrieve a song.
        Parameters
        ------------
        search: str [Required]
            The song to search and retrieve using YTDL. This could be a simple search, an ID or URL.
        """
        await ctx.trigger_typing()

        vc = ctx.voice_client

        if not vc:
            await ctx.invoke(self.connect_)

        player = self.get_player(ctx)

        # If download is False, source will be a dict which will be used later to regather the stream.
        # If download is True, source will be a discord.FFmpegPCMAudio with a VolumeTransformer.
        source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop, download=False)

        await player.queue.put(source)

    @commands.command(name='pause', description="pauses music")
    async def pause_(self, ctx):
        """Pause the currently playing song."""
        vc = ctx.voice_client

        if not vc or not vc.is_playing():
            embed = discord.Embed(title="", description="I am currently not playing anything",
                                  color=discord.Color.green())
            return await ctx.send(embed=embed)
        elif vc.is_paused():
            return

        vc.pause()
        await ctx.send("Paused ⏸️")

    @commands.command(name='resume', description="resumes music")
    async def resume_(self, ctx):
        """Resume the currently paused song."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed = discord.Embed(title="", description="I'm not connected to a voice channel",
                                  color=discord.Color.green())
            return await ctx.send(embed=embed)
        elif not vc.is_paused():
            return

        vc.resume()
        await ctx.send("Resuming ⏯️")

    @commands.command(name='skip', description="skips to next song in queue")
    async def skip_(self, ctx):
        """Skip the song."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed = discord.Embed(title="", description="I'm not connected to a voice channel",
                                  color=discord.Color.green())
            return await ctx.send(embed=embed)

        if vc.is_paused():
            pass
        elif not vc.is_playing():
            return

        vc.stop()

    @commands.command(name='remove', aliases=['rm', 'rem'], description="removes specified song from queue")
    async def remove_(self, ctx, pos: int = None):
        """Removes specified song from queue"""

        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed = discord.Embed(title="", description="I'm not connected to a voice channel",
                                  color=discord.Color.green())
            return await ctx.send(embed=embed)

        player = self.get_player(ctx)
        if pos == None:
            player.queue._queue.pop()
        else:
            try:
                s = player.queue._queue[pos - 1]
                del player.queue._queue[pos - 1]
                embed = discord.Embed(title="",
                                      description=f"Removed [{s['title']}]({s['webpage_url']}) [{s['requester'].mention}]",
                                      color=discord.Color.green())
                await ctx.send(embed=embed)
            except:
                embed = discord.Embed(title="", description=f'Could not find a track for "{pos}"',
                                      color=discord.Color.green())
                await ctx.send(embed=embed)

    @commands.command(name='clear', aliases=['clr', 'cl', 'cr'], description="clears entire queue")
    async def clear_(self, ctx):
        """Deletes entire queue of upcoming songs."""

        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed = discord.Embed(title="", description="I'm not connected to a voice channel",
                                  color=discord.Color.green())
            return await ctx.send(embed=embed)

        player = self.get_player(ctx)
        player.queue._queue.clear()
        await ctx.send('💣 **Cleared**')

    @commands.command(name='queue', aliases=['q', 'playlist', 'que'], description="shows the queue")
    async def queue_info(self, ctx):
        """Retrieve a basic queue of upcoming songs."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed = discord.Embed(title="", description="I'm not connected to a voice channel",
                                  color=discord.Color.green())
            return await ctx.send(embed=embed)

        player = self.get_player(ctx)
        if player.queue.empty():
            embed = discord.Embed(title="", description="queue is empty", color=discord.Color.green())
            return await ctx.send(embed=embed)

        seconds = vc.source.duration % (24 * 3600)
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        if hour > 0:
            duration = "%dh %02dm %02ds" % (hour, minutes, seconds)
        else:
            duration = "%02dm %02ds" % (minutes, seconds)

        # Grabs the songs in the queue...
        upcoming = list(itertools.islice(player.queue._queue, 0, int(len(player.queue._queue))))
        fmt = '\n'.join(
            f"`{(upcoming.index(_)) + 1}.` [{_['title']}]({_['webpage_url']}) | ` {duration} Requested by: {_['requester']}`\n"
            for _ in upcoming)
        fmt = f"\n__Now Playing__:\n[{vc.source.title}]({vc.source.web_url}) | ` {duration} Requested by: {vc.source.requester}`\n\n__Up Next:__\n" + fmt + f"\n**{len(upcoming)} songs in queue**"
        embed = discord.Embed(title=f'Queue for {ctx.guild.name}', description=fmt, color=discord.Color.green())
        embed.set_footer(text=f"{ctx.author.display_name}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(name='np', aliases=['song', 'current', 'currentsong', 'playing','nowplaying'],
                      description="shows the current playing song")
    async def now_playing_(self, ctx):
        """Display information about the currently playing song."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed = discord.Embed(title="", description="I'm not connected to a voice channel",
                                  color=discord.Color.green())
            return await ctx.send(embed=embed)

        player = self.get_player(ctx)
        if not player.current:
            embed = discord.Embed(title="", description="I am currently not playing anything",
                                  color=discord.Color.green())
            return await ctx.send(embed=embed)

        seconds = vc.source.duration % (24 * 3600)
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        if hour > 0:
            duration = "%dh %02dm %02ds" % (hour, minutes, seconds)
        else:
            duration = "%02dm %02ds" % (minutes, seconds)

        embed = discord.Embed(title="",
                              description=f"[{vc.source.title}]({vc.source.web_url}) [{vc.source.requester.mention}] | `{duration}`",
                              color=discord.Color.green())
        embed.set_author(icon_url=self.bot.user.avatar_url, name=f"Now Playing 🎶")
        await ctx.send(embed=embed)

    @commands.command(name='volume', aliases=['vol', 'v'], description="changes Kermit's volume")
    async def change_volume(self, ctx, *, vol: float = None):
        """Change the player volume.
        Parameters
        ------------
        volume: float or int [Required]
            The volume to set the player to in percentage. This must be between 1 and 100.
        """
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed = discord.Embed(title="", description="I am not currently connected to voice",
                                  color=discord.Color.green())
            return await ctx.send(embed=embed)

        if not vol:
            embed = discord.Embed(title="", description=f"🔊 **{(vc.source.volume) * 100}%**",
                                  color=discord.Color.green())
            return await ctx.send(embed=embed)

        if not 0 < vol < 101:
            embed = discord.Embed(title="", description="Please enter a value between 1 and 100",
                                  color=discord.Color.green())
            return await ctx.send(embed=embed)

        player = self.get_player(ctx)

        if vc.source:
            vc.source.volume = vol / 100

        player.volume = vol / 100
        embed = discord.Embed(title="", description=f'**`{ctx.author}`** set the volume to **{vol}%**',
                              color=discord.Color.green())
        await ctx.send(embed=embed)

    @commands.command(name='fuera', aliases=["stop", "dc", "disconnect", "bye",'leave'],
                      description="stops music and disconnects from voice")
    async def leave_(self, ctx):
        """Stop the currently playing song and destroy the player.
        !Warning!
            This will destroy the player assigned to your guild, also deleting any queued songs and settings.
        """
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed = discord.Embed(title="", description="I'm not connected to a voice channel",
                                  color=discord.Color.green())
            return await ctx.send(embed=embed)

        if (random.randint(0, 1) == 0):
            await ctx.message.add_reaction('👋')
        await ctx.send('**Successfully disconnected**')

        await self.cleanup(ctx.guild)
# import asyncio
# import discord
# from discord.ext import commands
# import os
# import cbot
# import datetime
# import random
# import youtube_dl
# import time
# from modulos.insultos import Insultos
# from cogotes.yanlukas import YanLukas
#
#
# youtube_dl.utils.bug_reports_message = lambda: ''
#
# ytdl_format_options = {
#     'format': '249/250/251',
#     'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
#     'restrictfilenames': True,
#     'noplaylist': True,
#     'nocheckcertificate': True,
#     'ignoreerrors': False,
#     'logtostderr': False,
#     'quiet': True,
#     'no_warnings': True,
#     'default_search': 'auto',
#     'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
# }
#
# ffmpeg_options = {
#     #'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
#     'options': '-vn'
# }
#
# ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
#
#
#
# class YTDLSource(discord.PCMVolumeTransformer):
#     def __init__(self, source, *, data, volume=0.2):
#         super().__init__(source, volume)
#
#         self.data = data
#
#         self.title = data.get('title')
#         self.url = data.get('url')
#
#     @classmethod
#     async def from_url(cls, url, *, loop=None, stream=False):
#         loop = loop or asyncio.get_event_loop()
#         data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
#
#         if 'entries' in data:
#             # take first item from a playlist
#             data = data['entries'][0]
#
#         filename = data['url'] if stream else ytdl.prepare_filename(data)
#         return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
#
#
# class Bich(commands.Cog):
#     def __init__(self, sapo):
#         self.sapo = sapo
#         self.db = cbot.get_db()
#         self.Insultos = Insultos(self.db, cbot.user)
#         self.Insultos.cargar_insultos()
#         self.state=False
#         self.q = []
#         #self.ytdlsource = YTDLSource()
#
#
#     async def actualizar_insultos(self):
#         user = cbot.sign_in()
#         self.Insultos.refrescar_usuario(user)
#         self.Insultos.cargar_insultos()
#
#     # async def enq(self, cbt, vc):
#     #     if not self.state:
#     #         self.state=True
#     #     tema = self.q.pop()
#     #     async with cbt.typing():
#     #         player = await YTDLSource.from_url(tema, loop=self.sapo.loop)
#     #         cbt.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
#     #
#     #     await cbt.send('**Now playing:** {}'.format(player.title))
#     #     while(vc.is_playing()):
#     #         time.sleep(.1)
#     #     for file in os.listdir('./'):
#     #         if file.endswith('.webm'):
#     #             os.remove(file)
#     #     if len(self.q)>0 and self.state:
#     #         self.enq(cbt,vc)
#     #     else:
#     #         self.state=False
#     #         return
#     async def play_next(self, cbt):
#         if len(self.q) > 0:
#             self.state = True
#
#             # get the first url
#             m_url = self.q[0]
#
#             # remove the first element as you are currently playing it
#             self.q.pop(0)
#
#             #self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
#             #PONER EL TEMA ACA
#             #async with cbt.typing():
#             player = await YTDLSource.from_url(m_url, loop=self.sapo.loop)
#             cbt.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else self.play_next(cbt))
#
#             await cbt.send('**Now playing:** {}'.format(player.title))
#         else:
#             self.state = False
#
#     # infinite loop checking
#     async def play_music(self, cbt):
#         if len(self.q) > 0:
#             self.state = True
#
#             m_url = self.q[0]
#
#             # try to connect to voice channel if you are not already connected
#
#             #if self.vc == "" or not self.vc.is_connected() or self.vc == None:
#             #    self.vc = await self.music_queue[0][1].connect()
#             #else:
#             #    await self.vc.move_to(self.music_queue[0][1])
#
#             print(self.q)
#             # remove the first element as you are currently playing it
#             self.q.pop(0)
#
#             #vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
#             #PONER EL TEMA
#             #async with cbt.typing():
#             player = await YTDLSource.from_url(m_url, loop=self.sapo.loop)
#             cbt.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else self.play_next(cbt))
#
#             await cbt.send('**Now playing:** {}'.format(player.title))
#         else:
#             self.state = False
#
#
#
#     @commands.Cog.listener()
#     async def on_ready(self):
#         print("MANOS EN EL PIANO")
#
#     @commands.command()
#     async def caiga(self, cbt):
#         racismo = cbt.author.voice.channel
#         if cbt.voice_client is None:
#             await racismo.connect()
#         elif racismo==cbt.guild.voice_client.channel:
#             await cbt.send("Ya estoy ahí "+ self.Insultos.insultar())
#         else:
#             await cbt.voice_client.move_to(racismo)
#
#
#     @commands.command()
#     async def fuera(self, cbt):
#         if cbt.voice_client is None:
#             await cbt.send("Yo no estoy conectado "+ self.Insultos.insultar())
#         elif (cbt.author.voice.channel and cbt.author.voice.channel == cbt.voice_client.channel) or await cbot.check_mod(cbt):
#             cbt.voice_client.stop()
#             self.q = []
#             self.state = False
#             await cbt.voice_client.disconnect()
#         else:
#             await cbt.send("¿Con la autoridad de quien?\n" + self.Insultos.insultar())
#
#     @commands.command()
#     async def play(self, cbt, tema):
#         racismo = cbt.author.voice.channel
#         if (cbt.guild.voice_client is not None and racismo!=cbt.guild.voice_client.channel) and not await cbot.check_mod(cbt):
#             await cbt.send("¿Con la autoridad de quien?\n" + self.Insultos.insultar())
#         else:
#             if cbt.voice_client is None:
#                 vc = await racismo.connect()
#             else:
#                 vc = cbt.voice_client
#             self.q.append(tema)
#             await cbt.send("Song added to the queue")
#             if not self.state:
#                 await self.play_music(cbt)
#
#
#     # @commands.command()
#     # async def stream(self, cbt, tema):
#     #     racismo = cbt.author.voice.channel
#     #     if (cbt.guild.voice_client is not None and racismo!=cbt.guild.voice_client.channel) and not await cbot.check_mod(cbt):
#     #         await cbt.send("¿Con la autoridad de quien?\n" + self.Insultos.insultar())
#     #     else:
#     #         vc = None
#     #         if cbt.voice_client is None:
#     #             vc = await racismo.connect()
#     #         else:
#     #             vc = cbt.voice_client
#     #         #de aca para abajo es código robado
#     #         async with cbt.typing():
#     #             player = await YTDLSource.from_url(tema, loop=self.sapo.loop, stream=True)
#     #             cbt.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
#     #
#     #     await cbt.send('**Now playing:** {}'.format(player.title))
#
#     @commands.command()
#     async def pause(self, cbt):
#         if cbt.voice_client is None:
#             await cbt.send("Yo no estoy conectado " + self.Insultos.insultar())
#         elif not (cbt.author.voice.channel and cbt.author.voice.channel == cbt.voice_client.channel):
#             await cbt.send("¿Con la autoridad de quien?\n" + self.Insultos.insultar())
#         elif cbt.voice_client.is_paused():
#             cbt.voice_client.resume()
#             await cbt.send("Audio reanudado")
#         else:
#             cbt.voice_client.pause()
#             await cbt.send("Audio pausado")
#
#     @commands.command()
#     async def stop(self, cbt):
#         if cbt.voice_client is None:
#             await cbt.send("Yo no estoy conectado " + self.Insultos.insultar())
#         elif not (cbt.author.voice.channel and cbt.author.voice.channel == cbt.voice_client.channel):
#             await cbt.send("¿Con la autoridad de quien?\n" + self.Insultos.insultar())
#         else:
#             cbt.voice_client.stop()
#             self.q = []
#             self.state = False
#             await cbt.send("Servicio detenido")
#
#
def setup(sapo):
    sapo.add_cog(bich(sapo))