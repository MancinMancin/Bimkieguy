from discord.ext import commands
import datetime
import random

def setup(bot):
    bot.add_command(pimpek)
    bot.add_command(pimpin)
    bot.add_command(boop)
    bot.add_command(ferb)
    bot.add_command(lama)
    bot.add_command(krumfka)
    bot.add_command(sepica)
    bot.add_command(plomykowka)
    bot.add_command(blush)
    bot.add_command(lisek)
    bot.add_command(hug)
    bot.add_command(love)
    bot.add_command(bite)
    bot.add_command(madge)
    bot.add_command(miss)
    bot.add_command(kiss)
    bot.add_command(countdown)
    bot.add_command(goodnight)
    bot.add_command(dobradzien)
    bot.add_command(pimepek)
    bot.add_command(essa)

@commands.command()
async def pimpek(ctx):
    if ctx.guild.id == 724867669257617518:
        await ctx.send("<@363017197926219777>")

@commands.command()
async def pimpin(ctx):
    if ctx.guild.id == 724867669257617518:
        await ctx.send("<@1032790497447657543>")

@commands.command()
async def boop(ctx, target=None):
    if ctx.guild.id == 724867669257617518:
        if ctx.author.id == 363017197926219777:
            if target is None:
                await ctx.send("Qujin boops Mooniedwagon's nose")
            elif target[-1] == 's' or target[-1] == "ś":
                await ctx.send(f"Qujin boops {target}' nose")
            else:
                await ctx.send(f"Qujin boops {target}'s nose")
        elif ctx.author.id == 1032790497447657543:
            if target is None:
                await ctx.send("Mooniedwagon boops Qujin's nose")
            elif target[-1] == 's' or target[-1] == "ś":
                await ctx.send(f"Mooniedwagon boops {target}' nose")
            else:
                await ctx.send(f"Mooniedwagon boops {target}'s nose")
        elif target is None:
            await ctx.send(f"{ctx.message.author} boops his nose")
        elif target[-1] == 's' or target[-1] == "ś":
            await ctx.send(f"{ctx.message.author} boops {target}' nose")
        else:
            await ctx.send(f"{ctx.message.author} boops {target}'s nose")

@commands.command()
async def ferb(ctx, arg=None):
    if ctx.guild.id == 724867669257617518:
        channel = ctx.guild.get_channel(1132957235857854534)
        if arg is None:
            thread = random.choice(channel.threads)
            await ctx.send(f"{thread.mention}")
        else:
            arg = arg.lower()
            for thread in channel.threads:
                if arg == thread.name.lower():
                    messages = []
                    async for message in thread.history(limit=None):
                        for line in message.content.split("\n"):
                            if line.startswith("- ~~") or line.startswith("* ~~") and line.endswith("~~"):
                                continue
                            elif line.startswith("-"):
                                messages.append(line)
                    if messages:
                        random_message = random.choice(messages)
                        await ctx.send(random_message)
                        break
                    else:
                        await ctx.send("W tym wątku nie ma takich rzeczy")
            else:
                await ctx.send("Tyle, że taki wątek nie istnieje")

@commands.command()
async def lama(ctx):
    if ctx.guild.id == 724867669257617518:
        url = "https://i.imgur.com/kc23dC1.png"
        await ctx.send(url)

@commands.command()
async def krumfka(ctx):
    if ctx.guild.id == 724867669257617518:
        url = "https://i.imgur.com/XOky09j.gifv"
        await ctx.send(url)

@commands.command()
async def sepica(ctx):
    if ctx.guild.id == 724867669257617518:
        url = "https://i.imgur.com/7UIP6vQ.png"
        await ctx.send(url)

@commands.command()
async def plomykowka(ctx):
    if ctx.guild.id == 724867669257617518:
        url = "https://i.imgur.com/pjexzEh.png"
        await ctx.send(url)

@commands.command()
async def blush(ctx):
    if ctx.guild.id == 724867669257617518:
        await ctx.send("<:evokerblush:1139320065620185179>")

@commands.command()
async def lisek(ctx):
    if ctx.guild.id == 724867669257617518:
        url = "https://i.imgur.com/Z3DPuoh.png"
        await ctx.send(url)

@commands.command()
async def hug(ctx):
    if ctx.guild.id == 724867669257617518:
        if ctx.channel.id == 1097460207312961606 or ctx.channel.id == 1138943112539017236 or ctx.channel.id == 1132957235857854534:
            url = "https://i.imgur.com/fIdplkT.jpg"
            await ctx.send(url)

@commands.command()
async def love(ctx):
    if ctx.guild.id == 724867669257617518:
        if ctx.channel.id == 1097460207312961606 or ctx.channel.id == 1138943112539017236 or ctx.channel.id == 1132957235857854534:
            await ctx.send("Jeg elsker Deg")

@commands.command()
async def bite(ctx):
    if ctx.guild.id == 724867669257617518:
        if ctx.channel.id == 1097460207312961606 or ctx.channel.id == 1138943112539017236 or ctx.channel.id == 1132957235857854534:
            await ctx.send("Quji bites Morkter with his sharp teeth")

@commands.command()
async def madge(ctx):
    if ctx.guild.id == 724867669257617518:
        url = "https://i.imgur.com/SqXaryv.png"
        await ctx.send(url)

@commands.command()
async def miss(ctx):
    if ctx.guild.id == 724867669257617518:
        if ctx.channel.id == 1097460207312961606 or ctx.channel.id == 1138943112539017236 or ctx.channel.id == 1132957235857854534:
            await ctx.send("Długa jest noc...")

@commands.command()
async def kiss(ctx):
    if ctx.guild.id == 724867669257617518:
        url = "https://i.imgur.com/BmOsHy6.png"
        await ctx.send(url)

@commands.command()
async def countdown(ctx):
    if ctx.guild.id == 724867669257617518:
        target_date = datetime.datetime(2023, 12, 31)
        date = datetime.datetime.now()
        time_difference = target_date - date
        days_remaining = time_difference.days
        if ctx.author.id == 363017197926219777:
            if days_remaining == 1:
                await ctx.send(f'**{days_remaining}** DZIEŃ DO ZOBACZENIA PIMPIN ❤️')
            else:
                await ctx.send(f'**{days_remaining}** DNI DO ZOBACZENIA PIMPIN ❤️')
        if ctx.author.id == 1032790497447657543:
            if days_remaining == 1:
                await ctx.send(f'**{days_remaining}** DZIEŃ DO ZOBACZENIA PIMPEK 🧡')
            else:
                await ctx.send(f'**{days_remaining}** DNI DO ZOBACZENIA PIMPEK 🧡')

@commands.command()
async def goodnight(ctx):
    if ctx.guild.id == 724867669257617518:
        if ctx.channel.id == 1097460207312961606 or ctx.channel.id == 1138943112539017236 or ctx.channel.id == 1132957235857854534:
            await ctx.send("Where /goodnight <:madge:1139642264826695730>")

@commands.command()
async def dobradzien(ctx):
    if ctx.guild.id == 724867669257617518:
        if ctx.channel.id == 1097460207312961606 or ctx.channel.id == 1138943112539017236 or ctx.channel.id == 1132957235857854534:
            await ctx.send("O KURWA RAID ZA 10 GODZIN")

@commands.command()
async def pimepek(ctx):
    if ctx.guild.id == 724867669257617518:
        # if ctx.channel.id == 1097460207312961606 or ctx.channel.id == 1138943112539017236 or ctx.channel.id == 1132957235857854534:
            url = "https://i.imgur.com/uc0j4Tk.png"
            await ctx.send(url)

@commands.command()
async def essa(ctx):
    if ctx.guild.id == 724867669257617518:
        user_nickname = ctx.author.nick if ctx.author.nick else ctx.author.name
        rolled_number = random.randint(0, 100)
        await ctx.send(f"Dzisiejszy poziom essy {user_nickname}: **{rolled_number}**")