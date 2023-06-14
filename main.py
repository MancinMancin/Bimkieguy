import discord
from discord.ext import commands
import random
import asyncio
import json
import re
import requests
import time
import schedule
import datetime
import os
from dungeon_guides import dungeon_guides

from config import TOKEN

bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())
bot.remove_command("help")

with open('keys.json', 'r') as f:
    keystones = json.load(f)

@bot.tree.command(description="Shows help")
async def help(interaction: discord.Interaction):
    name = "Bimkie Guy commands"
    url = "https://i.imgur.com/Ctg5Poz.jpg"
    color = "#f9b4d4"
    fields = {
        "Signup Event": ("🔸/signups <day> <time> <additonal info>", False),
        "Keys Storage": ("🔸/keys\n"
            "🔸/keys <dungeon>\n"
            "🔸/keys <character>\n"
            "🔸/keys <user ping>\n"
            "🔸/keys <level>\n"
            "🔸/keys <level><- or +>"
            "🔸/keys abbr\n" 
            "🔸<keyholder> - [Keystone: <dungeon> (<level>)]", False),
        "Raider.io": ("🔸/rio <character>-<realm>\n"
            "🔸/rio <character>-<realm> <level>\n"
            "🔸/rio <character>-<realm> <level> <f or t>", False),
        "Poll": ("🔸/poll <about>, <option_1>, <option_2>,...", False),
        "Dungeon ilvls": ("🔸/ilvl\n"
            "🔸/ilvl <level>\n", False),
        "Dungeon Guides": ("🔸/guide <dungeon>", False)
    }
    foot = "Mancin Mancin"
    foot_icon = "https://media.discordapp.net/attachments/1087696437426528269/1089293104089137282/OIG.awIefY1fsoRX0.jpg?width=676&height=676"
    desc = None
    embed = await make_embed(name, url, fields, foot, foot_icon, desc, color)
    await interaction.response.send_message(embed=embed)

async def reset_keystones():
    channel = bot.get_channel(1077890228854988860)
    keystones.clear()
    with open('keys.json', 'w') as f:
        json.dump(keystones, f)
    await channel.send("Key list reset.")

async def scheduler():
    schedule.every().wednesday.at("06:00").do(asyncio.create_task, reset_keystones)
    while True:
        schedule.run_pending()
        await asyncio.sleep(60)

cache = {}

async def reset_cache():
    while True:
        await asyncio.sleep(600)
        cache.clear()

async def start_cache_reset():
    await reset_cache()

async def check():
    while True:
        for message_id, data in message_ids.items():
            if datetime.datetime.utcnow() - data["time"] > datetime.timedelta(days=14):
                del message_ids[message_id]
        for message_id, data in message_users.items():
            if datetime.datetime.utcnow() - data["time"] > datetime.timedelta(hours=6):
                del message_users[message_id]
        await asyncio.sleep(24 * 60 * 60)

async def start_check():
    await check()
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    bot.loop.create_task(start_check())
    bot.loop.create_task(start_cache_reset())
    await bot.tree.sync()
    bot.loop.create_task(scheduler())

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
    if '<@&1087697492038131762>' in message.content:
        await message.add_reaction('<:Tank_icon:1103828509996089499>')
        await message.add_reaction('<:Healer_icon:1103828598722416690>')
        await message.add_reaction('<:Dps_icon:1103828601075413145>')
    await kielce(message)
    await on_keystone_message(message)
    await bot.process_commands(message)

embeds_to_edit = []
message_ids = {}
ping_messages = {}

async def make_embed(name, link, dicto, foot, foot_icon, desc, color):
    embed = discord.Embed(
        title = name,
        description = desc,
        color = discord.Color(int(color[1:], 16))
    )
    embed.set_thumbnail(url=link)
    embed.set_footer(text=(f"Made by {foot}"), icon_url=foot_icon)
    for k, _ in dicto.items():
        val = dicto[k][0]
        boo = dicto[k][1]
        embed.add_field(name=k, value=val, inline=boo)
    return embed

async def edit_embed(embed, message_id):
    new_embed = discord.Embed.from_dict(embed.to_dict())
    new_fields = []
    for field in new_embed.fields:
        if field.name == "Total:":
            total = len(message_ids[message_id]["tanks"] + message_ids[message_id]["healers"] + message_ids[message_id]["dps"])
            tent = len(message_ids[message_id]["tentative"])
            if len(message_ids[message_id]["tentative"]) == 0:
                field.value = total
            else:
                field.value = f"{total} + {tent}"
        elif "<:Tank_icon:1103828509996089499>__**Tanks**__" in field.name:
            field.name = f"<:Tank_icon:1103828509996089499>__**Tanks**__ (`{len(message_ids[message_id]['tanks'])}`):"
            tank_list = ", ".join(f"`{message_ids[message_id]['users'].index(tank) + 1}`{tank}" for tank in message_ids[message_id]["tanks"])
            field.value = tank_list
        elif "<:Healer_icon:1103828598722416690>__**Healers**__" in field.name:
            field.name = f"<:Healer_icon:1103828598722416690>__**Healers**__ (`{len(message_ids[message_id]['healers'])}`):"
            healer_list = ", ".join(f"`{message_ids[message_id]['users'].index(tank) + 1}`{tank}" for tank in message_ids[message_id]["healers"])
            field.value = healer_list
        elif "<:Dps_icon:1103828601075413145>__**Dps**__" in field.name:
            field.name = f"<:Dps_icon:1103828601075413145>__**Dps**__ (`{len(message_ids[message_id]['dps'])}`):"
            dps_list = ", ".join(f"`{message_ids[message_id]['users'].index(tank) + 1}`{tank}" for tank in message_ids[message_id]["dps"])
            field.value = dps_list
        elif "Tentative" in field.name:
            field.name = f"Tentative (`{len(message_ids[message_id]['tentative'])}`):"
            tent_list = ", ".join(f"`{message_ids[message_id]['users'].index(tank) + 1}`{tank}" for tank in message_ids[message_id]["tentative"])
            field.value = tent_list
        elif "Absence" in field.name:
            field.name = f"Absence (`{len(message_ids[message_id]['absent'])}`):"
            abs_list = ", ".join(f"`{message_ids[message_id]['users'].index(tank) + 1}`{tank}" for tank in message_ids[message_id]["absent"])
            field.value = abs_list
        new_fields.append(field)
    new_embed.clear_fields()
    for field in new_fields:
        new_embed.add_field(name=field.name, value=field.value, inline=field.inline)
    return new_embed
      
async def weekly_gaming(tanks, healers, dps):
    while True:
        unique_1, unique_2, unique_3 = None, None, None
        if len(tanks) >= 1 and unique_1 is None:
            unique_1 = random.choice(list(set(tanks)))
            healers = [el for el in healers if el != unique_1]
            dps = [el for el in dps if el != unique_1]
        if len(healers) >= 1 and unique_2 is None:
            unique_2 = random.choice(list(set(healers)))
            dps = [el for el in dps if el != unique_2]
        if len(dps) >= 3 and unique_3 is None:
            unique_3 = random.sample(list(set(dps)), 3)
        if not unique_1 or not unique_2 or not unique_3:
            continue
        return unique_1, unique_2, unique_3

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

@bot.command()
async def signups(ctx, *args):
    if len(args) < 2:
        await ctx.send("Wrong format, try:\n"
                       "<day> <time> <additional info>")
        return
    if re.match(r'^(0?[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$', args[1]):
        time = args[1]
    elif re.match(r'^(0?[0-9]|1[0-9]|2[0-3])$', args[1]):
        time = f"{args[1]}:00"
    else:
        await ctx.send("Invalid time given")
        return
    name = f"Raid - {args[0]} {time}"
    desc = ' '.join(args[2:])
    color = "#575660"
    url = "https://i.imgur.com/9rcj0qB.png"
    fields = {
        "Total:": ["0", False],
        f"<:Tank_icon:1103828509996089499>__**Tanks**__ (`0`):": ["", False],
        f"<:Healer_icon:1103828598722416690>__**Healers**__ (`0`):": ["", False],
        f"<:Dps_icon:1103828601075413145>__**Dps**__ (`0`):": ["", False],
        f"Tentative (`0`):": ["", False],
        f"Absence (`0`):": ["", False]
    }
    foot = ctx.author
    foot_icon = ctx.author.avatar.url
    embed = await make_embed(name, url, fields, foot, foot_icon, desc, color)
    await ctx.message.delete()
    ping_message = await ctx.send("<@&1105548968697540679>")
    su_message = await ctx.send(embed=embed)
    message_ids.update({su_message.id: {"tanks": [],
                                        "healers": [],
                                        "dps": [],
                                        "tentative": [],
                                        "absent": [],
                                        "users": [],
                                        "time": datetime.datetime.utcnow()
                                        }})
    embeds_to_edit.append(su_message)
    ping_messages.update({su_message.id: ping_message})
    await su_message.add_reaction("<:Tank_icon:1103828509996089499>")
    await su_message.add_reaction("<:Healer_icon:1103828598722416690>")
    await su_message.add_reaction("<:Dps_icon:1103828601075413145>")
    await su_message.add_reaction("❓")
    await su_message.add_reaction("<:negative:1104352809626902639>")
    await su_message.add_reaction("❎")

@bot.event
async def on_reaction_remove(reaction, user):
    if user.bot:
        return
    
    message_id = reaction.message.id
    message = reaction.message
    if '<@&1087697492038131762>' in message.content:
        if message_id in message_users:

            role = None
            if str(reaction.emoji) == '<:Tank_icon:1103828509996089499>':
                role = 'tanks'
            elif str(reaction.emoji) == '<:Healer_icon:1103828598722416690>':
                role = 'healers'
            elif str(reaction.emoji) == '<:Dps_icon:1103828601075413145>':
                role = 'dps'

            if role:
                if user in message_users[message_id][role]:
                    message_users[message_id][role].remove(user)
    if '<@&989535345370628126>' in message.content:
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
    if message_id in message_ids.keys():
        role = None
        if str(reaction.emoji) == "<:Tank_icon:1103828509996089499>":
            role = "tanks"
        elif str(reaction.emoji) == "<:Healer_icon:1103828598722416690>":
            role = "healers"
        elif str(reaction.emoji) == "<:Dps_icon:1103828601075413145>":
            role = "dps"
        elif str(reaction.emoji) == "❓":
            role = "tentative"
        elif str(reaction.emoji) == "<:negative:1104352809626902639>":
            role = "absent"
        if role:
            if user not in message_ids[message_id][role]:
                try:
                    message_ids[message_id][role].remove(f"<@{user.id}>")
                except:
                    return
            for role2, _ in message_ids[message_id].items():
                if role2 not in ["time", "users"]:
                    if user not in message_ids[message_id].values():
                        message_ids[message_id]["users"].remove(f"<@{user.id}>")
                        break
        for message in embeds_to_edit:
            if message.id == message_id:
                embed = message.embeds[0]
                edit_message = message
        edited_embed = await edit_embed(embed, message_id)
        await edit_message.edit(embed=edited_embed)

message_users = {}

@bot.event
async def on_reaction_add(reaction, user):
    message_id = reaction.message.id
    message = reaction.message
    if '<@&989535345370628126>' in message.content:
        if user.bot:
            if message_id not in message_users:
                    message_users[message_id] = {
                    'lock': asyncio.Lock(),
                    'tanks': [],
                    'healers': [],
                    'dps': [],
                    'keystone': [],
                    'sent': False,
                    'time': datetime.datetime.utcnow()
                    }
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
    if '<@&724869170734432258>' in message.content:
        if user.bot:
            if message_id not in message_users:
                message_users[message_id] = {
                    'lock': asyncio.Lock(),
                    'tanks': [],
                    'healers': [],
                    'dps': [],
                    'sent': False,
                    'time': datetime.datetime.utcnow()
                }
            return
        
        if message_id in message_users:

            role = None
            if str(reaction.emoji) == '<:Tank_icon:1103828509996089499>':
                role = 'tanks'
            elif str(reaction.emoji) == '<:Healer_icon:1103828598722416690>':
                role = 'healers'
            elif str(reaction.emoji) == '<:Dps_icon:1103828601075413145>':
                role = 'dps'

            if role:
                if user not in message_users[message_id][role]:
                    message_users[message_id][role].append(user)

            async with message_users[message_id]['lock']:
                if len(message_users[message_id]['tanks']) >= 1 and len(message_users[message_id]['healers']) >= 1 and len(message_users[message_id]['dps']) >= 3 and len(set(message_users[message_id]['tanks'] + message_users[message_id]['healers'])) >= 2 and len(set(message_users[message_id]['tanks'] + message_users[message_id]['healers'] + message_users[message_id]['dps'])) >= 5:
                    if message_users[message_id]['sent'] == False:
                        await message.channel.send(f"Team can now be made")
                        message_users[message_id]['sent'] = True

                        await asyncio.sleep(5)
                        if len(message_users[message_id]['tanks']) >= 1 and len(message_users[message_id]['healers']) >= 1 and len(message_users[message_id]['dps']) >=3 and len(set(message_users[message_id]['tanks'] + message_users[message_id]['healers'])) >=2 and len(set(message_users[message_id]['tanks'] + message_users[message_id]['healers'] + message_users[message_id]['dps'])) >= 5:

                            tank_weekly, healer_weekly, dps_weekly = await weekly_gaming(message_users[message_id]['tanks'], message_users[message_id]['healers'], message_users[message_id]['dps'])
                                
                            await message.channel.send(f"Keystone team:\n<:Tank_icon:1103828509996089499> {tank_weekly.mention}\n<:Healer_icon:1103828598722416690> {healer_weekly.mention}\n<:Dps_icon:1103828601075413145> {dps_weekly[0].mention}\n<:Dps_icon:1103828601075413145> {dps_weekly[1].mention}\n<:Dps_icon:1103828601075413145> {dps_weekly[2].mention}")

                            tank_weekly = []
                            healer_weekly = []
                            dps_weekly = []
                            del message_users[message_id]
                                
                        else:
                            await message.channel.send(f"Cannot form a team due to people unsigning.")
                            message_users[message_id]['sent'] = False
    if message_id in message_ids.keys():
        if user.bot:
            return
        for message in embeds_to_edit:
            if message.id == message_id:
                my_embed = message.embeds[0]
        my_footer = my_embed.footer
        role = None
        if str(reaction.emoji) == "<:Tank_icon:1103828509996089499>":
            role = "tanks"
        elif str(reaction.emoji) == "<:Healer_icon:1103828598722416690>":
            role = "healers"
        elif str(reaction.emoji) == "<:Dps_icon:1103828601075413145>":
            role = "dps"
        elif str(reaction.emoji) == "❓":
            role = "tentative"
        elif str(reaction.emoji) == "<:negative:1104352809626902639>":
            role = "absent"
        elif str(reaction.emoji) == "❎" and user.name in my_footer.text:
            ping_message = ping_messages[message_id]
            msg = [msg for msg in embeds_to_edit if msg.id == message_id][0]
            await msg.delete()
            await ping_message.delete()
            del message_ids[message_id]
            return
        if role:
            for role2, user_list in message_ids[message_id].items():
                if role2 not in ["time", "users"]:
                    if (f"<@{user.id}>") in user_list:
                        message_ids[message_id][role2].remove(f"<@{user.id}>")
                        emojis = {
                        "tanks": "<:Tank_icon:1103828509996089499>",
                        "healers": "<:Healer_icon:1103828598722416690>",
                        "dps": "<:Dps_icon:1103828601075413145>",
                        "tentative": "❓",
                        "absent": "<:negative:1104352809626902639>"
                    }
                        emoji = emojis[role2]
                        await reaction.message.remove_reaction(emoji, user)
            if (f"<@{user.id}>") not in message_ids[message_id]["users"]:
                message_ids[message_id]["users"].append(f"<@{user.id}>")
            message_ids[message_id][role].append(f"<@{user.id}>")

        for message in embeds_to_edit:
            if message.id == message_id:
                embed = message.embeds[0]
                edit_message = message
        edited_embed = await edit_embed(embed, message_id)
        await edit_message.edit(embed=edited_embed)            

@bot.event
async def kielce(message):
    if message.guild.id != 521281100069470208:
        return
    if "kielce" in message.content.lower():
        await message.channel.send(f'Czy to jest boss?')
    if "jestem" in message.content.lower():
        await message.channel.send(f'Jest Dawer?')
    if " zrob " in message.content.lower() or " zrób " in message.content.lower():
        await message.channel.send(f'Dziunia nie jestes mojim szefem')
    if "impreza" in message.content.lower():
        await message.channel.send(f'To jest moja w top 3 ubulio nych impez impeza')


@bot.event
async def on_keystone_message(message):
    unrecognized_dungeons = False
    if message.author.bot:
        return
    pattern = r'^(\w+) - \[Keystone: (.+) \((\d+)\)\]$'
    for line in message.content.split('\n'):
        match = re.match(pattern, line)
        if match:
            key_name = match.group(1)
            dungeon_name = match.group(2)
            dungeon_level = match.group(3)
            server_id = str(message.guild.id)
            keystones.setdefault(server_id, {})

            if dungeon_name not in ['Brackenhide Hollow', 'Halls of Infusion', 'Uldaman: Legacy of Tyr', "Neltharus", "Freehold", "The Underrot", "Neltharion's Lair", "The Vortex Pinnacle"]:
                unrecognized_dungeons = True
                continue
            for _, data in keystones[server_id].items():
                if key_name in data:
                    data.pop(key_name)

            author_id = str(message.author.id)
            keystones[server_id].setdefault(dungeon_name, {})
            keystones[server_id][dungeon_name].setdefault(key_name, {})
            keystones[server_id][dungeon_name][key_name][dungeon_level] = author_id

            with open("keys.json", "w") as f:
                json.dump(keystones, f)
            
            for line in message.content.split('\n'):
                match = re.match(pattern, line)
    if match:
        if unrecognized_dungeons == True:
            await message.channel.send(f'Dungeons provided not recognized')
            return
        key_name = match.group(1)
        if key_name in keystones[server_id][dungeon_name]:
            await message.delete()


@bot.command()
async def keys(ctx, *, arg=None):
    server_id = str(ctx.guild.id)

    matching_keys = []
    message_to_send = []
    abbreviations = {
'uld': 'Uldaman: Legacy of Tyr',
'bh': 'Brackenhide Hollow',
'nelt': 'Neltharus',
'hoi': 'Halls of Infusion',
'ur': 'The Underrot',
'fh': 'Freehold',
'nl': "Neltharion's Lair",
'vp': 'The Vortex Pinnacle',
}
    if arg is None:
        if len(keystones.get(server_id, {})) > 0:            
            for key, data in keystones[server_id].items():
                for keyholder, level in data.items():
                    matching_keys.append(f'{keyholder} - [Keystone: {key} ({", ".join(list(level.keys()))})]')
            if matching_keys:
                message_to_send = '\n'.join(matching_keys)
                await ctx.send(message_to_send)
        else:
            await ctx.send(f'There are no keys yet')
    elif arg.isdigit():
        if server_id in keystones:
            for key, data in keystones[server_id].items():
                for keyholder, level in data.items():
                    if arg in level:
                        matching_keys.append(f'{keyholder} - [Keystone: {key} ({", ".join(list(level.keys()))})]')
            if matching_keys:
                message_to_send = '\n'.join(matching_keys)
                await ctx.send(message_to_send)
            else:
                await ctx.send(f"There are no keys for level {arg}")
        else:
            await ctx.send(f"There are no keys yet")
    elif arg.endswith("-") or arg.endswith("+"):
        given_levels = arg[:-1]
        loh = arg[-1]
        if server_id in keystones:
            for key, data in keystones[server_id].items():
                for keyholder, level in data.items():
                    for c in level.keys():
                        if loh == ("+"):
                            if int(c) >= int(given_levels):
                                matching_keys.append(f'{keyholder} - [Keystone: {key} ({", ".join(list(level.keys()))})]')
                        elif loh == ("-"):
                            if int(c) <= int(given_levels):
                                matching_keys.append(f'{keyholder} - [Keystone: {key} ({", ".join(list(level.keys()))})]')
            if matching_keys:
                message_to_send = '\n'.join(matching_keys)
                await ctx.send(message_to_send)
            else:
                await ctx.send(f"There are no keys for levels {arg}")
        else:
            await ctx.send(f"There are no keys yet")
    elif arg.lower() == 'reset':
        keystones.clear()
        with open("keys.json", "w") as f:
            json.dump(keystones, f)
        await ctx.send("Key list reset")
    elif arg.lower() in map(str.lower, abbreviations.keys()) or arg.lower() in map(str.lower, abbreviations.values()):
        found_keys = {}
        key = abbreviations.get(arg.lower()) or [v for _, v in abbreviations.items() if v.lower() == arg.lower()][0]
        found_keys = keystones.get(server_id, {}).get(key, {})
        if found_keys:
            for keyholder, level in found_keys.items():
                matching_keys.append(f'{keyholder} - [Keystone: {key} ({", ".join(list(level.keys()))})]')
            if matching_keys:
                message_to_send = '\n'.join(matching_keys)
                await ctx.send(message_to_send)
        else:
            await ctx.send(f'There are no keys for {key}')
    elif arg.lower() == 'abbr':
        abbreviations_text = '\n'.join([f'"{key}" for {value}' for key, value in abbreviations.items()])
        await ctx.send(f'{abbreviations_text}')
    elif arg.startswith('<@') and arg.endswith('>'):
        member = int(arg[2:-1])
        if server_id in keystones:
            for key, data in keystones[server_id].items():
                for keyholder, level in data.items():
                    if member == int(list(level.values())[0]):
                        matching_keys.append(f'{keyholder} - [Keystone: {key} ({", ".join(list(level.keys()))})]')
            if matching_keys:
                message_to_send = '\n'.join(matching_keys)
                await ctx.send(message_to_send)
            else:
                await ctx.send("User doesn't have any keys")
        else:
            await ctx.send(f"User doesn't have any keys")
    elif any(arg.lower() in str(val).lower() for _, val in keystones.get(server_id, {}).items()):
        if server_id in keystones:
            for key, data in keystones[server_id].items():
                for keyholder, level in data.items():
                    if keyholder.lower() == arg.lower():
                        matching_keys.append(f'{keyholder} - [Keystone: {key} ({", ".join(list(level.keys()))})]')
            if matching_keys:
                message_to_send = '\n'.join(matching_keys)
                await ctx.send(message_to_send)
        else:
            await ctx.send("There are no keys yet")
    else:
        await ctx.send(f'Keyholder is absent in the list, or dungeon provided is invalid, check "/keys abbr"')


@bot.command()
async def rio(ctx, arg1=None, arg2=None, arg3=None):
    all_dungeons = ["The Vortex Pinnacle", "Neltharion's Lair", "The Underrot", "Freehold", "Neltharus", "Uldaman: Legacy of Tyr", "Halls of Infusion", "Brackenhide Hollow"]
    message_to_send = []
    default_realm = "burninglegion"
    base_score = {
        "2" : "40",
        "3" : "45",
        "4" : "55",
        "5" : "60",
        "6" : "65",
        "7" : "75",
        "8" : "80",
        "9" : "85",
        "10" : "100",
        "11" : "107",
        "12" : "114",
        "13" : "121",
        "14" : "128",
        "15" : "135",
        "16" : "142",
        "17" : "149",
        "18" : "156",
        "19" : "163",
        "20" : "170",
        "21" : "177",
        "22" : "184",
        "23" : "191",
        "24" : "198",
        "25" : "205",
        "26" : "212",
        "27" : "219",
        "28" : "226",
        "29" : "233",
        "30" : "240"
 }
    if arg1 is None or (arg3 is not None and arg3.lower() not in ["tyra", "tyrannical", "t", "forti", "f", "fortified"]):
        await ctx.send(f"Wrong format, try: \"/rio <character>-<realm> <level> <f or t> (optional)\"")
        return
    if arg2 is not None and arg2 not in base_score:
        await ctx.send(f"Dungeon level inappropriate")
        return
    if "-" in arg1:
        name, realm = arg1.split("-")
    else:
        name = arg1
        realm = default_realm
    rio_increase = {}
    points_at_lvl = []

    url = f"https://raider.io/api/v1/characters/profile?region=eu&realm={realm}&name={name}&fields=mythic_plus_best_runs"
    url2 = f"https://raider.io/api/v1/characters/profile?region=eu&realm={realm}&name={name}&fields=mythic_plus_alternate_runs"
    url3 = f"https://raider.io/api/v1/characters/profile?region=eu&realm={realm}&name={name}&fields=mythic_plus_scores_by_season%3Acurrent"
    if all(url in cache for url in [url, url2, url3]):
        response = cache[url]
        response2 = cache[url2]
        response3 = cache[url3]
    else:
        response = requests.get(url)
        response2 = requests.get(url2)
        response3 = requests.get(url3)
        cache[url] = response
        cache[url2] = response2
        cache[url3] = response3
    if response.status_code == 200 and response2.status_code == 200 and response3.status_code == 200:
        overall_score = response3.json()["mythic_plus_scores_by_season"][0]["scores"]["all"]
        nick = response.json()["name"]
        dungeon_list_tyra = {}
        dungeon_list_forti = {}
        best_runs = response.json()["mythic_plus_best_runs"]
        alt_runs = response2.json()["mythic_plus_alternate_runs"]
        if arg2 == None:
            if nick.endswith("s"):
                await ctx.send(f"{nick}' score: **{overall_score}**")
            else:
                await ctx.send(f"{nick}'s score: **{overall_score}**")
            return
        for dungeon in all_dungeons:
            if not any(item["dungeon"] == dungeon for item in best_runs):
                my_dict = {"dungeon": dungeon, "score": 0, "affixes": [{"name": "Fortified",}]}
                best_runs.append(my_dict)
            if not any(item["dungeon"] == dungeon for item in alt_runs):
                    if any (item["dungeon"] == dungeon and item["affixes"][0]["name"] == "Fortified" for item in best_runs):
                        my_dict = {"dungeon": dungeon, "score": 0, "affixes": [{"name": "Tyrannical"}]}
                    if any (item["dungeon"] == dungeon and item["affixes"][0]["name"] == "Tyrannical" for item in best_runs):
                        my_dict = {"dungeon": dungeon, "score": 0, "affixes": [{"name": "Fortified"}]}
                    alt_runs.append(my_dict)

        for run in alt_runs:
            affix = run["affixes"][0]["name"]
            dungeon = run["dungeon"]
            score = run["score"]
            if affix == "Tyrannical":
                dungeon_list_tyra.update({dungeon: score})
            if affix == "Fortified":
                dungeon_list_forti.update({dungeon: score})
        for run in best_runs:
            affix = run["affixes"][0]["name"]
            dungeon = run["dungeon"]
            score = run["score"]
            if affix == "Tyrannical":
                dungeon_list_tyra.update({dungeon: score})
            if affix == "Fortified":
                dungeon_list_forti.update({dungeon: score})
        points = int(base_score[arg2])
        for dungeon in dungeon_list_forti:
            if dungeon in dungeon_list_tyra:
                forti_score = dungeon_list_forti[dungeon]
                tyra_score = dungeon_list_tyra[dungeon]
                if forti_score != 0:
                    forti_best = (forti_score * 1.5).__round__(1)
                    forti_alt = (forti_score * 0.5).__round__(1)
                else:
                    forti_best = 0
                    forti_alt = 0
                if tyra_score != 0:
                    tyra_best = (tyra_score * 1.5).__round__(1)
                    tyra_alt = (tyra_score * 0.5).__round__(1)
                else:
                    tyra_best = 0
                    tyra_alt = 0
                half_points = (points * 0.5).__round__(1)
                one_half_points = (points * 1.5).__round__(1)
                two_points = (points * 2).__round__(1)
                if arg3 is not None:
                    if arg3.lower() == "tyra" or arg3.lower() == "tyrannical" or arg3.lower() == "t":
                        if points > forti_score:
                            if forti_score > tyra_score:
                                score_from_dung = one_half_points + forti_alt - forti_best - tyra_alt
                            elif forti_score <= tyra_score:
                                score_from_dung = one_half_points - tyra_best
                        if points <= forti_score:
                            score_from_dung = half_points - tyra_alt
                        if score_from_dung < 0:
                            score_from_dung = 0
                    elif arg3.lower() == "forti" or arg3.lower() == "fortified" or arg3.lower() == "f":
                        if points > tyra_score:
                            if forti_score >= tyra_score:
                                score_from_dung = one_half_points - forti_best
                            elif forti_score < tyra_score:
                                score_from_dung = one_half_points + tyra_alt - tyra_best - forti_alt
                        if points <= tyra_score:
                            score_from_dung = half_points - forti_alt
                        if score_from_dung < 0:
                            score_from_dung = 0
                    round_score = score_from_dung.__round__(1)
                    rio_increase.update({dungeon: round_score})
                elif arg3 == None:
                        if points <= tyra_score and points <= forti_score:
                            continue
                        if points > tyra_score and points > forti_score:
                            if tyra_score == 0 and forti_score != 0:
                                points_to_add = two_points - forti_best
                            elif forti_score == 0 and tyra_score != 0:
                                points_to_add = two_points - tyra_best
                            elif forti_score == 0 and tyra_score == 0:
                                points_to_add = two_points
                            else:
                                if tyra_score >= forti_score:
                                    points_to_add = two_points - tyra_best  - forti_alt
                                if tyra_score < forti_score:
                                    points_to_add = two_points - tyra_alt - forti_best
                        if points > tyra_score and points <= forti_score:
                            points_to_add = half_points - tyra_alt
                        if points <= tyra_score and points > forti_score:
                            points_to_add = half_points - forti_alt
                        points_rounded = points_to_add.__round__(1)
                        points_at_lvl.append(points_rounded)

        if points_at_lvl:
            summed = sum(points_at_lvl)
            summed_score = summed.__round__(1) + overall_score
            await ctx.send(f'**{summed.__round__(1)}** for a score of **{summed_score.__round__(1)}**')
        if rio_increase:
                    total_score = sum(rio_increase.values())
                    summed_score = total_score + overall_score
                    for key, value in rio_increase.items():
                        message_to_send.append(f"{key} - **{value}**")
                    message_to_send.append(f"\nTotal: **{total_score.__round__(1)}**, for a score of **{summed_score.__round__(1)}**")
                    message_to_send = "\n".join(message_to_send)
                    await ctx.send(message_to_send)
    else:
        await ctx.send(f"Error retrieving data: {response.status_code}")               
        
@bot.command()
async def ilvl(ctx, arg=None):
    message_to_send = []
    keystones_ilvl = {
        "2": (402, 415),
        "3": (405, 418),
        "4": (405, 421),
        "5": (408, 421),
        "6": (408, 424),
        "7": (411, 424),
        "8": (411, 428),
        "9": (415, 428),
        "10": (415, 431),
        "11": (418, 431),
        "12": (418, 434),
        "13": (421, 434),
        "14": (421, 437),
        "15": (424, 437),
        "16": (424, 441),
        "17": (428, 441),
        "18": (428, 444),
        "19": (431, 444),
        "20": (431, 447)
    }

    if arg == None:
        for k in keystones_ilvl:
            end = keystones_ilvl[k][0]
            gv = keystones_ilvl[k][1]
            message_to_send.append(f"**{k}**: {end}, {gv}")
        message_to_send = "\n".join(message_to_send)
        await ctx.send(message_to_send)
        return

    if int(arg) > 20:
        end_of_dung_ilvl = keystones_ilvl["20"][0]
        gv_ilvl = keystones_ilvl["20"][1]
    elif arg in keystones_ilvl:
        end_of_dung_ilvl = keystones_ilvl[arg][0]
        gv_ilvl = keystones_ilvl[arg][1]
    else:
        await ctx.send("Inappropriate dungeon level")
        return
    await ctx.send(f"End of dungeon ilvl: **{end_of_dung_ilvl}**\nGreat Vault ilvl: **{gv_ilvl}**")

@bot.command()
async def guide(ctx, *, arg=None):
    for dungeon in dungeon_guides:
        if dungeon["abbr"] == arg.lower() or dungeon["name"].lower() == arg.lower():
            guide = dungeon
            break
    else:
        abbr = []
        abbr.append("Try: /guide <dungeon>\n")
        for d in dungeon_guides:
            abbr.append(f'"{d["abbr"]}" for {d["name"]}')
        message_to_send = "\n".join(abbr)
        await ctx.send(message_to_send)
        return
    name = guide["name"]
    url = guide["url"]
    color = guide["color"]
    fields = guide["fields"]
    foot = "Mancin Mancin"
    foot_icon = 'https://media.discordapp.net/attachments/1087696437426528269/1089293104089137282/OIG.awIefY1fsoRX0.jpg?width=676&height=676'
    desc = None    
    embed = await make_embed(name, url, fields, foot, foot_icon, desc, color)
    await ctx.send(embed=embed)

@bot.command()
async def poll(ctx, *, arg):
    index = arg.find(',')
    if index == -1:
        await ctx.send("Please provide options separated by a comma.")
        return

    options = arg[:index].strip()
    arguments = arg[index + 1:].split(",")

    message_to_send = []
    emojis = ["🇦", "🇧", "🇨", "🇩", "🇪", "🇫", "🇬", "🇭", "🇮", "🇯", "🇰", "🇱"]

    for i, argument in enumerate(arguments):
        emoji = emojis[i] if i < len(emojis) else ''
        message_to_send.append(f'{emoji} - {argument.strip()}\n')

    poll_message = await ctx.send(f'**Poll:**\n{options}\n\n' + ''.join(message_to_send))
    await ctx.message.delete()

    for i in range(len(arguments)):
        if i < len(emojis):
            await poll_message.add_reaction(emojis[i])

bot.run(TOKEN)