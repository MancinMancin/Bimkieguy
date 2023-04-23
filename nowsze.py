import discord
from discord.ext import commands
import random
import asyncio
import json
import re

from config import TOKEN

bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())

with open('keys.json', 'r') as f:
    keystones = json.load(f)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if '<@&989535345370628126>' in message.content and message.channel.id == 736245738295656468:
        await message.add_reaction('<:Tank:1095150384164634624>') 
        await message.add_reaction('<:Healer:1095151227379130418>') 
        await message.add_reaction('<:DPS:1095151144864579725>')
        await message.add_reaction('<:Keystone:1095145259903750265>')
        await message.add_reaction('<:Muslim_Uncle_Pepe:1098289343627526266>')
    await kielce(message)
    await on_keystone_message(message)
    await bot.process_commands(message)
      

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
    if message.content != '<@&989535345370628126>':
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
    
    if message.content != '<@&989535345370628126>':
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
        elif str(reaction.emoji) == '<:Muslim_Uncle_Pepe:1098289343627526266>':
            await message.channel.send(f'Kazzakstan took the boost {message.jump_url}')
            del message_users[message_id]
            return
        
        if role:
            if user not in message_users[message_id][role]:
                message_users[message_id][role].append(user)
        
        async with message_users[message_id]['lock']:
            if len(message_users[message_id]['tanks']) >= 1 and len(message_users[message_id]['healers']) >= 1 and len(message_users[message_id]['dps']) >=2 and len(set(message_users[message_id]['tanks'] + message_users[message_id]['healers'])) >=2 and len(set(message_users[message_id]['tanks'] + message_users[message_id]['healers'] + message_users[message_id]['dps'])) >= 4 and len(message_users[message_id]['keystone']) >= 1 and any(element in message_users[message_id]['keystone'] for element in message_users[message_id]['tanks'] + message_users[message_id]['healers'] + message_users[message_id]['dps']):
                if message_users[message_id]['sent'] == False:
                    await message.channel.send(f"Team can now be made")
                    message_users[message_id]['sent'] = True
                
                await asyncio.sleep(5)

                if len(message_users[message_id]['tanks']) >= 1 and len(message_users[message_id]['healers']) >= 1 and len(message_users[message_id]['dps']) >=2 and len(set(message_users[message_id]['tanks'] + message_users[message_id]['healers'])) >=2 and len(set(message_users[message_id]['tanks'] + message_users[message_id]['healers'] + message_users[message_id]['dps'])) >= 4 and len(message_users[message_id]['keystone']) >= 1 and any(element in message_users[message_id]['keystone'] for element in message_users[message_id]['tanks'] + message_users[message_id]['healers'] + message_users[message_id]['dps']):

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
                

@bot.event
async def kielce(message):
    if "kielce" in message.content.lower():
        await message.channel.send(f'Czy to jest boss?')
    if "jestem" in message.content.lower():
        await message.channel.send(f'Jest Dawer?')


@bot.event
async def on_keystone_message(message):
    unrecognized_dungeons = False
    if message.author.bot:
        return
    if message.channel.id == 1077890228854988860:
        pattern = r'^(\w+) - \[Keystone: (.+) \((\d+)\)\]$'
        for line in message.content.split('\n'):
            match = re.match(pattern, line)
            if match:
                key_name = match.group(1)
                dungeon_name = match.group(2)
                dungeon_level = match.group(3)

                if dungeon_name not in ['Court of Stars', 'The Azure Vault', 'The Nokhud Offensive', 'Halls of Valor', 'Algeth\'ar Academy', 'Temple of the Jade Serpent', 'Shadowmoon Burial Grounds', 'Ruby Life Pools']:
                    unrecognized_dungeons = True
                    continue
                for dungeon, data in keystones.items():
                    if key_name in data and dungeon != dungeon_name:
                        data.pop(key_name)
                
                keystones.setdefault(dungeon_name, {})
                keystones[dungeon_name][key_name] = dungeon_level

                with open("keys.json", "w") as f:
                    json.dump(keystones, f)
                
                for line in message.content.split('\n'):
                    match = re.match(pattern, line)
        if match:
            if unrecognized_dungeons == True:
                await message.channel.send(f'Dungeons provided not recognized')
                return
            key_name = match.group(1)
            if key_name in keystones[dungeon_name]:
                await message.delete()


@bot.command()
async def keys(ctx, *, arg=None):

    if ctx.channel.id != 1077890228854988860:
        return
    abbreviations = {
    'cos': 'Court of Stars',
    'av': 'The Azure Vault',
    'no': 'The Nokhud Offensive',
    'hov': 'Halls of Valor',
    'aa': 'Algeth\'ar Academy',
    'tjs': 'Temple of the Jade Serpent',
    'sbg': 'Shadowmoon Burial Grounds',
    'rlp': 'Ruby Life Pools',
}
    matching_keys = []
    message_to_send = []
    if arg is None:
        if len(keystones) > 0:
            for key, data in keystones.items():
                for keyholder, level in data.items():
                    matching_keys.append(f'{keyholder} - [Keystone: {key} ({level})]')
            if matching_keys:
                message_to_send = '\n'.join(matching_keys)
                await ctx.send(message_to_send)
        else:
            await ctx.send(f'There are no keys yet')
    elif arg.lower() == 'reset':
        keystones.clear()
        with open("keys.json", "w") as f:
            json.dump(keystones, f)
        await ctx.send("Key list reset")
    elif arg.lower() in map(str.lower, abbreviations.keys()) or arg.lower() in map(str.lower, abbreviations.values()):
        found_keys = {}
        key = abbreviations.get(arg.lower()) or [v for _, v in abbreviations.items() if v.lower() == arg.lower()][0]
        found_keys = keystones.get(key, {})
        if found_keys:
            for keyholder, level in found_keys.items():
                matching_keys.append(f'{keyholder} - [Keystone: {key} ({level})]')
            if matching_keys:
                message_to_send = '\n'.join(matching_keys)
                await ctx.send(message_to_send)
        else:
            await ctx.send(f'There are no keys for {key}')
    elif any(arg.lower() in str(val).lower() for _, val in keystones.items()):
        for key, data in keystones.items():
            for keyholder, level in data.items():
                if keyholder.lower() == arg.lower():
                    matching_keys.append(f'{keyholder} - [Keystone: {key} ({level})]')
        if matching_keys:
            message_to_send = '\n'.join(matching_keys)
            await ctx.send(message_to_send)
    elif arg.lower() == 'abbr':
        abbreviations_text = '\n'.join([f'"{key}" for {value}' for key, value in abbreviations.items()])
        await ctx.send(f'{abbreviations_text}')
    else:
        await ctx.send(f'Keyholder is absent in the list, or dungeon provided is invalid, check "/keys abbr"')
                       
        
bot.run(TOKEN)