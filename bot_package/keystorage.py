from discord.ext import commands, tasks
import datetime
import json
import re
import discord

class keystorage(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.keystones = {}

        with open('keys.json', 'r') as f:
            self.keystones = json.load(f)

        self.dungeons = {
            "ad": "Atal'Dazar",
            "brh": "Black Rook Hold",
            "fall": "Dawn of the Infinite: Galakrond's Fall",
            "rise": "Dawn of the Infinite: Murozond's Rise",
            "dht": "Darkheart Thicket",
            "eb": "The Everbloom",
            "tott": "Throne of the Tides",
            "wm": "Waycrest Manor",
        }
        # self.dungeons = {
        # "bh": "Brackenhide Hollow",
        # "hoi": "Halls of Infusion",
        # "nelt": "Neltharus",
        # "uld": "Uldaman: Legacy of Tyr",
        # "aa": "Algeth'ar Academy",
        # "av": "The Azure Vault",
        # "no": "The Nokhud Offensive",
        # "rlp": "Ruby Life Pools"
        # }



    @tasks.loop(time=datetime.time(hour=4))
    async def reset_keys(self):
        if datetime.datetime.now().weekday() == 2:
            channel = self.bot.get_channel(1077890228854988860)
            self.keystones.clear()
            with open('keys.json', 'w') as f:
                json.dump(self.keystones, f)
            await channel.send("Key list reset")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or (message.channel.id != 1077890228854988860 and message.channel.id != 1155549608550871090):
            return
        unrecognized_dungeons = False
        pattern = r'^(\w+) - \[Keystone: (.+) \((\d+)\)\]$'
        for line in message.content.split("\n"):
            match = re.match(pattern, line)
            if match:
                keyholder_name = match.group(1)
                dungeon_name = match.group(2)
                dungeon_level = match.group(3)
                server_id = message.guild.id
                self.keystones.setdefault(server_id, {})
                if dungeon_name not in self.dungeons.values():
                    unrecognized_dungeons = True
                    break
                for _, data in self.keystones[server_id].items():
                    if keyholder_name in data:
                        data.pop(keyholder_name)
                author_id = message.author.id
                self.keystones[server_id].setdefault(dungeon_name, {})
                self.keystones[server_id][dungeon_name].setdefault(keyholder_name, {})
                self.keystones[server_id][dungeon_name][keyholder_name][dungeon_level] = author_id

                with open("keys.json", "w") as f:
                    json.dump(self.keystones, f)

        if match:
            if unrecognized_dungeons == True:
                await message.channel.send(f"Dungeons provided not recognized")
                return
            await message.delete()

    @commands.command()
    async def keys(self, ctx: commands.Context, arg: str = None):
        with open('keys.json', 'r') as f:
            self.keystones = json.load(f)
        server_id = str(ctx.guild.id)

        if server_id not in self.keystones:
            await ctx.send("There are no keys yet")
            return
        
        matching_keys = []
        if arg is None:
            for key, data in self.keystones[server_id].items():
                for keyholder, level in data.items():
                    matching_keys.append(f'{keyholder} - [Keystone: {key} ({list(level.keys())[0]})]')
        elif arg.isdigit():
            for key, data in self.keystones[server_id].items():
                for keyholder, level in data.items():
                    if arg in level:
                        matching_keys.append(f'{keyholder} - [Keystone: {key} ({list(level.keys())[0]})]')
        elif arg.endswith("-") or arg.endswith("+"):
            given_levels = arg[:-1]
            sign = arg[-1]
            for key, data in self.keystones[server_id].items():
                for keyholder, level in data.items():
                    for l in level.keys():
                        if sign == ("+") and int(l) >= int(given_levels):
                            matching_keys.append(f'{keyholder} - [Keystone: {key} ({list(level.keys())[0]})]')
                        elif sign == ("-") and int(l) <= int(given_levels):
                            matching_keys.append(f'{keyholder} - [Keystone: {key} ({list(level.keys())[0]})]')
        elif arg.lower() in self.dungeons.keys() or arg.lower in map(str.lower, self.dungeons.values()):
            found_keys = {}
            key = self.dungeons.get(arg.lower()) or [v for v in self.dungeons.values() if v.lower() == arg.lower()][0]
            found_keys = self.keystones.get(server_id, {}).get(key, {})
            if found_keys:
                for keyholder, level in found_keys.items():
                    matching_keys.append(f'{keyholder} - [Keystone: {key} ({list(level.keys())[0]})]')
        elif arg.lower() == "abbr":
            message_to_send = "\n".join([f'"{k}" for {v}' for k, v in self.dungeons.items()])
            await ctx.send(message_to_send)
            return
        elif arg.startswith("<@") and arg.endswith(">"):
            member_id = int(arg[2:-1])
            for key, data in self.keystones[server_id].items():
                for keyholder, level in data.items():
                    if member_id == int(list(level.values())[0]):
                        matching_keys.append(f'{keyholder} - [Keystone: {key} ({list(level.keys())[0]})]')
        elif any(arg.lower() in str(val).lower() for _, val in self.keystones.get(server_id, {}).items()):
            for key, data in self.keystones[server_id].items():
                for keyholder, level in data.items():
                    if keyholder.lower() == arg.lower():
                        matching_keys.append(f'{keyholder} - [Keystone: {key} ({list(level.keys())[0]})]')
        elif arg.lower() == "reset":
            self.keystones.clear()
            with open("keys.json", "w") as f:
                json.dump(self.keystones, f)
            await ctx.send("Key list reset")
            return

        if matching_keys:
            message_to_send = "\n".join(matching_keys)
            await ctx.send(message_to_send)
        else:
            await ctx.send("There are no such keys")

async def setup(bot):
    await bot.add_cog(keystorage(bot))