import discord
from discord.ext import commands
import random

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

        # Select users only when all roles are present
        if len(bot.tank_reactions) >= 1 and len(bot.healer_reactions) >= 1 and len(bot.dps_reactions) >= 2:
            # select one user from each category, ensuring they are different users
            tank_users = [random.choice([user for user in bot.tank_reactions])] 
            healer_users = ([random.choice([user for user in bot.healer_reactions if user not in tank_users])])  # select one healer user
            dps_users = (random.sample([user for user in bot.dps_reactions if user not in tank_users and user not in healer_users], 2))  # select two dps users
            print(f"dupa123")

            # dps_mentions = ""
            # for user in dps_users:
            #     dps_mentions += f"{user.mention}\n"

            # send a message with the selected users
            await message.channel.send(f"Keystone team: \n<:Tank:1095150384164634624> {''.join([user.mention for user in tank_users])} \n<:Healer:1095151227379130418> {''.join([user.mention for user in healer_users])} \n<:DPS:1095151144864579725> {', '.join([user.mention for user in dps_users])}")

        # else:
        #     await message.channel.send("Not enough players to form a team yet.")
            
            bot.tank_reactions.clear()
            bot.healer_reactions.clear()
            bot.dps_reactions.clear()
        # if bot.keystone_reactor is not None and 
        # if len(bot.tank_reactions) >= 1 and len(bot.healer_reactions) >= 1 and len(bot.dps_reactions) >= 1:
        #     # Select one tank user
        #     tank_users = [user for user in bot.tank_reactions if user not in bot.healer_reactions and user not in bot.dps_reactions]
        #     selected_tank = random.choice(tank_users) if tank_users else None
        #     print(f"wybrany tank", selected_tank)


        #     # Select one healer user
        #     healer_users = [user for user in bot.healer_reactions if user not in bot.tank_reactions and user not in bot.dps_reactions]
        #     selected_healer = random.choice(healer_users) if healer_users else None
        #     print(f"wybrany hiler", selected_healer)

        #     # Select two DPS users
        #     dps_users = [user for user in bot.dps_reactions if user not in bot.tank_reactions and user not in bot.healer_reactions]
        #     selected_dps = random.sample(dps_users, min(1, len(dps_users)))
        #     print(f"wybrany dps", selected_dps)

        #     # Combine selected users into a list
        #     selected_users = [selected_tank, selected_healer] + selected_dps
        #     selected_users = [user.name for user in selected_users if user is not None]
        #     print(f"ekipa", selected_users)

            # select one user from each category, ensuring they are different users
            # users = [user for user in bot.tank_reactions if user not in bot.healer_reactions and user not in bot.dps_reactions]  # select one tank user
            # users.extend([user for user in bot.healer_reactions if user not in bot.tank_reactions and user not in bot.dps_reactions])  # select one healer user
            # # users.extend([user for user in bot.dps_reactions if user not in bot.tank_reactions and user not in bot.healer_reactions])  # select two dps users
            # print("Keystone reactor is not None and all reaction requirements met")
            # # print(len(users))
            # print(bot.tank_reactions)
            # print(bot.healer_reactions)
            # print(bot.dps_reactions)
            # # if len(users) == 3:
            #     print("kurwa dziala")
            #     await message.channel.send(f"The drawn users are: {' '.join([user.mention for user in users])}")
            #     # reset the reaction lists and keystone reactor
            #     bot.tank_reactions = []
            #     bot.healer_reactions = []
            #     bot.dps_reactions = []
            #     bot.keystone_reactor = None


bot.run('MTA5NTA1NTE0MzU1ODQ2MzY2MA.GHkFFW.HWL4clvQlE_k3vflDaury9nKbSVoPpDlvtHRUs')