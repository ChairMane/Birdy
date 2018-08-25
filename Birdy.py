import discord
import json
from discord.ext import commands

config = json.load(open('config.json'))

bot = commands.Bot(command_prefix='--', description='Birdy is a bot made for birders. EBird is used in this bot to look for sightings around the world.')
bot.remove_command('help')

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