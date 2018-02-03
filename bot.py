import discord
from discord.ext import commands
import secrets
from config import IS_BOT

import traceback
from datetime import datetime
from random import seed, uniform

description = '''Serves events via 19hz.info'''

# this specifies what extensions to load when the infobot starts up
startup_extensions = ["info"]

infobot = commands.Bot(command_prefix='>', description=description)

@infobot.event
async def on_ready():
    seed(a=None)
    print('Logged in as')
    print(infobot.user.name)
    print('Servers: ' + ', '.join([str(s) for s in infobot.servers]))
    print('------')

@infobot.event
async def on_command(s, e):
    print("{0.name} used >{1} in {2.name} (Channel #{3})".format(e.message.author,s,e.message.server,e.message.channel))

@infobot.event
async def on_command_error(error,ctx):
    tb = "\n".join(traceback.format_tb(error.original.__traceback__))
    print("{}: {}\n{}".format(error.original.__class__.__name__,str(error),str(tb)))

@infobot.command()
async def load(extension_name : str):
    """Loads an extension."""
    try:
        infobot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await infobot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await infobot.say("{} loaded.".format(extension_name))

@infobot.command()
async def unload(extension_name : str):
    """Unloads an extension."""
    infobot.unload_extension(extension_name)
    await infobot.say("{} unloaded.".format(extension_name))

@infobot.command()
async def ti():
    '''
    Display the bot's time (PST)
    Usage: !ti
    '''
    now = datetime.now()
    return await infobot.say("Server time is %s:%s:%s PST  %s/%s/%s"
                           % (now.hour, now.minute, now.second, now.month,
                              now.day, now.year), delete_after=10)

@infobot.command()
async def rate(*args):
    '''
    Display the bot's time (PST)
    Usage: !ti
    '''
    if args:
        s = ' '.join(args)
        seed(s)
        number = round(uniform(1, 8), 1)
        return await infobot.say("Gr8 m8 I rate {}/8".format(number))

if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            infobot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    token = secrets.BOT_TOKEN if IS_BOT else secrets.USER_TOKEN
    infobot.run(token, bot=IS_BOT)
