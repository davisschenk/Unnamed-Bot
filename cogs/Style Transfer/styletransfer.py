import cv2
from discord.ext import commands
import asyncio
from utils.embeds import CustomEmbeds
import functools
import imutils
import discord
from io import BytesIO
from utils.pagination import Pages
import numpy as np
from PIL import Image
import typing


class StyleConverter(commands.Converter):
    models = {
        "starry": "/cogs/Style Transfer/models/starry_night.t7",
        "lamuse": "/cogs/Style Transfer/models/la_muse.t7",
        "composition": "/cogs/Style Transfer/models/composition_vii.t7",
        "mosaic": "/cogs/Style Transfer/models/mosaic.t7",
        "candy": "/cogs/Style Transfer/models/candy.t7",
        "feathers": "/cogs/Style Transfer/models/feathers.t7",
        "scream": "/cogs/Style Transfer/models/the_scream.t7",
        "wave": "/cogs/Style Transfer/models/the_wave.t7",
        "udnie": "/cogs/Style Transfer/models/udnie.t7"
    }

    async def convert(self, ctx, argument):
        model = self.models[argument]

        return model


class StyleTransfer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='style', invoke_without_command=True)
    async def transfer_style(self, ctx, model: StyleConverter, image: typing.Union[discord.Member, discord.Emoji] = None):
        """
        Use OpenCV to perform a neural network style transfer on an image.
        Image can be represented by a discord member, custom emoji or uploaded image
        """
        loop = asyncio.get_event_loop()
        if isinstance(image, discord.Member):
            image = await image.avatar_url.read()
            image = await loop.run_in_executor(None, self.prepare_image, image)

        elif isinstance(image, discord.Emoji):
            image = await image.url.read()
            image = await loop.run_in_executor(None, self.prepare_image, image)

        elif image is None:
            attachments = ctx.message.attachments
            if attachments:
                image = await attachments[0].read()
                image = await loop.run_in_executor(None, self.prepare_image, image)
            else:
                await ctx.send(embed=CustomEmbeds.question(author="Send a file for transfer!"))

                def check(message):
                    return ctx.author == message.author and ctx.channel == message.channel and len(message.attachments) > 0

                message = await self.bot.wait_for('message', check=check)
                image = await message.attachments[0].read()
                image = await loop.run_in_executor(None, self.prepare_image, image)
        else:
            raise commands.ArgumentParsingError

        await ctx.message.add_reaction("👌")

        style_args = functools.partial(self.style_image, image, model)
        styled_image = await loop.run_in_executor(None, style_args)

        encode_args = functools.partial(cv2.imencode, '.png', styled_image)
        ret, png = await loop.run_in_executor(None, encode_args)

        bytes_stream = BytesIO(png)

        await ctx.send(ctx.author.mention, file=discord.File(bytes_stream, filename='image.png'))

    @transfer_style.error
    async def style_error(self, ctx, error):
        if isinstance(error, commands.ConversionError):
            await ctx.send(embed=CustomEmbeds.remove(author="Invalid Style"))

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=CustomEmbeds.remove(author=str(error)))

    @transfer_style.command(name="list")
    async def list_models(self, ctx):
        entries = [k for k in StyleConverter.models.keys()]
        page = Pages(ctx, entries=entries, author="Available Styles")
        await page.paginate()

    @staticmethod
    def style_image(image, model_path):
        net = cv2.dnn.readNetFromTorch(model_path)

        # load the input image, resize it to have a width of 600 pixels,
        # then grab the image dimensions
        image = imutils.resize(image, width=600)
        (h, w) = image.shape[:2]

        # construct a blob from the image, set the input, and then
        # perform a forward pass of the network
        blob = cv2.dnn.blobFromImage(image, 1.0, (w, h),
                                     (103.939, 116.779, 123.680), swapRB=False, crop=False)
        net.setInput(blob)
        output = net.forward()

        # reshape the output tensor, add back in the mean subtraction,
        # and then swap the channel ordering
        output = output.reshape((3, output.shape[2], output.shape[3]))
        output[0] += 103.939
        output[1] += 116.779
        output[2] += 123.680
        output = output.transpose(1, 2, 0)

        return output

    @classmethod
    def prepare_image(cls, image):
        if isinstance(image, bytes):
            image = BytesIO(image)
            image = Image.open(image)

        image = image.convert("RGB")

        return np.asarray(image).astype('uint8')


def setup(bot):
    bot.add_cog(StyleTransfer(bot))
