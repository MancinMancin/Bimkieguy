from discord.ext import commands, tasks
import datetime
import requests
import asyncio
import random
from .global_variables import cache, message_users
from .dungeon_guides import dungeon_guides
from .other import make_embed

def setup(bot):
    bot.add_command(rio)
    bot.add_command(ilvl)
    bot.add_command(guide)
    bot.add_command(affix)

def select_elements(list_1, list_2, list_3, list_4): # @bułkarze
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
    
async def weekly_gaming(tanks, healers, dps): # @weekly
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

async def sign_mplus(reaction, user):
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
            if str(reaction.emoji) == '<:Tank_icon:1103828509996089499>':
                role = 'tanks'
            elif str(reaction.emoji) == '<:Healer_icon:1103828598722416690>':
                role = 'healers'
            elif str(reaction.emoji) == '<:Dps_icon:1103828601075413145>':
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
                            
                        await message.channel.send(f"Keystone team:\n<:Tank_icon:1103828509996089499> {tank_users.mention}\n<:Healer_icon:1103828598722416690> {healer_users.mention}\n<:Dps_icon:1103828601075413145> {dps_users[0].mention}\n<:Dps_icon:1103828601075413145> {dps_users[1].mention}\n<:Keystone:1095145259903750265> {keystone_users.mention}\n```{tank_users.mention}\n{healer_users.mention}\n{dps_users[0].mention}\n{dps_users[1].mention}```")

                        tank_users = []
                        healer_users = []
                        dps_users = []
                        keystone_users = []
                        del message_users[message_id]
                            
                    else:
                        await message.channel.send(f"Cannot form a team due to people unsigning.")
                        message_users[message_id]['sent'] = False
    if '<@&1087697492038131762>' in message.content:
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

async def unsign_mplus(reaction, user):
    if user.bot:
        return
    
    message_id = reaction.message.id
    message = reaction.message
    if '<@&1087697492038131762>' in message.content: # @weekly
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
    if '<@&989535345370628126>' in message.content: # @bułkarze
        if message_id in message_users:

            role = None
            if str(reaction.emoji) == '<:Tank_icon:1103828509996089499>':
                role = 'tanks'
            elif str(reaction.emoji) == '<:Healer_icon:1103828598722416690>':
                role = 'healers'
            elif str(reaction.emoji) == '<:Dps_icon:1103828601075413145>':
                role = 'dps'
            elif str(reaction.emoji) == '<:Keystone:1095145259903750265>':
                role = 'keystone'

            if role:
                if user in message_users[message_id][role]:
                    message_users[message_id][role].remove(user)

async def bot_react(message):
    if '<@&989535345370628126>' in message.content: # @bułkarze
        await message.add_reaction('<:Tank_icon:1103828509996089499>') 
        await message.add_reaction('<:Healer_icon:1103828598722416690>') 
        await message.add_reaction('<:Dps_icon:1103828601075413145>')
        await message.add_reaction('<:Keystone:1095145259903750265>')
        await message.add_reaction('<:Muslim_Uncle_Pepe:1098289343627526266>')
    if '<@&1087697492038131762>' in message.content: # @weekly
        await message.add_reaction('<:Tank_icon:1103828509996089499>')
        await message.add_reaction('<:Healer_icon:1103828598722416690>')
        await message.add_reaction('<:Dps_icon:1103828601075413145>')

@tasks.loop(minutes=10.0)
async def reset_cache():
        cache.clear()

@commands.command()
async def rio(ctx, arg1=None, arg2=None, arg3=None):
    # all_dungeons = ["Atal'dazar", "Black Rook Hold", "DOTI: Galakrond's Fall", "DOTI: Murozond's Rise", "Darkheart Thicket", "The Everbloom", "Throne of the Tides", "Waycrest Manor"]
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

@commands.command()
async def ilvl(ctx, arg=None):
    message_to_send = []
    keystones_ilvl = {
        "2": (441, "Veteran 1/8", 454, "Champion 1/8"),
        "3": (444, "Veteran 2/8", 457, "Champion 2/8"),
        "4": (444, "Veteran 2/8", 460, "Champion 3/8"),
        "5": (447, "Veteran 3/8", 460, "Champion 3/8"),
        "6": (447, "Veteran 3/8", 463, "Champion 4/8"),
        "7": (450, "Veteran 4/8", 463, "Champion 4/8"),
        "8": (450, "Veteran 4/8", 467, "Hero 1/6"),
        "9": (454, "Champion 1/8", 467, "Hero 1/6"),
        "10": (454, "Champion 1/8", 470, "Hero 2/6"),
        "11": (457, "Champion 2/8", 470, "Hero 2/6"),
        "12": (457, "Champion 2/8", 473, "Hero 3/6"),
        "13": (460, "Champion 3/8", 473, "Hero 3/6"),
        "14": (460, "Champion 3/8", 473, "Hero 3/6"),
        "15": (463, "Champion 4/8", 476, "Hero 4/6"),
        "16": (463, "Champion 4/8", 476, "Hero 4/6"),
        "17": (467, "Hero 1/6", 476, "Hero 4/6"),
        "18": (467, "Hero 1/6", 480, "Myth 1/4"),
        "19": (470, "Hero 2/6", 480, "Myth 1/4"),
        "20": (470, "Hero 2/6", 483, "Myth 2/4")
    }

    if arg == None:
        for k in keystones_ilvl:
            end = f"{keystones_ilvl[k][0]} {keystones_ilvl[k][1]}"
            gv = f"{keystones_ilvl[k][2]} {keystones_ilvl[k][3]}"
            message_to_send.append(f"**{k}**: {end} --- {gv}")
        message_to_send = "\n".join(message_to_send)
        await ctx.send(message_to_send)
        return

    if int(arg) > 20:
        end_of_dung_ilvl = f"{keystones_ilvl['20'][0]} {keystones_ilvl['20'][1]}"
        gv_ilvl = f"{keystones_ilvl['20'][2]} {keystones_ilvl['20'][3]}"
    elif arg in keystones_ilvl:
        end_of_dung_ilvl = f"{keystones_ilvl[arg][0]} {keystones_ilvl[arg][1]}"
        gv_ilvl = f"{keystones_ilvl[arg][2]} {keystones_ilvl[arg][3]}"
    else:
        await ctx.send("Inappropriate dungeon level")
        return
    await ctx.send(f"End of dungeon ilvl: **{end_of_dung_ilvl}**\nGreat Vault ilvl: **{gv_ilvl}**")

@commands.command()
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

@commands.command()
async def affix(ctx, next_week: int = 0):
    affix_rotation = {
    1: ("Tyrannical", "Storming", "Raging"),
    2: ("Fortified", "Entangling", "Bolstering"),
    3: ("Tyrannical", "Incorporeal", "Spiteful"),
    4: ("Fortified", "Afflicted", "Raging"),
    5: ("Tyrannical", "Volcanic", "Sanguine"),
    6: ("Fortified", "Storming", "Bursting"),
    7: ("Tyrannical", "Afflicted", "Bolstering"),
    8: ("Fortified", "Incorporeal", "Sanguine"),
    9: ("Tyrannical", "Entangling", "Bursting"),
    10: ("Fortified", "Volcanic", "Spiteful")
}

    start_date = datetime.date(2023, 9, 27)
    current_date = datetime.date.today()
    weeks_passed = (current_date - start_date).days // 7
    if weeks_passed < 0:
        weeks_passed = 0
    current_week = (weeks_passed % len(affix_rotation)) + 1
    target_week = current_week + next_week
    start_of_week = start_date + datetime.timedelta(weeks=target_week - 1)
    end_of_week = start_of_week + datetime.timedelta(days=6)
    affixes = affix_rotation[target_week]
    await ctx.send(f"**({start_of_week.strftime('%d.%m')} - {end_of_week.strftime('%d.%m')})** Affixes:\n\n"
                   f"**+2:** {affixes[0]}\n"
                   f"**+7:** {affixes[1]}\n"
                   f"**+14:** {affixes[2]}")