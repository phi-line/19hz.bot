import discord
import asyncio
from discord.ext import commands

from data import _config as c
import api

from random import randint
from fuzzywuzzy import process
import arrow

def na(param):
    return param or "n/a"

class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

class color(object):
    LIST = [0xffd6d6, 0xffdfba, 0xffffba, 0xbaffc9, 0xbae1ff, 0xeccdfa]
    def __init__(self):
        self.num, self.nums = 0, []
        self.cur = 0

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        if self.num < len(color.LIST):
            self.num += 1
            return color.LIST[self.num-1]
        else:
            self.num = 0

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
        # dump = api.fetch_data(''.join(args))
        concat = ''.join(args).lower()

        for k, v in c.DATA_ALIAS.items():
            for i in v:
                if concat == i:
                    concat = k

        best = process.extractOne(concat, c.DATA_SHORT)
        if best[1] < .50:
            Info.throw_error(best[0])
            return

        dump = api.fetch_data(best[0])
        if not dump: return

        utc = arrow.now('US/Pacific')
        today = utc.format('ddd: MMM D')
        data_list = [x for x in dump if x['date'] == today]
        roygbiv = color()

        msg = None
        for data in data_list:
            data = dotdict(data)

            embed = discord.Embed(title=data.name,
                                  url=(data.url2 or data.url1 or "19hz.info/#"),
                                  color=roygbiv.next())
            if data.url1 and data.url2:
                embed.set_author(name=data.name, url=data.url1)
                embed.title = "Extra Link"
            embed = Info.info_embed(embed, data)
            embed.set_footer(text="Powered by 19hz.info", icon_url=c.ICON_URL)

            if not msg:
                instead = (best[0] != concat) and 'instead of `{}`'.format(concat) or ''
                text = 'Fetching results for `{}`{}'.format(best[0], instead)

                msg = await self.bot.say(text, embed=embed)
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

    @classmethod
    async def throw_error(self, best: str):
        cities = ", ".join(c.DATA_SHORT)
        text = "`{}` didn't match with anything\nTry one of these cities:\n`{}`".format(best, cities)
        await self.bot.say(text)


def setup(bot):
    bot.add_cog(Info(bot))