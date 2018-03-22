# https://github.com/Rapptz/discord.py/blob/async/examples/reply.py
import discord
import random
import json
from data_holder import *

config = json.load(open('config.json'))

client = discord.Client()

#rand() will grab a random bird from the image_dict dictionary, using a random key.
#For example, if you want a random bird, you write '<> rand'
@client.event
async def rand(content, image_dict, message):
    #list(image_dict.values())[0]
    '''if len(content) > 2:
        family_name = ' '.join(content[1:].lower()
        
        rand_key = random.choice(list(image_dict))      
        name, species, desc, filename_list = image_dict[rand_key]
        embed = discord.Embed(title='Name', description=species, color=0x6606BA)
        embed.add_field(name="Description", value=desc, inline=False) 
        await client.send_file(message.channel, get_random(filename_list))
        await client.send_message(message.channel, embed=embed)                
    else:'''
    rand_key = random.choice(list(image_dict))      
    name, species, desc, filename_list = image_dict[rand_key]
    embed = discord.Embed(title='Name', description=species, color=0x6606BA)
    embed.add_field(name="Description", value=desc, inline=False) 
    await client.send_file(message.channel, get_random(filename_list))
    await client.send_message(message.channel, embed=embed)

#This function is called when the user knows the name of the bird they want information about
#For example, if you want information on the white crowned sparrow, you write '<> white crowned sparrow'    
@client.event
async def get_species(content, image_dict, message):
    usr_msg = ' '.join(content[0:]).lower()
    print(usr_msg)
    name, species, desc, filename_list = image_dict[usr_msg]
    embed = discord.Embed(title='Name', description=species, color=0x6606BA)
    embed.add_field(name="Description", value=desc, inline=False) 
    await client.send_file(message.channel, get_random(filename_list))
    await client.send_message(message.channel, embed=embed) 
    
@client.event
async def handle_command(content, message, image_dict):

    if len(content) == 1:
        return "ERROR, MISSING COMMAND"
    elif content[1] == 'rand':
        await rand(content[1:], image_dict, message)
    elif content[1] != 'rand':
        await get_species(content[1:], image_dict, message)

def get_random(mylist):
    r = random.randrange(len(mylist))
    return mylist[r]


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    
    content = message.content.split(' ')
    
    if '<>' != content[0]:
        return
        #await client.send_message(message.channel, 'Invalid Command. Please use `<> help` for list of commands')

    if '<>' == content[0]:
        #send to handle_command() to do something with
        await handle_command(content, message, image_dict)
        

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(config['token'])

