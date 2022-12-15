import discord
import time
import datetime
import discordSuperUtils
from time import monotonic
import pytz
from typing import Optional
from discord.ext import commands
from discord import Embed as embed
from discord import Colour as color
from discordSuperUtils import MusicManager
import random

 
class Music(commands.Cog, discordSuperUtils.CogManager.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client_id = "client id spotify"
        self.client_secret = "client secret spotify"
        self.MusicManager = discordSuperUtils.MusicManager(
            self.bot,
            spotify_support=True,
            client_secret=self.client_secret,
            client_id=self.client_id,
        )
        self.emoji = ["👌", "😋", "👽", "💪", "💬", "😁", "😎", "😍","🍀", "🍀", "🍀", "🎸", "🎸"]
        super().__init__()

    @staticmethod
    def __format_duration(duration: Optional[float]) -> str:
        return (
            time.strftime("%H:%M:%S", time.gmtime(duration))
            if duration != "LIVE"
            else duration
        )

    @discordSuperUtils.CogManager.event(discordSuperUtils.MusicManager)
    async def on_music_error(self, ctx, error):
        errors = {
            discordSuperUtils.NotPlaying: "I Don't Play Any Music!",
            discordSuperUtils.NotConnected: "I Haven't Joined The Voice Channel Yet!",
            discordSuperUtils.NotPaused: "The Currently Playing Player Is Not Paused!",
            discordSuperUtils.QueueEmpty: "The Queue Is Empty!",
            discordSuperUtils.AlreadyConnected: "I Already Connected To A Voice Channel!",
            discordSuperUtils.QueueError: "There Has Been A Queue Error!",
            # discordSuperUtils.SkipError: "There Is No Song To skip To!",
            discordSuperUtils.UserNotConnected: "User Is Not Connected To A Voice channel!",
            # discordSuperUtils.InvalidSkipIndex: "That Skip Index Is Invalid!",
        }
        fill = ' '
        emd = embed(color=color.red())
        for error_type, response in errors.items():
            if isinstance(error, error_type):
                emd.description =f"<:blobcoin:975289040997851206> {fill}{fill}**{response}**" 
                await ctx.reply(embed=emd, delete_after=10)
                return

        print("unexpected err")
        raise error

    @discordSuperUtils.CogManager.event(discordSuperUtils.MusicManager)
    async def on_queue_end(self, ctx): 
        print(f"The queue has ended in {ctx}")
        fill = ' '
        emd = embed(description=f"<:blobcoin:975289040997851206> {fill}{fill}**Queue Has Ended**",color=color.random())
        message = await ctx.send(embed=emd)
        await message.add_reaction("<a:tick:908666945971298375>")

        # You could wait and check activity, etc...


    @discordSuperUtils.CogManager.event(discordSuperUtils.MusicManager)
    async def on_inactivity_disconnect(self, ctx):
        print(f"I have left {ctx} due to inactivity..")
        fill = ' '
        emd = embed(description=f"**<:blobcoin:975289040997851206> {fill}{fill}Left Voice Channel Due To Inactivity**",color=color.random())
        message = await ctx.reply(embed=emd, delete_after=10)
        await message.add_reaction("<a:tick:908666945971298375>")


    @discordSuperUtils.CogManager.event(discordSuperUtils.MusicManager)
    async def on_play(self, ctx, player):
        async with ctx.typing():
            thumbnail = player.data["videoDetails"]["thumbnail"]["thumbnails"][-1]["url"]
            requester = player.requester.mention if player.requester else "Autoplay"
            idmember = ctx.author.id
            volume = 100
            await self.MusicManager.volume(ctx, volume)
            fill = ' '
            emds = embed(title=f"🎶  **Playing**", description=f"<a:music:995863530282680441> {fill} **[{player}]({player.url})**", color=color.random())
            emds.add_field(name=f"<:discord:908666046339248189> Requested by", value=f"<:reply1:996220355842674769>{requester}", inline=True)
            emds.add_field(name=f"<a:time1:933374453583323187> Duration", value=f"<:reply1:996220355842674769>`{self.__format_duration(player.duration)}`", inline=True)
            emds.add_field(name=f"\u200b", value="\u200b", inline=True)
            emds.set_thumbnail(url=thumbnail)
            emds.set_footer(text=f'{random.choice(self.emoji)}')
            emds.timestamp = datetime.datetime.now(pytz.utc)
            message = await ctx.send(embed=emds)
            await message.add_reaction("🎸")


    @commands.command()
    async def help(self, ctx):
        async with ctx.typing():
            fill = ' '
            # 
            emd = embed(color=color.random())
            emd.set_thumbnail(url="https://cdn.discordapp.com/attachments/990996729832816780/996212129738788974/home-hero1.png")
            emd.add_field(name=f"> **RICKTIFY COMMANDS** {fill}<:verified:974945295404265482>", value="\u200b", inline=False)
            emd.add_field(name=f"**> •「 <a:discord:970864400107970600> {fill}INFO 」**",value=f"\n> **PREFIX** = `r!`, `R!`\n> Remove brackets when typing commands `<  >`\n> **Top.gg : [Vote Me](https://top.gg/bot/878538776564088832) {fill}<a:BongoCat:974575938920644628>**", inline=False)
            emd.add_field(name=f"**\n> •「 <a:play:974961954395402240> {fill}MUSIC 」**\n", value="\n> `r!join`, `r!leave`, `r!dc`\n> `r!play <music>`, `r!p <music>`\n> `r!skip <order/none>`, `r!pause`, `r!resume`\n> `r!stop`, `r!shuffle`, `r!nowplaying`, `r!np`\n> `r!remove <order>`, `r!rm <order>`\n> `r!loop`, `r!loopstatus`, `r!ls`\n> `r!queue`, `r!q`, `r!queueloop`, `r!ql`\n> `r!volume <number>`, `r!vol <number>`", inline=True)
            emd.add_field(name=f"**\n> •「 <a:Nitro:974575275050418176> {fill}OTHER 」**\n", value="\n> `r!invite`, `r!ping`, `r!stats`", inline=False)
            emd.set_footer(text=f'{random.choice(self.emoji)}')
            emd.set_image(url="https://cdn.discordapp.com/attachments/990996729832816780/992390539582382090/RICKTIFY61.png")
            emd.timestamp = datetime.datetime.now(pytz.utc)
            await ctx.reply(embed=emd) 

    @commands.command()
    async def invite(self, ctx):
        async with ctx.typing():
            fill = ' '
            emd = embed(color=color.random())
            emd.add_field(name=f"<:DiscordPartner:974609668200599603> {fill}Invite Ricktify", value="<:reply1:996220355842674769>**[Click Here!](https://discord.com/api/oauth2/authorize?client_id=878538776564088832&permissions=412353912129&scope=bot)**", inline=True)
            emd.add_field(name=f"<:topgg:987994558686171147> {fill}Vote Ricktify", value=f"<:reply1:996220355842674769>**[Vote Me!](https://top.gg/bot/878538776564088832/vote)**", inline=True)
            emd.set_footer(text=f'{random.choice(self.emoji)}')
            emd.timestamp = datetime.datetime.now(pytz.utc)
            await ctx.reply(embed= emd)

    @commands.command()
    async def ping(self, ctx):
        # async def ping(ctx):
        async with ctx.typing():
            # before = monotonic()
            # message = await ctx.send("Pong!")
            ping = round(self.bot.latency * 1000)
            fill = ' '
            if ping < 250:
                emd = embed(description=f"<a:up:994556060046204939> {fill}Pong! `{ping}ms`", color=color.random())
            else:
                emd = embed(description=f"<a:down:994555989938425856> {fill}Pong! `{ping}ms`", color=color.random())
            await ctx.reply(embed = emd)

    @commands.command(aliases=["dc", "DC"])
    async def leave(self, ctx):
        voicetrue = ctx.author.voice
        if voicetrue is None:
            fill = ' '
            emd = embed(description=f"<:blobcoin:975289040997851206> {fill}{fill}**You Are Not Connected to Voice Channel**", color=color.random())
            return await ctx.reply(embed=emd, delete_after=10)

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                fill = ' '
                emd = embed(description=f"<:blobcoin:975289040997851206> {fill}{fill}**You Are Not Connected To The Same Voice Channel**", color=color.random())
                return await ctx.send(embed=emd, delete_after=10)

        if channel := await self.MusicManager.leave(ctx):
            # await ctx.send("Left Voice Channel")
            async with ctx.typing():
                fill = ' '
                emd = embed(description=f"<:IconStatusWebDND:908667642095763466> {fill}**Disconnected** {fill}<#{channel.id}>", color=color.random())
                message = await ctx.send(embed=emd)
                await message.add_reaction("<a:tick:908666945971298375>")


    @commands.command(aliases=["nowplaying", "NP"])
    async def np(self, ctx):

        voicetrue = ctx.author.voice
        if voicetrue is None:
            fill = ' '
            emd = embed(description=f"<:blobcoin:975289040997851206> {fill}{fill}**You Are Not Connected to Voice Channel**", color=color.random())
            return await ctx.reply(embed=emd, delete_after=10)

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                fill = ' '
                emd = embed(description=f"<:blobcoin:975289040997851206> {fill}{fill}**You Are Not Connected To The Same Voice Channel**", color=color.random())
                return await ctx.send(embed=emd, delete_after=10)

        async with ctx.typing():
            if player := await self.MusicManager.now_playing(ctx):
                duration_played = await self.MusicManager.get_player_played_duration(ctx, player)
                
                # Loop status
                loop = (await self.MusicManager.get_queue(ctx)).loop
                if loop == discordSuperUtils.Loops.LOOP:
                    loop_status = "Looping enabled."
                elif loop == discordSuperUtils.Loops.QUEUE_LOOP:
                    loop_status = "Queue looping enabled."
                else:
                    loop_status = "Looping disabled."

                # Fecthing other details
                thumbnail = player.data["videoDetails"]["thumbnail"]["thumbnails"][-1]["url"]
                requester = player.requester.mention if player.requester else "Autoplay"
                idmember = ctx.author.id
                fill = ' '
                emds = embed(title=f"🎶  **Now Playing**", description=f"<a:music:995863530282680441> {fill} **[{player}]({player.url})**", color=color.random())
                emds.add_field(name=f"<:discord:908666046339248189> Requested by", value=f"<:reply1:996220355842674769>{requester}", inline=True)
                emds.add_field(name="<a:loop:990448508953853993> Looping", value=f"<:reply1:996220355842674769>**{loop_status}**", inline=True)
                emds.add_field(name=f"<a:time1:933374453583323187> Duration", value=f"<:reply1:996220355842674769>`{self.__format_duration(duration_played)}` **>** `{self.__format_duration(player.duration)}` ", inline=False)
                emds.set_thumbnail(url=thumbnail)
                emds.set_footer(text=f'{random.choice(self.emoji)}')
                emds.timestamp = datetime.datetime.now(pytz.utc)
                message = await ctx.send(embed=emds)
                await message.add_reaction("🎸")

    @commands.command()
    async def join(self, ctx):
        
        voicetrue = ctx.author.voice
        if voicetrue is None:
            fill = ' '
            emd = embed(description=f"<:blobcoin:975289040997851206> {fill}{fill}**You Are Not Connected to Voice Channel**", color=color.random())
            return await ctx.reply(embed=emd, delete_after=10)

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                fill = ' '
                emd = embed(description=f"<:blobcoin:975289040997851206> {fill}{fill}**You Are Not Connected To The Same Voice Channel**", color=color.random())
                return await ctx.send(embed=emd, delete_after=10)

        if channel := await self.MusicManager.join(ctx):
            # await ctx.send("Joined Voice Channel")
            async with ctx.typing():
                fill = ' '
                emd = embed(description=f"<:IconStatusWebOnline:908667544041291797> {fill}**Connected** <#{channel.id}>", color=color.random())
                message = await ctx.send(embed=emd)
                await message.add_reaction("<a:tick:908666945971298375>")

    @commands.command(aliases=["p", "P"])
    async def play(self, ctx, *, query: str):

        voicetrue = ctx.author.voice
        if voicetrue is None:
            fill = ' '
            emd = embed(description=f"<:blobcoin:975289040997851206> {fill}{fill}**You Are Not Connected to Voice Channel**", color=color.random())
            return await ctx.send(embed=emd, delete_after=10)

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                fill = ' '
                emd = embed(description=f"<:blobcoin:975289040997851206> {fill}{fill}**You Are Not Connected To The Same Voice Channel**", color=color.random())
                return await ctx.send(embed=emd, delete_after=10)

        if not ctx.voice_client or not ctx.voice_client.is_connected():
            await self.MusicManager.join(ctx)

        async with ctx.typing():
            player = await self.MusicManager.create_player(query, ctx.author)

        if player:
            if await self.MusicManager.queue_add(players=player, ctx=ctx) and not await self.MusicManager.play(ctx):
                fill = ' '
                thumbnail = player[0].data["videoDetails"]["thumbnail"]["thumbnails"][-1]["url"]
                emd = embed(title=f"<:hydroxadd:908668072422940703> {fill}**Added to queue**",description=f"<a:music:995863530282680441> {fill} **[{player[0].title}]({player[0].url})**", color=color.random())
                emd.set_footer(text=f'{random.choice(self.emoji)}')
                emd.timestamp = datetime.datetime.now(pytz.utc)
                idmember = ctx.author.id
                emd.add_field(name=f"<:discord:908666046339248189> {fill}Requested by", value=f"<:reply1:996220355842674769><@{idmember}>", inline=True)
                emd.set_thumbnail(url=thumbnail)
                message = await ctx.send(embed=emd)
                await message.add_reaction("<:hydroxadd:908668072422940703>")
            
        else:
            fill = ' '
            emds = embed(description=f"**<:blobcoin:975289040997851206> {fill}{fill}Query not found.**", color=color.red())
            message = await ctx.reply(embed=emds, delete_after=10)
            await message.add_reaction("<:blobcoin:975289040997851206>")


    @commands.command()
    async def lyrics(self, ctx, query: str = None):
        voicetrue = ctx.author.voice
        if voicetrue is None:
            fill = ' '
            emd = embed(description=f"<:blobcoin:975289040997851206> {fill}{fill}**You Are Not Connected to Voice Channel**", color=color.random())
            return await ctx.send(embed=emd, delete_after=10)

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                fill = ' '
                emd = embed(description=f"<:blobcoin:975289040997851206> {fill}{fill}**You Are Not Connected To The Same Voice Channel**", color=color.random())
                return await ctx.send(embed=emd, delete_after=10)

        if response := await self.MusicManager.lyrics(ctx, query):
            title, author, query_lyrics = response
            splitted = query_lyrics.split("\n")
            res = []
            current = ""
            for i, split in enumerate(splitted):
                if len(splitted) <= i + 1 or len(current) + len(splitted[i + 1]) > 1024:
                    res.append(current)
                    current = ""
                    continue
                current += split + "\n"
            
            fill = ' '
            embeds = [
                    discord.Embed(
                        # title=f"Lyrics for '{title}' by '{author}', (Page {i + 1}/{len(res)})",
                        title=f"<a:music:995863530282680441> {fill}{title} by {author}",
                        description=x,
                        color=color.random(),
                    ).add_field(name="Page", value=f"**{i + 1}/{len(res)}**", inline=False).set_footer(
                    text=f"{random.choice(self.emoji)}")
                    for i, x in enumerate(res)
            ]

            for embed in embeds:
                embed.timestamp = datetime.datetime.now(pytz.utc)

            page_manager = discordSuperUtils.PageManager(
                ctx,
                embeds,
                public=True,
                timeout=1000,
            )
            await page_manager.run()
        else:
                    # await ctx.send("No lyrics found.")
            fill = ' '
            emds = discord.Embed(description=f"**<:blobcoin:975289040997851206> {fill}{fill}No Lyrics Found**", color=color.red())
                # emds.set_footer(text=f"Requested by: {ctx.author.name}", icon_url=ctx.author.avatar_url)
            message = await ctx.reply(embed=emds, delete_after=10)
            await message.add_reaction("<:blobcoin:975289040997851206>")

    @commands.command()
    async def pause(self, ctx):
        voicetrue = ctx.author.voice
        if voicetrue is None:
            fill = ' '
            emd = embed(description=f"<:blobcoin:975289040997851206> {fill}{fill}**You Are Not Connected to Voice Channel**", color=color.random())
            return await ctx.reply(embed=emd)

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                fill = ' '
                emd = embed(description=f"<:blobcoin:975289040997851206> {fill}{fill}**You Are Not Connected To The Same Voice Channel**", color=color.random())
                return await ctx.send(embed=emd, delete_after=10)

        if await self.MusicManager.pause(ctx):
            # await ctx.send("Player paused.")
            emd = embed(title="🎶  **Paused**", color=color.random())
            idmember = ctx.author.id
            fill = ' '
            emd.set_footer(text=f'{random.choice(self.emoji)}')
            emd.timestamp = datetime.datetime.now(pytz.utc)
            emd.add_field(name=f"<:discord:908666046339248189> {fill}Requested by", value=f"<:reply1:996220355842674769><@{idmember}>", inline=True)
            message = await ctx.send(embed=emd)
            await message.add_reaction("⏸️")


    @commands.command()
    async def resume(self, ctx):
        voicetrue = ctx.author.voice
        if voicetrue is None:
            fill = ' '
            emd = embed(description=f"<:blobcoin:975289040997851206> {fill}{fill}**You Are Not Connected to Voice Channel**", color=color.random())
            return await ctx.reply(embed=emd, delete_after=10)

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                fill = ' '
                emd = embed(description=f"<:blobcoin:975289040997851206> {fill}{fill}**You Are Not Connected To The Same Voice Channel**", color=color.random())
                return await ctx.send(embed=emd, delete_after=10)

        if await self.MusicManager.resume(ctx):
            # await ctx.send("Player resumed.")
            emd = embed(title=f"🎶  **Resumed**", color=color.random())
            idmember = ctx.author.id
            fill = ' '
            emd.set_footer(text=f'{random.choice(self.emoji)}')
            emd.timestamp = datetime.datetime.now(pytz.utc)
            emd.add_field(name=f"<:discord:908666046339248189> {fill}Requested by", value=f"<:reply1:996220355842674769><@{idmember}>", inline=True)
            message = await ctx.send(embed=emd)
            await message.add_reaction("▶️")

    @commands.command(aliases=["vol", "VOL"])
    async def volume(self, ctx, volume: int):
        voicetrue = ctx.author.voice
        if voicetrue is None:
            fill = ' '
            emd = embed(description=f"<:blobcoin:975289040997851206> {fill}{fill}**You Are Not Connected to Voice Channel**", color=color.random())
            return await ctx.reply(embed=emd, delete_after=10)

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                fill = ' '
                emd = embed(description=f"<:blobcoin:975289040997851206> {fill}{fill}**You Are Not Connected To The Same Voice Channel**", color=color.random())
                return await ctx.send(embed=emd, delete_after=10)

        fill = ' '
        if volume >= 150 and volume <= 200:
            await self.MusicManager.volume(ctx, volume)
            emd = embed(title=f"🎶  **Volume High {volume}%**", color=color.random())
            idmember = ctx.author.id
            emd.set_footer(text=f'{random.choice(self.emoji)}')
            emd.timestamp = datetime.datetime.now(pytz.utc)
            emd.add_field(name=f"<:discord:908666046339248189> {fill}Requested by", value=f"<:reply1:996220355842674769><@{idmember}>", inline=True)
            message = await ctx.send(embed=emd)
            await message.add_reaction("🔊")
            
        elif volume >= 80 and volume <= 150:
            await self.MusicManager.volume(ctx, volume)
            emd = embed(title=f"🎶  **Volume Medium {volume}%**", color=color.random())
            idmember = ctx.author.id
            emd.set_footer(text=f'{random.choice(self.emoji)}')
            emd.timestamp = datetime.datetime.now(pytz.utc)
            emd.add_field(name=f"<:discord:908666046339248189> {fill}Requested by", value=f"<:reply1:996220355842674769><@{idmember}>", inline=True)
            message = await ctx.send(embed=emd)
            await message.add_reaction("🔉")
        else :
            await self.MusicManager.volume(ctx, volume)
            emd = embed(title=f"🎶  **Volume Low {volume}%** ", color=color.random())
            idmember = ctx.author.id
            emd.set_footer(text=f'{random.choice(self.emoji)}')
            emd.timestamp = datetime.datetime.now(pytz.utc)
            emd.add_field(name=f"<:discord:908666046339248189> {fill}Requested by", value=f"<:reply1:996220355842674769><@{idmember}>", inline=True)
            message = await ctx.send(embed=emd)
            await message.add_reaction("🔈")



    @commands.command()
    async def loop(self, ctx):
        voicetrue = ctx.author.voice
        if voicetrue is None:
            fill = ' '
            emd = embed(description=f"<:blobcoin:975289040997851206> {fill}{fill}**You Are Not Connected to Voice Channel**", color=color.random())
            return await ctx.reply(embed=emd, delete_after=10)

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                fill = ' '
                emd = embed(description=f"<:blobcoin:975289040997851206> {fill}{fill}**You Are Not Connected To The Same Voice Channel**", color=color.random())
                return await ctx.send(embed=emd, delete_after=10)

        is_loop = await self.MusicManager.loop(ctx)
        fill = ' '
        if is_loop is not None:
            # await ctx.send(f"Looping toggled to {is_loop}")
            emd = embed(title=f"🎶  **Looping {is_loop}**", color=color.random())
            idmember = ctx.author.id
            emd.set_footer(text=f'{random.choice(self.emoji)}')
            emd.timestamp = datetime.datetime.now(pytz.utc)
            emd.add_field(name=f"<:discord:908666046339248189> {fill}Requested by", value=f"<:reply1:996220355842674769><@{idmember}>", inline=True)
            message = await ctx.send(embed=emd)
            await message.add_reaction("🔂")

    @commands.command(aliases=["ql", "QL"])
    async def queueloop(self, ctx):
        voicetrue = ctx.author.voice
        if voicetrue is None:
            fill = ' '
            emd = embed(description=f"<:blobcoin:975289040997851206> {fill}{fill}**You Are Not Connected to Voice Channel**", color=color.random())
            return await ctx.reply(embed=emd, delete_after=10)

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                fill = ' '
                emd = embed(description=f"<:blobcoin:975289040997851206> {fill}{fill}**You Are Not Connected To The Same Voice Channel**", color=color.random())
                return await ctx.send(embed=emd, delete_after=10)

        fill = ' '
        is_loop = await self.MusicManager.queueloop(ctx)
        if is_loop is not None:
            # await ctx.send(f"Queue looping toggled to {is_loop}")
            emd = embed(title=f"🎶  **Queue looping {is_loop}**", color=color.random())
            idmember = ctx.author.id
            emd.set_footer(text=f'{random.choice(self.emoji)}')
            emd.timestamp = datetime.datetime.now(pytz.utc)
            emd.add_field(name=f"<:discord:908666046339248189> {fill}Requested by", value=f"<:reply1:996220355842674769><@{idmember}>", inline=True)
            msg = await ctx.send(embed=emd) 
            await msg.add_reaction("🔁")

    @commands.command(aliases=["rm", "RM"])
    async def remove(self, ctx, index: int):
        voicetrue = ctx.author.voice
        if voicetrue is None:
            fill = ' '
            emd = embed(description=f"<:blobcoin:975289040997851206> {fill}{fill}**You Are Not Connected to Voice Channel**", color=color.random())
            return await ctx.reply(embed=emd, delete_after=10)

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                fill = ' '
                emd = embed(description=f"<:blobcoin:975289040997851206> {fill}{fill}**You Are Not Connected To The Same Voice Channel**", color=color.random())
                return await ctx.send(embed=emd, delete_after=10)

        if player := await self.MusicManager.queue_remove(ctx=ctx, index=index):
            fill = ' '
            emd = embed(title="🎶  **Remove**", description=f"<a:music:995863530282680441> {fill}**[{player}]({player.url})**", color=color.random())
            idmember = ctx.author.id
            thumbnail = player.data["videoDetails"]["thumbnail"]["thumbnails"][-1]["url"]
            emd.set_footer(text=f'{random.choice(self.emoji)}')
            emd.timestamp = datetime.datetime.now(pytz.utc)
            emd.add_field(name=f"<:discord:908666046339248189> {fill}Requested by", value=f"<:reply1:996220355842674769><@{idmember}>", inline=True)
            emd.set_thumbnail(url=thumbnail)
            message = await ctx.send(embed=emd) 
            await message.add_reaction("🗑️")

    @commands.command()
    async def shuffle(self, ctx):
        voicetrue = ctx.author.voice
        if voicetrue is None:
            fill = ' '
            emd = embed(description=f"<:blobcoin:975289040997851206> {fill}{fill}**You Are Not Connected to Voice Channel**", color=color.random())
            return await ctx.reply(embed=emd, delete_after=10)

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                fill = ' '
                emd = embed(description=f"<:blobcoin:975289040997851206> {fill}{fill}**You Are Not Connected To The Same Voice Channel**", color=color.random())
                return await ctx.send(embed=emd, delete_after=10)

        is_shuffle = await self.MusicManager.shuffle(ctx)
        if is_shuffle is not None:
                # await ctx.send(f"Shuffle toggled to {is_shuffle}")
            emd = embed(title=f"🎶  **Shuffle {is_shuffle}**", color=color.random())
            idmember = ctx.author.id
            fill = ' '
            emd.set_footer(text=f'{random.choice(self.emoji)}')
            emd.timestamp = datetime.datetime.now(pytz.utc)
            emd.add_field(name=f"<:discord:908666046339248189> {fill}Requested by", value=f"<:reply1:996220355842674769><@{idmember}>", inline=True)
            msg = await ctx.send(embed=emd) 
            await msg.add_reaction("🔀")

    @commands.command()
    async def skip(self, ctx, index: int = None):
        voicetrue = ctx.author.voice
        

        try:
            if voicetrue is None:
                fill = ' '
                emd = embed(description=f"<:blobcoin:975289040997851206> {fill}{fill}**You Are Not Connected to Voice Channel**", color=color.random())
                return await ctx.reply(embed=emd, delete_after=10)

                if ctx.voice_client:
                    if ctx.voice_client.channel != ctx.author.voice.channel:
                        fill = ' '
                        emd = embed(description=f"<:blobcoin:975289040997851206> {fill}{fill}**You Are Not Connected To The Same Voice Channel**", color=color.random())
                        return await ctx.send(embed=emd, delete_after=10)

            if await self.MusicManager.skip(ctx, index):
                emd = embed(title=f"🎶  **Skipp**", color=color.random())
                idmember = ctx.author.id
                emd.set_footer(text=f'{random.choice(self.emoji)}')
                emd.timestamp = datetime.datetime.now(pytz.utc)
                fill = ' '
                emd.add_field(name=f"<:discord:908666046339248189> {fill}Requested by", value=f"<:reply1:996220355842674769><@{idmember}>", inline=True)
                msg =  await ctx.send(embed=emd)
                await msg.add_reaction("⏭️")

        except:
        # if not await MusicManager.skip(ctx, index):
            emdr = embed(description="🎶  **No song to skip to.**", color=color.random())
            await ctx.send(embed=emdr)
            time.sleep(0.3)
            ctx.voice_client.stop()
            emd = embed(title="🎶  **Stop**", color=color.random())
            idmember = ctx.author.id
            fill = ' '
            emd.set_footer(text=f'{random.choice(self.emoji)}')
            emd.timestamp = datetime.datetime.now(pytz.utc)
            emd.add_field(name=f"<:discord:908666046339248189> {fill}Requested by", value=f"<:reply1:996220355842674769><@{idmember}>", inline=True)
            msg =  await ctx.send(embed=emd)
            await msg.add_reaction("⏹️")


    @commands.command()
    async def stop(self, ctx):
        voicetrue = ctx.author.voice
        if voicetrue is None:
            fill = ' '
            emd = embed(description=f"<:blobcoin:975289040997851206> {fill}{fill}**You Are Not Connected to Voice Channel**", color=color.random())
            return await ctx.reply(embed=emd, delete_after=10)

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                fill = ' '
                emd = embed(description=f"<:blobcoin:975289040997851206> {fill}{fill}**You Are Not Connected To The Same Voice Channel**", color=color.random())
                return await ctx.send(embed=emd, delete_after=10)

        if ctx.voice_client.is_playing() is True:
            await self.MusicManager.cleanup(voice_client=None, guild=ctx.guild)
            ctx.voice_client.stop()
            emd = embed(title="🎶  **Stop**", color=color.random())
            idmember = ctx.author.id
            fill = ' '
            emd.set_footer(text=f'{random.choice(self.emoji)}')
            emd.timestamp = datetime.datetime.now(pytz.utc)
            emd.add_field(name=f"<:discord:908666046339248189>{fill}Requested by", value=f"<:reply1:996220355842674769><@{idmember}>", inline=True)
            msg =  await ctx.send(embed=emd)
            await msg.add_reaction("⏹️")
        
        else:
            emdr = embed(description="🎶  **No song to stop to.**", color=color.random())
            await ctx.send(embed=emdr)
            time.sleep(0.3)

            if channel := await self.MusicManager.leave(ctx):
            # await ctx.send("Left Voice Channel")
                fill = ' '
                emd = embed(description=f"<:IconStatusWebDND:908667642095763466> {fill}**Disconnected** {fill}<#{channel.id}>", color=color.random())
                message = await ctx.send(embed=emd)
                await message.add_reaction("<a:tick:908666945971298375>")

          


    @commands.command(aliases=["q", "Q"])
    async def queue(self, ctx):
        voicetrue = ctx.author.voice
        if voicetrue is None:
            fill = ' '
            emd = embed(description=f"<:blobcoin:975289040997851206> {fill}{fill}**You Are Not Connected to Voice Channel**", color=color.random())
            return await ctx.reply(embed=emd, delete_after=10)

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                fill = ' '
                emd = embed(description=f"<:blobcoin:975289040997851206> {fill}{fill}**You Are Not Connected To The Same Voice Channel**", color=color.random())
                return await ctx.send(embed=emd, delete_after=10)

        if ctx_queue := await self.MusicManager.get_queue(ctx):

            formatted_queue = [
                # f"`{x.title}` **>** {x.requester and x.requester.mention}"
                f"{x.title} **>** {x.requester and x.requester.mention}"
                for x in ctx_queue.queue[ctx_queue.pos + 1 :]
            ]

            player = await self.MusicManager.now_playing(ctx)
            uploader = player.data["videoDetails"]["author"]
            thumbnail = player.data["videoDetails"]["thumbnail"]["thumbnails"][-1]["url"]
            requestera = player.requester.mention if player.requester else "Autoplay"

            fill = ' '
            embeds = discordSuperUtils.generate_embeds(
                formatted_queue,
                "🎶 **Queue** -",
                f"<a:music:995863530282680441> {fill}**Now Playing**\t: **[{player.title}]({player.url}) > **{requestera}",
                6,
                string_format="{}",
            )
                

            # embeds.
            embeds[0].set_thumbnail(url=thumbnail)
            for embed in embeds:
                embed.timestamp = datetime.datetime.now(pytz.utc)

            page_manager = discordSuperUtils.PageManager(ctx, embeds, public=True, timeout=1000)
            await page_manager.run()

    @commands.command(aliases=["loopstatus", "LS"])
    async def ls(self, ctx):
        voicetrue = ctx.author.voice
        if voicetrue is None:
            fill = ' '
            emd = embed(title=f"<:blobcoin:975289040997851206> {fill}{fill}**You Are Not Connected to Voice Channel**", color=color.random())
            return await ctx.reply(embed=emd, delete_after=10)

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                fill = ' '
                emd = embed(description=f"<:blobcoin:975289040997851206> {fill}{fill}**You Are Not Connected To The Same Voice Channel**", color=color.random())
                return await ctx.send(embed=emd, delete_after=10)

        if queue := await self.MusicManager.get_queue(ctx):
            loop = queue.loop
            loop_status = None

            if loop == discordSuperUtils.Loops.LOOP:
                loop_status = "Looping enabled."

            elif loop == discordSuperUtils.Loops.QUEUE_LOOP:
                loop_status = "Queue looping enabled."

            elif loop == discordSuperUtils.Loops.NO_LOOP:
                loop_status = "No loop enabled."

            if loop_status:
                # await ctx.send(loop_status)
                emd = embed(title=f"🎶  {loop_status}", color=color.random())
                idmember = ctx.author.id
                fill = ' '
                emd.set_footer(text=f'{random.choice(self.emoji)}')
                emd.timestamp = datetime.datetime.now(pytz.utc)
                emd.add_field(name=f"<:discord:908666046339248189> {fill}Requested by", value=f"<:reply1:996220355842674769><@{idmember}>", inline=True)     
                message = await ctx.send(embed=emd)
                await message.add_reaction("🔁")

async def setup(bot):
    await bot.add_cog(Music(bot))