import discord
import json
from discord.ext import commands

config = json.load(open('config.json'))

bot = commands.Bot(command_prefix=['--', '––'], description='Birdy is a bot made for birders. EBird is used in this bot to look for sightings around the world.')
bot.remove_command('help')

extensions = ['birdyCommands']

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_member_join(member):
    server = member.server.id
    channels = member.server.channels
    if server != config['CSserver']:
        return

    ntsk_welcome_msg = await bot.wait_for_message(timeout=1, author=member.server.get_member(config['ntsk']))
    if ntsk_welcome_msg == None:
        welcome_message = config['welcome'].format(member.server.get_member(config['ntsk']).mention, member.mention)
        info = config['info']
    else:
        welcome_message = config['welcomeNAU'].format(member.mention)
        info = config['info']
    embed = discord.Embed(title='WELCOME!', description=welcome_message)
    embed.add_field(name='About us',value=info)
    await bot.send_message(member.server, embed=embed)

if __name__ == '__main__':

    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as error:
            print('{} cannot be loaded. [{}]'.format(Exception, error))


bot.run(config['token'])