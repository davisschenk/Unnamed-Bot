from discord.ext import commands


class UnnamedContext(commands.Context):
    def __init__(self, **attrs):
        super().__init__(**attrs)

    async def get_emotes(self, **kwargs):
        embed = kwargs.get("embed")
        prompt = kwargs.get("prompt")
        timeout = kwargs.get("timeout", 60)
        confirm_emote = kwargs.get("confirm", "✅")
        file = kwargs.get("file", None)

        def check(reaction, user):
            return str(reaction.emoji) == confirm_emote and user.id == self.author.id

        if not embed and not prompt:
            raise ValueError("Either prompt or embed needs to be defined")

        message = await self.send(content=prompt, embed=embed, file=file)
        await message.add_reaction(confirm_emote)
        await self.bot.wait_for('reaction_add', check=check, timeout=timeout)
        message = await self.fetch_message(message.id)

        return [str(emoji.emoji) for emoji in message.reactions if not emoji.me]

    async def confirm(self, **kwargs):
        def check(reaction, user):
            return self.author.id == user.id and reaction.emoji in ['👎', '👍']

        prompt = kwargs.get("prompt", None)
        embed = kwargs.get("embed", None)
        timeout = kwargs.get('timeout', 60)
        file = kwargs.get("file", None)

        if prompt is None and embed is None:
            raise ValueError("You need to define prompt or embed")

        msg = await self.send(content=prompt, embed=embed, file=file)

        await msg.add_reaction('👍')
        await msg.add_reaction('👎')
        try:
            reaction, member = await self.bot.wait_for('reaction_add', check=check, timeout=timeout)
        except TimeoutError:
            raise commands.CommandError("Timed out!")
        if reaction.emoji == '👍':
            return True
        return False

    async def get_member(self, **kwargs):
        embed = kwargs.get("embed")
        prompt = kwargs.get("prompt")
        timeout = kwargs.get("timeout", 60)
        file = kwargs.get("file", None)

        def check(message):
            return self.author == message.author and message.channel == self.channel

        if not embed and not prompt:
            raise ValueError("Either prompt or embed needs to be defined")

        await self.send(content=prompt, embed=embed, file=file)

        message = await self.bot.wait_for('message', check=check, timeout=timeout)
        try:
            member = await commands.MemberConverter().convert(ctx=self, argument=message.content)
            return member
        except commands.BadArgument as e:
            await self.send(str(e))

        if await self.confirm(prompt="Try again??"):
            await self.get_member(**kwargs)

    async def get_text_channel(self, **kwargs):
        embed = kwargs.get("embed")
        prompt = kwargs.get("prompt")
        timeout = kwargs.get("timeout", 60)
        file = kwargs.get("file", None)

        def check(message):
            return self.author == message.author and message.channel == self.channel

        if not embed and not prompt:
            raise ValueError("Either prompt or embed needs to be defined")

        await self.send(content=prompt, embed=embed, file=file)

        message = await self.bot.wait_for('message', check=check, timeout=timeout)
        try:
            member = await commands.TextChannelConverter().convert(ctx=self, argument=message.content)
            return member
        except commands.BadArgument as e:
            await self.send(str(e))

        # if await self.confirm(prompt="Try again??"):
        #     await self.get_text_channel(**kwargs)

    async def get_voice_channel(self, **kwargs):
        embed = kwargs.get("embed")
        prompt = kwargs.get("prompt")
        timeout = kwargs.get("timeout", 60)
        file = kwargs.get("file", None)

        def check(message):
            return self.author == message.author and message.channel == self.channel

        if not embed and not prompt:
            raise ValueError("Either prompt or embed needs to be defined")

        await self.send(content=prompt, embed=embed, file=file)

        message = await self.bot.wait_for('message', check=check, timeout=timeout)
        try:
            member = await commands.VoiceChannelConverter().convert(ctx=self, argument=message.content)
            return member
        except commands.BadArgument as e:
            await self.send(str(e))

        if await self.confirm(prompt="Try again??"):
            await self.get_voice_channel(**kwargs)

    async def get_category(self, **kwargs):
        embed = kwargs.get("embed")
        prompt = kwargs.get("prompt")
        timeout = kwargs.get("timeout", 60)
        file = kwargs.get("file", None)

        def check(message):
            return self.author == message.author and message.channel == self.channel

        if not embed and not prompt:
            raise ValueError("Either prompt or embed needs to be defined")

        await self.send(content=prompt, embed=embed, file=file)

        message = await self.bot.wait_for('message', check=check, timeout=timeout)
        try:
            member = await commands.CategoryChannelConverter().convert(ctx=self, argument=message.content)
            return member
        except commands.BadArgument as e:
            await self.send(str(e))

        if await self.confirm(prompt="Try again??"):
            await self.get_category(**kwargs)

    async def get_string(self, **kwargs):
        embed = kwargs.get("embed")
        prompt = kwargs.get("prompt")
        timeout = kwargs.get("timeout", 60)
        file = kwargs.get("file", None)

        def check(message):
            return self.author == message.author and message.channel == self.channel

        if not embed and not prompt:
            raise ValueError("Either prompt or embed needs to be defined")

        await self.send(content=prompt, embed=embed, file=file)

        message = await self.bot.wait_for('message', check=check, timeout=timeout)
        return message.content

    async def get_int(self, **kwargs):
        embed = kwargs.get("embed")
        prompt = kwargs.get("prompt")
        timeout = kwargs.get("timeout", 60)
        file = kwargs.get("file", None)

        def check(message):
            return self.author == message.author and message.channel == self.channel and message.content.isdigit()

        if not embed and not prompt:
            raise ValueError("Either prompt or embed needs to be defined")

        await self.send(content=prompt, embed=embed, file=file)

        message = await self.bot.wait_for('message', check=check, timeout=timeout)
        return int(message.content)

    async def get_image(self, **kwargs):
        embed = kwargs.get("embed")
        prompt = kwargs.get("prompt")
        timeout = kwargs.get("timeout", 60)
        file = kwargs.get("file", None)

        def check(message):
            return self.author == message.author and message.channel == self.channel and message.attachments

        if not embed and not prompt:
            raise ValueError("Either prompt or embed needs to be defined")

        await self.send(content=prompt, embed=embed, file=file)

        message = await self.bot.wait_for('message', check=check, timeout=timeout)
        return message.attachments[0].proxy_url
