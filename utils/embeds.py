import discord
from discord.embeds import EmptyEmbed

class CustomEmbeds:
    confirm_path = 'https://raw.githubusercontent.com/davisschenk/Unnamed-Bot/master/images/ConfirmIcon.png?token=AIRYAKQHGVMHHBQ73J7G2AK5FKHRK'
    add_path = 'https://raw.githubusercontent.com/davisschenk/Unnamed-Bot/master/images/AddIcon.png?token=AIRYAKXEWWR4CFXQTWXSAR25FKHI2'
    remove_path = 'https://raw.githubusercontent.com/davisschenk/Unnamed-Bot/master/images/MinusIcon.png?token=AIRYAKTRTDTZ4R54N5DN6EC5FKHTU'
    question_path = 'https://raw.githubusercontent.com/davisschenk/Unnamed-Bot/master/images/QuestionIcon.png?token=AIRYAKXDB5BW4TAKDGPRFI25FKHU6'
    info_path = 'https://raw.githubusercontent.com/davisschenk/Unnamed-Bot/master/images/InfoIcon.png?token=AIRYAKVHWJUI5UE22CS6QQC5FKHWI'

    @classmethod
    def confirm(cls, **kwargs):
        title = kwargs.get('title', EmptyEmbed)
        description = kwargs.get('description', EmptyEmbed)
        url = kwargs.get('url', EmptyEmbed)
        color = kwargs.get('color', discord.Color.from_rgb(46, 204, 113))
        author = kwargs.get('author', 'Confirm')

        embed = discord.Embed(title=title, description=description, url=url, color=color)
        embed.set_author(name=author, icon_url=cls.confirm_path)

        return embed

    @classmethod
    def add(cls, **kwargs):
        title = kwargs.get('title', EmptyEmbed)
        description = kwargs.get('description', EmptyEmbed)
        url = kwargs.get('url', EmptyEmbed)
        color = kwargs.get('color', discord.Color.from_rgb(46, 204, 113))
        author = kwargs.get('author', 'Add')

        embed = discord.Embed(title=title, description=description, url=url, color=color)
        embed.set_author(name=author, icon_url=cls.add_path)

        return embed

    @classmethod
    def remove(cls, **kwargs):
        title = kwargs.get('title', EmptyEmbed)
        description = kwargs.get('description', EmptyEmbed)
        url = kwargs.get('url', EmptyEmbed)
        color = kwargs.get('color', discord.Color.from_rgb(231, 76, 60))
        author = kwargs.get('author', 'Remove')

        embed = discord.Embed(title=title, description=description, url=url, color=color)
        embed.set_author(name=author, icon_url=cls.remove_path)

        return embed

    @classmethod
    def question(cls, **kwargs):
        title = kwargs.get('title', EmptyEmbed)
        description = kwargs.get('description', EmptyEmbed)
        url = kwargs.get('url', EmptyEmbed)
        color = kwargs.get('color', discord.Color.from_rgb(52, 152, 219))
        author = kwargs.get('author', 'Question')

        embed = discord.Embed(title=title, description=description, url=url, color=color)
        embed.set_author(name=author, icon_url=cls.question_path)

        return embed

    @classmethod
    def info(cls, **kwargs):
        title = kwargs.get('title', EmptyEmbed)
        description = kwargs.get('description', EmptyEmbed)
        url = kwargs.get('url', EmptyEmbed)
        color = kwargs.get('color', discord.Color.from_rgb(52, 152, 219))
        author = kwargs.get('author', 'Info')

        embed = discord.Embed(title=title, description=description, url=url, color=color)
        embed.set_author(name=author, icon_url=cls.info_path)

        return embed

    @classmethod
    def starboard(cls, message, **kwargs):
        title = kwargs.get('title', EmptyEmbed)
        description = kwargs.get('description', f'{message.content}\n [Jump To](https://discordapp.com/channels/{message.guild.id}/{message.channel.id}/{message.id})')
        url = kwargs.get('url', EmptyEmbed)
        color = kwargs.get('color', 13103696)
        author = kwargs.get('author', ':star: Starboard :star:')

        embed = discord.Embed(color=color,
                              description=description)
        embed.set_footer(text=f"Author: {message.author}", icon_url=message.author.avatar_url)
        return embed
