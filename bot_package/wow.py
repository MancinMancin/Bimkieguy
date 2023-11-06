from discord.ext import commands

def setup(bot):
    bot.add_command(wa)

@commands.command()
async def wa(ctx):
    await ctx.send("Dungeon Talent Reminder:\n"
                   "<https://wago.io/Vt4e96WAA>")