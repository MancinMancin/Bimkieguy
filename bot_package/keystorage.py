from discord.ext import commands, tasks
import re
import json
import datetime

with open('keys.json', 'r') as f:
    keystones = json.load(f)

def setup(bot):
    bot.add_command(keys)

@tasks.loop(minutes=60.0)
async def reset_keys(bot):
    if datetime.datetime.now().weekday() == 2 and datetime.datetime.now().hour == 6:
        channel = bot.get_channel(1077890228854988860)
        keystones.clear()
        with open('keys.json', 'w') as f:
            json.dump(keystones, f)
        await channel.send("Key list reset")

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
            # if dungeon_name not in ["Atal'dazar", "Black Rook Hold", "DOTI: Galakrond's Fall", "DOTI: Murozond's Rise", "Darkheart Thicket", "Everbloom", "Throne of the Tides", "Waycrest Manor"]:
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

@commands.command()
async def keys(ctx, *, arg=None):
    server_id = str(ctx.guild.id)
    matching_keys = []
    message_to_send = []
    # abbreviations = {
# 'ad': "Atal'dazar",
# 'brh': 'Black Rook Hold',
# 'fall': 'DOTI: Galakrond's Fall',
# 'rise': 'DOTI: Murozond's Rise',
# 'dht': 'Darkheart Thicket',
# 'eb': 'The Everbloom',
# 'tott': "Throne of the Tides",
# 'wm': 'Waycrest Manor',
# }
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