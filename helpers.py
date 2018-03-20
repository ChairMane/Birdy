import discord
import random

client = discord.Client()

def get_random(mylist):
    r = random.randrange(len(mylist))
    return mylist[r]

@client.event
async def rand(content, image_dict, message):
    #if len(content) > 2:
    #    family_name = ' '.join(content[2:].lower()
    #else:
        rand_key = random.choice(list(image_dict))      
        name, species, desc, filename_list = image_dict[rand_key]
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

        
        
