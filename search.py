import discord
from discord.ext import commands

from urllib.parse import urlencode
import soundcloud


class Search():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def sc(self, *args):
        '''
        Twitch username lookup
        Usage: !sc [query]
        e.g:   !tw asmr rap
        '''
        url = ("https://soundcloud.com/search/sounds?{}".format(urlencode({'q': ' '.join(args)})))

        print(url)
        return await self.bot.say(url)

    @commands.command()
    async def yt(self, *args):
        '''
        YouTube search
        Usage: !yt [query]
        e.g:   !yt cat videos
        '''
        url = ("https://www.youtube.com/results?search_{}".format(
            urlencode({'query': ' '.join(args)})))
        return await self.bot.say(url, delete_after=10)


def setup(bot):
    bot.add_cog(Search(bot))