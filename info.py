import discord
from discord.ext import commands

from urllib.parse import urlsplit
from data import _config as c
import api

from fuzzywuzzy import process
import arrow


def na(param):
    return param or "n/a"


class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class Color(object):
    LIST = [0xff3352, 0xf9d814, 0x7ae576, 0xbaffc9, 0x7fa0fb, 0xae86d8]

    def __init__(self):
        self.idx = 0

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        self.idx += 1
        if self.idx > len(Color.LIST)-1:
            self.idx = 0
        return Color.LIST[self.idx - 1]


class Carousel(object):
    def __init__(self, data_list):
        self.idx = 0
        self.data_list = data_list

    def __iter__(self):
        return self

    def next(self):
        self.idx += 1
        if self.idx > len(self.data_list)-1:
            self.idx = 0
        return self.idx

    def prev(self):
        self.idx -= 1
        if self.idx > 0:
            self.idx = len(self.data_list)-1
        return self.idx

    def close(self):
        raise StopIteration


def newEmbed(data_list, idx: int, roygbiv):
    e = discord.Embed(title=data_list[idx-1].name,
                      url=(data_list[idx-1].url2 or data_list[idx-1].url1 or "19hz.info/#"),
                      color=roygbiv.next())
    e = Info.info_embed(e, data_list[idx - 1])
    return e


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
        concat = ''.join(args).lower()

        for k, v in c.DATA_ALIAS.items():
            for i in v:
                if concat == i:
                    concat = k

        best = process.extractOne(concat, c.DATA_SHORT)
        if best[1] < .50:
            cities = ", ".join(c.DATA_SHORT)
            text = "`{}` didn't match with anything\nTry one of these cities:\n`{}`".format(best[0], cities)
            await self.bot.say(text)
            return

        dump = api.fetch_data(best[0])
        if not dump: return

        utc = arrow.now('US/Pacific')
        today = utc.format('ddd: MMM D')
        data_list = [dotdict(x) for x in dump if x['date'] == today]

        carousel = Carousel(data_list)
        roygbiv = Color()

        embed = newEmbed(data_list, 0, roygbiv)

        instead = (best[0] != concat) and ' instead of `{}`'.format(concat) or ''
        text = 'Fetching results for `{}`{}'.format(best[0], instead)

        msg = await self.bot.say(text, embed=embed)
        await self.bot.add_reaction(msg, '◀')
        await self.bot.add_reaction(msg, '⬇')
        await self.bot.add_reaction(msg, '▶')

        try:
            while True:
                res = await self.bot.wait_for_reaction(message=msg)
                if res:
                    if res.reaction.emoji == '◀':
                        embed = newEmbed(data_list, carousel.prev(), roygbiv)
                        await self.bot.edit_message(msg, embed=embed)
                        await self.bot.remove_reaction(msg, '◀', res.user)
                    if res.reaction.emoji == '▶' and res.user != self.bot.user:
                        embed = newEmbed(data_list, carousel.next(), roygbiv)
                        await self.bot.edit_message(msg, embed=embed)
                        await self.bot.remove_reaction(msg, '▶', res.user)
                    elif res.reaction.emoji == '⬇':
                        await self.bot.delete_message(msg)
        except discord.HTTPException:
            await self.bot.delete_message(msg)
            return

    @staticmethod
    def info_embed(embed: discord.Embed, data):
        if data.url1 and data.url2:
            embed.set_author(name=data.name, url=data.url1)
            embed.title = "{0.scheme}://{0.netloc}/".format(urlsplit(data.url2))

        time = '{}\n`{}`'.format(na(data.date), na(data.time))
        embed.add_field(name=":alarm_clock: __Time__", value=time, inline=True)

        genre = '`{}`'.format(na(data.genre))
        embed.add_field(name=":musical_note: __Genre(s)__", value=genre, inline=True)

        info = 'Location: `{}`\nPrice: `{}`\nAges: `{}`'.format(na(data.location), na(data.price), na(data.ages))
        embed.add_field(name=":grey_question: __Info__", value=info, inline=False)

        embed.set_footer(text="Powered by 19hz.info", icon_url=c.ICON_URL)
        return embed


def setup(bot):
    bot.add_cog(Info(bot))