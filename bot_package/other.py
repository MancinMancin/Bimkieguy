from discord.ext import commands
import discord

class other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx: commands.Context):
        name = "Bimkie Guy commands"
        url = "https://i.imgur.com/Ctg5Poz.jpg"
        color = discord.Color.magenta()
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

        embed = discord.Embed(title=name, color=color)
        embed.set_footer(text=(f"Made by {foot}"), icon_url=foot_icon)
        embed.set_thumbnail(url=url)
        for k, v in fields.items():
            embed.add_field(name=k, value=v[0], inline=v[1])
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(other(bot))