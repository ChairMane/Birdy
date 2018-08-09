# https://github.com/Rapptz/discord.py/blob/async/examples/reply.py
import discord
import random
import json
from birdyCommands import *
from data_holder import *
from discord.ext import commands

config = json.load(open('config.json'))

bot = commands.Bot(command_prefix='--')

extensions = ['birdyCommands']

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as error:
            print('{} cannot be loaded. [{}]'.format(Exception, error))

bot.run(config['token'])