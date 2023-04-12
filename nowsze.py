import discord
from discord.ext import commands
import random
import time

with open("tokenisko.py", "r") as f:
    TOKEN = f.read().strip()


bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

bot.tank_reactions = []
bot.healer_reactions = []
bot.dps_reactions = []
bot.keystone_reactor = None

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
        print(user.name)
        if str(reaction.emoji) == '<:Tank:1095150384164634624>':
            print(f"{bot.tank_reactions}")
            bot.tank_reactions.append(user)
            print(f"Added {user.name} {len(bot.tank_reactions)}to tank reactions list")
            print(f"tankowie", bot.tank_reactions)
        elif str(reaction.emoji) == '<:Healer:1095151227379130418>':
            bot.healer_reactions.append(user)
            print(f"Added {user.name} {len(bot.healer_reactions)} to healer reactions list")
        elif str(reaction.emoji) == '<:DPS:1095151144864579725>':
            bot.dps_reactions.append(user)
            print(f"Added {user.name} {len(bot.dps_reactions)}to DPS reactions list")

        if len(bot.tank_reactions) >= 1 and len(bot.healer_reactions) >= 1 and len(bot.dps_reactions) >= 2:
        
            tank_users = [random.choice([user for user in bot.tank_reactions])] 
            healer_users = ([random.choice([user for user in bot.healer_reactions if user not in tank_users])])  # select one healer user
            dps_users = ([random.choice([user for user in bot.dps_reactions if user not in tank_users and user not in healer_users])])  # select two dps users
            dps_users2 = ([random.choice([user for user in bot.dps_reactions if user not in tank_users and user not in healer_users and user not in dps_users])])
            print(f"dupa123")

            await message.channel.send(f"Keystone team: \n<:Tank:1095150384164634624> {''.join([user.mention for user in tank_users])} \n<:Healer:1095151227379130418> {''.join([user.mention for user in healer_users])} \n<:DPS:1095151144864579725> {''.join([user.mention for user in dps_users])} \n<:DPS:1095151144864579725> {''.join([user.mention for user in dps_users2])}")
        # else:
        #     await message.channel.send("Not enough players to form a team yet.")
            
            bot.tank_reactions.clear()
            bot.healer_reactions.clear()
            bot.dps_reactions.clear()

bot.run()