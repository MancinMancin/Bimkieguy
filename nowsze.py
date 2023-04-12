import os
import discord
from discord.ext import commands
import random
import time

from config import TOKEN

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

bot.tank_reactions = []
bot.healer_reactions = []
bot.dps_reactions = []
bot.keystone_reactor = None
start_tank = []
start_healer = []
start_dps = []

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
        if user in bot.tank_reactions and user not in bot.healer_reactions and user not in bot.dps_reactions:
            start_tank.append(user)
        if user in bot.healer_reactions and user not in bot.tank_reactions and user not in bot.dps_reactions:
            start_healer.append(user)
        if user in bot.dps_reactions and user not in bot.tank_reactions and user not in bot.healer_reactions:
            start_dps.append(user)

        if len(start_tank) >= 1:
            if len(start_healer) >= 1:
                if len(start_dps) >= 2:
                    await message.channel.send(f"Group can now be made")
                    time.sleep(3)
                    
                    tank_users = random.choice([u for u in bot.tank_reactions])
                    healer_users = random.choice([u for u in bot.healer_reactions if user not in tank_users])
                    dps_users = random.sample([u for u in bot.dps_reactions if user not in tank_users and user not in healer_users], 2)

                    await message.channel.send(f"Keystone team: \n<:Tank:1095150384164634624> {tank_users[0].mention} \n<:Healer:1095151227379130418> {healer_users[0].mention} \n<:DPS:1095151144864579725> {dps_users[0].mention} \n<:DPS:1095151144864579725> {dps_users[1].mention}")
                    # await message.channel.send(f"Keystone team: \n<:Tank:1095150384164634624> {''.join([user.mention for user in tank_users])} \n<:Healer:1095151227379130418> {''.join([user.mention for user in healer_users])} \n<:DPS:1095151144864579725> {''.join([user.mention for user in dps_users])} \n<:DPS:1095151144864579725> {''.join([user.mention for user in dps_users2])}")
            # else:
    #     await message.channel.send("Not enough players to form a team yet.")
        
                    bot.tank_reactions.clear()
                    bot.healer_reactions.clear()
                    bot.dps_reactions.clear()



bot.run(TOKEN)
