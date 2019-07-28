from discord.ext import commands
from utils.pagination import FieldPages


class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.command_usage_collection = self.bot.db["command_usage"]

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        if ctx.command is None:
            pass
        await self.command_usage_collection.update_one({"qualified_name": ctx.command.qualified_name},
                                                       {"$inc": {"completion": 1}},
                                                       upsert=True)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if ctx.command is None:
            pass
        await self.command_usage_collection.update_one({"qualified_name": ctx.command.qualified_name},
                                                       {"$inc": {"errors": 1}},
                                                       upsert=True)

        pass

    @commands.Cog.listener()
    async def on_command(self, ctx):
        if ctx.command is None:
            pass
        await self.command_usage_collection.update_one({"qualified_name": ctx.command.qualified_name},
                                                       {"$inc": {"total": 1}},
                                                       upsert=True)

    @commands.group(name='stats')
    async def stats(self, ctx):
        """Group of commands that show different bot stats"""
        pass

    @stats.command(name='commands')
    async def command_stats(self, ctx):
        """Get the usage for every command"""
        entries = []
        async for command in self.command_usage_collection.find({}):
            entries.append((command.get("qualified_name"), f"Completed {command.get('completion', 0)} times\n"
                                                           f"{command.get('errors', 0)} errors\n"
                                                           f"Used {command.get('total', 0)} times"))

        paginator = FieldPages(ctx, entries=entries, per_page=4)
        await paginator.paginate()


def setup(bot):
    bot.add_cog(Stats(bot))
