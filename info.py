import discord
import asyncio
from discord.ext import commands
import api

from random import randint
import arrow

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
        dump = api.fetch_data(''.join(args))
        random_num = randint(1, len(dump))

        utc = arrow.now('US/Pacific')
        today = utc.format('ddd: MMM D')

        data_list = [x for x in dump if x['date'] == today]

        msg = None
        for data in data_list:
            data = dotdict(data)

            r = lambda: randint(0, 255)
            hexc = int('0x{:02X}{:02X}{:02X}'.format(r(), r(), r()), 16)

            embed = discord.Embed(title=data.name, url=(data.url2 or data.url1 or "19hz.info/#"), color=hexc)
            if data.url1 and data.url2:
                embed.set_author(name=data.name, url=data.url1)
                embed.title = "Extra Link"
            embed = Info.info_embed(embed, data)

            if not msg:
                msg = await self.bot.say(embed=embed)
            else: await self.bot.edit_message(msg, embed=embed)
            await asyncio.sleep(1)

        return

    @staticmethod
    def info_embed(embed: discord.Embed, data):
        genre = '`{}`'.format(na(data.genre))
        embed.add_field(name=":musical_note: __Genre(s)__", value=genre, inline=False)

        time = '{}\n`{}`'.format(na(data.date), na(data.time))
        embed.add_field(name=":alarm_clock: __Time__", value=time, inline=True)

        info = 'Location: `{}`\nPrice: `{}`\nAges: `{}`'.format(na(data.location), na(data.price), na(data.ages))
        embed.add_field(name=":grey_question: __Info__", value=info, inline=True)
        return embed


def setup(bot):
    bot.add_cog(Info(bot))