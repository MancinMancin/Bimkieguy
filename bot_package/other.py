from discord.ext import commands
import discord
import json

class other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.roles_dict = {
            "<:Muslim_Uncle_Pepe:1098289343627526266>": 989535345370628126,
            "<:icon_chaos_dungeon:1287839347952848979>": 1087697492038131762,
            "<:ui_profession_alchemy:1287875578212651069>": 1278676590397489253,
            "<:raven:1287875463397642282>": 1105548968697540679,
            "<:Phasmo:1287875301510090814>": 1203456671490506862,
        }

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
                "🔸/keys <level><- or +>\n"
                "🔸/keys abbr\n" 
                "🔸<keyholder> - [Keystone: <dungeon> (<level>)]", False),
            "Raider.io": ("🔸/rio <character>-<realm>\n"
                "🔸/rio <character>-<realm> <level>", False),
            "Poll": ("🔸/poll <about>, <option_1>, <option_2>,...", False),
            "Dungeon ilvls": ("🔸/ilvl\n"
                "🔸/ilvl <level>\n", False),
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

    @commands.command()
    async def role(self, ctx: commands.Context):
        await ctx.message.delete()
        message_key = "message_id"
        message_to_send = "Zareaguj, by dostać rolę"
        for emoji, role_id in self.roles_dict.items():
            role = ctx.guild.get_role(role_id)
            message_to_send += f"\n\n{emoji}: `{role.name}`"
        try:
            with open("options.json", "r") as f:
                options = json.load(f)
            message_id = options[message_key]
        except FileNotFoundError:
            options = {}
            message_id = None
        except KeyError:
            message_id = None

        if not message_id:
            message = await ctx.send(message_to_send)
            for emoji in self.roles_dict.keys():
                await message.add_reaction(emoji)
            options[message_key] = message.id
            with open("options.json", "w") as f:
                json.dump(options, f)
        else:
            message: discord.Message = await ctx.fetch_message(message_id)
            await message.edit(content=message_to_send)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if str(payload.emoji) in self.roles_dict.keys():
            role_id = self.roles_dict[str(payload.emoji)]
            guild = self.bot.get_guild(payload.guild_id)
            role = guild.get_role(role_id)
            await payload.member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        if str(payload.emoji) in self.roles_dict.keys():
            role_id = self.roles_dict[str(payload.emoji)]
            guild = self.bot.get_guild(payload.guild_id)
            role = guild.get_role(role_id)
            member = guild.get_member(payload.user_id)
            await member.remove_roles(role)

async def setup(bot):
    await bot.add_cog(other(bot))