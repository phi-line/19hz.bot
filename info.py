import discord
from discord.ext import commands
import api
from config import COLOR

# import maya

def na(param):
    return param or "n/a"

class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

class Info():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def event(self, *args):
        '''
        Serves today's local events via 19hz.info
        Usage: !event [location]
        e.g:   !event Bay Area
        '''
        data = dotdict(api.fetch_data(args[0])[0])

        embed = discord.Embed(title=data.name, url=(data.url1 or data.url2 or "19hz.info/#"), color=COLOR)
        if data.ur1 and data:
            embed.set_author(name="Extra Link", url=data.url2)
        embed = Info.info_embed(embed, data)

        return await self.bot.say(embed=embed)

    @staticmethod
    def info_embed(embed: discord.Embed, data):
        genre = '`{}`'.format(na(data.genre))
        embed.add_field(name="__Genre(s)__", value=genre, inline=False)

        time = '{}\n`{}`'.format(na(data.date), na(data.time))
        embed.add_field(name="__Time__", value=time, inline=True)

        info = 'Location: `{}`\nPrice: `{}`\nAges: `{}`'.format(na(data.location), na(data.price), na(data.ages))
        embed.add_field(name="__Info__", value=info, inline=True)
        return embed


def setup(bot):
    bot.add_cog(Info(bot))