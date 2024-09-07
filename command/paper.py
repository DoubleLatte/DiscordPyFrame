import discord
from discord import app_commands, Interaction, Embed, ButtonStyle, InteractionType, PermissionOverwrite
from discord.ext import commands
from discord.ui import Button, View
from datetime import datetime, timedelta
import asyncio


def has_admin_role():
    async def predicate(interaction: Interaction) -> bool:
        admin_role_ids = interaction.client.config.get('administrator_role_ids', [])
        return any(role.id in admin_role_ids for role in interaction.user.roles)
    return app_commands.check(predicate)


class Paper(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.user_channel_count = {}

    @has_admin_role()
    @app_commands.command(name="명령어", description="명령어 설명")
    async def paper(self, interaction: Interaction) -> None:
        await interaction.response.send_message("테스트")

    @paper.error
    async def worktime_management_error(self, interaction: Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message("이 명령어를 사용할 권한이 없습니다.", ephemeral=True)



async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Paper(bot))