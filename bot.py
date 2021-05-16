import datetime
import aiohttp
from discord.ext import commands
from discord_slash import SlashCommand
from lib.manager import Manager

__all__: tuple = (
    'Spaceman'
)

initial_extensions: tuple = (
    'cogs.handlers.events',
    'cogs.handlers.errors',
    'cogs.commands.ethereum',
    'cogs.commands.dev.debug'
)


class Spaceman(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or(';'))
        self.ses: aiohttp.ClientSession = aiohttp.ClientSession(loop=self.loop, headers={})
        self.mgr: Manager = Manager(self.ses)
        self.slash: SlashCommand = SlashCommand(self, sync_commands=True, sync_on_cog_reload=True)
        self.started_at: datetime.datetime = datetime.datetime.utcnow()
        for ext in initial_extensions:
            self.load_extension(ext)

    @property
    def uptime(self) -> datetime.timedelta:
        return datetime.datetime.utcnow() - self.started_at

    async def on_ready(self) -> None:
        self.mgr.log(f'Ready: {self.user} (ID: {self.user.id})')
