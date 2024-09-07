import sys
import os
import yaml
import discord
from discord.ext import commands
from discord import Game, Status

def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# config.yml 로드 함수
def load_config():
    config_path = 'config.yml'  # 실행 파일과 같은 디렉토리에 있다고 가정
    try:
        with open(config_path, 'r', encoding='utf-8') as config_file:
            return yaml.safe_load(config_file)
    except FileNotFoundError:
        print(f"Error: {config_path} not found. Please make sure it's in the same directory as the executable.")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error reading {config_path}: {e}")
        sys.exit(1)

class MyBot(commands.Bot):
    def __init__(self, config):
        super().__init__(
            command_prefix='!',
            intents=discord.Intents.all(),
            sync_command=True,
            application_id=config['application_id']
        )
        self.config = config  # 봇 인스턴스에 config 저장
        self.initial_extension = [
            "command.paper",
            #"폴더명.명령어 파일 이름"
            #쉼표로 파일 추가 , 이거로
        ]

    async def setup_hook(self):
        for ext in self.initial_extension:
            try:
                await self.load_extension(ext)
            except commands.ExtensionNotFound:
                print(f"Error: Extension {ext} not found.")
            except commands.ExtensionFailed as e:
                print(f"Error: Failed to load extension {ext}. {e}")

        try:
            await self.tree.sync()
        except discord.HTTPException as e:
            print(f"Error syncing command tree: {e}")

    async def on_ready(self):
        print("===============")
        print("login")
        print("BOT_Name", self.user.name)
        print("BOT_id", self.user.id)
        print("===============")
        game = Game("~~~ 하는중")
        await self.change_presence(status=Status.online, activity=game)

if __name__ == "__main__":
    config = load_config()
    bot = MyBot(config)

    try:
        bot.run(config['token'])
    except KeyError:
        print("Error: 'token' not found in config.yml")
        sys.exit(1)
    except discord.LoginFailure:
        print("Error: Failed to login. Please check if the token is correct.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)