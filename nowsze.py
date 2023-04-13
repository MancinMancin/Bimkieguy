import discord
from discord.ext import commands
import random
import time

from config import TOKEN

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

bot.tank_reactions = []
bot.healer_reactions = []
bot.dps_reactions = []

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

def select_elements(list_1, list_2, list_3):
    unique_1, unique_2, unique_3 = None, None, None
    if len(list_1) >= 1:
        unique_1 = random.choice(list(set(list_1)))
        list_2 = [el for el in list_2 if el != unique_1]
        list_3 = [el for el in list_3 if el != unique_1]
    if len(list_2) >= 1:
        unique_2 = random.choice(list(set(list_2)))
        list_3 = [el for el in list_3 if el != unique_2]
    if len(list_3) >= 2:
        unique_3 = random.sample(list(set(list_3)), 2)
    if not unique_1 or not unique_2 or not unique_3:
        return
    return unique_1, unique_2, unique_3

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    
    message = reaction.message
    if '<@&724869170734432258>' in message.content:
        if str(reaction.emoji) == '<:Tank:1095150384164634624>':
            bot.tank_reactions.append(user)
        elif str(reaction.emoji) == '<:Healer:1095151227379130418>':
            bot.healer_reactions.append(user)
        elif str(reaction.emoji) == '<:DPS:1095151144864579725>':
            bot.dps_reactions.append(user)
        print(bot.tank_reactions[0].id)
        try:
            start_tank, start_healer, start_dps = (select_elements(bot.tank_reactions, bot.healer_reactions, bot.dps_reactions))
        except TypeError:
            return

        await message.channel.send(f"Group can now be made")
        time.sleep(3)
        try:
            tank_users, healer_users, dps_users = (select_elements(bot.tank_reactions, bot.healer_reactions, bot.dps_reactions))
        except TypeError:
            await message.channel.send(f"Cannot form a team due to people unsigning.")
            return
        
        await message.channel.send(f"Keystone team:\n<:Tank:1095150384164634624> {tank_users.mention}\n<:Healer:1095151227379130418> {healer_users.mention}\n<:DPS:1095151144864579725> {dps_users[0].mention}\n<:DPS:1095151144864579725> {dps_users[1].mention}\n```{tank_users.mention}\n{healer_users.mention}\n{dps_users[0].mention}\n{dps_users[1].mention}```")

        
bot.tank_reactions.clear()
bot.healer_reactions.clear()
bot.dps_reactions.clear()


bot.run(TOKEN)