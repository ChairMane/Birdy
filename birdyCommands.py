from data_holder import *
from eBirdAPI import *
from discord.ext import commands
from async_error_handler import *
import json
import discord
import random
import dateparser

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

    def __init__(self, bot):
        self.bot = bot

    #Testing this function out with one sample mp3
    #In the future, this function will return a song from a bird
    @commands.command(pass_context=True)
    async def song(self, ctx):
        await self.bot.send_file(ctx.message.channel, "Audio/Auks/Ancient Murrelet/song.mp3")

    #facts() just returns facts from a list of facts retrieved from https://www.factretriever.com/bird-facts
    @commands.command(pass_context=True)
    async def facts(self, ctx):
        fact = factlist[str(random.randint(1,100))]
        embed = discord.Embed(title='Fact:', description=fact, color=0x6606BA)

        await self.bot.say(ctx.message.channel, embed=embed)

    #Grabs random images from a meme folder.
    @commands.command(pass_context=True)
    async def birbs(self, ctx):
        meme_index = random.randint(1,174)
        filename = "Memes/{}.jpg".format(meme_index)

        await self.bot.send_file(ctx.message.channel, filename)

    #Using the eBird API, it grabs recent sightings from a specified location and region.
    @commands.command(pass_context=True, name='recent')
    async def get_recent(self, ctx, regional_code, maxResults='25', back=None):

        observations = bird_e.get_recent_observation(regional_code, maxResults, back)
        embed = discord.Embed(title='Sightings:', description=observations, color=0x6606BA)
        await self.bot.send_message(ctx.message.channel, embed=embed)

    #Same as the get_recent() function, but outputs notable sightings.
    @commands.command(pass_context=True, name='recent_notable')
    async def get_recent_notable(self, ctx, regional_code, maxResults='25', back=None):

        observations = bird_e.get_recent_notable_observation(regional_code, maxResults, back)
        embed = discord.Embed(title='Sightings:', description=observations, color=0x6606BA)
        await self.bot.send_message(ctx.message.channel, embed=embed)

    #Grabs info on specified species.
    @commands.command(pass_context=True, name='recent_species')
    async def get_recent_species(self, ctx, speciescode, regional_code, maxResults='25', back=None):

        observations = bird_e.get_recent_species_observation(regional_code, speciescode, maxResults, back)
        embed = discord.Embed(title='Sightings:', description=observations, color=0x6606BA)
        await self.bot.send_message(ctx.message.channel, embed=embed)

    #Assuming the user knows the latitude and longitude coordinates of the location they want
    #this function grabs those coordinates and finds observations with a radius (dist)
    @commands.command(pass_context=True, name='nearby')
    async def get_nearby(self, ctx, lat, lon, dist=None, maxResults='25', back=None):

        observations = bird_e.get_recent_nearby_observation(lat, lon, dist, maxResults, back)
        embed = discord.Embed(title='Sightings:', description=observations, color=0x6606BA)
        await self.bot.send_message(ctx.message.channel, embed=embed)

    #Assuming the user knows the latitude and longitude coordinates of the location they want
    #this function grabs those coordinates and finds observations with a radius (dist)
    @commands.command(pass_context=True, name='nearby_species')
    async def get_nearby_species(self, ctx, speciesCode, lat, lon, dist=None, maxResults='25', back=None):

        observations = bird_e.get_species_nearby_observation(speciesCode, lat, lon, dist, maxResults, back)
        embed = discord.Embed(title='Sightings:', description=observations, color=0x6606BA)

        await self.bot.send_message(ctx.message.channel, embed=embed)

    #Assuming the user knows the latitude and longitude coordinates of the location they want
    #this function grabs those coordinates and finds nearest observations with a radius (dist)
    @commands.command(pass_context=True, name='nearest')
    async def get_nearest_species(self, ctx, speciesCode, lat, lon, dist=None, maxResults='25', back=None):

        observations = bird_e.get_nearest_species_observation(speciesCode, lat, lon, dist, maxResults, back)
        embed = discord.Embed(title='Sightings:', description=observations, color=0x6606BA)

        await self.bot.send_message(ctx.message.channel, embed=embed)

    # Assuming the user knows the latitude and longitude coordinates of the location they want
    # this function grabs those coordinates and finds observations with a radius (dist)
    @commands.command(pass_context=True, name='nearby_notable')
    async def get_nearby_notable(self, ctx, lat, lon, dist=None, maxResults='25', back=None):

        observations = bird_e.get_nearby_notable_observation(lat, lon, dist, maxResults, back)
        embed = discord.Embed(title='Sightings:', description=observations, color=0x6606BA)
        await self.bot.send_message(ctx.message.channel, embed=embed)


    # Assuming the user knows the latitude and longitude coordinates of the location they want
    # this function grabs those coordinates and finds observations with a radius (dist)
    @commands.command(pass_context=True, name='historic')
    async def get_historic(self, ctx, regionCode, date, maxResults='25'):

        year = str(dateparser.parse(date).year)
        month = str(dateparser.parse(date).month)
        day = str(dateparser.parse(date).day)

        observations = bird_e.get_historic_observation(regionCode, year, month, day, maxResults)
        embed = discord.Embed(title='Sightings:', description=observations, color=0x6606BA)
        await self.bot.send_message(ctx.message.channel, embed=embed)

    #Grabs a list of birds from a category of shape.
    @commands.command(pass_context=True, name='list')
    async def list_birds(self, ctx, species):
        birds = ''
        bird_list = species_by_family[species.lower()]
        for i in range(0, len(bird_list)):
            if i % 3 == 0:
                birds += '\n'
            birds += '{}. '.format(i + 1) + '{message:{fill}{align}}'.format(message=bird_list[i], fill=' ', align='<25')
        await self.bot.send_message(ctx.message.author, '```fix\n' + 'Below is the list of ' + species + 's:\n' + birds + '\n```')

    #rand() grabs a random bird from the dictionary image_dict and outputs
    #basic information about the random bird grabbed
    @commands.command(pass_context=True)
    async def rand(self, ctx, family_name=''):

        #If <> rand <shape_of_bird> was called, you would get only a random bird within
        #the shape of the bird category.
        if (len(family_name) > 0):
            #family_name = ' '.join(content[1:]).lower()
            get_family = species_by_family[family_name.lower()]
            rand_bird = random.choice(get_family)

            name, species, desc, filename_list = birds[rand_bird]
            embed = discord.Embed(title='Name', description=species, color=0x6606BA)
            embed.add_field(name="Description", value=desc, inline=False)

            await self.bot.send_file(ctx.message.channel, self.get_random(filename_list))
            await self.bot.send_message(ctx.message.channel, embed=embed)

        #Otherwise just output a random bird from the entire dictionary
        else:
            rand_key = random.choice(list(birds))
            name, species, desc, filename_list = birds[rand_key]

            embed = discord.Embed(title='Name', description=species, color=0x6606BA)
            embed.add_field(name="Description", value=desc, inline=False)

            await self.bot.send_file(ctx.message.channel, self.get_random(filename_list))
            await self.bot.send_message(ctx.message.channel, embed=embed)

    #get_species() grabs a bird from the dictionary with the same name inputted by the
    #user. EXAMPLE: <> white crowned sparrow
    @commands.command(pass_context=True, name='bird')
    async def get_species(self, ctx, *bird_name):

        bird = ' '.join(bird_name)
        name, species, desc, filename_list = birds[bird.lower()]
        embed = discord.Embed(title='Name', description=species, color=0x6606BA)
        embed.add_field(name="Description", value=desc, inline=False)

        await self.bot.send_file(ctx.message.channel, self.get_random(filename_list))
        await self.bot.send_message(ctx.message.channel, embed=embed)

    @commands.command(pass_context=True, name='info')
    async def command_list(self, ctx):
        await self.bot.send_message(ctx.message.author, help_message)

    def get_random(self, mylist):
        r = random.randrange(len(mylist))
        return mylist[r]

    async def on_command_error(self, error, ctx):
        if isinstance(error, commands.CommandNotFound):
            await self.bot.send_message(ctx.message.channel, 'Command not found. Use `--info` for more information.')

def setup(bot):
    bot.add_cog(birdyCommands(bot))