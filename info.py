import discord
from discord.ext import commands


class Info():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def event(self, *args):
        '''
        Serves today's local events via 19hz.info
        Usage: !event [location]
        e.g:   !event bayarea
        '''
        print(args)
        return await self.bot.say(url, delete_after=10)

def setup(bot):
    bot.add_cog(Info(bot))