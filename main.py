from discord.ext import commands
from discord import Game
from discord import Status
import discord

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='!',
            intents=discord.Intents.all(),
            sync_command=True,
            application_id=""
        )
        self.initial_extension = [
            "command.file1",
        ]

    async def setup_hook(self):
        for ext in self.initial_extension:
            await self.load_extension(ext)
        await bot.tree.sync()
        #await bot.tree.sync(guild=Object(id=))


    async def on_ready(self):
        print("login")
        print("BOT_Name",self.user.name)
        print("BOT_id",self.user.id)
        print("===============")
        game = Game("---------INPUT---------")
        await self.change_presence(status=Status.online, activity=game)
    
bot = MyBot()
bot.run("---------INPUT---------")