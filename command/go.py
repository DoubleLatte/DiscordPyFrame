from discord import app_commands
from discord.ext import commands
from discord import Interaction


class file1(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="command",description="commandINFO")  
    async def file1(self, interaction: Interaction) -> None:
        user_id = str (interaction.user.id)
        user_name = interaction.user.name
        user_nick = interaction.user.nick
        user_role = str(interaction.user.roles)
        
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        file1(bot)
    )