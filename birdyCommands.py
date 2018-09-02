from data_holder import *
from eBirdAPI import *
from discord.ext import commands
from async_error_handler import *
from google_images_download import google_images_download
from difflib import SequenceMatcher
import string
import sqlite3
import json
import discord
import random
import dateparser

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
        """
        This command does not work currently. It's a test command, with
        an Ancient Murrelet song.
        """
        await self.bot.send_file(ctx.message.channel, "Audio/Auks/Ancient Murrelet/song.mp3")

    #facts() just returns facts from a list of facts retrieved from https://www.factretriever.com/bird-facts
    @commands.command()
    async def facts(self):
        """
        Returns a random fact about birds.

        `EXAMPLE`:
        ```--facts```
        """
        fact = factlist[str(random.randint(1,100))]
        embed = discord.Embed(title='Fact:', description=fact, color=0x6606BA)
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    async def bird(self, ctx, *name):
        """
        For when you know the bird name, you can use this instead of rand.
        ```--bird <name>```

        `EXAMPLE`:
        ```--bird white crowned sparrow``` -> Returns white crowned sparrow image and info.

        `name`:             Name of the species

        `return`:           An image of said bird and information on it.
        """
        response = google_images_download.googleimagesdownload()  # class instantiation
        birdname = ' '.join(name)
        want = self.get_name('Birds.db', birdname)
        max = 0
        correctname = ''
        for names in want:
            if self.similar(birdname, names[0]) > max:
                max = self.similar(birdname, names[0])
                correctname = names[0]
        if max >= 0.80:
            arguments = {"keywords": correctname, "safe_search": True, "metadata": False, "limit": 5, "size": ">800*600",
                         "format": "jpg", "no_directory": True, "output_directory": "birdy"}
        elif max > 0.70 and max < 0.80:
            await self.bot.say('Did you mean: `' + correctname + '`?')
        else:
            await self.bot.say('Not a bird.')

        paths = response.download(arguments)  # passing the arguments to the function
        links = []

        for dict in paths:
            links.append(dict['image_link'])

        image_url = self.get_random(links)

        embed = discord.Embed(title='Name', description=correctname.title())
        embed.set_image(url=image_url)
        #embed.add_field(name=correctname, inline=False)
        await self.bot.say(embed=embed)

    #Grabs random images from a meme folder.
    @commands.command(pass_context=True)
    async def birbs(self, ctx):
        """
        Returns a random bird meme.

        `EXAMPLE`:
        ```--birbs```
        """
        meme_index = random.randint(1,174)
        filename = "Memes/{}.jpg".format(meme_index)

        await self.bot.send_file(ctx.message.channel, filename)

    #Using the eBird API, it grabs recent sightings from a specified location and region.
    @commands.command(pass_context=True)
    async def recent(self, ctx, regional_code, maxResults='25', back=None):
        """
        Using the eBird API, a list of recent sightings are returned from specified location.
        ```--recent <regional_code> [maxResults='25'] [back=None]```

        `EXAMPLE`:
        ```--recent US-CA 25 30```\n --> Looks in California, Returns 25 results, back 30 days.

        `regional_code`: `<country>-<state/province>-<county_number>`

        `maxResults`: How many results wanted. May not return over 25.

        `back`: How many days you want to go back. Max is 30 days.

        `return`: List of sightings.
        """

        observations = bird_e.get_recent_observation(regional_code, maxResults, back)
        embed = discord.Embed(title='Sightings:', description=observations, color=0x6606BA)
        await self.bot.send_message(ctx.message.channel, embed=embed)

    #Same as the get_recent() function, but outputs notable sightings.
    @commands.command(pass_context=True)
    async def recent_notable(self, ctx, regional_code, maxResults='25', back=None):
        """
        Using the eBird API, a list of recent and notable sightings are returned from a specified location.
        ```--recent_notable <regional_code> [maxResults='25'] [back=None]```

        `EXAMPLE`:
        ```--recent_notable JP 30``` -> Looks in Japan, returns 30 results

        `regional_code`:  `<country>-<state/province>-<county_number>`

        `maxResults`:     How many results wanted. May not return over 25.

        `back`:           How many days you want to go back. Max is 30 days.

        `return`:         List of sightings.
        """

        observations = bird_e.get_recent_notable_observation(regional_code, maxResults, back)
        embed = discord.Embed(title='Sightings:', description=observations, color=0x6606BA)
        await self.bot.send_message(ctx.message.channel, embed=embed)

    #Grabs info on specified species.
    @commands.command(pass_context=True)
    async def recent_species(self, ctx, speciescode, regional_code, maxResults='25', back=None):
        """
        Using the eBird API, a list of recent species sightings are returned from a specified location.
        ```--recent_species <speciescode> <regional_code> [maxResults='25'] [back=None]```

        `EXAMPLE`:
        ```--recent_species amekes US-NY``` -> Looks in USA-New York for American Kestrels

        `speciescode`:    Six letter abbreviation of species.
                          Two names, take first three letters of each name.
                          Three names, first two letters of first, first letter of second and first three letters of last.
                          Four names, first letter of first three names, and first three letters of last name.

        `Examples`:       Mourning Dove -> `moudov`
                          Violet-Green Swallow -> `vigswa`
                          Grey-Crowned Rosy Finch -> `gcrfin`

        `regional_code`:  `<country>-<state/province>-<county_number>`

        `maxResults`:     How many results wanted. May not return over 25.

        `back`:           How many days you want to go back. Max is 30 days.

        `return`:         List of sightings.
        """

        observations = bird_e.get_recent_species_observation(regional_code, speciescode, maxResults, back)
        embed = discord.Embed(title='Sightings:', description=observations, color=0x6606BA)
        await self.bot.send_message(ctx.message.channel, embed=embed)

    #Assuming the user knows the latitude and longitude coordinates of the location they want
    #this function grabs those coordinates and finds observations with a radius (dist)
    @commands.command(pass_context=True)
    async def nearby(self, ctx, lat, lon, dist=None, maxResults='25', back=None):
        """
        Using the eBird API, a list of sightings near the coordinate given are returned.
        ```--nearby <lat> <lon> [dist=None] [maxResults='25'] [back=None]```

        `EXAMPLE`:
        ```--nearby 45.18222 -116.1235 50``` -> Looks at these coordinates with a radius of 50 kilometers.

        `lat`:            Latitude coordinate of wanted location.

        `lon`:            Longitude coordinate of wanted location.

        `dist`:           Radius in kilometers. Max is 50km.

        `maxResults`:     How many results wanted. May not return over 25.

        `back`:           How many days you want to go back. Max is 30 days.

        `return`:         List of sightings.
        """

        observations = bird_e.get_recent_nearby_observation(lat, lon, dist, maxResults, back)
        embed = discord.Embed(title='Sightings:', description=observations, color=0x6606BA)
        await self.bot.send_message(ctx.message.channel, embed=embed)

    #Assuming the user knows the latitude and longitude coordinates of the location they want
    #this function grabs those coordinates and finds observations with a radius (dist)
    @commands.command(pass_context=True)
    async def nearby_species(self, ctx, speciesCode, lat, lon, dist=None, maxResults='25', back=None):
        """
        Using the eBird API, a list of specificed species found at the specified coordinates is returned.
        ```--nearby_species <speciesCode> <lat> <lon> [dist=None] [maxResults='25'] [back=None]```

        `EXAMPLE`:
        ```--nearby_species cangoo 45.18222 -116.1235``` -> looks for a Canada Goose at these coordinates

        `speciesCode`:  Six letter abbreviation of species.
                        Two names, take first three letters of each name.
                        Three names, first two letters of first, first letter of second and first three letters of last.
                        Four names, first letter of first three names, and first three letters of last name.

        `Examples`:     Mourning Dove -> `moudov`
                        Violet-Green Swallow -> `vigswa`
                        Grey-Crowned Rosy Finch -> `gcrfin`

        `lat`:            Latitude coordinate of wanted location.

        `lon`:            Longitude coordinate of wanted location.

        `dist`:           Radius in kilometers. Max is 50km.

        `maxResults`:     How many results wanted. May not return over 25.

        `back`:           How many days you want to go back. Max is 30 days.

        `return`:         List of sightings.
        """

        observations = bird_e.get_species_nearby_observation(speciesCode, lat, lon, dist, maxResults, back)
        embed = discord.Embed(title='Sightings:', description=observations, color=0x6606BA)

        await self.bot.send_message(ctx.message.channel, embed=embed)

    #Assuming the user knows the latitude and longitude coordinates of the location they want
    #this function grabs those coordinates and finds nearest observations with a radius (dist)
    @commands.command(pass_context=True)
    async def nearest(self, ctx, speciesCode, lat, lon, dist=None, maxResults='25', back=None):
        """
        A list of species found nearest the specified coordinates is returned.
        ```--nearest <speciesCode> <lat> <lon> [dist=None] [maxResults='25'] [back=None]```

        `EXAMPLE`:
        ```nearest houspa 32.523309 -89.710361``` -> Looks for nearest house sparrow sighting

        `speciesCode`:    Six letter abbreviation of species.
                          Two names, take first three letters of each name.
                          Three names, first two letters of first, first letter of second and first three letters of last.
                          Four names, first letter of first three names, and first three letters of last name.

        `Examples`:       Mourning Dove -> moudov,
                          Violet-Green Swallow -> vigswa
                          Grey-Crowned Rosy Finch -> gcrfin

        `lat`:            Latitude coordinate of wanted location.

        `lon`:            Longitude coordinate of wanted location.

        `dist`:           Radius in kilometers. Max is 50km.

        `maxResults`:     How many results wanted. May not return over 25.

        `back`:           How many days you want to go back. Max is 30 days.

        `return`:         List of sightings.
        """

        observations = bird_e.get_nearest_species_observation(speciesCode, lat, lon, dist, maxResults, back)
        embed = discord.Embed(title='Sightings:', description=observations, color=0x6606BA)

        await self.bot.send_message(ctx.message.channel, embed=embed)

    # Assuming the user knows the latitude and longitude coordinates of the location they want
    # this function grabs those coordinates and finds observations with a radius (dist)
    @commands.command(pass_context=True)
    async def nearby_notable(self, ctx, lat, lon, dist=None, maxResults='25', back=None):
        """
        A list of notable sightings near the specified coordinates is returned.
        ```--nearby_notable <lat> <lon> [dist=None] [maxResults='25'] [back=None]```

        `EXAMPLE`:
        ```--nearby_notable 32.523309 -89.710361 42``` -> Looks 42km out from the coordinate

        `lat`:            Latitude coordinate of wanted location.

        `lon`:            Longitude coordinate of wanted location.

        `dist`:           Radius in kilometers. Max is 50km.

        `maxResults`:     How many results wanted. May not return over 25.

        `back`:           How many days you want to go back. Max is 30 days.

        `return`:         List of sightings.
        """

        observations = bird_e.get_nearby_notable_observation(lat, lon, dist, maxResults, back)
        embed = discord.Embed(title='Sightings:', description=observations, color=0x6606BA)
        await self.bot.send_message(ctx.message.channel, embed=embed)


    # Assuming the user knows the latitude and longitude coordinates of the location they want
    # this function grabs those coordinates and finds observations with a radius (dist)
    @commands.command(pass_context=True)
    async def historic(self, ctx, regionCode, date, maxResults='25'):
        """
        A list of sightings on a specified date and region.
        ```--historic <regionCode> <date> [maxResults='25']```

        `EXAMPLE`:
        ```--historic AU 5/6/2015``` -> Looks in Australia for sightings on 5/6/2015

        `regionCode`:  `<country>-<state/province>-<county_number>`

        `date`:           Date can be in mm-dd-yyyy or mm/dd/yyyy format. Earliest year is 1800.

        `maxResults`:     How many results wanted. May not return over 25.

        `return`:         List of sightings.
        """

        year = str(dateparser.parse(date).year)
        month = str(dateparser.parse(date).month)
        day = str(dateparser.parse(date).day)

        observations = bird_e.get_historic_observation(regionCode, year, month, day, maxResults)
        embed = discord.Embed(title='Sightings:', description=observations, color=0x6606BA)
        await self.bot.send_message(ctx.message.channel, embed=embed)

    # Assuming the user knows the latitude and longitude coordinates of the location they want
    # this function grabs those coordinates and finds observations with a radius (dist)
    @commands.command(pass_context=True)
    async def top100(self, ctx, regionCode, date):
        """
        A list of the top 100 users of the specified date is returned. Whoever has most species sighted is on the list.
        ```--top100 <regionCode> <date>```

        `EXAMPLE`:
        ```--top100 IE 4/5/2006``` -> Looks in Ireland to find out who was in the top 100 on 4/5/2006

        `regionCode`:  `<country>-<state/province>-<county_number>`

        `date`:        Date can be in mm-dd-yyyy or mm/dd/yyyy format. Earliest year is 1800.

        `return`:      A list of People who ranked top 100.
        """


        year = str(dateparser.parse(date).year)
        month = str(dateparser.parse(date).month)
        day = str(dateparser.parse(date).day)

        observations = bird_e.get_top_100(regionCode, year, month, day)
        embed = discord.Embed(title='Top 100 users:', description=observations, color=0x6606BA)
        await self.bot.send_message(ctx.message.channel, embed=embed)


    # Assuming the user knows the latitude and longitude coordinates of the location they want
    # this function grabs those coordinates and finds observations with a radius (dist)
    @commands.command(pass_context=True)
    async def stats(self, ctx, regionCode, date):
        """
        Grabs stats from specified date.
        ```--stats <regionCode> <date>```

        `EXAMPLE`:
        ```--stats MX 1/7/2001``` -> Looks in Mexico to find out how many checklists created, species sighted and contributors on 1/7/2001

        `regionCode`:  `<country>-<state/province>-<county_number>`

        `date`:        Date can be in mm-dd-yyyy or mm/dd/yyyy format. Earliest year is 1800.

        `return`:      Stats for checklists created, species sighted and how many people contributed
        """

        year = str(dateparser.parse(date).year)
        month = str(dateparser.parse(date).month)
        day = str(dateparser.parse(date).day)

        observations = bird_e.get_stats(regionCode, year, month, day)
        embed = discord.Embed(title='Stats for {}/{}/{}:'.format(month, day, year), description=observations, color=0x6606BA)
        await self.bot.send_message(ctx.message.channel, embed=embed)


    # Assuming the user knows the latitude and longitude coordinates of the location they want
    # this function grabs those coordinates and finds observations with a radius (dist)
    @commands.command(pass_context=True)
    async def adjacent_regions(self, ctx, regionCode):
        """
        Finds region codes near your region.
        ```--adjacent_regions <regionCode>```

        `EXAMPLE`:
        ```--adjacent_regions US-CA``` -> Returns regions next to California.

        `regionCode`:  `<country>-<state/province>-<county_number>`

        `return`:      List of adjacent regions and their region codes.
        """
        observations = bird_e.get_adjacent_region(regionCode)
        embed = discord.Embed(title='Adjacent regions to {}'.format(regionCode), description=observations, color=0x6606BA)
        await self.bot.send_message(ctx.message.channel, embed=embed)


    #Grabs a list of birds from a category of shape.
    @commands.command(pass_context=True)
    async def list(self, ctx, species):
        """
        This is a older command that may be discontinued. Currently supposed to list birds available in database.
        ```--list <species>```

        `EXAMPLE`:
        ```--list finch``` -> Returns a list of all available finches in database. May be wrong.

        `species`:      Supposed to be bird shape.

        `return`:       Sends a direct message with birds available.
        """

        birds = ''
        bird_list = species_by_family[species.lower()]
        for i in range(0, len(bird_list)):
            if i % 3 == 0:
                birds += '\n'
            birds += '{}. '.format(i + 1) + '{message:{fill}{align}}'.format(message=bird_list[i], fill=' ', align='<25')
        await self.bot.send_message(ctx.message.author, '```fix\n' + 'Below is the list of ' + species + 's:\n' + birds + '\n```')

    #rand() grabs a random bird from the dictionary image_dict and outputs
    #basic information about the random bird grabbed
    @commands.command()
    async def rand(self):
        """
        For grabbing random bird images and information.
        ```--rand```

        `EXAMPLE`:
        ```--rand``` -> Returns a random bird.

        `return`:        A random bird image and information on that bird.
        """

        response = google_images_download.googleimagesdownload()  # class instantiation
        want = self.get_rand_name('Birds.db')
        name = self.get_random(want)
        arguments = {"keywords": name[0], "safe_search": True, "metadata": False, "limit": 5, "size": ">1024*768",
                     "format": "jpg", "no_directory": True, "output_directory": "birdy"}

        paths = response.download(arguments)  # passing the arguments to the function
        links = []

        for dict in paths:
            links.append(dict['image_link'])

        image_url = self.get_random(links)

        embed = discord.Embed(title='Name', description=name[0].title())
        embed.set_image(url=image_url)
        #embed.add_field(name=correctname, inline=False)
        await self.bot.say(embed=embed)

    def get_random(self, mylist):
        r = random.randrange(len(mylist))
        return mylist[r]

    async def on_command_error(self, error, ctx):
        if isinstance(error, commands.CommandNotFound):
            await self.bot.send_message(ctx.message.channel, 'Command not found. Use `--help` for more information.')

    def similar(self, a, b):
        return SequenceMatcher(None, a, b).ratio()

    def get_name(self, database_file, bird):

        connection = sqlite3.connect(database_file)
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM {}".format(bird[0]))
        want = result.fetchall()
        cursor.close()
        connection.close()

        return want

    def get_rand_name(self, database_file):
        letters = list(string.ascii_lowercase)
        rand_letter = self.get_random(letters)
        connection = sqlite3.connect(database_file)
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM {}".format(rand_letter))
        want = result.fetchall()
        cursor.close()
        connection.close()

        return want

    @commands.command(pass_context=True)
    async def help(self, ctx, arg=None):
        coms = set(self.bot.commands.keys())

        if arg in coms:
            wt = self.bot.get_command(arg).help

        if arg == None:

            embed = discord.Embed(title='Help', description='Commands', colour=discord.Colour.purple())

            embed.set_author(name="Birdy", url="https://github.com/ChairMane/Birdy", icon_url="https://avatars1.githubusercontent.com/u/19229124?s=400&u=d98831706311ca2f43bbf12187119ff62d80bd18&v=4")

            embed.add_field(name='facts', value='Returns random bird fact.', inline=True)
            embed.add_field(name='birbs', value='Returns random bird meme.', inline=True)
            embed.add_field(name='list', value='Returns list of bird family.', inline=True)
            embed.add_field(name='bird', value='Returns the bird asked for.', inline=True)
            embed.add_field(name='rand', value='Returns random bird.', inline=True)
            embed.add_field(name='recent', value='Returns recent sighting.', inline=True)
            embed.add_field(name='nearby', value='Returns nearby sighting.', inline=True)
            embed.add_field(name='nearby_species', value='Returns nearby species.', inline=True)
            embed.add_field(name='nearby_notable', value='Returns notable nearby sighting.', inline=True)
            embed.add_field(name='nearest', value='Returns nearest sighting.', inline=True)
            embed.add_field(name='historic', value='Returns historic sighting.', inline=True)
            embed.add_field(name='top100', value='Returns top 100 users.', inline=True)
            embed.add_field(name='stats', value='Returns number of species sighted.', inline=True)
            embed.add_field(name='adjacent_regions', value='Returns region codes.', inline=True)
            embed.add_field(name='recent_notable', value='Returns notable recent sighting.', inline=True)
            embed.add_field(name='recent_species', value='Returns recent species sighting.', inline=True)

        else:
            embed = discord.Embed(title=arg, description=wt, colour=discord.Colour.purple())
            embed.set_author(name="Birdy", url="https://github.com/ChairMane/Birdy", icon_url="https://avatars1.githubusercontent.com/u/19229124?s=400&u=d98831706311ca2f43bbf12187119ff62d80bd18&v=4")

        await self.bot.say(embed=embed)


def setup(bot):
    bot.add_cog(birdyCommands(bot))
