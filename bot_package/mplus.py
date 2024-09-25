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
        self.loops = [self.reset_cache, self.check]
        [x.start() for x in self.loops]

    def cog_unload(self):
        [x.cancel() for x in self.loops]

    def select_elements(tanks_to_roll, healers_to_roll, dps_to_roll, keyholders_to_roll): # @bułkarze
        while True:
            tanks, healers, dps, keyholders = tanks_to_roll, healers_to_roll, dps_to_roll, keyholders_to_roll
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

    def weekly_gaming(tanks_to_roll, healers_to_roll, dps_to_roll): # @donzon
        while True:
            tanks, healers, dps = tanks_to_roll, healers_to_roll, dps_to_roll
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
        
    def make_embed(self, title=None, desc=None, color=None, list=None,):
        embed = discord.Embed(title=title, description=desc, colour=color)
        for n in range(len(list)):
            embed.add_field(name=list[n][0], inline=list[n][1], value='\n'.join(list[n][2:]))
        return embed
        
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, member: discord.Member):
        mode = None
        message_id = reaction.message.id
        message = reaction.message
        if self.role_bulkarze in message.content:
            mode = "bulkarze"
            dps_count = 2
        elif self.role_donzon in message.content:
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
                has_at_least_three_unique_tank_dps = len(set(tanks + dps)) >= 1 + dps_count
                has_at_least_three_unique_healer_dps = len(set(healers + dps)) >= 1 + dps_count
                if mode == "bulkarze":
                    has_at_least_one_keystone = len(keystone_holders) >= 1
                    at_least_one_role_with_keystone = any(element in keystone_holders for element in tanks + healers + dps)
                elif mode == "donzon":
                    has_at_least_one_keystone = True
                    at_least_one_role_with_keystone = True

                async with self.message_users[message_id]["lock"]:
                    if (has_enough_tanks and has_enough_healers and has_enough_dps and
                        has_at_least_two_unique_tank_healer and has_at_least_four_unique_tank_healer_dps and
                        has_at_least_one_keystone and at_least_one_role_with_keystone and has_at_least_three_unique_tank_dps and has_at_least_three_unique_healer_dps):
                        if self.message_users[message_id]["sent"] == False:
                            await message.channel.send("Team can now be made")
                            self.message_users[message_id]['sent'] = True
                        
                        await asyncio.sleep(5)

                        if (has_enough_tanks and has_enough_healers and has_enough_dps and
                            has_at_least_two_unique_tank_healer and has_at_least_four_unique_tank_healer_dps and
                            has_at_least_one_keystone and at_least_one_role_with_keystone and has_at_least_three_unique_tank_dps and has_at_least_three_unique_healer_dps):

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
    async def rio(self, ctx: commands.Context, char: str = None, level: str = None):
        all_dungeons = [
            "Ara-Kara, City of Echoes",
            "City of Threads",
            "Grim Batol",
            "Mists of Tirna Scithe",
            "Siege of Boralus",
            "The Dawnbreaker",
            "The Necrotic Wake",
            "The Stonevault"
        ]
        base_score = {
            "2" : "165",
            "3" : "180",
            "4" : "205",
            "5" : "220",
            "6" : "235",
            "7" : "265",
            "8" : "280",
            "9" : "295",
            "10" : "320",
            "11" : "335",
            "12" : "365",
            "13" : "380",
            "14" : "395",
            "15" : "410",
            "16" : "425",
            "17" : "440",
            "18" : "455",
            "19" : "470",
            "20" : "485",
            "21" : "500",
            "22" : "515",
            "23" : "530",
            "24" : "545",
            "25" : "560",
            "26" : "575",
            "27" : "590",
            "28" : "605",
            "29" : "620",
            "30" : "635"
    }
        default_realm = "burninglegion"
        message_to_send = []
        if char is None:
            await ctx.send("Wrong format, try: \"/rio <character>-<realm> <level>\"")
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
        url = f"https://raider.io/api/v1/characters/profile?region=eu&realm={realm}&name={name}&fields=mythic_plus_best_runs"
        url3 = f"https://raider.io/api/v1/characters/profile?region=eu&realm={realm}&name={name}&fields=mythic_plus_scores_by_season%3Acurrent"
        if all(url in self.cache for url in [url, url3]):
            response = self.cache[url]
            response3 = self.cache[url3]
        else:
            response = requests.get(url)
            response3 = requests.get(url3)
            self.cache[url] = response
            self.cache[url3] = response3
        if response.status_code != 200 or response3.status_code != 200:
            await ctx.send(f"Error retrieving data")
            return
        overall_score = response3.json()["mythic_plus_scores_by_season"][0]["scores"]["all"]
        nick = response.json()["name"]
        dungeon_list = {}
        best_runs = response.json()["mythic_plus_best_runs"]     
        if level == None:
            if nick.endswith("s"):
                await ctx.send(f"{nick}' score: **{overall_score}**")
            else:
                await ctx.send(f"{nick}'s score: **{overall_score}**")
            return
        
        for dungeon in all_dungeons:
            if not any(item["dungeon"] == dungeon for item in best_runs):
                my_dict = {"dungeon": dungeon, "score": 0}
                best_runs.append(my_dict)

        for run in best_runs:
            dungeon = run["dungeon"]
            score = run["score"]
            dungeon_list.update({dungeon: score})

        points = int(base_score[level])

        for dungeon in dungeon_list:
            score = dungeon_list[dungeon]
            if points > score:
                score_from_dung = points - score
            else:
                score_from_dung = 0
            round_score = score_from_dung.__round__(1)
            rio_increase.update({dungeon: round_score})

        total_score = sum(rio_increase.values())
        summed_score = total_score + overall_score

        for key, value in rio_increase.items():
            message_to_send.append(f"{key} - **{value}**")
        message_to_send.append(f"\nTotal: **{total_score.__round__(1)}**, for a score of **{summed_score.__round__(1)}**")
        message_to_send = "\n".join(message_to_send)
        await ctx.send(message_to_send)
    
    @commands.command()
    async def ilvl(self, ctx: commands.Context, arg: str = None):
        keystones_ilvl = {
            "hc": ("580", "Adventurer 4/8", "593", "Veteran 4/8", "Weathered"),
            "0": ("593", "Veteran 4/8", "603", "Champion 3/8", "Carved"),
            "2": ("597", "Champion 1/8", "606", "Champion 4/8", "Carved"),
            "3": ("597", "Champion 1/8", "610", "Hero 1/6", "Carved"),
            "4": ("600", "Champion 2/8", "610", "Hero 1/6", "Runed"),
            "5": ("603", "Champion 3/8", "613", "Hero 2/6", "Runed"),
            "6": ("606", "Champion 4/8", "613", "Hero 2/6", "Runed"),
            "7": ("610", "Hero 1/6", "616", "Hero 3/6", "Runed"),
            "8": ("610", "Hero 1/6", "619", "Hero 4/6", "Runed"),
            "9": ("613", "Hero 2/6", "619", "Hero 4/6", "Gilded"),
            "10": ("613", "Hero 2/6", "623", "Myth 1/6", "Gilded"),
        }
        if arg == None:
            pass
        elif arg.isdigit():
            arg = int(arg)
            if arg == 1:
                arg = 0
            elif arg > 10:
                arg = 10
        elif arg.lower() in keystones_ilvl:
            arg = arg.lower()

        end_ilvl_list = ["Ilvl", True]
        end_track_list = ["Track", True]
        gv_ilvl_list = ["GV ilvl", True]
        gv_track_list = ["GV track", True]
        crest_list = ["Crest", True]
        for level, value in keystones_ilvl.items():
            if arg is None or str(arg) == level:
                end_ilvl, end_track, gv_ilv, gv_track, crest = value
                end_ilvl = f"`{level}` {end_ilvl}"
                end_track = f"`{level}` {end_track}"
                gv_ilv = f"`{level}` {gv_ilv}"
                gv_track = f"`{level}` {gv_track}"
                crest = f"`{level}` {crest}"
                end_ilvl_list.append(end_ilvl)
                end_track_list.append(end_track)
                gv_ilvl_list.append(gv_ilv)
                gv_track_list.append(gv_track)
                crest_list.append(crest)
        embed_list = [end_ilvl_list, end_track_list, gv_ilvl_list, gv_track_list, crest_list]
        for n in range(5):
            value = '\n'.join(embed_list[n][2:])
            embed_list[n].append(value)
            del embed_list[n][2:-1]

        title = "Dungeon item levels"
        embed = self.make_embed(title, None, None, embed_list)
        await ctx.send(embed=embed)

    @commands.command()
    async def affix(self, ctx: commands.Context, next_week: str = "0"):
        if not next_week.isdigit():
            await ctx.send("Podaj cyfrę")
            return
        affix_rotation = (
            "Ascendant",
            "Oblivion",
            "Voidbound",
            "Devour",
        )
        forti_or_tyra = ("Tyrannical", "Fortified")
        start_date = datetime.date(2024, 9, 18)
        current_date = datetime.date.today()
        weeks_passed = (current_date - start_date).days // 7
        if weeks_passed < 0:
            weeks_passed = 0
        current_week = weeks_passed % len(affix_rotation)
        target_week = (current_week + int(next_week)) % len(affix_rotation)
        fortyra = int(next_week) % 2
        start_of_week = start_date + datetime.timedelta(weeks=weeks_passed + int(next_week))
        end_of_week = start_of_week + datetime.timedelta(days=6)
        affix = affix_rotation[target_week]
        await ctx.send(f"**({start_of_week.strftime('%d.%m')} - {end_of_week.strftime('%d.%m')})** Affixes:\n\n"
                        f"**+2:** Bargain: {affix}\n"
                        f"**+4:** {forti_or_tyra[fortyra]}")

    @tasks.loop(hours=24.0)
    async def check(self):
        for message_id, data in self.message_users.items():
            if datetime.datetime.now() - data["time"] > datetime.timedelta(hours=6):
                del self.message_users[message_id]

async def setup(bot):
    await bot.add_cog(mplus(bot))