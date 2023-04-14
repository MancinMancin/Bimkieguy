from unittest.mock import MagicMock
import discord
from discord.ext import commands
import random
import asyncio


import discord
from discord.ext import test

async def test_reaction_add():
    # create a testing context
    ctx = test.Context()

    # create a fake message
    message = await ctx.send('<@&724869170734432258>')

    # simulate reactions
    await ctx.simulate_reaction_add(message, '🛡️', ctx.author)
    await ctx.simulate_reaction_add(message, '🩹', ctx.author)
    await ctx.simulate_reaction_add(message, '🗡️', ctx.author)
    await ctx.simulate_reaction_add(message, '🔑', ctx.author)

    # assert that the message was sent
    assert ctx.sent[-1].content == "Keystone team:\n<:Tank:1095150384164634624> @TestUser\n<:Healer:1095151227379130418> @TestUser\n<:DPS:1095151144864579725> @TestUser\n<:DPS:1095151144864579725> @TestUser\n<:Keystone:1095145259903750265> @TestUser\n```@TestUser\n@TestUser\n@TestUser\n@TestUser```"

