from __future__ import annotations


from logging import getLogger


from discord.ext import commands


logger = getLogger(__name__)


class CogTemplateClass(commands.cog):
    def __init__(self, bot):
        self.bot = bot

        logger.info('load extention is success')

    async def cog_check(self, ctx):
        return True

    async def cog_command_error(self, ctx, error):
        return await ctx.re_error('不明なエラーが発生しました。')

    @commands.is_owner()
    @commands.group(invoke_without_command=True, aliases=['gc'])
    async def group_command(self, ctx):
        """group command template
        """
        await ctx.send_help(ctx.command)

    @grouo_command.command()
    async def sub_command_template(self, ctx):
        """sub command template
        """
        await ctx.re_info('this is subcommand')

    @commands.is_owner()
    @commands.command(name='print')
    async def _print(self, ctx, *, args):
        await ctx.re_info(args)


def setup(bot):
    return bot.add_cog(CogTemplateClass(bot))
