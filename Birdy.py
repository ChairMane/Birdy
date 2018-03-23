# https://github.com/Rapptz/discord.py/blob/async/examples/reply.py
import discord
import random
import json
from data_holder import *

config = json.load(open('config.json'))

client = discord.Client()

#TODO-ERROR HANDLING LIKE SHOWING WHAT COMMANDS ARE AVAILABLE

#This gets printed out when only '<>' is sent.
@client.event
async def error_handle(message):
    await client.send_message(message.channel, "Invalid command entered. Please enter `<> help` for commands.")

@client.event
async def command_list(message):
    help_message = "```\n" \
                   "INFO: Creator of this bot is ChairMane: https://github.com/ChairMane/Birdy\n\n" \
                   "DESCRIPTION: Birdy is for those discord users who are interested\n" \
                   "in birds.\n\n" \
                   "COMMAND PREFIX: To be able to use the commands, '<>' must be\n" \
                   "present before any commands are used.\n\n" \
                   "Below are commands available:\n\n" \
                   "__________________________________________________________\n\n" \
                   "COMMAND:              <> <name_of_bird>\n" \
                   "EXAMPLES:             <> white crowned sparrow\n" \
                   "                      <> northern parula\n" \
                   "                      <> annas hummingbird\n" \
                   "DESCRIPTION: If you know the name of the bird you want,\n" \
                   "you can call this command to grab information on it.\n" \
                   "__________________________________________________________\n\n" \
                   "COMMAND:              <> rand\n" \
                   "DESCRIPTION: Use <> rand to grab information on a random\n" \
                   "within the Birdy database.\n" \
                   "__________________________________________________________\n\n" \
                   "COMMAND:              <> rand <shape_of_bird>\n" \
                   "EXAMPLES:             <> rand finch\n" \
                   "                      <> rand sparrow\n" \
                   "DESCRIPTION: If you want a random bird within a specific\n" \
                   "bird shape category, you call this command.\n" \
                   "__________________________________________________________\n\n" \
                   "COMMAND:              <> help\n" \
                   "DESCRIPTION: If you forget commands, you can call this\n" \
                   "command to get a list of commands.\n" \
                   "__________________________________________________________\n\n" \
                   "LIST OF CURRENT BIRD SHAPES:\n" \
                   "Sparrow, Finch, Warbler, Hummingbird.\n" \
                   "```"
    await client.send_message(message.author, help_message)

#rand() will grab a random bird from the image_dict dictionary, using a random key.
#For example, if you want a random bird, you write '<> rand'
@client.event
async def rand(content, image_dict, message):

    if (len(content) > 1):

        family_name = ' '.join(content[1:]).lower()
        get_family = species_by_family[family_name]
        rand_bird = random.choice(get_family)
        
        name, species, desc, filename_list = image_dict[rand_bird]
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
        await client.send_message(message.channel, embed=embed)


#This function is called when the user knows the name of the bird they want information about
#For example, if you want information on the white crowned sparrow, you write '<> white crowned sparrow'    
@client.event
async def get_species(content, image_dict, message):
    usr_msg = ' '.join(content).lower()
    print(usr_msg)
    name, species, desc, filename_list = image_dict[usr_msg]
    embed = discord.Embed(title='Name', description=species, color=0x6606BA)
    embed.add_field(name="Description", value=desc, inline=False) 
    await client.send_file(message.channel, get_random(filename_list))
    await client.send_message(message.channel, embed=embed) 

    
@client.event
async def handle_command(content, message, image_dict):
    commands = ['help', 'rand']
    if content[1] not in commands:
        await error_handle(message)
    elif content[1] == 'help':
        await command_list(message)
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

