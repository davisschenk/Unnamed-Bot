from discord.ext import commands
import discord
import config as config
from contextlib import redirect_stdout
import textwrap
import io
import traceback
from utils.converters import Code


class Owner(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

    @commands.group(invoke_without_command=True)
    async def owner(self, ctx):
        await ctx.send_help(self.owner)

    @owner.group(name='reload', invoke_without_command=True)
    async def reload(self, ctx, extension: str):
        """Reload an extension"""
        embed = discord.Embed(title="Reload Extension")
        try:
            self.bot.reload_extension(name=extension)
            embed.add_field(name=extension, value="Success!")
            color = discord.Color.green()
        except Exception as e:
            embed.add_field(name=extension, value="Failure! \n Error: " + str(e))
            color = discord.Color.red()

        embed._colour = color
        await ctx.send(embed=embed)

    @owner.group(name="load", invoke_without_command=True)
    async def load(self, ctx, extension: str):
        """Load an Extension"""

        embed = discord.Embed(title="Load Extension")
        try:
            self.bot.load_extension(name=extension)
            embed.add_field(name=extension, value="Success!")
            color = discord.Color.green()
        except commands.ExtensionAlreadyLoaded:
            embed.add_field(name=extension, value="Success! Was Already Loaded!")
            color = discord.Color.green()
        except Exception as e:
            embed.add_field(name=extension, value="Failure! \n Error: " + str(e))
            color = discord.Color.red()

        embed._colour = color
        await ctx.send(embed=embed)

    @owner.group(name="unload", invoke_without_command=True)
    async def unload(self, ctx, extension: str):
        """Unload an extension"""

        embed = discord.Embed(title="Unload Extension")
        try:
            self.bot.unload_extension(name=extension)
            embed.add_field(name=extension, value="Success!")
            color = discord.Color.green()
        except Exception as e:
            embed.add_field(name=extension, value="Failure! \n Error: " + str(e))
            color = discord.Color.red()

        embed._colour = color
        await ctx.send(embed=embed)

    @reload.command(name="all")
    async def reload_all_extensions(self, ctx):
        """Reload all currently loaded extensions"""

        success = {}
        embed = discord.Embed(title="Reload All")
        for extension in self.bot.extensions.copy():
            if extension in success.keys():
                continue

            try:
                self.bot.reload_extension(extension)
                embed.add_field(name=extension, value="Successful!", inline=False)
                success.update({extension: 1})
            except Exception as e:
                embed.add_field(name=extension, value="Failure! \n Error: " + str(e), inline=False)
                success.update({extension: 0})

        if sum(success.values()) == len(success):
            embed._colour = discord.Color.green()
        else:
            embed._colour = discord.Color.red()

        await ctx.send(embed=embed)

    @load.command(name="all")
    async def load_all_extensions(self, ctx, directory: str = config.extension_dir):
        """Recursively search for and load extensions from folder"""

        success = {}
        embed = discord.Embed(title="Load All")
        for extension in self.bot.get_all_extensions_from_dir(directory=directory):
            if extension in success.keys():
                continue

            try:
                self.bot.load_extension(extension)
                embed.add_field(name=extension, value="Success!", inline=False)
                success.update({extension: 1})
            except commands.ExtensionAlreadyLoaded:
                embed.add_field(name=extension, value="Success! Was Already Loaded!", inline=False)
                success.update({extension: 1})
            except Exception as e:
                embed.add_field(name=extension, value="Failure! \n Error: " + str(e), inline=False)
                success.update({extension: 0})

        if sum(success.values()) == len(success):
            embed._colour = discord.Color.green()
        else:
            embed._colour = discord.Color.red()

        await ctx.send(embed=embed)

    @unload.command(name="all")
    async def unload_all_extensions(self, ctx):
        """Unload all currently loaded extensions"""

        embed = discord.Embed(title="Unload All")
        success = {}
        for extension in self.bot.extensions.copy():
            if extension in success.keys():
                continue

            if extension == __name__:
                if not await self.bot.confirm(ctx, "Unload owner? Doing so will make it impossible to reload without "
                                                   "restarting bot and editing loaded.json"):
                    continue

            try:
                self.bot.unload_extension(extension)
                embed.add_field(name=extension, value="Successful!", inline=False)
                success.update({extension: 1})
            except Exception as e:
                embed.add_field(name=extension, value="Failure! \n Error: " + str(e), inline=False)
                success.update({extension: 0})

        if sum(success.values()) == len(success):
            embed._colour = discord.Color.green()
        else:
            embed._colour = discord.Color.red()

        await ctx.send(embed=embed)

    @owner.command(name="list")
    async def list_extensions(self, ctx):
        """List all of the loaded extensions"""
        embed = discord.Embed(title="Extensions", color=discord.Color.green())
        for extension in self.bot.extensions:
            embed.add_field(name=extension, value="Loaded!", inline=False)
        await ctx.send(embed=embed)

    @owner.command(name="eval")
    async def owner_eval(self, ctx, *, code: Code):
        # Interface to store console output
        stdout = io.StringIO()
        embed = discord.Embed(title="Eval Code")

        # variable to add to environment when we compile code
        env = {
            'ctx': ctx,
            'bot': self.bot,
            'guild': ctx.guild,
            'channel': ctx.channel,
            'author': ctx.author,
            'message': ctx.message,
            'self': self
        }

        # add globals to env
        env.update(globals())

        # wrap code in a func
        formatted_code = f'async def my_func(): \n{textwrap.indent(code, "  ")}'

        # Compile code into usable object
        try:
            with redirect_stdout(stdout):
                exec(formatted_code, env)
        except Exception as e:
            embed._colour = discord.Color.red()
            embed.add_field(name="Error", value=f'```py\n{e.__class__.__name__}: {e}\n```')
            return await ctx.send(embed=embed)
        # get function from env
        func = env['my_func']

        # call func and capture output
        try:
            with redirect_stdout(stdout):
                func_return = await func()
        except Exception:
            value = stdout.getvalue()
            embed._colour = discord.Color.red()
            embed.add_field(name="Error", value=f'```py\n{value}{traceback.format_exc()}\n```')
            return await ctx.send(embed=embed)
        else:
            value = stdout.getvalue()
            embed._colour = discord.Color.green()
            if value:
                embed.add_field(name="Console Output", value=f'```py\n{value}```')
            if func_return:
                embed.add_field(name="Returned", value=f'```py\n{func_return}```')
            if not embed.fields:
                embed.description = "Success!"

            return await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Owner(bot))
