from discord.ext import commands

class wow(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def wago(self, ctx: commands.Context):
        await ctx.send("**Dungeon Talent Reminder:**\n"
                       "<https://wago.io/Vt4e96WAA>\n\n"
                       
                       "**Dungeon Teleports:**\n"
                       "<https://wago.io/aCa7oAT5y>\n\n"

                       "**CC Rotation:**\n"
                       "<https://wago.io/F2nyTZ7q8>\n\n"
                       
                       "**Cresty Addon:**\n"
                       "<https://www.curseforge.com/wow/addons/cresty>\n\n"
                       
                       "**Voidbound Absorb Mod**\n"
                       "<https://wago.io/9jR3ONZiz>")  

async def setup(bot):
    await bot.add_cog(wow(bot))