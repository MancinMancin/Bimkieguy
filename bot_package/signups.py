from discord.ext import tasks, commands
import datetime
import re
import typing
import time as tm
import discord
import asyncio

class signups(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.klasy = {
            "Death Knight": (("Tank", "DPS"), "<:deathknight:1274858415629271141>"),
            "Demon Hunter": (("Tank", "DPS"), "<:demon_hunter:1274858416656879692>"),
            "Druid": (("Tank", "Heal", "DPS"), "<:druid:1274858419089838172>"),
            "Evoker": (("Heal", "DPS"), "<:evoker:1274858507388321844>"),
            "Hunter": (("DPS",), "<:hunter:1274858422264664064>"),
            "Mage": (("DPS",), "<:mage:1274858423149920389>"),
            "Monk": (("Tank", "Heal", "DPS"), "<:monk:1274858425142083636>"),
            "Paladin": (("Tank", "Heal", "DPS"), "<:paladin:1274858426547310633>"),
            "Priest": (("Heal", "DPS"), "<:priest:1274858427956592670>"),
            "Rogue": (("DPS",), "<:rogue:1274858509263175693>"),
            "Shaman": (("Heal", "DPS"), "<:shaman:1274858431131680850>"),
            "Warlock": (("DPS",), "<:warlock:1274858433488752773>"),
            "Warrior": (("Tank", "DPS"), "<:warrior:1274858511112736798>")
        }
        self.dreadful = "Dreadful"
        self.mystic = "Mystic"
        self.venerated = "Venerated"
        self.zenith = "Zenith"
        self.sets = {
            self.dreadful: ("<:deathknight:1274858415629271141>", "<:demon_hunter:1274858416656879692>", "<:warlock:1274858433488752773>"),
            self.mystic: ("<:druid:1274858419089838172>", "<:hunter:1274858422264664064>", "<:mage:1274858423149920389>"),
            self.venerated: ("<:paladin:1274858426547310633>", "<:priest:1274858427956592670>", "<:shaman:1274858431131680850>"),
            self.zenith: ("<:evoker:1274858507388321844>", "<:monk:1274858425142083636>", "<:rogue:1274858509263175693>", "<:warrior:1274858511112736798>"),
        }
        self.eventy: list[discord.Message] = []
        self.loops = [self.delete_event]
        [x.start() for x in self.loops]

    def cog_unload(self):
        [x.cancel() for x in self.loops]

    @tasks.loop(hours=24)
    async def delete_event(self):
        for tuple in self.eventy:
            message = tuple[0]
            unix = tuple[1]
            if datetime.datetime.now() > datetime.datetime.fromtimestamp(unix):
                await message.edit(view=self.ZapisyZamkniete())
                self.eventy.remove(tuple)
    
    async def edit_embed(self, interaction: discord.Interaction, role: str, answers: list[str]):
        for message, _ in self.eventy:
            if interaction.message.id == message.id:
                embed_to_edit: discord.Embed = message.embeds[0]
                for i, field in enumerate(embed_to_edit.fields[4:]):
                    emoji = self.klasy.get(answers[0])[1]
                    lines = field.value.split("\n")
                    new_lines = [line for line in lines if interaction.user.mention not in line]
                    field.value = "\n".join(new_lines)
                    if role in field.name:
                        field.value = f"{field.value}\n{emoji}{interaction.user.mention}"
                    length = len(field.value.split("\n"))
                    embed_to_edit.set_field_at(i + 4, name=f"{field.name[:-4]} `{length - 1}`", value=field.value, inline=field.inline)

                # Edit total
                all = sum(len(field.value.split("\n")) for field in embed_to_edit.fields[4:]) - 3
                kek_field = embed_to_edit.fields[3]
                kek_field.value = f"`{all}`"
                embed_to_edit.set_field_at(3, name=kek_field.name, value=kek_field.value, inline=kek_field.inline)

                # Edit buffs
                buff_field = embed_to_edit.fields[1]
                buffs = ''.join([value[1] for value in self.klasy.values()])
                buffs += "\n"
                classes_in_embed = "".join([field.value for field in embed_to_edit.fields[4:]])
                for value in self.klasy.values():
                    buffs += "<a:check:1274861623525376194>" if value[1] in classes_in_embed else "❌"
                buff_field.value = buffs
                embed_to_edit.set_field_at(1, name=buff_field.name, value=buff_field.value, inline=buff_field.inline)

                # Edit sets
                sets = [0, 0, 0, 0]
                for i, (_, emojis) in enumerate(self.sets.items()):
                    for emoji in emojis:
                        count = classes_in_embed.count(emoji)
                        sets[i] += count
                sets_field = embed_to_edit.fields[2]
                sets_field.value = (f"{self.dreadful}: `{sets[0]}` {''.join(self.sets.get(self.dreadful))}\n"
                                    f"{self.mystic}: `{sets[1]}` {''.join(self.sets.get(self.mystic))}\n"
                                    f"{self.venerated}: `{sets[2]}` {''.join(self.sets.get(self.venerated))}\n"
                                    f"{self.zenith}: `{sets[3]}` {''.join(self.sets.get(self.zenith))}")
                embed_to_edit.set_field_at(2, name=sets_field.name, value=sets_field.value, inline=sets_field.inline)
                await message.edit(embed=embed_to_edit)

    def get_emojis(self, name: str) -> list[str]:
        classes = self.sets[name]
        emoji_list = []
        for classa in classes:
            emoji = self.klasy.get(classa)[1]
            emoji_list.append(emoji)
        return emoji_list
    
    async def edit_unix_desc(self, interaction: discord.Interaction, new_unix: typing.Tuple[str, str], new_desc: str):
        for idx, (message, _) in enumerate(self.eventy):
            if interaction.message.id == message.id:
                if new_unix:
                    self.eventy[idx] = (message, new_unix)
                    new_unix = f"<t:{new_unix}:F>"
                embed_to_edit: discord.Embed = message.embeds[0]
                embed_to_edit.description = new_desc or embed_to_edit.description
                time_field = embed_to_edit.fields[0]
                embed_to_edit.set_field_at(0, name=time_field.name, value=new_unix or time_field.value, inline=time_field.inline)
                await message.edit(embed=embed_to_edit)

    async def get_new_unix_desc(self, dm_recipient: discord.User) -> typing.Tuple[typing.Tuple[str, str], str]:
        skip = "skip"
        unix, new_desc = None, None
        await dm_recipient.send(f"Change date/time or `{skip}`")
        while True:
            try:
                response_time: discord.Message = await self.bot.wait_for("message", timeout=60, check=lambda m: not m.author.bot)
            except asyncio.TimeoutError:
                await dm_recipient.send("You took too long to respond")
                return
            if response_time.content.lower() != skip:
                split_msg = response_time.content.split()
                date = split_msg[0]
                time = split_msg[1]
                unix = self.make_unix(date, time)
                if not unix:
                    await dm_recipient.send("Wrong date or time, try again")
                    continue
                else:
                    break
            break
        await dm_recipient.send("Change description or `skip`")
        try:
            response_desc: discord.Message = await self.bot.wait_for("message", timeout=60, check=lambda m: not m.author.bot)
        except asyncio.TimeoutError:
            await dm_recipient.send("You took too long to respond")
            return
        if response_desc.content.lower() != skip:
            new_desc = response_desc.content
        return unix, new_desc

    class ZapisyZamkniete(discord.ui.View):
        def __init__(self):
            super().__init__()
            options=[
                discord.SelectOption(label="Lootbody", value="Lootbody")
            ]
            self.select = discord.ui.Select(placeholder="Zapisy zamknięte", options=options, disabled=True)
            self.add_item(self.select)

    class ChooseClass(discord.ui.Select):
        def __init__(self, cog_self, main_interaction: discord.Interaction, role):
            self.cog_self = cog_self
            self.main_interaction = main_interaction
            self.role = role
            options = [
                discord.SelectOption(emoji=role_emoji[1], label=klasa, value=klasa)
                                    for klasa, role_emoji in self.cog_self.klasy.items() if role in role_emoji[0]
            ]
            super().__init__(options=options, placeholder="Wybierz klasę")
        async def callback(self, interaction: discord.Interaction):
            await self.cog_self.edit_embed(self.main_interaction, self.role, self.values)
            await self.main_interaction.edit_original_response(content="Zapisano", view=None)

    class View(discord.ui.View):
        def __init__(self, cog_self, author_id):
            super().__init__(timeout=None)
            self.cog_self = cog_self
            self.author_id = author_id
        async def button_click(self, interaction: discord.Interaction, role: str):
            select_class = self.cog_self.ChooseClass(self.cog_self, interaction, role)
            view = discord.ui.View()
            view.add_item(select_class)
            await interaction.response.send_message(view=view, ephemeral=True)
        @discord.ui.button(label="Tank", style=discord.ButtonStyle.blurple, emoji="<:Tank_icon:1103828509996089499>")
        async def callback_tank(self, interaction: discord.Interaction, button: discord.ui.Button):
            await self.button_click(interaction, "Tank")
        @discord.ui.button(label="Healer", style=discord.ButtonStyle.blurple, emoji="<:Healer_icon:1103828598722416690>")
        async def callback_healer(self, interaction: discord.Interaction, button: discord.ui.Button):
            await self.button_click(interaction, "Heal")
        @discord.ui.button(label="DPS", style=discord.ButtonStyle.blurple, emoji="<:Dps_icon:1103828601075413145>")
        async def callback_dps(self, interaction: discord.Interaction, button: discord.ui.Button):
            await self.button_click(interaction, "DPS")
        @discord.ui.button(label="Wypisz się", style=discord.ButtonStyle.red)
        async def callback_out(self, interaction: discord.Interaction, button: discord.ui.Button):
            await self.cog_self.edit_embed(interaction, "None", ["Druid"])
            await interaction.response.send_message(content="Wypisano", ephemeral=True)
        @discord.ui.button(label="Edytuj", style=discord.ButtonStyle.green)
        async def callback_edit(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.defer()
            if interaction.user.id == self.author_id or interaction.user.guild_permissions.administrator:
                dm_recipient = interaction.user
                unix, new_desc = await self.cog_self.get_new_unix_desc(dm_recipient)
                await self.cog_self.edit_unix_desc(interaction, unix, new_desc)
                await dm_recipient.send("Event updated")

    def make_unix(self, date: str, time: str) -> typing.Tuple[str, str]:
        pattern_date = r"(3[01]|[12][0-9]|0?[1-9])[\.\-\:\/]?(1[0-2]|0?[1-9])?[.\-\:\/]?(\d{4})?"
        date_match = re.match(pattern_date, date)
        pattern_time = r"([01][0-9]|2[0-3]|[0-9])[\.\-\:]?([0-5][0-9])?"
        time_match = re.match(pattern_time, time)
        if not date_match and not time_match:
            return
        day = date_match.group(1)
        month = date_match.group(2)
        year = date_match.group(3)
        hour = time_match.group(1)
        minute = time_match.group(2)
        if not month:
            now = datetime.datetime.now()
            day_now = now.day
            if int(day) < day_now:
                month = now.month + 1
            else:
                month = now.month
        if not year:
            now = datetime.datetime.now()
            month_now = now.month
            if int(month) < month_now:
                year = now.year + 1
            else:
                year = now.year
        if not minute:
            minute = 0
        target_datetime = datetime.datetime(int(year), int(month), int(day), int(hour) - 2, int(minute), second=0)
        unix = int(tm.mktime(target_datetime.timetuple()))
        return unix
    
    def make_embed(self, title: typing.Union[None, str], desc: typing.Union[None, str], colour: typing.Union[None, str], 
                   fields: typing.Union[None, list[typing.Tuple[str, str, bool]]], url: str) -> discord.Embed:
        colour = discord.Colour(colour)
        embed = discord.Embed(title=title, description=desc, color=colour)
        for field in fields:
            name = field[0]
            value = field[1]
            inline = field[2]
            embed.add_field(name=name, value=value, inline=inline)
        embed.set_thumbnail(url=url)
        return embed

    @commands.command()
    async def signups(self, ctx: commands.Context, date: str, time: str, *args: str):
        await ctx.message.delete()
        unix = self.make_unix(date, time)
        if not unix:
            await ctx.send("Wrong date or time")
            return
        author_id = ctx.message.author.id
        info = " ".join(args)
        title = "Event"
        colour = 000000
        sets_value = (f"{self.dreadful}: `0` {''.join(self.sets.get(self.dreadful))}\n"
                        f"{self.mystic}: `0` {''.join(self.sets.get(self.mystic))}\n"
                        f"{self.venerated}: `0` {''.join(self.sets.get(self.venerated))}\n"
                        f"{self.zenith}: `0` {''.join(self.sets.get(self.zenith))}")
        fields = [
            ("Time", f"<t:{unix}:F>", False),
            ("Buffs", f"{''.join([value[1] for value in self.klasy.values()])}\n{'❌'*len(self.klasy)}", False),
            ("Sets", sets_value, True),
            ("<:kekwsalute:1165092829886951424>", "`0`", False),
            ("<:Tank_icon:1103828509996089499>Tanks `0`" , "", True),    
            ("<:Healer_icon:1103828598722416690>Healers `0`", "", True),
            ("<:Dps_icon:1103828601075413145>DPS `0`", "", True)
            ]
        url = "https://i.imgur.com/9rcj0qB.png"
        embed = self.make_embed(title, info, colour, fields, url)
        await ctx.send("<@&1105548968697540679>")
        message = await ctx.send(embed=embed, view=self.View(self, author_id))
        self.eventy.append((message, unix))

async def setup(bot):
    await bot.add_cog(signups(bot))