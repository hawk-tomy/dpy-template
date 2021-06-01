from dataclasses import asdict, dataclass
from logging import getLogger
import traceback


import discord
from discord import AllowedMentions, Intents
from discord.ext import commands

from bot_util import dispander, Embed, help_command, split_line
from bot_util.config import config, ConfigBase
#from bot_util.sio_client import SioClient
#if you need socket.up client, please enabled.

from cog import extension


__all__ = ('Bot',)


@dataclass
class Main(ConfigBase):
    TOKEN: str= ''


config.add_default_config(Main)


logger = getLogger(__name__)


class Bot(commands.Bot):
    def __init__(self):
        intents = Intents.all()
        intents.typing = False
        allowed_mentions = AllowedMentions(everyone=False, replied_user=False)

        super().__init__(
            allowed_mentions= allowed_mentions,
            command_prefix= '/',
            description= 'This message is template. Please rewrite',
            help_command= help_command.Help(),
            intents= intents,
            )

        def log(ctx):
            guild_id = ctx.guild.id if ctx.guild else '@me'
            channel_id = ctx.channel.id
            message_id = ctx.message.id
            author_id = ctx.message.author.id
            logger.info(
                f'{guild_id}/{channel_id}/{message_id}:{author_id}'
            )
            return True

        self.check_once(log)
        self.__default_embed: Embed= Embed(**asdict(config.embed_setting))
#        self.sio: SioClient= SioClient()
#        self.sio_task = self.loop.create_task(self.sio.run())
        for ext in extension:
            self.load_extension(ext)

    @property
    def default_embed(self)-> Embed:
        return self.__default_embed.copy()

    def run(self):
        super().run(config.Main.TOKEN)

    async def on_ready(self):
        logger.info('login success')
        await self.change_presence(activity=discord.Game('/help'))
        appinfo = await self.application_info()
        self.owner_id = appinfo.owner.id
        await self.get_user(self.owner_id).send('起動しました。')

    async def on_message(self, message):
        if isinstance(message.channel, discord.TextChannel):
            if message.author == self.user:
                return
            await dispander.dispand(message)
        if message.author.bot:
            return
        await self.process_commands(message)

    async def on_command_error(self, ctx, error):
        error = error if error.__context__ is None else error.__context__
        if self.extra_events.get('on_command_error', None):
            return

        if hasattr(ctx.command, 'on_error'):
            return

        cog = ctx.cog
        if cog and commands.Cog._get_overridden_method(cog.cog_command_error) is not None:
            return
        err_msg = (
            f'Ignoring exception in command {ctx.command}:\n'
            f'{"".join(traceback.format_exception(type(error), error, error.__traceback__))}'
            )
        embed = self.default_embed
        embed.title = 'traceback (command)'
        for msg in split_line(err_msg, 1000):
            embed.add_field(
                name='traceback',
                value=f'```py\n{msg}\n```',
                inline=False,
            )
        logger.exception(err_msg)
        await self.get_user(self.owner_id).send(embed=embed)

    async def on_error(self, event_method, *args, **kwargs):
        err_msg = (
            f'Ignoring exception in {event_method}\n'
            f'{traceback.format_exc()}'
            )
        embed = self.default_embed
        embed.title = 'traceback (any)'
        for msg in split_line(err_msg, 1000):
            embed.add_field(
                name='traceback',
                value= f'```py\n{msg}\n```',
                inline=False,
            )
        logger.exception(err_msg)
        await self.get_user(self.owner_id).send(embed=embed)
