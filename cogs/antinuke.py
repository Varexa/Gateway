from re import I
import discord
import datetime
from discord.ext import commands, tasks
from ast import literal_eval
import sqlite3
from cogs.premium import check_upgraded
from paginators import PaginationView, PaginatorView


class BasicView(discord.ui.View):
    def __init__(self, ctx: commands.Context, timeout=60):
        super().__init__(timeout=timeout)
        self.ctx = ctx

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and interaction.user.id not in [
            978930369392951366,
            979353019235840000,
        ]:
            await interaction.response.send_message(
                f"Um, Looks like you are not the author of the command...",
                ephemeral=True,
            )
            return False
        return True


class xddd(BasicView):
    def __init__(self, ctx: commands.Context):
        super().__init__(ctx, timeout=60)
        self.value = None

    @discord.ui.button(label="Ban", style=discord.ButtonStyle.red)
    async def _b(self, interaction, button):
        self.value = "ban"
        self.stop()

    @discord.ui.button(label="Kick", style=discord.ButtonStyle.green)
    async def _k(self, interaction, button):
        self.value = "kick"
        self.stop()


def wl(guild_id, user_id, type):
    query = "SELECT * FROM  wl WHERE guild_id = ?"
    val = (guild_id,)
    with sqlite3.connect("./database.sqlite3") as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        cursor.execute(query, val)
        anti_db = cursor.fetchone()
    if anti_db is None:
        return False
    if anti_db[type] is None:
        return False
    if user_id in literal_eval(anti_db[type]):
        return True
    else:
        return False


def punish(guild_id):
    query = "SELECT * FROM  punish WHERE guild_id = ?"
    val = (guild_id,)
    with sqlite3.connect("./database.sqlite3") as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        cursor.execute(query, val)
        anti_db = cursor.fetchone()
    if anti_db["PUNISHMENT"] == "KICK":
        return False
    else:
        return True


def check(guild_id, type):
    query = "SELECT * FROM  toggle WHERE guild_id = ?"
    val = (guild_id,)
    with sqlite3.connect("./database.sqlite3") as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        cursor.execute(query, val)
        anti_db = cursor.fetchone()
    if anti_db is None:
        return False
    if anti_db[type] == 0:
        return False
    else:
        return True


def toggle(guild, type, icon, prefix):
    query = "SELECT * FROM  toggle WHERE guild_id = ?"
    val = (guild.id,)
    with sqlite3.connect("./database.sqlite3") as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        cursor.execute(query, val)
        anti_db = cursor.fetchone()
    if anti_db is None or anti_db["ALL"] == 0:
        em = discord.Embed(
            description=f"First enable the security for {guild.name} by using `{prefix}antinuke enable`",
            color=0xC283FE,
        )
        return em
    else:
        if anti_db[type] == 0:
            c = 1
        else:
            c = 0
        sql1 = f"UPDATE toggle SET '{type}' = ? WHERE guild_id = ?"
        val1 = (c, guild.id)
        cursor.execute(sql1, val1)
    db.commit()
    query = "SELECT * FROM  wl WHERE guild_id = ?"
    val = (guild.id,)
    with sqlite3.connect("./database.sqlite3") as db1:
        db1.row_factory = sqlite3.Row
        cursor1 = db1.cursor()
        cursor1.execute(query, val)
        anti_db1 = cursor1.fetchone()
    des = ""
    ls = [
        "BAN",
        "KICK",
        "BOT",
        "GUILD UPDATE",
        "ROLE CREATE",
        "ROLE DELETE",
        "ROLE UPDATE",
        "CHANNEL CREATE",
        "CHANNEL DELETE",
        "CHANNEL UPDATE",
        "MEMBER UPDATE",
        "WEBHOOK",
    ]
    for i in sorted(ls):
        if anti_db[i] == 1:
            des += f"**Anti {i.capitalize()}:** <:enabled:1152981697084797059>\n"
        else:
            des += f"**Anti {i.capitalize()}:** <:disabled:1152981709663506492>\n"
    embed = discord.Embed(color=0xC283FE)
    embed.set_author(name=f"{str(guild.me.name)} Security", icon_url=icon)
    embed.title = f"{guild.name} Security Settings"
    try:
        ls = [
            "BAN",
            "KICK",
            "BOT",
            "GUILD UPDATE",
            "ROLE CREATE",
            "ROLE DELETE",
            "ROLE UPDATE",
            "CHANNEL CREATE",
            "CHANNEL DELETE",
            "CHANNEL UPDATE",
            "MEMBER UPDATE",
            "WEBHOOK",
        ]
        ls1 = []
        c = 0
        for i in ls:
            for j in literal_eval(anti_db1[i]):
                if j not in ls1:
                    x = discord.utils.get(guild.members, id=j)
                    if x is None:
                        continue
                    ls1.append(j)
                    c += 1
        if c != 0:
            wl = len(ls1)
    except:
        wl = 0
    embed.description = f"Move my role above for more protection.\n\n<:banhammer:1155963619691986944>Punishments:\n\n{des}\nWhitelisted {wl} Users\nTo Change Punishment type `{prefix}antinuke punishment <type>`\nThere are two types of punishments Ban or Kick\nTo Enable or disable event type `{prefix}antinuke anti <event>`"
    query = "SELECT * FROM  punish WHERE guild_id = ?"
    val = (guild.id,)
    with sqlite3.connect("./database.sqlite3") as db2:
        db2.row_factory = sqlite3.Row
        cursor2 = db2.cursor()
        cursor2.execute(query, val)
        anti_db2 = cursor2.fetchone()
    if anti_db2 is None:
        sql = f"INSERT INTO punish(guild_id) VALUES(?)"
        val = (guild.id,)
        cursor.execute(sql, val)
        punishment = "Ban"
    else:
        punishment = anti_db2["PUNISHMENT"].capitalize()
    embed.set_footer(
        text=f"Current Punishment is {punishment}",
        icon_url="https://media.discordapp.net/attachments/1155964405129953391/1155964438332063854/verified.png?width=160&height=160",
    )
    db.commit()
    cursor.close()
    db.close()
    db1.commit()
    cursor1.close()
    db1.close()
    db2.commit()
    cursor2.close()
    db2.close()
    return embed


class whitelistMenu(discord.ui.Select):
    def __init__(self, ctx: commands.Context, user: discord.Member):
        options = [
            discord.SelectOption(label="Anti Ban", value="BAN"),
            discord.SelectOption(label="Anti Bot", value="BOT"),
            discord.SelectOption(label="Anti Channel Create", value="CHANNEL CREATE"),
            discord.SelectOption(label="Anti Channel Delete", value="CHANNEL DELETE"),
            discord.SelectOption(label="Anti Channel Update", value="CHANNEL UPDATE"),
            discord.SelectOption(label="Anti Guild Update", value="GUILD UPDATE"),
            discord.SelectOption(label="Anti Kick", value="KICK"),
            discord.SelectOption(label="Anti Member Update", value="MEMBER UPDATE"),
            discord.SelectOption(label="Anti Role Create", value="ROLE CREATE"),
            discord.SelectOption(label="Anti Role Delete", value="ROLE DELETE"),
            discord.SelectOption(label="Anti Role Update", value="ROLE UPDATE"),
            discord.SelectOption(label="Anti Webhook", value="WEBHOOK"),
        ]
        super().__init__(
            placeholder="Select specific events for whitelisting the user",
            min_values=1,
            max_values=12,
            options=options,
        )
        self.ctx = ctx
        self.user = user

    async def callback(self, interaction: discord.Interaction):
        query = "SELECT * FROM  wl WHERE guild_id = ?"
        val = (self.ctx.guild.id,)
        with sqlite3.connect("./database.sqlite3") as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            anti_db = cursor.fetchone()
        des = ""
        for i in self.values:
            if anti_db[i] is None:
                human = [self.user.id]
                sql = f"UPDATE wl SET '{i}' = ? WHERE guild_id = ?"
                val = (f"{human}", self.ctx.guild.id)
                cursor.execute(sql, val)
                des += f"Anti {i.title()}, "
                pass
            if self.user.id in literal_eval(anti_db[i]):
                pass
            else:
                human = literal_eval(anti_db[i])
                human.append(self.user.id)
                sql = f"UPDATE wl SET '{i}' = ? WHERE guild_id = ?"
                val = (f"{human}", self.ctx.guild.id)
                cursor.execute(sql, val)
                des += f"Anti {i.title()}, "
        db.commit()
        cursor.close()
        db.close()
        if des == "":
            em = discord.Embed(
                description=f"<:cross:1156150663802265670> {self.user.mention} is Already a Whitelisted User for the events you passed",
                color=0xC283FE,
            )
        else:
            em = discord.Embed(
                description=f"<:confirm:1156150922200748053> {self.user.mention} was successfully added in whitelisted users for {des[:-2]} events",
                color=0xC283FE,
            )
        await self.ctx.reply(embed=em)
        await interaction.message.delete()
        self.stop()


class wlMenu(discord.ui.View):
    def __init__(self, ctx: commands.Context, user: discord.Member):
        super().__init__(timeout=60)
        self.add_item(whitelistMenu(ctx, user))
        self.ctx = ctx
        self.user = user

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and interaction.user.id not in [
            978930369392951366,
            979353019235840000,
        ]:
            await interaction.response.send_message(
                f"Um, Looks like you are not the author of the command...",
                ephemeral=True,
            )
            return False
        return True

    @discord.ui.button(
        label="Whitelist the user from all the events",
        style=discord.ButtonStyle.blurple,
    )
    async def _wl(self, interaction, button):
        user = self.user
        ctx = self.ctx
        query = "SELECT * FROM  wl WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect("./database.sqlite3") as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            anti_db = cursor.fetchone()
        ls = [
            "BAN",
            "KICK",
            "BOT",
            "GUILD UPDATE",
            "ROLE CREATE",
            "ROLE DELETE",
            "ROLE UPDATE",
            "CHANNEL CREATE",
            "CHANNEL DELETE",
            "CHANNEL UPDATE",
            "MEMBER UPDATE",
            "WEBHOOK",
        ]
        c = 0
        for i in ls:
            if anti_db is not None:
                if user.id in literal_eval(anti_db[i]):
                    c = +1
        if c == 12:
            em = discord.Embed(
                description=f"<:cross:1156150663802265670> {user.mention} is Already a Whitelisted User",
                color=0xC283FE,
            )
            await ctx.reply(embed=em, mention_author=False)
            await interaction.message.delete()
            self.stop()
        if anti_db is None:
            sql = f"INSERT INTO wl(guild_id) VALUES(?, ?)"
            val = (ctx.guild.id,)
            cursor.execute(sql, val)
        db.commit()
        for i in ls:
            human = literal_eval(anti_db[i])
            human.append(user.id)
            sql = f"UPDATE wl SET '{i}' = ? WHERE guild_id = ?"
            val = (f"{human}", ctx.guild.id)
            cursor.execute(sql, val)
        db.commit()
        em = discord.Embed(
            description=f"<:confirm:1156150922200748053> {user.mention} was successfully added in whitelisted users",
            color=0xC283FE,
        )
        await ctx.reply(embed=em)
        cursor.close()
        db.close()
        await interaction.message.delete()
        self.stop()


class whitelistedMenu(discord.ui.Select):
    def __init__(self, ctx: commands.Context):
        options = [
            discord.SelectOption(label="Anti Ban", value="BAN"),
            discord.SelectOption(label="Anti Bot", value="BOT"),
            discord.SelectOption(label="Anti Channel Create", value="CHANNEL CREATE"),
            discord.SelectOption(label="Anti Channel Delete", value="CHANNEL DELETE"),
            discord.SelectOption(label="Anti Channel Update", value="CHANNEL UPDATE"),
            discord.SelectOption(label="Anti Guild Update", value="GUILD UPDATE"),
            discord.SelectOption(label="Anti Kick", value="KICK"),
            discord.SelectOption(label="Anti Member Update", value="MEMBER UPDATE"),
            discord.SelectOption(label="Anti Role Create", value="ROLE CREATE"),
            discord.SelectOption(label="Anti Role Delete", value="ROLE DELETE"),
            discord.SelectOption(label="Anti Role Update", value="ROLE UPDATE"),
            discord.SelectOption(label="Anti Webhook", value="WEBHOOK"),
        ]
        super().__init__(
            placeholder="Select specific event to see the whitelisted user",
            min_values=1,
            max_values=1,
            options=options,
        )
        self.ctx = ctx

    async def callback(self, interaction: discord.Interaction):
        ctx = self.ctx
        query = "SELECT * FROM  wl WHERE guild_id = ?"
        val = (self.ctx.guild.id,)
        with sqlite3.connect("./database.sqlite3") as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            anti_db = cursor.fetchone()
        db.commit()
        cursor.close()
        db.close()
        ls = []
        lss = []
        count = 1
        for i in literal_eval(anti_db[self.values[0]]):
            u = discord.utils.get(ctx.guild.members, id=i)
            if u is None:
                continue
            lss.append(
                f"`[{'0' + str(count) if count < 10 else count}]` | {u.mention} `[{u.id}]`"
            )
            count += 1
        if count == 1:
            em = discord.Embed(
                description=f"There are no whitelisted users for Anti {self.values[0].capitalize()}",
                color=0xC283FE,
            )
            await ctx.reply(embed=em, mention_author=False)
            await interaction.message.delete()
            self.stop()
        for i in range(0, len(lss), 10):
            ls.append(lss[i : i + 10])
        em_list = []
        no = 1
        for k in ls:
            embed = discord.Embed(color=0xC283FE)
            embed.title = f"List of Whitelisted users of Anti {self.values[0].capitalize()} in {ctx.guild.name} - {count-1}"
            embed.description = "\n".join(k)
            embed.set_footer(
                text=f"{ctx.guild.me.name} • Page {no}/{len(ls)}",
                icon_url=ctx.guild.me.display_avatar.url,
            )
            em_list.append(embed)
            no += 1
        page = PaginationView(embed_list=em_list, ctx=ctx)
        await page.start(ctx)
        await interaction.message.delete()
        self.stop()


class wldMenu(discord.ui.View):
    def __init__(self, ctx: commands.Context):
        super().__init__(timeout=60)
        self.add_item(whitelistedMenu(ctx))
        self.ctx = ctx

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and interaction.user.id not in [
            978930369392951366,
            979353019235840000,
        ]:
            await interaction.response.send_message(
                f"Um, Looks like you are not the author of the command...",
                ephemeral=True,
            )
            return False
        return True

    @discord.ui.button(label="Whitelisted users", style=discord.ButtonStyle.blurple)
    async def _wld(self, interaction, button):
        ctx = self.ctx
        query = "SELECT * FROM  wl WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect("./database.sqlite3") as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            anti_db = cursor.fetchone()
        db.commit()
        cursor.close()
        db.close()
        ls = [
            "BAN",
            "KICK",
            "BOT",
            "GUILD UPDATE",
            "ROLE CREATE",
            "ROLE DELETE",
            "ROLE UPDATE",
            "CHANNEL CREATE",
            "CHANNEL DELETE",
            "CHANNEL UPDATE",
            "MEMBER UPDATE",
            "WEBHOOK",
        ]
        ls1 = []
        c = 0
        for i in ls:
            for j in literal_eval(anti_db[i]):
                if j not in ls1:
                    ls1.append(j)
                    c += 1
        if c == 0:
            em = discord.Embed(
                description=f"There are no whitelisted users", color=0xC283FE
            )
            await ctx.reply(embed=em, mention_author=False)
            await interaction.message.delete()
            self.stop()
        ls = []
        lss = []
        count = 1
        for i in ls1:
            u = discord.utils.get(ctx.guild.members, id=i)
            if u is None:
                continue
            lss.append(
                f"`[{'0' + str(count) if count < 10 else count}]` | {u.mention} `[{u.id}]`"
            )
            count += 1
        for i in range(0, len(lss), 10):
            ls.append(lss[i : i + 10])
        em_list = []
        no = 1
        for k in ls:
            embed = discord.Embed(color=0xC283FE)
            embed.title = f"List of Whitelisted users in {ctx.guild.name} - {count-1}"
            embed.description = "\n".join(k)
            em_list.append(embed)
            no += 1
        page = PaginationView(embed_list=em_list, ctx=ctx)
        await page.start(ctx)
        await interaction.message.delete()
        self.stop()


class unwhitelistMenu(discord.ui.Select):
    def __init__(self, ctx: commands.Context, user: discord.Member):
        options = [
            discord.SelectOption(label="Anti Ban", value="BAN"),
            discord.SelectOption(label="Anti Bot", value="BOT"),
            discord.SelectOption(label="Anti Channel Create", value="CHANNEL CREATE"),
            discord.SelectOption(label="Anti Channel Delete", value="CHANNEL DELETE"),
            discord.SelectOption(label="Anti Channel Update", value="CHANNEL UPDATE"),
            discord.SelectOption(label="Anti Guild Update", value="GUILD UPDATE"),
            discord.SelectOption(label="Anti Kick", value="KICK"),
            discord.SelectOption(label="Anti Member Update", value="MEMBER UPDATE"),
            discord.SelectOption(label="Anti Role Create", value="ROLE CREATE"),
            discord.SelectOption(label="Anti Role Delete", value="ROLE DELETE"),
            discord.SelectOption(label="Anti Role Update", value="ROLE UPDATE"),
            discord.SelectOption(label="Anti Webhook", value="WEBHOOK"),
        ]
        super().__init__(
            placeholder="Select specific events for blacklisting the user",
            min_values=1,
            max_values=12,
            options=options,
        )
        self.ctx = ctx
        self.user = user

    async def callback(self, interaction: discord.Interaction):
        query = "SELECT * FROM  wl WHERE guild_id = ?"
        val = (self.ctx.guild.id,)
        with sqlite3.connect("./database.sqlite3") as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            anti_db = cursor.fetchone()
        des = ""
        for i in self.values:
            if anti_db[i] is None:
                pass
            if self.user.id not in literal_eval(anti_db[i]):
                continue
            else:
                human = literal_eval(anti_db[i])
                human.remove(self.user.id)
                sql = f"UPDATE wl SET '{i}' = ? WHERE guild_id = ?"
                val = (f"{human}", self.ctx.guild.id)
                cursor.execute(sql, val)
                des += f"Anti {i.title()}, "
        db.commit()
        cursor.close()
        db.close()
        if des == "":
            em = discord.Embed(
                description=f"{self.user.mention} is Already a Blacklisted User for the events you passed",
                color=0xC283FE,
            )
        else:
            em = discord.Embed(
                description=f"{self.user.mention} was successfully added in Blacklisted users for {des[:-2]} events",
                color=0xC283FE,
            )
        await self.ctx.reply(embed=em)
        await interaction.message.delete()
        self.stop()


class uwlMenu(discord.ui.View):
    def __init__(self, ctx: commands.Context, user: discord.Member):
        super().__init__(timeout=60)
        self.add_item(unwhitelistMenu(ctx, user))
        self.ctx = ctx
        self.user = user

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and interaction.user.id not in [
            978930369392951366,
            979353019235840000,
        ]:
            await interaction.response.send_message(
                f"Um, Looks like you are not the author of the command...",
                ephemeral=True,
            )
            return False
        return True

    @discord.ui.button(
        label="Blacklists the user from all the events",
        style=discord.ButtonStyle.blurple,
    )
    async def _uwl(self, interaction, button):
        user = self.user
        ctx = self.ctx
        query = "SELECT * FROM  wl WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect("./database.sqlite3") as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            anti_db = cursor.fetchone()
        ls = [
            "BAN",
            "KICK",
            "BOT",
            "GUILD UPDATE",
            "ROLE CREATE",
            "ROLE DELETE",
            "ROLE UPDATE",
            "CHANNEL CREATE",
            "CHANNEL DELETE",
            "CHANNEL UPDATE",
            "MEMBER UPDATE",
            "WEBHOOK",
        ]
        if anti_db is None:
            em = discord.Embed(
                description=f"{user.mention} is Already a Blacklisted User",
                color=0xC283FE,
            )
            await ctx.reply(embed=em, mention_author=False)
            await interaction.message.delete()
            self.stop()
            return
        if (
            user.id not in literal_eval(anti_db["BAN"])
            and user.id not in literal_eval(anti_db["BOT"])
            and user.id not in literal_eval(anti_db["KICK"])
            and user.id not in literal_eval(anti_db["GUILD UPDATE"])
            and user.id not in literal_eval(anti_db["ROLE CREATE"])
            and user.id not in literal_eval(anti_db["ROLE DELETE"])
            and user.id not in literal_eval(anti_db["ROLE UPDATE"])
            and user.id not in literal_eval(anti_db["CHANNEL CREATE"])
            and user.id not in literal_eval(anti_db["CHANNEL DELETE"])
            and user.id not in literal_eval(anti_db["CHANNEL UPDATE"])
            and user.id not in literal_eval(anti_db["MEMBER UPDATE"])
            and user.id not in literal_eval(anti_db["WEBHOOK"])
        ):
            em = discord.Embed(
                description=f"{user.mention} is Already a Blacklisted User",
                color=0xC283FE,
            )
            await ctx.reply(embed=em, mention_author=False)
            await interaction.message.delete()
            self.stop()
            return
        else:
            for i in ls:
                human = literal_eval(anti_db[i])
                human.remove(user.id)
                sql = f"UPDATE wl SET '{i}' = ? WHERE guild_id = ?"
                val = (f"{human}", ctx.guild.id)
                cursor.execute(sql, val)
        db.commit()
        em = discord.Embed(
            description=f"{user.mention} was successfully added in Blacklisted users",
            color=0xC283FE,
        )
        await ctx.reply(embed=em)
        cursor.close()
        db.close()
        await interaction.message.delete()
        self.stop()


class antinuke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(
        invoke_without_command=True,
        description="Shows the help menu for Antinuke commands",
    )
    async def antinuke(self, ctx):
        prefix = ctx.prefix
        if prefix == f"<@{self.bot.user.id}> ":
            prefix = f"@{str(self.bot.user)} "
        anay = discord.utils.get(self.bot.users, id=978930369392951366)
        ls = [
            "antinuke",
            "antinuke anti",
            "antinuke punishment",
            "antinuke enable",
            "antinuke disable",
            "antinuke whitelist",
            "antinuke unwhitelist",
            "antinuke whitelisted",
            "antinuke config",
        ]
        des = ""
        for i in sorted(ls):
            cmd = self.bot.get_command(i)
            des += f"`{prefix}{i}`\n{cmd.description}\n\n"
        listem = discord.Embed(
            title=f"<:880765863953858601:1152979775321812992> Security Commands",
            colour=0xC283FE,
            description=f"<...> Duty | [...] Optional\n\n{des}",
        )
        listem.set_author(
            name=f"{str(ctx.author)}", icon_url=ctx.author.display_avatar.url
        )
        listem.set_footer(text=f"Made by stars.gg", icon_url=anay.avatar.url)
        await ctx.send(embed=listem)

    @antinuke.command(
        description="Shows the current settings for Security of the server"
    )
    @commands.has_guild_permissions(administrator=True)
    async def config(self, ctx):
        if ctx.author.id == ctx.guild.owner.id:
            pass
        else:
            if (
                ctx.author.top_role.position <= ctx.guild.me.top_role.position
                and ctx.author.id not in [978930369392951366, 979353019235840000]
            ):
                em = discord.Embed(
                    description=f"<:error:1153009680428318791> You must Have Higher Role than Bot To run This Command",
                    color=0xFF0000,
                )
                return await ctx.send(embed=em)
        query = "SELECT * FROM  toggle WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect("./database.sqlite3") as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            anti_db = cursor.fetchone()
        if anti_db is None or anti_db["ALL"] == 0:
            embed = discord.Embed(color=0xC283FE)
            embed.set_author(
                name=f"{self.bot.user.name} Security",
                icon_url="https://media.discordapp.net/attachments/1155964405129953391/1155964438332063854/verified.png?width=160&height=160",
            )
            embed.title = f"{ctx.guild.name} Security Settings"
            embed.description = f"<:next:1154735525505269871> The Security system is disabled\nTo enable Security `{ctx.prefix}antinuke enable`"
            embed.set_footer(
                text=f"{self.bot.user.name} Security",
                icon_url="https://media.discordapp.net/attachments/1155964405129953391/1155964438332063854/verified.png?width=160&height=160",
            )
            return await ctx.send(embed=embed)
        query = "SELECT * FROM  wl WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect("./database.sqlite3") as db1:
            db1.row_factory = sqlite3.Row
            cursor1 = db1.cursor()
            cursor1.execute(query, val)
            anti_db1 = cursor1.fetchone()
        if anti_db1 is None:
            sql = f"INSERT INTO wl(guild_id) VALUES(?)"
            val = (ctx.guild.id,)
            cursor.execute(sql, val)
        db.commit()
        des = ""
        ls = [
            "BAN",
            "KICK",
            "BOT",
            "GUILD UPDATE",
            "ROLE CREATE",
            "ROLE DELETE",
            "ROLE UPDATE",
            "CHANNEL CREATE",
            "CHANNEL DELETE",
            "CHANNEL UPDATE",
            "MEMBER UPDATE",
            "WEBHOOK",
        ]
        for i in sorted(ls):
            if anti_db[i] == 1:
                des += f"**Anti {i.capitalize()}:** <:enabled:1152981697084797059>\n"
            else:
                des += f"**Anti {i.capitalize()}:** <:disabled:1152981709663506492>\n"
        embed = discord.Embed(color=0xC283FE)
        embed.set_author(
            name=f"{self.bot.user.name} Security",
            icon_url="https://media.discordapp.net/attachments/1155964405129953391/1155964438332063854/verified.png?width=160&height=160",
        )
        embed.title = f"{ctx.guild.name} Security Settings"
        wl = 0
        try:
            ls = [
                "BAN",
                "KICK",
                "BOT",
                "GUILD UPDATE",
                "ROLE CREATE",
                "ROLE DELETE",
                "ROLE UPDATE",
                "CHANNEL CREATE",
                "CHANNEL DELETE",
                "CHANNEL UPDATE",
                "MEMBER UPDATE",
                "WEBHOOK",
            ]
            ls1 = []
            c = 0
            for i in ls:
                for j in literal_eval(anti_db1[i]):
                    if j not in ls1:
                        x = discord.utils.get(ctx.guild.members, id=j)
                        if x is None:
                            continue
                        ls1.append(j)
                        c += 1
            if c != 0:
                wl = c
            else:
                wl = 0
        except:
            wl = 0
        embed.description = f"Move my role above for more protection.\n\n<:banhammer:1155963619691986944> Punishments:\n\n{des}\nWhitelisted {wl} Users\nTo Change Punishment type `{ctx.prefix}antinuke punishment <type>`\nThere are two types of punishments Ban or Kick\nTo Enable or disable event type `{ctx.prefix}antinuke anti <event>`"
        query = "SELECT * FROM  punish WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect("./database.sqlite3") as db2:
            db2.row_factory = sqlite3.Row
            cursor2 = db2.cursor()
            cursor2.execute(query, val)
            anti_db2 = cursor2.fetchone()
        if anti_db2 is None:
            sql = f"INSERT INTO punish(guild_id) VALUES(?)"
            val = (ctx.guild.id,)
            cursor.execute(sql, val)
            punishment = "Ban"
        else:
            punishment = anti_db2["PUNISHMENT"].capitalize()
        embed.set_footer(
            text=f"Current Punishment is {punishment}",
            icon_url="https://media.discordapp.net/attachments/1155964405129953391/1155964438332063854/verified.png?width=160&height=160",
        )
        await ctx.send(embed=embed)
        db.commit()
        cursor.close()
        db.close()
        db1.commit()
        cursor1.close()
        db1.close()
        db2.commit()
        cursor2.close()
        db2.close()

    @antinuke.command(aliases=["on"], description="Enables the antinuke for the server")
    @commands.has_guild_permissions(administrator=True)
    async def enable(self, ctx):
        if ctx.author.id != ctx.guild.owner.id:
            em = discord.Embed(
                description=f"<:error:1153009680428318791> Only owner of the server can run this command",
                color=0xFF0000,
            )
            return await ctx.send(embed=em)
        query = "SELECT * FROM  toggle WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect("./database.sqlite3") as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            anti_db = cursor.fetchone()
        if anti_db is None:
            sql = f"INSERT OR REPLACE INTO toggle(guild_id) VALUES(?)"
            val = (ctx.guild.id,)
            cursor.execute(sql, val)
        ls = [
            "BAN",
            "KICK",
            "BOT",
            "GUILD UPDATE",
            "ROLE CREATE",
            "ROLE DELETE",
            "ROLE UPDATE",
            "CHANNEL CREATE",
            "CHANNEL DELETE",
            "CHANNEL UPDATE",
            "MEMBER UPDATE",
            "WEBHOOK",
        ]
        for i in ls:
            sql1 = f"UPDATE toggle SET '{i}' = ? WHERE guild_id = ?"
            val1 = (
                1,
                ctx.guild.id,
            )
            cursor.execute(sql1, val1)
        sql1 = f"UPDATE toggle SET 'ALL' = ? WHERE guild_id = ?"
        val1 = (
            1,
            ctx.guild.id,
        )
        cursor.execute(sql1, val1)
        db.commit()
        query = "SELECT * FROM  toggle WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect("./database.sqlite3") as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            anti_db = cursor.fetchone()
        query = "SELECT * FROM  wl WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect("./database.sqlite3") as db1:
            db1.row_factory = sqlite3.Row
            cursor1 = db1.cursor()
            cursor1.execute(query, val)
            anti_db1 = cursor1.fetchone()
        if anti_db1 is None:
            sql = f"INSERT INTO wl(guild_id) VALUES(?)"
            val = (ctx.guild.id,)
            cursor.execute(sql, val)
        db.commit()
        des = ""
        ls = [
            "BAN",
            "KICK",
            "BOT",
            "GUILD UPDATE",
            "ROLE CREATE",
            "ROLE DELETE",
            "ROLE UPDATE",
            "CHANNEL CREATE",
            "CHANNEL DELETE",
            "CHANNEL UPDATE",
            "MEMBER UPDATE",
            "WEBHOOK",
        ]
        for i in sorted(ls):
            if anti_db[i] == 1:
                des += f"**Anti {i.capitalize()}:** <:enabled:1152981697084797059>\n"
            else:
                des += f"**Anti {i.capitalize()}:** <:disabled:1152981709663506492>\n"
        embed = discord.Embed(color=0xC283FE)
        embed.set_author(
            name=f"{self.bot.user.name} Security",
            icon_url="https://media.discordapp.net/attachments/1155964405129953391/1155964438332063854/verified.png?width=160&height=160",
        )
        embed.title = f"{ctx.guild.name} Security Settings"
        wl = 0
        try:
            ls = [
                "BAN",
                "KICK",
                "BOT",
                "GUILD UPDATE",
                "ROLE CREATE",
                "ROLE DELETE",
                "ROLE UPDATE",
                "CHANNEL CREATE",
                "CHANNEL DELETE",
                "CHANNEL UPDATE",
                "MEMBER UPDATE",
                "WEBHOOK",
            ]
            ls1 = []
            c = 0
            for i in ls:
                for j in literal_eval(anti_db1[i]):
                    if j not in ls1:
                        ls1.append(j)
                        c += 1
            if c != 0:
                wl = c
            else:
                wl = 0
        except:
            wl = 0
        embed.description = f"Move my role above for more protection.\n\n<:banhammer:1155963619691986944> Punishments:\n\n{des}\nWhitelisted {wl} Users\nTo Change Punishment type `{ctx.prefix}antinuke punishment <type>`\nThere are two types of punishments Ban or Kick\nTo Enable or disable event type `{ctx.prefix}antinuke anti <event>`"
        query = "SELECT * FROM  punish WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect("./database.sqlite3") as db2:
            db2.row_factory = sqlite3.Row
            cursor2 = db2.cursor()
            cursor2.execute(query, val)
            anti_db2 = cursor2.fetchone()
        if anti_db2 is None:
            sql = f"INSERT INTO punish(guild_id) VALUES(?)"
            val = (ctx.guild.id,)
            cursor.execute(sql, val)
            punishment = "Ban"
        else:
            punishment = anti_db2["PUNISHMENT"].capitalize()
        embed.set_footer(
            text=f"Current Punishment is {punishment}",
            icon_url="https://media.discordapp.net/attachments/1155964405129953391/1155964438332063854/verified.png?width=160&height=160",
        )
        await ctx.send(embed=embed)
        db.commit()
        cursor.close()
        db.close()

    @antinuke.command(
        aliases=["off"], description="Disables the antinuke for the server"
    )
    @commands.has_guild_permissions(administrator=True)
    async def disable(self, ctx):
        if ctx.author.id != ctx.guild.owner.id:
            em = discord.Embed(
                description=f"<:error:1153009680428318791>Only owner of the server can run this command",
                color=0xFF0000,
            )
            return await ctx.send(embed=em)
        query = "SELECT * FROM  toggle WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect("./database.sqlite3") as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            anti_db = cursor.fetchone()
        if anti_db is None:
            sql = f"INSERT OR REPLACE INTO toggle(guild_id) VALUES(?)"
            val = (ctx.guild.id,)
            cursor.execute(sql, val)
        ls = [
            "BAN",
            "KICK",
            "BOT",
            "GUILD UPDATE",
            "ROLE CREATE",
            "ROLE DELETE",
            "ROLE UPDATE",
            "CHANNEL CREATE",
            "CHANNEL DELETE",
            "CHANNEL UPDATE",
            "MEMBER UPDATE",
            "WEBHOOK",
        ]
        for i in ls:
            sql1 = f"UPDATE toggle SET '{i}' = ? WHERE guild_id = ?"
            val1 = (0, ctx.guild.id)
            cursor.execute(sql1, val1)
        sql1 = f"UPDATE toggle SET 'ALL' = ? WHERE guild_id = ?"
        val1 = (
            0,
            ctx.guild.id,
        )
        cursor.execute(sql1, val1)
        db.commit()
        cursor.close()
        db.close()
        query = "SELECT * FROM  toggle WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect("./database.sqlite3") as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            anti_db = cursor.fetchone()
        des = ""
        ls = [
            "BAN",
            "KICK",
            "BOT",
            "GUILD UPDATE",
            "ROLE CREATE",
            "ROLE DELETE",
            "ROLE UPDATE",
            "CHANNEL CREATE",
            "CHANNEL DELETE",
            "CHANNEL UPDATE",
            "MEMBER UPDATE",
            "WEBHOOK",
        ]
        for i in sorted(ls):
            if anti_db[i] == 1:
                des += f"**Anti {i.capitalize()}:** <:enabled:1152981697084797059>\n"
            else:
                des += f"**Anti {i.capitalize()}:** <:disabled:1152981709663506492>\n"
        embed = discord.Embed(color=0xC283FE)
        embed.set_author(
            name=f"{self.bot.user.name} Security",
            icon_url="https://media.discordapp.net/attachments/1155964405129953391/1155964438332063854/verified.png?width=160&height=160",
        )
        embed.title = f"{ctx.guild.name} Security Settings"
        embed.description = f"Disabled the Security system\nTo enable Security `{ctx.prefix}antinuke enable`"
        embed.set_footer(
            text=f"{self.bot.user.name} Security",
            icon_url="https://media.discordapp.net/attachments/1155964405129953391/1155964438332063854/verified.png?width=160&height=160",
        )
        await ctx.send(embed=embed)

    @antinuke.command(description="Enable or disbales a specific event in Security")
    @commands.has_guild_permissions(administrator=True)
    async def anti(self, ctx, *, event):
        if ctx.author.id != ctx.guild.owner.id:
            em = discord.Embed(
                description=f"<:error:1153009680428318791>Only owner of the server can run this command",
                color=0xFF0000,
            )
            return await ctx.send(embed=em)
        ls = [
            "BAN",
            "KICK",
            "BOT",
            "GUILD UPDATE",
            "ROLE CREATE",
            "ROLE DELETE",
            "ROLE UPDATE",
            "CHANNEL CREATE",
            "CHANNEL DELETE",
            "CHANNEL UPDATE",
            "MEMBER UPDATE",
            "WEBHOOK",
        ]
        if event.upper() not in ls:
            return await ctx.reply("Please provide a valid event")
        em = toggle(ctx.guild, event.upper(), self.bot.user.avatar.url, ctx.prefix)
        return await ctx.reply(embed=em)

    @antinuke.command(
        description="<:banhammer:1155963619691986944> To change the punishment for antinuke"
    )
    @commands.has_guild_permissions(administrator=True)
    async def punishment(self, ctx):
        if ctx.author.id == ctx.guild.owner.id:
            pass
        else:
            if (
                ctx.author.top_role.position <= ctx.guild.me.top_role.position
                and ctx.author.id not in [978930369392951366, 979353019235840000]
            ):
                em = discord.Embed(
                    description=f"<:error:1153009680428318791>You must Have Higher Role than Bot To run This Command",
                    color=0xFF0000,
                )
                return await ctx.send(embed=em)
        query = "SELECT * FROM  punish WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect("./database.sqlite3") as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            anti_db = cursor.fetchone()
        if not check(ctx.guild.id, "all"):
            em = discord.Embed(
                description=f"First enable antinuke in order to change the punishment",
                color=0xC283FE,
            )
            return await ctx.reply(embed=em, mention_author=False)
        v = xddd(ctx)
        xd = await ctx.reply(
            embed=discord.Embed(
                description="<:banhammer:1155963619691986944> Select the punishment for antinuke",
                color=0xC283FE,
            ),
            view=v,
        )
        await v.wait()
        if anti_db["PUNISHMENT"] == v.value.upper():
            em = discord.Embed(
                description=f"Punishment is already set to {v.value.capitalize()}",
                color=0xC283FE,
            )
            await xd.delete()
            return await ctx.reply(embed=em)
        else:
            pass
        if anti_db is None:
            sql = f"INSERT INTO punish(guild_id, PUNISHMENT) VALUES(?, ?)"
            val = (ctx.guild.id, f"{v.value.upper()}")
            cursor.execute(sql, val)
        else:
            sql = f"UPDATE punish SET 'PUNISHMENT' = ? WHERE guild_id = ?"
            val = (
                f"{v.value.upper()}",
                ctx.guild.id,
            )
            cursor.execute(sql, val)
        db.commit()
        em = discord.Embed(
            description=f"Punishment is set to {v.value.capitalize()}", color=0xC283FE
        )
        await xd.edit(embed=em, view=None)
        cursor.close()
        db.close()

    @antinuke.command(
        aliases=["wl"], description="To add a whitelisted user for Security"
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_guild_permissions(administrator=True)
    async def whitelist(self, ctx, *, user: discord.Member):
        if ctx.author.id == ctx.guild.owner.id:
            pass
        else:
            if (
                ctx.author.top_role.position <= ctx.guild.me.top_role.position
                and ctx.author.id not in [978930369392951366, 979353019235840000]
            ):
                em = discord.Embed(
                    description=f"<:error:1153009680428318791>You must Have Higher Role than Bot To run This Command",
                    color=0xFF0000,
                )
                return await ctx.send(embed=em)
        query = "SELECT * FROM  wl WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect("./database.sqlite3") as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            anti_db = cursor.fetchone()
        if anti_db is None:
            sql = f"INSERT INTO wl(guild_id) VALUES(?)"
            val = (ctx.guild.id,)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
        if not check(ctx.guild.id, "ALL"):
            em = discord.Embed(
                description=f"First enable antinuke in order to whitelist a user",
                color=0xC283FE,
            )
            return await ctx.reply(embed=em, mention_author=False)
        view = wlMenu(ctx, user)
        em = discord.Embed(
            description=f"Select the options given to whitelist {user.mention}",
            color=0xC283FE,
        )
        m = await ctx.reply(embed=em, view=view)
        await view.wait()

    @antinuke.command(
        aliases=["bl", "uwl", "unwhitelist"],
        description="To remove a whitelisted user from Security",
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_guild_permissions(administrator=True)
    async def blacklist(self, ctx, *, user: discord.Member):
        if ctx.author.id == ctx.guild.owner.id:
            pass
        else:
            if (
                ctx.author.top_role.position <= ctx.guild.me.top_role.position
                and ctx.author.id not in [978930369392951366, 979353019235840000]
            ):
                em = discord.Embed(
                    description=f"<:error:1153009680428318791>You must Have Higher Role than Bot To run This Command",
                    color=0xFF0000,
                )
                return await ctx.send(embed=em)
        if not check(ctx.guild.id, "ALL"):
            em = discord.Embed(
                description=f"First enable antinuke in order to blacklist a user",
                color=0xC283FE,
            )
            return await ctx.reply(embed=em, mention_author=False)
        view = uwlMenu(ctx, user)
        em = discord.Embed(
            description=f"Select the options given to Blacklist {user.mention}",
            color=0xC283FE,
        )
        m = await ctx.reply(embed=em, view=view)
        await view.wait()

    @antinuke.command(aliases=["wld"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_guild_permissions(administrator=True)
    async def whitelisted(self, ctx):
        if ctx.author.id == ctx.guild.owner.id:
            pass
        else:
            if (
                ctx.author.top_role.position <= ctx.guild.me.top_role.position
                and ctx.author.id not in [978930369392951366, 979353019235840000]
            ):
                em = discord.Embed(
                    description=f"<:error:1153009680428318791>You must Have Higher Role than Bot To run This Command",
                    color=0xFF0000,
                )
                return await ctx.send(embed=em)
        query = "SELECT * FROM  wl WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect("./database.sqlite3") as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            anti_db = cursor.fetchone()
        if anti_db is None or not check(ctx.guild.id, "ALL"):
            em = discord.Embed(
                description=f"First enable antinuke in order to check the whitelisted users",
                color=0xC283FE,
            )
            return await ctx.reply(embed=em, mention_author=False)
        view = wldMenu(ctx)
        em = discord.Embed(
            description=f"Select the options given to see the whitelisted users",
            color=0xC283FE,
        )
        m = await ctx.reply(embed=em, view=view)
        await view.wait()

    @commands.Cog.listener()
    async def on_member_update(
        self, before: discord.Member, after: discord.Member
    ) -> None:
        await self.bot.wait_until_ready()

        guild = after.guild
        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        c = check(after.guild.id, "MEMBER UPDATE")
        if not c:
            return
        if before.pending:
            return
        async for entry in after.guild.audit_logs(
            limit=1,
            after=datetime.datetime.now() - datetime.timedelta(minutes=2),
            action=discord.AuditLogAction.member_role_update,
        ):
            _entry_user_id = "6969"
            if entry.user and entry.user.id == self.bot.user.id:
                return
            if entry.user:
                _entry_user_id = entry.user.id

            IGNORE = wl(after.guild.id, _entry_user_id, "MEMBER UPDATE")
            if (
                IGNORE
                or _entry_user_id == guild.owner.id
                or _entry_user_id == self.bot.user.id
            ):
                return
            else:
                punishment = punish(guild.id)
                for role in after.roles:
                    if role not in before.roles:
                        if (
                            role.permissions.administrator
                            or role.permissions.manage_guild
                            or role.permissions.kick_members
                            or role.permissions.ban_members
                            or role.permissions.manage_channels
                            or role.permissions.manage_roles
                            or role.permissions.manage_webhooks
                            or role.permissions.mention_everyone
                        ):
                            if (
                                entry.user.top_role.position
                                < guild.me.top_role.position
                            ):
                                if (
                                    guild.me.guild_permissions.ban_members
                                    and punishment
                                ):
                                    await guild.ban(
                                        entry.user,
                                        reason=f"{self.bot.user.name} | Anti Member Role Update",
                                    )
                                if (
                                    guild.me.guild_permissions.kick_members
                                    and not punishment
                                ):
                                    await guild.kick(
                                        entry.user,
                                        reason=f"{self.bot.user.name} | Anti Member Role Update",
                                    )
                                await after.remove_roles(
                                    role, reason=f"{self.bot.user.name} | Recovery"
                                )

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user) -> None:
        await self.bot.wait_until_ready()

        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        c = check(guild.id, "BAN")
        if not c:
            return
        async for entry in guild.audit_logs(
            limit=1,
            after=datetime.datetime.now() - datetime.timedelta(minutes=2),
            action=discord.AuditLogAction.ban,
        ):
            if entry.user.id == self.bot.user.id:
                return

            IGNORE = wl(guild.id, entry.user.id, "BAN")
            if (
                IGNORE
                or entry.user.id == guild.owner.id
                or entry.user.id == self.bot.user.id
            ):
                return
            else:
                punishment = punish(guild.id)
                if entry.user.top_role.position < guild.me.top_role.position:
                    if guild.me.guild_permissions.ban_members and punishment:
                        await guild.ban(
                            entry.user, reason=f"{self.bot.user.name} | Anti Ban"
                        )
                    if guild.me.guild_permissions.kick_members and not punishment:
                        await guild.kick(
                            entry.user, reason=f"{self.bot.user.name} | Anti Ban"
                        )
                    if guild.me.guild_permissions.ban_members:
                        await guild.unban(
                            entry.target.id, reason=f"{self.bot.user.name} | Recovery"
                        )

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member) -> None:
        await self.bot.wait_until_ready()
        if member.id == self.bot.user.id:
            return

        guild = member.guild
        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        c = check(guild.id, "KICK")
        if not c:
            return
        async for entry in guild.audit_logs(
            limit=1,
            after=datetime.datetime.now() - datetime.timedelta(minutes=2),
            action=discord.AuditLogAction.kick,
        ):
            if entry.user.id == self.bot.user.id:
                return

            if member.id != entry.target.id:
                return
            IGNORE = wl(guild.id, entry.user.id, "KICK")
            if (
                IGNORE
                or entry.user.id == guild.owner.id
                or entry.user.id == self.bot.user.id
            ):
                return
            else:
                punishment = punish(guild.id)
                if entry.user.top_role.position < guild.me.top_role.position:
                    if guild.me.guild_permissions.ban_members and punishment:
                        await guild.ban(
                            entry.user, reason=f"{self.bot.user.name} | Anti Kick"
                        )
                    if guild.me.guild_permissions.kick_members and not punishment:
                        await guild.kick(
                            entry.user, reason=f"{self.bot.user.name} | Anti Kick"
                        )

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        await self.bot.wait_until_ready()

        guild = member.guild
        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        c = check(guild.id, "BOT")
        if not c:
            return
        async for entry in guild.audit_logs(
            limit=1,
            after=datetime.datetime.now() - datetime.timedelta(minutes=2),
            action=discord.AuditLogAction.bot_add,
        ):
            if entry.user.id == self.bot.user.id:
                return

            IGNORE = wl(guild.id, entry.user.id, "BOT")
            if (
                IGNORE
                or entry.user.id == guild.owner.id
                or entry.user.id == self.bot.user.id
            ):
                return
            if member.bot:
                await member.ban(reason=f"{self.bot.user.name} | Anti Bot")
                punishment = punish(guild.id)
                if entry.user.top_role.position < guild.me.top_role.position:
                    if guild.me.guild_permissions.ban_members and punishment:
                        await guild.ban(
                            entry.user, reason=f"{self.bot.user.name} | Anti Bot"
                        )
                    else:
                        if guild.me.guild_permissions.kick_members and not punishment:
                            await guild.kick(
                                entry.user, reason=f"{self.bot.user.name} | Anti Bot"
                            )

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel) -> None:
        await self.bot.wait_until_ready()

        guild = channel.guild
        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        c = check(guild.id, "CHANNEL CREATE")
        if not c:
            return
        async for entry in guild.audit_logs(
            limit=1,
            after=datetime.datetime.now() - datetime.timedelta(minutes=2),
            action=discord.AuditLogAction.channel_create,
        ):
            if entry.user.id == self.bot.user.id:
                return

            IGNORE = wl(guild.id, entry.user.id, "CHANNEL CREATE")
            if (
                IGNORE
                or entry.user.id == guild.owner.id
                or entry.user.id == self.bot.user.id
            ):
                return
            else:
                punishment = punish(guild.id)
                if entry.user.top_role.position < guild.me.top_role.position:
                    if guild.me.guild_permissions.ban_members and punishment:
                        await guild.ban(
                            entry.user,
                            reason=f"{self.bot.user.name} | Anti Channel Create",
                        )
                    if guild.me.guild_permissions.kick_members and not punishment:
                        await guild.kick(
                            entry.user,
                            reason=f"{self.bot.user.name} | Anti Channel Create",
                        )

                if not guild.me.guild_permissions.manage_channels:
                    return
                await channel.delete(reason=f"{self.bot.user.name} | Recovery")

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel) -> None:
        await self.bot.wait_until_ready()

        guild = channel.guild
        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        c = check(guild.id, "CHANNEL DELETE")
        if not c:
            return
        async for entry in guild.audit_logs(
            limit=1,
            after=datetime.datetime.now() - datetime.timedelta(minutes=2),
            action=discord.AuditLogAction.channel_delete,
        ):
            if entry.user.id == self.bot.user.id:
                return

            IGNORE = wl(guild.id, entry.user.id, "CHANNEL DELETE")
            if (
                IGNORE
                or entry.user.id == guild.owner.id
                or entry.user.id == self.bot.user.id
            ):
                return
            else:
                punishment = punish(guild.id)
                if entry.user.top_role.position < guild.me.top_role.position:
                    if guild.me.guild_permissions.ban_members and punishment:
                        await guild.ban(
                            entry.user,
                            reason=f"{self.bot.user.name} | Anti Channel Delete",
                        )
                    if guild.me.guild_permissions.kick_members and not punishment:
                        await guild.kick(
                            entry.user,
                            reason=f"{self.bot.user.name} | Anti Channel Delete",
                        )
                if not guild.me.guild_permissions.manage_channels:
                    return
                await channel.clone(reason=f"{self.bot.user.name} | Recovery")

    @commands.Cog.listener()
    async def on_guild_channel_update(
        self, after: discord.abc.GuildChannel, before: discord.abc.GuildChannel
    ) -> None:
        await self.bot.wait_until_ready()

        name = before.name
        guild = after.guild
        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        c = check(after.guild.id, "CHANNEL UPDATE")
        if not c:
            return
        async for entry in guild.audit_logs(
            limit=1,
            after=datetime.datetime.now() - datetime.timedelta(minutes=2),
            action=discord.AuditLogAction.channel_update,
        ):
            if entry.user.id == self.bot.user.id:
                return

            IGNORE = wl(after.guild.id, entry.user.id, "CHANNEL UPDATE")
            if (
                IGNORE
                or entry.user.id == guild.owner.id
                or entry.user.id == self.bot.user.id
            ):
                return
            else:
                punishment = punish(guild.id)
                try:
                    if entry.user.top_role.position < guild.me.top_role.position:
                        if guild.me.guild_permissions.ban_members and punishment:
                            await guild.ban(
                                entry.user,
                                reason=f"{self.bot.user.name} | Anti Channel Update",
                            )
                        if guild.me.guild_permissions.kick_members and not punishment:
                            await guild.kick(
                                entry.user,
                                reason=f"{self.bot.user.name} | Anti Channel Update",
                            )
                    if not guild.me.guild_permissions.manage_channels:
                        return
                    await after.edit(
                        name=f"{name}", reason=f"{self.bot.user.name} | Recovery"
                    )
                except:
                    pass

    @commands.Cog.listener()
    async def on_guild_update(
        self, after: discord.Guild, before: discord.Guild
    ) -> None:
        await self.bot.wait_until_ready()

        guild = after
        name = before.name
        if not guild.me.guild_permissions.view_audit_log:
            return
        c = check(after.id, "GUILD UPDATE")
        if not c:
            return
        async for entry in after.audit_logs(
            limit=1,
            after=datetime.datetime.now() - datetime.timedelta(minutes=2),
            action=discord.AuditLogAction.guild_update,
        ):
            if entry.user.id == self.bot.user.id:
                return
            IGNORE = wl(entry.guild.id, entry.user.id, "GUILD UPDATE")
            if (
                IGNORE
                or entry.user.id == guild.owner.id
                or entry.user.id == self.bot.user.id
            ):
                return
            else:
                punishment = punish(guild.id)
                if entry.user.top_role.position < guild.me.top_role.position:
                    if guild.me.guild_permissions.ban_members and punishment:
                        await guild.ban(
                            entry.user,
                            reason=f"{self.bot.user.name} | Anti Server Update",
                        )
                    if guild.me.guild_permissions.kick_members and not punishment:
                        await guild.kick(
                            entry.user,
                            reason=f"{self.bot.user.name} | Anti Server Update",
                        )
                if not guild.me.guild_permissions.manage_guild:
                    return
                if entry.before.name != entry.after.name:
                    await after.edit(
                        name=entry.before.name,
                        reason=f"{self.bot.user.name} | Recovery",
                    )

    @commands.Cog.listener()
    async def on_webhooks_update(self, channel) -> None:
        await self.bot.wait_until_ready()

        guild = channel.guild
        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        c = check(guild.id, "WEBHOOK")
        if not c:
            return
        async for entry in guild.audit_logs(
            limit=1,
            after=datetime.datetime.now() - datetime.timedelta(minutes=2),
            action=discord.AuditLogAction.webhook_create,
        ):
            if entry.user.id == self.bot.user.id:
                return
            IGNORE = wl(guild.id, entry.user.id, "WEBHOOK")
            if (
                IGNORE
                or entry.user.id == guild.owner.id
                or entry.user.id == self.bot.user.id
            ):
                return
            else:
                punishment = punish(guild.id)
                if entry.user.top_role.position < guild.me.top_role.position:
                    if guild.me.guild_permissions.ban_members and punishment:
                        await guild.ban(
                            entry.user, reason=f"{self.bot.user.name} | Anti Webhook"
                        )
                    if guild.me.guild_permissions.kick_members and not punishment:
                        await guild.kick(
                            entry.user, reason=f"{self.bot.user.name} | Anti Webhook"
                        )
                webhooks = await guild.webhooks()
                for webhook in webhooks:
                    if webhook.id == entry.target.id:
                        if guild.me.guild_permissions.manage_webhooks:
                            await webhook.delete(
                                reason=f"{self.bot.user.name} | Recovery"
                            )
                            break

    @commands.Cog.listener()
    async def on_guild_role_create(self, role) -> None:
        await self.bot.wait_until_ready()

        guild = role.guild
        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        c = check(guild.id, "ROLE CREATE")
        if not c:
            return
        async for entry in guild.audit_logs(
            limit=1,
            after=datetime.datetime.now() - datetime.timedelta(minutes=2),
            action=discord.AuditLogAction.role_create,
        ):
            if entry.user.id == self.bot.user.id:
                return

            IGNORE = wl(guild.id, entry.user.id, "ROLE CREATE")
            if (
                IGNORE
                or entry.user.id == guild.owner.id
                or entry.user.id == self.bot.user.id
            ):
                return
            else:
                punishment = punish(guild.id)
                if entry.user.top_role.position < guild.me.top_role.position:
                    if guild.me.guild_permissions.ban_members and punishment:
                        await guild.ban(
                            entry.user,
                            reason=f"{self.bot.user.name} | Anti Role Create",
                        )
                    if guild.me.guild_permissions.kick_members and not punishment:
                        await guild.kick(
                            entry.user,
                            reason=f"{self.bot.user.name} | Anti Role Create",
                        )
                if not guild.me.guild_permissions.manage_roles:
                    return
                await role.delete(reason=f"{self.bot.user.name} | Recovery")

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role) -> None:
        await self.bot.wait_until_ready()

        guild = role.guild
        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        c = check(guild.id, "ROLE DELETE")
        if not c:
            return
        async for entry in guild.audit_logs(
            limit=1,
            after=datetime.datetime.now() - datetime.timedelta(minutes=2),
            action=discord.AuditLogAction.role_delete,
        ):
            if entry.user.id == self.bot.user.id:
                return
            IGNORE = wl(guild.id, entry.user.id, "ROLE DELETE")
            if (
                IGNORE
                or entry.user.id == guild.owner.id
                or entry.user.id == self.bot.user.id
            ):
                return
            else:
                punishment = punish(guild.id)
                if entry.user.top_role.position < guild.me.top_role.position:
                    if guild.me.guild_permissions.ban_members and punishment:
                        await guild.ban(
                            entry.user,
                            reason=f"{self.bot.user.name} | Anti Role Delete",
                        )
                    if guild.me.guild_permissions.kick_members and not punishment:
                        await guild.kick(
                            entry.user,
                            reason=f"{self.bot.user.name} | Anti Role Delete",
                        )

    @commands.Cog.listener()
    async def on_guild_role_update(
        self, after: discord.Role, before: discord.Role
    ) -> None:
        await self.bot.wait_until_ready()

        guild = after.guild
        name = before.name
        colour = before.colour
        perm = before.permissions
        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        c = check(after.guild.id, "ROLE UPDATE")
        if not c:
            return
        async for entry in guild.audit_logs(
            limit=1,
            after=datetime.datetime.now() - datetime.timedelta(minutes=2),
            action=discord.AuditLogAction.role_update,
        ):
            if entry.user.id == self.bot.user.id:
                return
            IGNORE = wl(after.guild.id, entry.user.id, "ROLE UPDATE")
            if (
                IGNORE
                or entry.user.id == guild.owner.id
                or entry.user.id == self.bot.user.id
            ):
                return
            else:
                punishment = punish(guild.id)
                if entry.user.top_role.position < guild.me.top_role.position:
                    if guild.me.guild_permissions.ban_members and punishment:
                        await guild.ban(
                            entry.user,
                            reason=f"{self.bot.user.name} | Anti Role Update",
                        )
                    if guild.me.guild_permissions.kick_members and not punishment:
                        await guild.kick(
                            entry.user,
                            reason=f"{self.bot.user.name} | Anti Role Update",
                        )
                if not guild.me.guild_permissions.manage_roles:
                    return
                if name != after.name:
                    await after.edit(
                        name=name, reason=f"{self.bot.user.name} | RECOVERY"
                    )
                if colour != after.colour:
                    await after.edit(
                        colour=colour, reason=f"{self.bot.user.name} | RECOVERY"
                    )
                if perm != after.permissions:
                    await after.edit(
                        permissions=perm, reason=f"{self.bot.user.name} | RECOVERY"
                    )


async def setup(bot):
    await bot.add_cog(antinuke(bot))
