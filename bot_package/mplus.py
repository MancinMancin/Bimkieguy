from discord.ext import commands, tasks
import random
import discord
import asyncio
import datetime
import requests
import json

class mplus(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.message_users = {}
        self.role_bulkarze = "<@&989535345370628126>"
        self.role_donzon = "<@&1087697492038131762>"
        self.cache = {}
        self.reset_cache.start()
        self.check.start()

    def select_elements(tanks, healers, dps, keyholders): # @bułkarze
        while True:
            chosen_dps, chosen_healer, chosen_tank, chosen_keyholder = None, None, None, None
            while chosen_keyholder not in dps + healers + tanks:
                chosen_keyholder = random.choice(list(set(keyholders)))
            roles_with_keyholder = []
            for num, role_list in enumerate([tanks, healers, dps]):
                if chosen_keyholder in role_list:
                    roles_with_keyholder.append(num)

            random_role_list = random.choice(roles_with_keyholder)
            if random_role_list == 0:
                chosen_tank = chosen_keyholder
                healers = [x for x in healers if x != chosen_keyholder]
                dps = [x for x in dps if x != chosen_keyholder]
            elif random_role_list == 1:
                chosen_healer = chosen_keyholder
                dps = [x for x in dps if x != chosen_keyholder]
                tanks = [x for x in tanks if x != chosen_keyholder]
            elif random_role_list == 2:
                chosen_dps = [chosen_keyholder]
                dps.remove(chosen_keyholder)
                tanks = [x for x in tanks if x != chosen_keyholder]
                healers = [x for x in healers if x != chosen_keyholder]

            if len(tanks) >= 1 and chosen_tank is None:
                chosen_tank = random.choice(list(set(tanks)))
                healers = [x for x in healers if x != chosen_tank]
                dps = [x for x in dps if x != chosen_tank]
            if len(healers) >= 1 and chosen_healer is None:
                chosen_healer = random.choice(list(set(healers)))
                dps = [x for x in dps if x != chosen_healer]
            if len(dps) >= 2 and chosen_dps is None:
                chosen_dps = random.sample(list(set(dps)), 2)
            elif len(dps) >= 1 and chosen_dps is not None:
                chosen_dps.append(random.choice(list(set(dps))))

            if not all([chosen_tank, chosen_healer, chosen_dps]):
                continue
            return chosen_tank, chosen_healer, chosen_dps, chosen_keyholder

    def weekly_gaming(tanks, healers, dps): # @weekly
        while True:
            chosen_tank, chosen_healer, chosen_dps = None, None, None
            if len(tanks) >= 1:
                chosen_tank = random.choice(list(set(tanks)))
                healers = [x for x in healers if x != chosen_tank]
                dps = [x for x in dps if x != chosen_tank]
            if len(healers) >= 1:
                chosen_healer = random.choice(list(set(healers)))
                dps = [x for x in dps if x != chosen_healer]
            if len(dps) >= 3 and chosen_dps is None:
                chosen_dps = random.sample(list(set(dps)), 3)

            if not all([chosen_tank, chosen_healer, chosen_dps]):
                continue
            return chosen_tank, chosen_healer, chosen_dps
        
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, member: discord.Member):
        mode = None
        message_id = reaction.message.id
        message = reaction.message
        if self.role_bulkarze in message.content:
            mode = "bulkarze"
            dps_count = 2
        if self.role_donzon in message.content:
            mode = "donzon"
            dps_count = 3
        if mode:
            if member.bot:
                if message_id not in self.message_users:
                    self.message_users[message_id] = {
                        "lock": asyncio.Lock(),
                        "tanks": [],
                        "healers": [],
                        "dps": [],
                        "keystone": [],
                        "sent": False,
                        "time": datetime.datetime.now()
                    }
                return
            if message_id in self.message_users:
                role = None
                if str(reaction.emoji) == '<:Tank_icon:1103828509996089499>':
                    role = 'tanks'
                elif str(reaction.emoji) == '<:Healer_icon:1103828598722416690>':
                    role = 'healers'
                elif str(reaction.emoji) == '<:Dps_icon:1103828601075413145>':
                    role = 'dps'
                elif str(reaction.emoji) == '<:Keystone:1095145259903750265>' and mode == "bulkarze":
                    role = 'keystone'
                elif str(reaction.emoji) == '<:Muslim_Uncle_Pepe:1098289343627526266>' and mode == "bulkarze":
                    await message.channel.send(f'Kazzakstan took the boost {message.jump_url}')
                    del self.message_users[message_id]
                    return
            
                if role:
                    if member not in self.message_users[message_id][role]:
                        self.message_users[message_id][role].append(member)
                
                tanks = self.message_users[message_id]['tanks']
                healers = self.message_users[message_id]['healers']
                dps = self.message_users[message_id]['dps']
                keystone_holders = self.message_users[message_id]['keystone']
                has_enough_tanks = len(tanks) >= 1
                has_enough_healers = len(healers) >= 1
                has_enough_dps = len(dps) >= dps_count
                has_at_least_two_unique_tank_healer = len(set(tanks + healers)) >= 2
                has_at_least_four_unique_tank_healer_dps = len(set(tanks + healers + dps)) >= 2 + dps_count
                if mode == "bulkarze":
                    has_at_least_one_keystone = len(keystone_holders) >= 1
                    at_least_one_role_with_keystone = any(element in keystone_holders for element in tanks + healers + dps)
                elif mode == "donzon":
                    has_at_least_one_keystone = True
                    at_least_one_role_with_keystone = True

                async with self.message_users[message_id]["lock"]:
                    if (has_enough_tanks and has_enough_healers and has_enough_dps and
                        has_at_least_two_unique_tank_healer and has_at_least_four_unique_tank_healer_dps and
                        has_at_least_one_keystone and at_least_one_role_with_keystone):
                        if self.message_users[message_id]["sent"] == False:
                            await message.channel.send("Team can now be made")
                            self.message_users[message_id]['sent'] = True
                        
                        await asyncio.sleep(5)

                        if (has_enough_tanks and has_enough_healers and has_enough_dps and
                            has_at_least_two_unique_tank_healer and has_at_least_four_unique_tank_healer_dps and
                            has_at_least_one_keystone and at_least_one_role_with_keystone):

                            if mode == "bulkarze":
                                tank_users, healer_users, dps_users, keystone_users = self.select_elements(tanks, healers, dps, keystone_holders)
                                await message.channel.send(f"Keystone team:\n"
                                                        f"<:Tank_icon:1103828509996089499> {tank_users.mention}\n"
                                                        f"<:Healer_icon:1103828598722416690> {healer_users.mention}\n"
                                                        f"<:Dps_icon:1103828601075413145> {dps_users[0].mention}\n"
                                                        f"<:Dps_icon:1103828601075413145> {dps_users[1].mention}\n"
                                                        f"<:Keystone:1095145259903750265> {keystone_users.mention}\n"
                                                        f"```{tank_users.mention}\n{healer_users.mention}\n{dps_users[0].mention}\n{dps_users[1].mention}```")
                                
                            elif mode == "donzon":
                                tank_users, healer_users, dps_users = self.weekly_gaming(tanks, healers, dps)
                                await message.channel.send(f"Keystone team:\n"
                                                           f"<:Tank_icon:1103828509996089499> {tank_users.mention}\n"
                                                           f"<:Healer_icon:1103828598722416690> {healer_users.mention}\n"
                                                           f"<:Dps_icon:1103828601075413145> {dps_users[0].mention}\n"
                                                           f"<:Dps_icon:1103828601075413145> {dps_users[1].mention}\n"
                                                           f"<:Dps_icon:1103828601075413145> {dps_users[2].mention}")

                        else:
                            await message.channel.send("Cannot form a team due to people unsigning.")
                            self.message_users[message_id]["sent"] = False
    
    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction: discord.Reaction, member: discord.Member):
        if member.bot:
            return
        message_id = reaction.message.id
        message = reaction.message
        if self.role_bulkarze in message.content or self.role_donzon in message.content:
            if message_id in self.message_users:

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
                    if member in self.message_users[message_id][role]:
                        self.message_users[message_id][role].remove(member)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if self.role_bulkarze in message.content:
            await message.add_reaction('<:Tank_icon:1103828509996089499>') 
            await message.add_reaction('<:Healer_icon:1103828598722416690>') 
            await message.add_reaction('<:Dps_icon:1103828601075413145>')
            await message.add_reaction('<:Keystone:1095145259903750265>')
            await message.add_reaction('<:Muslim_Uncle_Pepe:1098289343627526266>')
        if self.role_donzon in message.content:
            await message.add_reaction('<:Tank_icon:1103828509996089499>')
            await message.add_reaction('<:Healer_icon:1103828598722416690>')
            await message.add_reaction('<:Dps_icon:1103828601075413145>')

    @tasks.loop(minutes=10)
    async def reset_cache(self):
        self.cache.clear()

    @commands.command()
    async def rio(self, ctx: commands.Context, char: str = None, level: str = None, fortyra: str = None):
        all_dungeons = [
            "Atal'Dazar",
            "Black Rook Hold",
            "DOTI: Galakrond's Fall",
            "DOTI: Murozond's Rise",
            "Darkheart Thicket",
            "The Everbloom",
            "Throne of the Tides",
            "Waycrest Manor"
        ]
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
        default_realm = "burninglegion"
        message_to_send = []
        if char is None or (fortyra is not None and fortyra.lower() not in ["tyra", "tyrannical", "t", "forti", "f", "fortified"]):
            await ctx.send("Wrong format, try: \"/rio <character>-<realm> <level> <f or t>(optional)\"")
            return
        if level is not None and level not in base_score:
            await ctx.send("Dungeon level inappropriate")
            return
        if "-" in char:
            name, realm = char.split("-")
        else:
            name = char
            realm = default_realm
        rio_increase = {}
        points_at_lvl = []
        url = f"https://raider.io/api/v1/characters/profile?region=eu&realm={realm}&name={name}&fields=mythic_plus_best_runs"
        url2 = f"https://raider.io/api/v1/characters/profile?region=eu&realm={realm}&name={name}&fields=mythic_plus_alternate_runs"
        url3 = f"https://raider.io/api/v1/characters/profile?region=eu&realm={realm}&name={name}&fields=mythic_plus_scores_by_season%3Acurrent"
        if all(url in self.cache for url in [url, url2, url3]):
            response = self.cache[url]
            response2 = self.cache[url2]
            response3 = self.cache[url3]
        else:
            response = requests.get(url)
            response2 = requests.get(url2)
            response3 = requests.get(url3)
            self.cache[url] = response
            self.cache[url2] = response2
            self.cache[url3] = response3
        if response.status_code != 200 or response2.status_code != 200 or response3.status_code != 200:
            await ctx.send(f"Error retrieving data")
            return
        overall_score = response3.json()["mythic_plus_scores_by_season"][0]["scores"]["all"]
        nick = response.json()["name"]
        dungeon_list_tyra = {}
        dungeon_list_forti = {}
        best_runs = response.json()["mythic_plus_best_runs"]
        alt_runs = response2.json()["mythic_plus_alternate_runs"]      
        if level == None:
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
        points = int(base_score[level])
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
                if fortyra is not None:
                    if fortyra.lower() == "tyra" or fortyra.lower() == "tyrannical" or fortyra.lower() == "t":
                        if points > forti_score:
                            if forti_score > tyra_score:
                                score_from_dung = one_half_points + forti_alt - forti_best - tyra_alt
                            elif forti_score <= tyra_score:
                                score_from_dung = one_half_points - tyra_best
                        if points <= forti_score:
                            score_from_dung = half_points - tyra_alt
                        if score_from_dung < 0:
                            score_from_dung = 0
                    elif fortyra.lower() == "forti" or fortyra.lower() == "fortified" or fortyra.lower() == "f":
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
                elif fortyra == None:
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
    
    @commands.command()
    async def ilvl(self, ctx: commands.Context, arg: str = None):
        if arg is not None and not arg.isdigit():
            await ctx.send("Podaj liczbę")
            return
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
    async def affix(self, ctx: commands.Context, next_week: str = "0"):
        if not next_week.isdigit():
            await ctx.send("Podaj cyfrę")
            return
        affix_rotation = {
        1: ("Fortified", "Incorporeal", "Sanguine"),
        2: ("Tyrannical", "Entangling", "Bursting"),
        3: ("Fortified", "Volcanic", "Spiteful"),
        4: ("Tyrannical", "Storming", "Raging"),
        5: ("Fortified", "Entangling", "Bolstering"),
        6: ("Tyrannical", "Incorporeal", "Spiteful"),
        7: ("Fortified", "Afflicted", "Raging"),
        8: ("Tyrannical", "Volcanic", "Sanguine"),
        9: ("Fortified", "Storming", "Bursting"),
        10: ("Tyrannical", "Afflicted", "Bolstering")
        }

        start_date = datetime.date(2023, 11, 15)
        current_date = datetime.date.today()
        weeks_passed = (current_date - start_date).days // 7
        if weeks_passed < 0:
            weeks_passed = 0
        current_week = (weeks_passed % len(affix_rotation)) + 1
        target_week = current_week + int(next_week)
        start_of_week = start_date + datetime.timedelta(weeks=weeks_passed + int(next_week))
        end_of_week = start_of_week + datetime.timedelta(days=6)
        affixes = affix_rotation[target_week]
        await ctx.send(f"**({start_of_week.strftime('%d.%m')} - {end_of_week.strftime('%d.%m')})** Affixes:\n\n"
                        f"**+2:** {affixes[0]}\n"
                        f"**+7:** {affixes[1]}\n"
                        f"**+14:** {affixes[2]}")

    @tasks.loop(hours=24.0)
    async def check(self):
        for message_id, data in self.message_users.items():
            if datetime.datetime.now() - data["time"] > datetime.timedelta(hours=6):
                del self.message_users[message_id]

async def setup(bot):
    await bot.add_cog(mplus(bot))