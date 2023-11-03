import discord

def setup(bot):
    command_setup(bot)

def command_setup(bot):
    @bot.tree.command(description="Shows help") # Help Command
    async def help(interaction: discord.Interaction):
        name = "Bimkie Guy commands"
        url = "https://i.imgur.com/Ctg5Poz.jpg"
        color = "#f9b4d4"
        fields = {
            "Signup Event": ("🔸/signups <day> <time> <additonal info>", False),
            "Keys Storage": ("🔸/keys\n"
                "🔸/keys <dungeon>\n"
                "🔸/keys <character>\n"
                "🔸/keys <user ping>\n"
                "🔸/keys <level>\n"
                "🔸/keys <level><- or +>"
                "🔸/keys abbr\n" 
                "🔸<keyholder> - [Keystone: <dungeon> (<level>)]", False),
            "Raider.io": ("🔸/rio <character>-<realm>\n"
                "🔸/rio <character>-<realm> <level>\n"
                "🔸/rio <character>-<realm> <level> <f or t>", False),
            "Poll": ("🔸/poll <about>, <option_1>, <option_2>,...", False),
            "Dungeon ilvls": ("🔸/ilvl\n"
                "🔸/ilvl <level>\n", False),
            "Dungeon Guides": ("🔸/guide <dungeon>", False),
            "Affixes": ("🔸/affix\n"
                        "🔸/affix <week in advance>", False)
        }
        foot = "Mancin Mancin"
        foot_icon = "https://media.discordapp.net/attachments/1087696437426528269/1089293104089137282/OIG.awIefY1fsoRX0.jpg?width=676&height=676"
        desc = None
        embed = await make_embed(name, url, fields, foot, foot_icon, desc, color)
        await interaction.response.send_message(embed=embed)

async def make_embed(name, link, dicto, foot, foot_icon, desc, color):
    embed = discord.Embed(
        title = name,
        description = desc,
        color = discord.Color(int(color[1:], 16))
    )
    embed.set_thumbnail(url=link)
    embed.set_footer(text=(f"Made by {foot}"), icon_url=foot_icon)
    for k, _ in dicto.items():
        val = dicto[k][0]
        boo = dicto[k][1]
        embed.add_field(name=k, value=val, inline=boo)
    return embed