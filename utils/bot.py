from discord.ext import commands
import discord
import sys
from pathlib import Path
import motor.motor_asyncio
from config import token, extension_dir
from utils.context import UnnamedContext
from utils.help import PaginatedHelpCommand


class UnnamedBot(commands.Bot):
    def __init__(self, command_prefix, **options):
        self.db_client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
        self.db = self.db_client['unnamed-bot']
        super().__init__(command_prefix, **options)

    async def on_ready(self):
        print(f"\n{'#' * 40}"
              f"\n{self.user.name}"
              f"\nPython version: {sys.version}"
              f"\nDiscord.py version: {discord.__version__}\n{'#' * 40}"
              f"\nLogged in as: {self.user.name} (ID: {self.user.id})")

        self.help_command = PaginatedHelpCommand()

    def run(self, **kwargs):
        if kwargs.get('load_all'):
            self.load_all_extensions(self.get_all_extensions_from_dir())
        super().run(token)

    async def get_context(self, message, *, cls=None):
        return await super().get_context(message, cls=UnnamedContext)

    @staticmethod
    def format_cog(path, replacements=(('/', '.'), ('\\', '.'), ('.py', ''))):
        for replacement in replacements:
            path = path.replace(*replacement)

        return path

    def get_all_extensions_from_dir(self, directory=extension_dir):
        for cog in Path(directory).glob('**/*.py'):
            cog_path = self.format_cog(str(cog))
            yield cog_path
        yield 'jishaku'

    def load_all_extensions(self, extensions):
        for extension in extensions:
            try:
                self.load_extension(extension)
                print(f"Loaded {extension}")
            except Exception as e:
                print(f"Could'nt load {extension}. {e.__class__}: {e}")
