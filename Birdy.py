# https://github.com/Rapptz/discord.py/blob/async/examples/reply.py
import discord
import random
import json
from helpers import rand, handle_command

config = json.load(open('config.json'))

image_dict = {'white crowned sparrow' : ('Sparrow', 'White Crowned Sparrow','You’ll see White-crowned Sparrows low at the edges of brushy habitat, hopping on the ground or on branches usually below waist level. They’re also found in open ground (particularly on their breeding grounds) but typically with the safety of shrubs or trees nearby.',['Birds/Sparrow/White Crowned Sparrow/1.jpg', 'Birds/Sparrow/White Crowned Sparrow/2.jpg', 'Birds/Sparrow/White Crowned Sparrow/3.jpg'])
              ,'white throated sparrow' : ('Sparrow', 'White Throated Sparrow','White-throated Sparrows stay near the ground, scratching through leaves in search of food, often in flocks. You may see them low in bushes as well, particularly in spring when they eat fresh buds. White-throated Sparrows sing their distinctive songs frequently, even in winter.',['Birds/Sparrow/White Throated Sparrow/1.jpg', 'Birds/Sparrow/White Throated Sparrow/2.jpg', 'Birds/Sparrow/White Throated Sparrow/3.jpg'])
              ,'aberts towhee' : ('Sparrow', 'Aberts Towhee', 'A very large sparrow, Aberts Towhee inhabits riparian corridors in the Sonoran Desert of Arizona. Plain and rather secretive, Aberts Towhee stays in its breeding range year-round.', ['Birds/Sparrow/Aberts Towhee/1.jpg', 'Birds/Sparrow/Aberts Towhee/2.jpg', 'Birds/Sparrow/Aberts Towhee/3.jpg'])
              ,'american pipit' : ('Sparrow', 'American Pipit', 'The American Pipit is a small, slender, drab bird of open country. Although it appears similar to sparrows, it can be distinguished by its thin bill and its habit of bobbing its tail.', ['Birds/Sparrow/American Pipit/1.jpg', 'Birds/Sparrow/American Pipit/2.jpg', 'Birds/Sparrow/American Pipit/3.jpg'])
              ,'house finch' : ('Finch', 'House Finch', 'House Finches are gregarious birds that collect at feeders or perch high in nearby trees. When they’re not at feeders, they feed on the ground, on weed stalks, or in trees. They move fairly slowly and sit still as they shell seeds by crushing them with rapid bites. Flight is bouncy, like many finches.', ['Birds/Finch/House Finch/1.jpg', 'Birds/Finch/House Finch/2.jpg', 'Birds/Finch/House Finch/3.jpg'])
              }

client = discord.Client()


def get_random(mylist):
    r = random.randrange(len(mylist))
    return mylist[r]


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    usr_msg = ""
    content = message.content.split(' ')
    
    if '<>' not in content[0]:
        return
        #await client.send_message(message.channel, 'Invalid Command. Please use `<> help` for list of commands')

    if '<>' == content[0]:
        #send to handle_command() to do something with
        await handle_command(content, message, image_dict)
        
    '''usr_msg = ' '.join(content[1:]).lower() #Grabs everything after '<>' and inserts spaces before each element in content[]
    
    if usr_msg in image_dict.keys(): #If '<>' and 
        name, species, desc, filename_list = image_dict[usr_msg]
        embed = discord.Embed(title='Name', description=species, color=0x6606BA)
        embed.add_field(name="Description", value=desc, inline=False) 
        await client.send_file(message.channel, get_random(filename_list))
        await client.send_message(message.channel, embed=embed)    

    if '<>' in content and 'rand' in content:
        
        if usr_msg in list(image_dict.values())[0]:
            rand_key = random.choice(list(image_dict[usr_msg]))
            name, species, desc, filename_list = image_dict[rand_key]
            embed = discord.Embed(title='Name', description=species, color=0x6606BA)
            embed.add_field(name="Description", value=desc, inline=False) 
            await client.send_file(message.channel, get_random(filename_list))
            await client.send_message(message.channel, embed=embed) 
        else:
            rand_key = random.choice(list(image_dict))      
            name, species, desc, filename_list = image_dict[rand_key]
            embed = discord.Embed(title='Name', description=species, color=0x6606BA)
            embed.add_field(name="Description", value=desc, inline=False) 
            await client.send_file(message.channel, get_random(filename_list))
            await client.send_message(message.channel, embed=embed) '''



@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(config['token'])

