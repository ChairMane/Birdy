from data_holder import *
from prettytable import PrettyTable
import discord
import random

#TODO- Try accessing eBird API, for sightings. (Look into REST API)
#TODO- Make funny bird image function
#TODO- Look into maybe using ext.commands at one point
#TODO- Make command `<> <bird_found> <where>`
#TODO- Allow users to make lists of birds they have seen
#TODO- Make <> quiz function that tests user with bird image.

class birdyCommands:

    def __init__(self, brdy):
        self.brdy = brdy

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
    async def rand(self, content, image_dict, message):

        #If <> rand <shape_of_bird> was called, you would get only a random bird within
        #the shape of the bird category.
        if (len(content) > 1):
            family_name = ' '.join(content[1:]).lower()
            get_family = species_by_family[family_name]
            rand_bird = random.choice(get_family)

            name, species, desc, filename_list = image_dict[rand_bird]
            embed = discord.Embed(title='Name', description=species, color=0x6606BA)
            embed.add_field(name="Description", value=desc, inline=False)
            await self.brdy.send_file(message.channel, self.get_random(filename_list))
            await self.brdy.send_message(message.channel, embed=embed)

        #Otherwise just output a random bird from the entire dictionary
        else:
            rand_key = random.choice(list(image_dict))
            name, species, desc, filename_list = image_dict[rand_key]

            embed = discord.Embed(title='Name', description=species, color=0x6606BA)
            embed.add_field(name="Description", value=desc, inline=False)
            await self.brdy.send_file(message.channel, self.get_random(filename_list))
            await self.brdy.send_message(message.channel, embed=embed)

    #get_species() grabs a bird from the dictionary with the same name inputted by the
    #user. EXAMPLE: <> white crowned sparrow
    async def get_species(self, content, image_dict, message):

        usr_msg = ' '.join(content).lower()

        name, species, desc, filename_list = image_dict[usr_msg]
        embed = discord.Embed(title='Name', description=species, color=0x6606BA)
        embed.add_field(name="Description", value=desc, inline=False)
        await self.brdy.send_file(message.channel, self.get_random(filename_list))
        await self.brdy.send_message(message.channel, embed=embed)


    async def handle_command(self, content, message, image_dict, species_by_family):
        commands = ['rand', 'help']
        if len(content) < 2:
            await self.error_handle(message)
        elif content[1] == 'help':
            await self.command_list(message)
        elif content[1] == 'rand':
            await self.rand(content[1:], image_dict, message)
        elif content[1] in species_by_family:
            await self.list_birds(content, species_by_family, message)
        elif len(content) >= 2:
            await self.get_species(content[1:], image_dict, message)

    async def error_handle(self, message):
        await self.brdy.send_message(message.channel, "Invalid command entered. Please enter `<> help` for commands.")

    async def command_list(self, message):
        await self.brdy.send_message(message.author, help_message)

    def get_random(self, mylist):
        r = random.randrange(len(mylist))
        return mylist[r]