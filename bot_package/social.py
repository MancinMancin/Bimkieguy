from discord.ext import commands
import random

def setup(bot):
    bot.add_command(poll)
    bot.add_command(pick)

async def kielce(message):
    if message.guild.id == 521281100069470208:
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
    if message.guild.id == 724867669257617518: 
        if "ferb" in message.content.lower():
            await message.channel.send('Już wiem co będziemy dzisiaj robić')
        if "zrob " in message.content.lower() or "zrób " in message.content.lower():
            await message.channel.send(f'Dziunia nie jestes mojim szefem')
        if "impreza" in message.content.lower():
            await message.channel.send(f'To jest moja w top 3 ubulio nych impez impeza')

@commands.command()
async def poll(ctx, *, arg):
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
async def pick(ctx, *args):
    if len(args) == 0:
        await ctx.send("Dej jakieś rzeczy do losowania byq")
        return
    item = random.choice(args)
    await ctx.send(f"{item}")