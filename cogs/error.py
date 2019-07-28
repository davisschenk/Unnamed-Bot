from discord.ext import commands
import data.custom_emotes as emotes
import traceback
import sys
from utils.embeds import CustomEmbeds


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        error = getattr(error, 'original', error)

        if await self.bot.is_owner(ctx.author):
            embed = CustomEmbeds.remove(author="Owner Induced Error", description=f"```\n{''.join(traceback.format_exception(type(error), error, error.__traceback__))}```")
            await ctx.author.send(embed=embed)

        if hasattr(ctx.commands, 'on_error'):
            return

        if isinstance(error, commands.CheckFailure):
            return await ctx.message.add_reaction(":no_entry:")

        if isinstance(error, commands.CommandNotFound):
            return await ctx.message.add_reaction(emotes.thrinking)

        if isinstance(error, commands.CommandOnCooldown):
            return await ctx.send(embed=CustomEmbeds.remove(author=f"Command is on cooldown. Wait {error.retry_after} seconds"))

        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
        return await ctx.send(embed=CustomEmbeds.remove(author=str(error)))


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
