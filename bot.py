# from discord.ext import commands
import os
import discord
import asyncio
from discord.ext import commands
from discord import Embed as embed
from discord import Colour as color

token = "token here"	

class MyBot(commands.Bot):
    def __init__(self):
    	self.PREFIX = ["r!", "R!"]
    	intents = discord.Intents.all()
    	intents.members = True
    	super().__init__(
    		command_prefix = self.PREFIX, help_command=None, intents=intents
    	)

    async def setup_hook(self):
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    await bot.load_extension(f'cogs.{filename[:-3]}')
                    print(f"[Cogs] {filename} loaded")
                except Exception as e:
                    print(f"[Error] {e}")


    async def close(self):
        await super().close()

bot = MyBot()
bot.run(token)


	
		


