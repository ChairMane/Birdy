# https://github.com/Rapptz/discord.py/blob/async/examples/reply.py
import discord
import random
import json
from birdyCommands import *
from data_holder import *

config = json.load(open('config.json'))

pfx = '<>'

class Birdy(discord.Client):

    async def on_ready(self):
        self.com = birdyCommands(self)
        print('Logged in as')
        print(brdy.user.name)
        print(brdy.user.id)
        print('------')

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author == brdy.user:
            return

        content = message.content.split(' ')

        if pfx != content[0]:
            return

        if pfx == content[0]:
            # send to birdyCommands.handle_command() to do something with
            await self.com.handle_command(content, message, image_dict, species_by_family)

brdy = Birdy()
brdy.run(config['token'])
