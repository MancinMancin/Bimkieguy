from discord.ext import commands, tasks
import discord
import re
import datetime
from .global_variables import message_ids, embeds_to_edit, ping_messages, message_users
from .other import make_embed

def setup(bot):
    bot.add_command(signups)

async def sign_signups(reaction, user):
    message_id = reaction.message.id
    message = reaction.message
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
        edited_embed = await edit_signups(embed, message_id)
        await edit_message.edit(embed=edited_embed)

async def unsign_signups(reaction, user):
    message_id = reaction.message.id
    message = reaction.message
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
        edited_embed = await edit_signups(embed, message_id)
        await edit_message.edit(embed=edited_embed)

@tasks.loop(hours=24.0)
async def check():
    for message_id, data in message_ids.items():
        if datetime.datetime.utcnow() - data["time"] > datetime.timedelta(days=14):
            del message_ids[message_id]
    for message_id, data in message_users.items():
        if datetime.datetime.utcnow() - data["time"] > datetime.timedelta(hours=6):
            del message_users[message_id]

@commands.command()
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

async def edit_signups(embed, message_id):
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