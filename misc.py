import discord
from discord.ext import commands

from random import seed, uniform


class Misc():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rate(self, *args):
        '''
        Rate a word or user
        Usage: !rate
        '''
        if args:
            s = ' '.join(args).lower()
            seed(s)
            number = round(uniform(1, 8), 1)
            return await self.bot.say("Gr8 m8 I rate {}/8".format(number))

    @commands.command()
    async def pussyhacks(self):
        pass



def setup(bot):
    bot.add_cog(Misc(bot))