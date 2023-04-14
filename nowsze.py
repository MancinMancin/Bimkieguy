import discord
from discord.ext import commands
import random
import asyncio

from config import TOKEN

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if '<@&724869170734432258>' in message.content:
        await message.add_reaction('<:Tank:1095150384164634624>') 
        await message.add_reaction('<:Healer:1095151227379130418>') 
        await message.add_reaction('<:DPS:1095151144864579725>')
        await message.add_reaction('<:Keystone:1095145259903750265>')
      

def select_elements(list_1, list_2, list_3, list_4):
    while True:
        lis_1, lis_2, lis_3, lis_4 = list_1, list_2, list_3, list_4
        unique_1, unique_2, unique_3, unique_4 = None, None, None, None
        unique_4 = random.choice(list(set(lis_4)))
        while unique_4 not in lis_1 + lis_2 + lis_3:
            unique_4 = random.choice(list(set(lis_4)))
        lists_with_unique_4 = []
        if unique_4 in lis_1:
            lists_with_unique_4.append('list_1')
        if unique_4 in lis_2:
            lists_with_unique_4.append('list_2')
        if unique_4 in lis_3:
            lists_with_unique_4.append('list_3')

        selected_list = random.choice(lists_with_unique_4)
        if selected_list == 'list_1':
            unique_1 = unique_4
            lis_2 = [el for el in lis_2 if el != unique_1]
            lis_3 = [el for el in lis_3 if el != unique_1]
        if selected_list == 'list_2':
            unique_2 = unique_4
            lis_1 = [el for el in lis_1 if el != unique_2]
            lis_3 = [el for el in lis_3 if el != unique_2]
        if selected_list == 'list_3':
            unique_3 = [unique_4]
            list_3.remove(unique_4)
            lis_1 = [el for el in lis_1 if el != unique_4]
            lis_2 = [el for el in lis_2 if el != unique_4]
        

        if len(lis_1) >= 1 and unique_1 is None:
            unique_1 = random.choice(list(set(lis_1)))
            lis_2 = [el for el in lis_2 if el != unique_1]
            lis_3 = [el for el in lis_3 if el != unique_1]
        if len(lis_2) >= 1 and unique_2 is None:
            unique_2 = random.choice(list(set(lis_2)))
            lis_3 = [el for el in lis_3 if el != unique_2]
        if len(lis_3) >= 2 and unique_3 is None:
            unique_3 = random.sample(list(set(lis_3)), 2)
        elif len(lis_3) >= 1 and unique_3 is not None:
            unique_3.append(random.choice(list(set(lis_3))))
        else:
            try:
                if unique_3 is not None and len(unique_3) >= 1 and unique_4 not in list_3:
                    list_3.append(unique_4)
                    continue
            except:
                continue
        if not unique_1 or not unique_2 or not unique_3:
            continue
        return unique_1, unique_2, unique_3, unique_4

@bot.event
async def on_reaction_remove(reaction,user):
    if user.bot:
        return
    
    message_id = reaction.message.id
    message = reaction.message
    if message.content != '<@&724869170734432258>':
        return
    if message_id in message_users:

        role = None
        if str(reaction.emoji) == '<:Tank:1095150384164634624>':
            role = 'tanks'
        elif str(reaction.emoji) == '<:Healer:1095151227379130418>':
            role = 'healers'
        elif str(reaction.emoji) == '<:DPS:1095151144864579725>':
            role = 'dps'
        elif str(reaction.emoji) == '<:Keystone:1095145259903750265>':
            role = 'keystone'

        if role:
            if user in message_users[message_id][role]:
                message_users[message_id][role].remove(user)


message_users = {}

@bot.event
async def on_reaction_add(reaction, user):
    message_id = reaction.message.id
    message = reaction.message
    if user.bot:
        if message_id not in message_users:
                message_users[message_id] = {
                'lock': asyncio.Lock(),
                'tanks': [],
                'healers': [],
                'dps': [],
                'keystone': [],
                'sent': False
                }
                    
        return
    
    if message.content != '<@&724869170734432258>':
        return
    if message_id in message_users:
    
        role = None
        if str(reaction.emoji) == '<:Tank:1095150384164634624>':
            role = 'tanks'
        elif str(reaction.emoji) == '<:Healer:1095151227379130418>':
            role = 'healers'
        elif str(reaction.emoji) == '<:DPS:1095151144864579725>':
            role = 'dps'
        elif str(reaction.emoji) == '<:Keystone:1095145259903750265>':
            role = 'keystone'
        
        if role:
            if user not in message_users[message_id][role]:
                message_users[message_id][role].append(user)
        
        async with message_users[message_id]['lock']:
            if len(message_users[message_id]['tanks']) >= 1 and len(message_users[message_id]['healers']) >= 1 and len(message_users[message_id]['dps']) >=2 and len(set(message_users[message_id]['tanks'] + message_users[message_id]['healers'] + message_users[message_id]['dps'])) >= 4 and len(message_users[message_id]['keystone']) >= 1 and any(element in message_users[message_id]['keystone'] for element in message_users[message_id]['tanks'] + message_users[message_id]['healers'] + message_users[message_id]['dps']):
                if message_users[message_id]['sent'] == False:
                    await message.channel.send(f"Team can now be made")
                    message_users[message_id]['sent'] = True
                
                await asyncio.sleep(5)

                if len(message_users[message_id]['tanks']) >= 1 and len(message_users[message_id]['healers']) >= 1 and len(message_users[message_id]['dps']) >=2 and len(set(message_users[message_id]['tanks'] + message_users[message_id]['healers'] + message_users[message_id]['dps'])) >= 4 and len(message_users[message_id]['keystone']) >= 1 and any(element in message_users[message_id]['keystone'] for element in message_users[message_id]['tanks'] + message_users[message_id]['healers'] + message_users[message_id]['dps']):

                    tank_users, healer_users, dps_users, keystone_users = (select_elements(message_users[message_id]['tanks'], message_users[message_id]['healers'], message_users[message_id]['dps'], message_users[message_id]['keystone']))
                        
                    await message.channel.send(f"Keystone team:\n<:Tank:1095150384164634624> {tank_users.mention}\n<:Healer:1095151227379130418> {healer_users.mention}\n<:DPS:1095151144864579725> {dps_users[0].mention}\n<:DPS:1095151144864579725> {dps_users[1].mention}\n<:Keystone:1095145259903750265> {keystone_users.mention}\n```{tank_users.mention}\n{healer_users.mention}\n{dps_users[0].mention}\n{dps_users[1].mention}```")

                    tank_users = []
                    healer_users = []
                    dps_users = []
                    keystone_users = []
                    del message_users[message_id]
                        
                else:
                    await message.channel.send(f"Cannot form a team due to people unsigning.")
                    message_users[message_id]['sent'] = False
                
        
bot.run(TOKEN)