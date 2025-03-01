import discord
from discord import app_commands, Interaction, Embed, ButtonStyle
from discord.ext import commands
from discord.ui import Button, View


def has_admin_role():
    """
    사용자가 config에 정의된 관리자 역할을 가지고 있는지 확인하는 데코레이터 함수
    
    Returns:
        app_commands.check: 권한 검사를 수행하는 데코레이터
    """
    async def predicate(interaction: Interaction) -> bool:
        # config에서 관리자 역할 ID 가져오기
        admin_role_ids = interaction.client.config.get('administrator_role_ids', [])
        
        # 사용자가 관리자 역할 중 하나를 가지고 있는지 확인
        return any(role.id in admin_role_ids for role in interaction.user.roles)
    
    # 검사 함수를 데코레이터로 변환하여 반환
    return app_commands.check(predicate)


class Paper(commands.Cog):
    """
    페이퍼 관련 명령어를 처리하는 Cog
    
    Attributes:
        bot (commands.Bot): 봇 인스턴스
        user_channel_count (dict): 사용자 채널 카운트를 저장하는 딕셔너리
    """
    
    def __init__(self, bot: commands.Bot) -> None:
        """
        Paper Cog 초기화
        
        Args:
            bot (commands.Bot): 봇 인스턴스
        """
        self.bot = bot
        self.user_channel_count = {}
    
    @app_commands.command(
        name="명령어", 
        description="명령어 설명"
    )
    @has_admin_role()
    async def paper_command(self, interaction: Interaction) -> None:
        """
        페이퍼 명령어 처리기
        
        Args:
            interaction (Interaction): 발생한 인터랙션 객체
        """
        # 테스트 메시지 전송
        await interaction.response.send_message("테스트")
    
    @paper_command.error
    async def paper_command_error(self, interaction: Interaction, error: app_commands.AppCommandError):
        """
        페이퍼 명령어의 오류를 처리하는 함수
        
        Args:
            interaction (Interaction): 발생한 인터랙션 객체
            error (app_commands.AppCommandError): 발생한 오류
        """
        if isinstance(error, app_commands.CheckFailure):
            # 권한 부족 오류 처리
            await interaction.response.send_message(
                "이 명령어를 사용할 권한이 없습니다.", 
                ephemeral=True
            )
        else:
            # 예상치 못한 오류 로깅 및 처리
            print(f"페이퍼 명령어에서 오류 발생: {error}")
            await interaction.response.send_message(
                "명령어 실행 중 오류가 발생했습니다.", 
                ephemeral=True
            )


async def setup(bot: commands.Bot) -> None:
    """
    이 Cog를 봇에 추가하는 설정 함수
    
    Args:
        bot (commands.Bot): Cog를 추가할 봇 인스턴스
    """
    # Paper Cog를 봇에 추가
    await bot.add_cog(Paper(bot))
    print("Paper cog가 성공적으로 로드되었습니다")
