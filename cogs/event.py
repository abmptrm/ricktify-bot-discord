import re
import discord
from discord import channel
from discord import user
from discord import Embed as embed
from discord import Colour as color
from discord.ext import commands
import pytz
import datetime
import random
from discord.utils import get
from platform import *


class Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # self.on_readyid = 982850933958516812
        self.on_guild_joins = 982850933958516813
        self.on_commands = 982851097578340372
        # self.bot_version = '1.0.0'
        self.logger = 982851136904134720
        self.emoji = ["👌", "😋", "👽", "💪", "💬", "😁", "😎", "😍","🍀", "🍀", "🍀", "🎸", "🎸"]

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{str(self.bot.user)} is ready.")
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,name=f"r!help {random.choice(self.emoji)} :3"))

        ch = [922056508085260299, 982850933958516809]
        for i in ch:
            channel = self.bot.get_channel(i)
            fill = ' '
            await channel.send(f"📡 <@878538776564088832> **Online**")
        return

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.author == self.bot.user:
            return

        if f'<@878538776564088832>' in message.content:
            print(message.content)
            emd = embed(title="My prefix is `r! , R!`", color=color.random())
            emd.set_footer(text=f'{random.choice(self.emoji)}')
            emd.timestamp = datetime.datetime.now(pytz.utc)
            await message.channel.send(embed=emd)
            return

    @commands.Cog.listener()
    async def on_command(self, ctx):
        channel = self.bot.get_channel(self.on_commands)
        channel1 = self.bot.get_channel(self.logger)
        embed = discord.Embed(
            title=f"{ctx.author} used a command!",
            description=f'**Information :**\n```cs\nauthor : {ctx.author}\nguild : {ctx.guild.name}\nchannel : {ctx.message.channel.name}\ncontent : {ctx.message.content}```**Id :**\n```cs\nauthor : {ctx.author.id}\nguild : {ctx.guild.id}\nchannel : {ctx.message.channel.id}```',
            color=ctx.author.colour,
            timestamp=ctx.message.created_at
        )
        await channel.send("––––––––––––––––––––––––––––––––––––––––––––––––", embed=embed)
        await channel1.send("––––––––––––––––––––––––––––––––––––––––––––––––", embed=embed)
        return

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        channel = self.bot.get_channel(self.on_commands)
        channel1 = self.bot.get_channel(self.logger)
        embed = discord.Embed(
            title=f"Completed {ctx.author}'s command!",
            description=f'**Information :**\n```cs\nauthor : {ctx.author}\nguild : {ctx.guild.name}\nchannel : {ctx.message.channel.name}\ncontent : {ctx.message.content}```**Id :**\n```cs\nauthor : {ctx.author.id}\nguild : {ctx.guild.id}\nchannel : {ctx.message.channel.id}```',
            color=ctx.author.colour,
            timestamp=ctx.message.created_at
        )
        await channel.send(embed=embed)
        await channel1.send(embed=embed)
        return

    @commands.Cog.listener()
    async def on_guild_join(self, ctx):
        channel_log = self.bot.get_channel(self.on_guild_joins)
        await channel_log.send('**Bot has been added to a new server**')
        await channel_log.send('**List of servers the bot is in: **')

        for guild in self.bot.guilds:
            await channel_log.send(f"nama = **{guild.name}**, id = **{guild.id}**", delete_after=72000000)
        return


async def setup(bot):
    await bot.add_cog(Event(bot))