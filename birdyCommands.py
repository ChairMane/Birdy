from data_holder import *
from eBirdAPI import *
import json
import discord
import random

#TODO- Try accessing eBird API, for sightings. (Look into REST API)
#TODO- Look into maybe using ext.commands at one point
#TODO- Make command `<> <bird_found> <where>`
#TODO- Allow users to make lists of birds they have seen
#TODO- Make <> quiz function that tests user with bird image.
#TODO- Look into sending bird calls and songs (Sent the same way images are uploaded)

birds = json.load(open('birdsDB.json'))
factlist = json.load(open('birdfacts.json'))
bird_e = Bird_e()

class birdyCommands:

    def __init__(self, brdy):
        self.brdy = brdy

    async def song(self, content, message):
        await self.brdy.send_file(message.channel, "Audio/Auks/Ancient Murrelet/song.mp3")

    async def facts(self, content, message):
        fact = factlist[str(random.randint(1,100))]
        embed = discord.Embed(title='Fact:', description=fact, color=0x6606BA)

        await self.brdy.send_message(message.channel, embed=embed)

    async def birbs(self, content, message):
        meme_index = random.randint(1,174)
        filename = "Memes/{}.jpg".format(meme_index)

        await self.brdy.send_file(message.channel, filename)

    async def get_recent(self, content, message):
        variables = ' '.join(content[2:])
        arguments = variables.split(' ')
        regional_code = ''
        maxResults = '25'
        back = ''

        if len(arguments) > 3:
            await self.brdy.send_message(message.channel, 'Too many arguments sent.')

        elif len(arguments) == 3:
            regional_code = arguments[0]
            maxResults = arguments[1]
            back = arguments[2]

        elif len(arguments) == 2:
            regional_code = arguments[0]
            maxResults = arguments[1]

        elif len(arguments) == 1:
            regional_code = arguments[0]

        observations = bird_e.get_recent_observation(regional_code, maxResults, back)
        embed = discord.Embed(title='Sightings:', description=observations, color=0x6606BA)
        await self.brdy.send_message(message.channel, embed=embed)

    #Grabs a list of birds from a category of shape.
    async def list_birds(self, content, species_by_family, message):
        birds = ""
        usr_msg = content[1].lower()
        bird_list = species_by_family[usr_msg.lower()]
        for i in range(0, len(bird_list)):
            if i % 3 == 0:
                birds += '\n'
            birds += '{}. '.format(i + 1) + '{message:{fill}{align}}'.format(message=bird_list[i], fill=' ', align='<25')
        await self.brdy.send_message(message.author, '```fix\n' + 'Below is the list of ' + usr_msg + 's:\n' + birds + '\n```')

    #rand() grabs a random bird from the dictionary image_dict and outputs
    #basic information about the random bird grabbed
    async def rand(self, content, message):

        #If <> rand <shape_of_bird> was called, you would get only a random bird within
        #the shape of the bird category.
        if (len(content) > 1):
            family_name = ' '.join(content[1:]).lower()
            get_family = species_by_family[family_name]
            rand_bird = random.choice(get_family)

            name, species, desc, filename_list = birds[rand_bird]
            embed = discord.Embed(title='Name', description=species, color=0x6606BA)
            embed.add_field(name="Description", value=desc, inline=False)

            await self.brdy.send_file(message.channel, self.get_random(filename_list))
            await self.brdy.send_message(message.channel, embed=embed)

        #Otherwise just output a random bird from the entire dictionary
        else:
            rand_key = random.choice(list(birds))
            name, species, desc, filename_list = birds[rand_key]

            embed = discord.Embed(title='Name', description=species, color=0x6606BA)
            embed.add_field(name="Description", value=desc, inline=False)

            await self.brdy.send_file(message.channel, self.get_random(filename_list))
            await self.brdy.send_message(message.channel, embed=embed)

    #get_species() grabs a bird from the dictionary with the same name inputted by the
    #user. EXAMPLE: <> white crowned sparrow
    async def get_species(self, content, message):

        usr_msg = ' '.join(content).lower()

        name, species, desc, filename_list = birds[usr_msg]
        embed = discord.Embed(title='Name', description=species, color=0x6606BA)
        embed.add_field(name="Description", value=desc, inline=False)

        await self.brdy.send_file(message.channel, self.get_random(filename_list))
        await self.brdy.send_message(message.channel, embed=embed)


    async def handle_command(self, content, message, species_by_family):
        commands = ['rand', 'help', 'birbs', 'fact', 'test', 'recent']
        usr_msg = ' '.join(content[1:]).lower()

        if content[1].lower() not in commands and usr_msg not in species_by_family and usr_msg not in birds:
            await self.error_handle(message)
        elif content[1].lower() == 'help':
            await self.command_list(message)
        elif content[1].lower() == 'rand':
            await self.rand(content[1:], message)
        elif content[1].lower() == 'birbs':
            await self.birbs(content[1:], message)
        elif content[1].lower() == 'fact':
            await self.facts(content[1:], message)
        elif content[1].lower() == 'test':
            await self.song(content[1:], message)
        elif content[1].lower() in species_by_family:
            await self.list_birds(content, species_by_family, message)
        elif content[1].lower() == 'recent':
            await self.get_recent(content, message)
        elif len(content) >= 2:
            await self.get_species(content[1:], message)

    async def error_handle(self, message):
        await self.brdy.send_message(message.channel, "Invalid command entered. Please enter `<> help` for commands.")

    async def command_list(self, message):
        await self.brdy.send_message(message.author, help_message)

    def get_random(self, mylist):
        r = random.randrange(len(mylist))
        return mylist[r]
