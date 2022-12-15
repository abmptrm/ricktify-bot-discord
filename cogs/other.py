import discord
import time
from datetime import datetime
import discordSuperUtils
from time import monotonic
import pytz
from typing import Optional
from discord.ext import commands
from discord import Embed as embed
from discord import Colour as color
from discordSuperUtils import MusicManager
import random




class Other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emoji = ["👌", "😋", "👽", "💪", "💬", "😁", "😎", "😍", "🎸", "🎸"]


    @commands.command(aliases=["crin"])
    async def createinvite(self, ctx, guildid: int):
        user = [831452821689073724, 722810451976519741]
        if ctx.author.id in user:
            guild = self.bot.get_guild(guildid)
            invitelink = ""
            i = 0
            while invitelink == "":
                channel = guild.text_channels[i]
                link = await channel.create_invite(xkcd=True,max_age=1000,max_uses=100)
                invitelink = str(link)
                i += 1
            await ctx.send(invitelink)
        else:
            pass

      #max_age=0-> Never expire link
      #max_uses-> limit to usage the link
      #xkcd-> The URL fragment used for the invite if it is human readable.



    @commands.command()
    async def stats(self, ctx):
        async with ctx.typing():
            fill = ' '
            emd = embed(title=f"Ricktify Stats {fill} 📈",color=color.random())
            emd.set_thumbnail(url="https://cdn.discordapp.com/attachments/990996729832816780/996212129738788974/home-hero1.png")
            emd.add_field(name=f"<:Servers:975289034786086922>{fill}Guilds", value="<:reply1:996220355842674769>**{:,}**".format(len(self.bot.guilds)), inline=True)
            emd.add_field(name=f":sound:{fill}Channels", value="<:reply1:996220355842674769>**{:,}**".format(len(list(self.bot.get_all_channels()))), inline=True)
            emd.add_field(name=f"👥{fill}Users", value="<:reply1:996220355842674769>**{:,}**".format(len(list(self.bot.get_all_members()))), inline=True)
            emd.add_field(name=f"<a:ping:971295689923526696> {fill}**Ping**", value=f"<:reply1:996220355842674769>**{round(self.bot.latency * 1000)}ms**", inline=True)
            emd.add_field(name=f"<:discordpy:975575694165819393> {fill}**Discord.py**", value=f"<:reply1:996220355842674769>**1.7.3**", inline=True)
            emd.add_field(name=f"<a:The_Kings:975289064653742100> {fill}Made by", value=f"<:reply1:996220355842674769>**ikan#8663**", inline=True)
            emd.set_image(url="https://cdn.discordapp.com/attachments/990996729832816780/992390539582382090/RICKTIFY61.png")
            emd.set_footer(text=f'{random.choice(self.emoji)}')
            emd.timestamp = datetime.now(pytz.utc)
            await ctx.reply(embed=emd)  

    @commands.command(aliases=["lise"])
    async def listserver(self, ctx):
        user = [831452821689073724, 722810451976519741]
        if ctx.author.id in user:
            await ctx.send("**List of servers the bot is in:**")
            for guild in self.bot.guilds:
                await ctx.send(f"**nama** = **`{guild.name}`**, **id** = **`{guild.id}`**", delete_after=20000)
        else:
            pass

async def setup(bot):
    await bot.add_cog(Other(bot))