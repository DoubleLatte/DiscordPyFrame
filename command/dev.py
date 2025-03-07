import discord
from discord import app_commands, Interaction
from discord.ext import commands
import importlib
import os

class DevCommands(commands.Cog):
    """
    개발자를 위한 명령어 관리 기능을 제공하는 Cog
    """
    
    def __init__(self, bot: commands.Bot) -> None:
        """
        DevCommands Cog 초기화
        
        Args:
            bot (commands.Bot): 봇 인스턴스
        """
        self.bot = bot
    
    @has_admin_role()
    @app_commands.command(
        name="reload", 
        description="지정한 Cog를 다시 로드합니다"
    )
    @app_commands.describe(extension="다시 로드할 확장 기능 이름 (예: command.paper)")
    async def reload_command(self, interaction: Interaction, extension: str) -> None:
        """
        지정된 확장 기능(Cog)을 다시 로드하는 명령어
        
        Args:
            interaction (Interaction): 발생한 인터랙션 객체
            extension (str): 다시 로드할 확장 기능 이름 (예: command.paper)
        """
        try:
            await self.bot.reload_extension(extension)
            await interaction.response.send_message(
                f"✅ `{extension}` 확장 기능이 성공적으로 다시 로드되었습니다.", 
                ephemeral=True
            )
        except commands.ExtensionNotFound:
            await interaction.response.send_message(
                f"❌ `{extension}` 확장 기능을 찾을 수 없습니다.", 
                ephemeral=True
            )
        except commands.ExtensionNotLoaded:
            await interaction.response.send_message(
                f"❌ `{extension}` 확장 기능이 로드되지 않았습니다. 먼저 로드해주세요.", 
                ephemeral=True
            )
        except commands.NoEntryPointError:
            await interaction.response.send_message(
                f"❌ `{extension}` 확장 기능에 setup 함수가 없습니다.", 
                ephemeral=True
            )
        except commands.ExtensionFailed as e:
            await interaction.response.send_message(
                f"❌ `{extension}` 확장 기능 로드 중 오류 발생: {str(e)}", 
                ephemeral=True
            )
    
    @has_admin_role()
    @app_commands.command(
        name="load", 
        description="새 Cog를 로드합니다"
    )
    @app_commands.describe(extension="로드할 확장 기능 이름 (예: command.paper)")
    async def load_command(self, interaction: Interaction, extension: str) -> None:
        """
        새로운 확장 기능(Cog)을 로드하는 명령어
        
        Args:
            interaction (Interaction): 발생한 인터랙션 객체
            extension (str): 로드할 확장 기능 이름 (예: command.paper)
        """
        try:
            await self.bot.load_extension(extension)
            # 명령어 트리 동기화
            await self.bot.tree.sync()
            await interaction.response.send_message(
                f"✅ `{extension}` 확장 기능이 성공적으로 로드되었습니다.", 
                ephemeral=True
            )
        except commands.ExtensionAlreadyLoaded:
            await interaction.response.send_message(
                f"❌ `{extension}` 확장 기능이 이미 로드되어 있습니다.", 
                ephemeral=True
            )
        except commands.ExtensionNotFound:
            await interaction.response.send_message(
                f"❌ `{extension}` 확장 기능을 찾을 수 없습니다.", 
                ephemeral=True
            )
        except commands.NoEntryPointError:
            await interaction.response.send_message(
                f"❌ `{extension}` 확장 기능에 setup 함수가 없습니다.", 
                ephemeral=True
            )
        except commands.ExtensionFailed as e:
            await interaction.response.send_message(
                f"❌ `{extension}` 확장 기능 로드 중 오류 발생: {str(e)}", 
                ephemeral=True
            )
    
    @has_admin_role()
    @app_commands.command(
        name="unload", 
        description="Cog를 언로드합니다"
    )
    @app_commands.describe(extension="언로드할 확장 기능 이름 (예: command.paper)")
    async def unload_command(self, interaction: Interaction, extension: str) -> None:
        """
        확장 기능(Cog)을 언로드하는 명령어
        
        Args:
            interaction (Interaction): 발생한 인터랙션 객체
            extension (str): 언로드할 확장 기능 이름 (예: command.paper)
        """
        # 개발 명령어 자체는 언로드할 수 없게 방지
        if extension == "command.dev":
            await interaction.response.send_message(
                "❌ 개발 명령어 자체는 언로드할 수 없습니다.", 
                ephemeral=True
            )
            return
            
        try:
            await self.bot.unload_extension(extension)
            # 명령어 트리 동기화
            await self.bot.tree.sync()
            await interaction.response.send_message(
                f"✅ `{extension}` 확장 기능이 성공적으로 언로드되었습니다.", 
                ephemeral=True
            )
        except commands.ExtensionNotFound:
            await interaction.response.send_message(
                f"❌ `{extension}` 확장 기능을 찾을 수 없습니다.", 
                ephemeral=True
            )
        except commands.ExtensionNotLoaded:
            await interaction.response.send_message(
                f"❌ `{extension}` 확장 기능이 로드되지 않았습니다.", 
                ephemeral=True
            )
    
    @has_admin_role()
    @app_commands.command(
        name="sync", 
        description="슬래시 명령어를 동기화합니다"
    )
    async def sync_command(self, interaction: Interaction) -> None:
        """
        슬래시 명령어를 디스코드와 동기화하는 명령어
        
        Args:
            interaction (Interaction): 발생한 인터랙션 객체
        """
        await interaction.response.defer(ephemeral=True)
        try:
            synced = await self.bot.tree.sync()
            await interaction.followup.send(
                f"✅ {len(synced)}개의 명령어가 성공적으로 동기화되었습니다.", 
                ephemeral=True
            )
        except discord.HTTPException as e:
            await interaction.followup.send(
                f"❌ 명령어 동기화 중 오류 발생: {str(e)}", 
                ephemeral=True
            )
    
    @has_admin_role()
    @app_commands.command(
        name="list_extensions", 
        description="현재 로드된 모든 확장 기능을 표시합니다"
    )
    async def list_extensions(self, interaction: Interaction) -> None:
        """
        현재 로드된 모든 확장 기능을 표시하는 명령어
        
        Args:
            interaction (Interaction): 발생한 인터랙션 객체
        """
        loaded_extensions = list(self.bot.extensions.keys())
        
        if not loaded_extensions:
            await interaction.response.send_message(
                "현재 로드된 확장 기능이 없습니다.", 
                ephemeral=True
            )
            return
            
        embed = discord.Embed(
            title="로드된 확장 기능 목록",
            color=discord.Color.blue()
        )
        
        for i, ext in enumerate(loaded_extensions, 1):
            embed.add_field(name=f"{i}. {ext}", value="✅ 로드됨", inline=False)
            
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot) -> None:
    """
    이 Cog를 봇에 추가하는 설정 함수
    
    Args:
        bot (commands.Bot): Cog를 추가할 봇 인스턴스
    """
    await bot.add_cog(DevCommands(bot))
    print("DevCommands cog가 성공적으로 로드되었습니다")
