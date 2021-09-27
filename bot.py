import traceback
from logging import getLogger
from os import getenv

import discord
import dispander
from discord import AllowedMentions, Intents
from discord.ext import commands

from lib import Context, Help, split_line #sio_client
from cog import extension

__all__ = ('Bot',)


logger = getLogger(__name__)


class Bot(commands.Bot):
    def __init__(self):
        intents = Intents.all()
        intents.typing = False
        allowed_mentions = AllowedMentions(everyone=False, replied_user=False)

        super().__init__(
            allowed_mentions=allowed_mentions,
            command_prefix='/',
            description='This message is template sentence. Please rewrite',
            help_command=Help(),
            intents=intents,
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
        super().run(getenv('DISCORD_BOT_TOKEN'))

    async def get_context(self, message):
        return await super().get_context(message, cls=Context)

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

    async def on_raw_reaction_add(self, payload):
        await dispander.delete_dispand(self, payload=payload)

    async def on_command_error(self, ctx: Context, exc: commands.CommandError):
        if ctx.invoked_error:
            return
        if isinstance(exc, commands.MissingRequiredArgument):
            await ctx.re_error(f'`{exc.param.name}`は必須です。')
            return
        log_msg = f'Ignoring exception in command {ctx.command}:'
        err_msg = f'{log_msg}\n{"".join(traceback.format_exception(type(exc), exc, exc.__traceback__))}'
        logger.exception(log_msg, exc_info=exc)
        if len(err_msg) < 5000:
            embed = self.default_embed
            embed.title = 'traceback (on_command_error)'
            for msg in split_line(err_msg, 1000):
                embed.add_field(name='traceback', value=f'```py\n{msg}\n```', inline=False)
            await self.get_user(self.owner_id).send(embed=embed)
        else:
            await self.get_user(self.owner_id).send(file=File(fp=StringIO(err_msg), filename='tb_command_error.py'))

    async def on_error(self, event_method, *args, **kwargs):
        log_msg = f'Ignoring exception in {event_method}:'
        err_msg = f'{log_msg}\n{traceback.format_exc()}'
        logger.exception(log_msg)
        if len(err_msg) < 5000:
            embed = self.default_embed
            embed.title = 'traceback (on_error)'
            for msg in split_line(err_msg, 1000):
                embed.add_field(name='traceback', value=f'```py\n{msg}\n```', inline=False)
            await self.get_user(self.owner_id).send(embed=embed)
        else:
            await self.get_user(self.owner_id).send(file=File(fp=StringIO(err_msg), filename='tb_error.py'))
