import discord
from discord.ext import commands
from config import TOKEN

bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())
bot.remove_command("help")

ext = ["keystorage", "mplus", "other", "social", "wow", "signups"]

@bot.event
async def on_ready():
    for extension in ext:
        try:
            await bot.load_extension(f"bot_package.{extension}")
            print(f"{extension} successfully loaded")
        except (commands.ExtensionNotFound, commands.ExtensionAlreadyLoaded) as e:
            print(f"{extension} couldn't load\n\nError: {e}")
    print(f"Logged in as {bot.user}")

@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    try:
        await bot.load_extension(f"bot_package.{extension}")
        desc = f"{extension} successfully loaded"
    except (commands.ExtensionNotFound, commands.ExtensionAlreadyLoaded) as e:
        desc = f"{extension} couldn't load\n\nError: {e}"
    finally:
        embed = discord.Embed(title='Load', description=desc, color=0xff00c8)
        await ctx.send(embed=embed)

@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
    try:
        await bot.reload_extension(f"bot_package.{extension}")
        desc = f"{extension} successfully reloaded"
    except commands.ExtensionNotLoaded as e:
        desc = f"{extension} couldn't reload\n\nError: {e}"
    finally:
        embed = discord.Embed(title='Reload', description=desc, color=0xff00c8)
        await ctx.send(embed=embed)

bot.run(TOKEN)