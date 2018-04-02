from data_holder import *
import discord
import random

#TODO- Make `<> <shape_of_bird>` a command that gives the user a list of birds from that category
#TODO- Try accessing eBird API, for sightings. (Look into REST API)
#TODO- Make funny bird image function
#TODO- Look into refactoring code. Maybe use ext.commands at one point
#TODO- Make command `<> <bird_found> <where>`
#TODO- Allow users to make lists of birds they have seen

class birdyCommands:

    def __init__(self, brdy):
        self.brdy = brdy


    async def rand(self, content, image_dict, message):

        if (len(content) > 1):
            family_name = ' '.join(content[1:]).lower()
            get_family = species_by_family[family_name]
            rand_bird = random.choice(get_family)

            name, species, desc, filename_list = image_dict[rand_bird]
            embed = discord.Embed(title='Name', description=species, color=0x6606BA)
            embed.add_field(name="Description", value=desc, inline=False)
            await self.brdy.send_file(message.channel, self.get_random(filename_list))
            await self.brdy.send_message(message.channel, embed=embed)

        else:
            rand_key = random.choice(list(image_dict))
            name, species, desc, filename_list = image_dict[rand_key]

            embed = discord.Embed(title='Name', description=species, color=0x6606BA)
            embed.add_field(name="Description", value=desc, inline=False)
            await self.brdy.send_file(message.channel, self.get_random(filename_list))
            await self.brdy.send_message(message.channel, embed=embed)



    async def get_species(self, content, image_dict, message):

        usr_msg = ' '.join(content).lower()

        name, species, desc, filename_list = image_dict[usr_msg]
        embed = discord.Embed(title='Name', description=species, color=0x6606BA)
        embed.add_field(name="Description", value=desc, inline=False)
        await self.brdy.send_file(message.channel, self.get_random(filename_list))
        await self.brdy.send_message(message.channel, embed=embed)


    async def handle_command(self, content, message, image_dict):
        commands = ['rand', 'help']
        if len(content) < 2:
            await self.error_handle(message)
        elif content[1] == 'help':
            await self.command_list(message)
        elif content[1] == 'rand':
            await self.rand(content[1:], image_dict, message)
        elif len(content) >= 2:
            await self.get_species(content[1:], image_dict, message)

    async def error_handle(self, message):
        await self.brdy.send_message(message.channel, "Invalid command entered. Please enter `<> help` for commands.")

    async def command_list(self, message):
        await self.brdy.send_message(message.author, help_message)

    def get_random(self, mylist):
        r = random.randrange(len(mylist))
        return mylist[r]