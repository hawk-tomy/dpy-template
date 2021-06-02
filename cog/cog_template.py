from __future__ import annotations


from logging import getLogger


from discord.ext import commands


logger = getLogger(__name__)


class CogTemplateClass(commands.cog):
    def __init__(self, bot):
        self.bot = bot

        logger.info('load extention is success')

    def cog_check(self, ctx):
        return True

    @commands.is_owner()
    @commands.group(alies=['gc'])
    async def group_command(self, ctx):
        """group command template
        """
        if ctx.invoked_subcommand is None:
            self.bot.help_command.context = ctx
            await self.bot.help_command.send_group_help(ctx.command)
        pass

    @commands.is_owner()
    @grouo_command.command()
    async def sub_command_template(self, ctx):
        """sub command template
        """
        await ctx.send('this is subcommand')

    @commands.command(name='print')
    async _print(self, ctx, *, args):
        await ctx.reply(args)


def setup(bot):
    return bot.add_cog(CogTemplateClass(bot))
