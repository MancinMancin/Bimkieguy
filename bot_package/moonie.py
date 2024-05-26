from discord.ext import commands
import datetime
import random
import discord

class moonie(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def is_moojins(self, ctx: commands.Context) -> bool:
        if ctx.guild.id == 724867669257617518:
            return True
        else:
            return False
        
    def is_liskonoski(self, ctx: commands.Context) -> bool:
        if ctx.channel.category and ctx.channel.category_id == 1150536810515157063:
            return True
        else:
            return False

    @commands.command()
    async def pimpek(self, ctx: commands.Context):
        if self.is_moojins(ctx):
            await ctx.send("<@363017197926219777>")

    @commands.command()
    async def pimpin(self, ctx: commands.Context):
        if self.is_moojins(ctx):
            await ctx.send("<@1032790497447657543>")

    @commands.command()
    async def boop(self, ctx: commands.Context, target: str = None):
        if self.is_moojins(ctx):
            outside_booper = False
            if ctx.author.id == 363017197926219777:
                booper = "Qujin"
                booped = "Mooniedwagon"
            elif ctx.author.id == 1032790497447657543:
                booper = "Mooniedwagon"
                booped = "Qujin"
            elif ctx.author.id == 1209505224222580741:
                booper = "Nisia"
                booped = "Quji"
            else:
                booper = ctx.message.author
                outside_booper = True
            if target is None:
                if not outside_booper:
                    await ctx.send(f"{booper} boops {booped}'s nose")
                else:
                    await ctx.send(f"{booper} boops his nose")
            elif target[-1].lower() == "s" or target[-1].lower() == "ś":
                await ctx.send(f"{booper} boops {target}' nose")
            else:
                await ctx.send(f"{booper} boops {target}'s nose")     

    @commands.command()
    async def ferb(self, ctx: commands.Context, arg: str = None):
        if self.is_moojins(ctx):
            channel = ctx.guild.get_channel(1132957235857854534)
            if arg is None:
                thread = random.choice(channel.threads)
                await ctx.send(thread.mention)
            else:
                arg = arg.lower()
                for thread in channel.threads:
                    if arg == thread.name.lower():
                        messages = []
                        async for message in thread.history(limit=None):
                            for line in message.content.split("\n"):
                                if (line.startswith("- ~~") or line.startswith("* ~~")) and line.endswith("~~"):
                                    continue
                                elif line.startswith("-") or line.startswith("*"):
                                    messages.append(line)
                        if messages:
                            random_message = random.choice(messages)
                            await ctx.send(random_message)
                        else:
                            await ctx.send("W tym wątku nie ma takich rzeczy")
                    else:
                        await ctx.send("Tyle, że taki wątek nie istnieje")

    @commands.command()
    async def lama(self, ctx: commands.Context):
        if self.is_moojins(ctx):
            url = "https://i.imgur.com/kc23dC1.png"
            await ctx.send(url)

    @commands.command()
    async def krumfka(self, ctx: commands.Context):
        if self.is_moojins(ctx):
            url = "https://i.imgur.com/XOky09j.gifv"
            await ctx.send(url)
    
    @commands.command()
    async def sepica(self, ctx: commands.Context):
        if self.is_moojins(ctx):
            url = "https://i.imgur.com/7UIP6vQ.png"
            await ctx.send(url)

    @commands.command()
    async def plomykowka(self, ctx: commands.Context):
        if self.is_moojins(ctx):
            url = "https://i.imgur.com/pjexzEh.png"
            await ctx.send(url)

    @commands.command()
    async def lisek(self, ctx: commands.Context):
        if self.is_moojins(ctx):
            url = "https://i.imgur.com/Z3DPuoh.png"
            await ctx.send(url)

    @commands.command()
    async def blush(self, ctx: commands.Context):
        if self.is_moojins(ctx):
            await ctx.send("<:evokerblush:1139320065620185179>")

    @commands.command()
    async def hug(self, ctx: commands.Context):
        if self.is_moojins(ctx) and self.is_liskonoski(ctx):
            url = "https://i.imgur.com/fIdplkT.jpg"
            await ctx.send(url)

    @commands.command()
    async def love(self, ctx: commands.Context):
        if self.is_moojins(ctx) and self.is_liskonoski(ctx):
            await ctx.send("Jeg elsker Deg")

    @commands.command()
    async def bite(self, ctx: commands.Context):
        if self.is_moojins(ctx) and self.is_liskonoski(ctx):
            await ctx.send("Quji bites Morkter with his sharp teeth")

    @commands.command()
    async def bite(self, ctx: commands.Context):
        if self.is_moojins(ctx):
            url = "https://i.imgur.com/SqXaryv.png"
            await ctx.send(url)

    @commands.command()
    async def miss(self, ctx: commands.Context):
        if self.is_moojins(ctx) and self.is_liskonoski(ctx):
            await ctx.send("Długa jest noc...")

    @commands.command()
    async def kiss(self, ctx: commands.Context):
        if self.is_moojins(ctx) and self.is_liskonoski(ctx):
            url = "https://i.imgur.com/BmOsHy6.png"
            await ctx.send(url)

    @commands.command()
    async def countdown(self, ctx: commands.Context):
        if self.is_moojins(ctx):
            target_date = datetime.datetime(2024, 8, 24)
            date = datetime.datetime.now()
            time_difference = target_date - date
            days_remaining = time_difference.days
            if ctx.author.id == 363017197926219777:
                target_seen = "PIMPIN ❤️"
            elif ctx.author.id == 1032790497447657543 or ctx.author.id == 1209505224222580741:
                target_seen = "PIMPEK 🧡"
            if days_remaining == 1:
                await ctx.send(f"**{days_remaining}** DZIEŃ DO ZOBACZENIA {target_seen}")
            else:
                await ctx.send(f"**{days_remaining}** DNI DO ZOBACZENIA {target_seen}")

    @commands.command()
    async def goodnight(self, ctx: commands.Context):
        if self.is_moojins(ctx):
            await ctx.send("Where /goodnight <:madge:1139642264826695730>")

    @commands.command()
    async def dobradzien(self, ctx: commands.Context):
        if self.is_moojins(ctx):
            await ctx.send("Where /goodnight <:madge:1139642264826695730>")
  
    @commands.command()
    async def pimepek(self, ctx: commands.Context):
        url = "https://i.imgur.com/uc0j4Tk.png"
        await ctx.send(url)

    @commands.command()
    async def essa(self, ctx: commands.Context):
        poziom_essy = random.randint(0, 100)
        if poziom_essy <= 50:
            message = "Tak se."
        elif poziom_essy <= 100:
            message = "Ale essa!"
        dsc_color = discord.Colour.light_embed()
        embed = discord.Embed(title=f"{ctx.author.display_name}!", color=dsc_color, description=f"{message}\n\nTwój dzisiejszy poziom essy to **{poziom_essy}**")
        embed.set_thumbnail(url=ctx.author.avatar)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(moonie(bot))