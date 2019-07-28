from discord.ext import commands
from utils.embeds import CustomEmbeds
import time
import aiohttp
from utils.pagination import UrbanDictionaryPages
from emojificate.filter import emojificate


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='about')
    async def about(self, ctx):
        embed = CustomEmbeds.info(author="About")
        embed.add_field(name='Creator', value='Davis#9654')
        embed.add_field(name='Bot Discord', value='http://discord.gg/yzyRUFr')
        embed.add_field(name="Purpose", value='Bot with some commands that I find cool/interesting or just want to code')
        await ctx.send(embed=embed)

    @commands.command(name='ping')
    async def ping(self, ctx):
        start = time.perf_counter()
        message = await ctx.send("Ping...")
        end = time.perf_counter()
        duration = (end - start) * 1000
        await message.edit(content='Pong! {:.2f}ms'.format(duration))

    @commands.is_nsfw()
    @commands.command(name="ud", aliases=["slang"])
    async def define(self, ctx, *, word: str):
        """Query urban dictionary for a word"""
        url = f"http://api.urbandictionary.com/v0/define?term={word}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                json_response = await r.json()

        entries = [d for d in json_response.get("list")]

        paginator = UrbanDictionaryPages(ctx, entries=entries, per_page=1)
        await paginator.paginate()

    @commands.command(name="emojificate")
    async def emoji_cv(self, ctx, *, emoji: str):
        await ctx.send(emojificate(emoji))


def setup(bot):
    bot.add_cog(Misc(bot))
