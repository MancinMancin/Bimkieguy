import discord
from discord.ext import commands
from bot_package.moonie import setup as setup_moonie
from bot_package.social import setup as setup_social, kielce
from bot_package.keystorage import setup as setup_keystorage, reset_keys, on_keystone_message
from bot_package.mplus import setup as setup_mplus, reset_cache, bot_react, sign_mplus, unsign_mplus
from bot_package.signups import setup as setup_signups, check, sign_signups, unsign_signups
from bot_package.other import setup as setup_other
from bot_package.wow import setup as setup_wow
from config import TOKEN

bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())
bot.remove_command("help")

setup_moonie(bot)
setup_social(bot)
setup_keystorage(bot)
setup_mplus(bot)
setup_signups(bot)
setup_other(bot)
setup_wow(bot)

@bot.event
async def on_message(message):
    await bot_react(message)
    await kielce(message)
    await on_keystone_message(message)
    await bot.process_commands(message)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    reset_keys.start(bot)
    reset_cache.start()
    check.start()
    await bot.tree.sync()

@bot.event
async def on_reaction_add(reaction, user):
    await sign_mplus(reaction, user)
    await sign_signups(reaction, user)

@bot.event
async def on_reaction_remove(reaction, user):
    await unsign_mplus(reaction, user)
    await unsign_signups(reaction, user)

bot.run(TOKEN)