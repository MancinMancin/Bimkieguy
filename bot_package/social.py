from discord.ext import commands
import discord
import random

class social(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if "kielce" in message.content.lower():
            await message.channel.send(f'Czy to jest boss?')
        if "jestem" in message.content.lower():
            await message.channel.send(f'Jest Dawer?')
        if "zrob " in message.content.lower() or "zrób " in message.content.lower():
            await message.channel.send(f'Dziunia nie jestes mojim szefem')
        if "impreza" in message.content.lower():
            await message.channel.send(f'To jest moja w top 3 ubulio nych impez impeza')
        if "ferb" in message.content.lower():
            await message.channel.send('Już wiem co będziemy dzisiaj robić')

    @commands.command()
    async def poll(self, ctx: commands.Context, *, arg: str):
        index = arg.find(',')
        if index == -1:
            await ctx.send("Please provide options separated by a comma.")
            return

        options = arg[:index].strip()
        arguments = arg[index + 1:].split(",")

        message_to_send = []
        emojis = ["🇦", "🇧", "🇨", "🇩", "🇪", "🇫", "🇬", "🇭", "🇮", "🇯", "🇰", "🇱"]

        for i, argument in enumerate(arguments):
            emoji = emojis[i] if i < len(emojis) else ''
            message_to_send.append(f'{emoji} - {argument.strip()}\n')

        poll_message = await ctx.send(f'**Poll:**\n{options}\n\n' + ''.join(message_to_send))
        await ctx.message.delete()

        for i in range(len(arguments)):
            if i < len(emojis):
                await poll_message.add_reaction(emojis[i])

    @commands.command()
    async def pick(self, ctx: commands.Context, *args: list[str]):
        if len(args) == 0:
            await ctx.send("Daj jakieś rzeczy do losowania ")
            return
        item = random.choice(args)
        await ctx.send(f"{item}")

async def setup(bot):
    await bot.add_cog(social(bot))