import discord
import datetime
from discord.ext import commands, tasks
from ast import literal_eval
import sqlite3
import io
from paginators import PaginationView
import asyncio

async def getopenuser(guild, channel):
    query = "SELECT * FROM  ticket WHERE guild_id = ?"
    val = (guild.id,)
    with sqlite3.connect('./database.sqlite3') as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        cursor.execute(query, val)
        m_db = cursor.fetchone()
    if m_db is None:
        return None
    data = literal_eval(m_db['opendata'])
    for i in data:
        if data[i][1] == channel.id:
            u = discord.utils.get(guild.members, id=data[i][0])
            return u
    return None

async def getcloseduser(guild, channel):
    query = "SELECT * FROM  ticket WHERE guild_id = ?"
    val = (guild.id,)
    with sqlite3.connect('./database.sqlite3') as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        cursor.execute(query, val)
        m_db = cursor.fetchone()
    if m_db is None:
        return None
    data = literal_eval(m_db['closeddata'])
    for i in data:
        if data[i][1] == channel.id:
            u = discord.utils.get(guild.members, id=data[i][0])
            return u
    return None

async def getuser(guild, channel):
    query = "SELECT * FROM  ticket WHERE guild_id = ?"
    val = (guild.id,)
    with sqlite3.connect('./database.sqlite3') as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        cursor.execute(query, val)
        m_db = cursor.fetchone()
    if m_db is None:
        return None
    data = literal_eval(m_db['opendata'])
    dataa = literal_eval(m_db['closeddata'])
    for i in data:
        if data[i][1] == channel.id:
            u = discord.utils.get(guild.members, id=data[i][0])
            return u
    for i in dataa:
        if dataa[i][1] == channel.id:
            u = discord.utils.get(guild.members, id=dataa[i][0])
            return u
    return None

async def getucount(guild, channel):
    query = "SELECT * FROM  ticket WHERE guild_id = ?"
    val = (guild.id,)
    with sqlite3.connect('./database.sqlite3') as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        cursor.execute(query, val)
        m_db = cursor.fetchone()
    if m_db is None:
        return False
    data = literal_eval(m_db['opendata'])
    dataa = literal_eval(m_db['closeddata'])
    for i in data:
        if data[i][1] == channel.id:
            return i
    for i in dataa:
        if dataa[i][1] == channel.id:
            return i
    return None

async def getcount(guild):
    query = "SELECT * FROM  ticket WHERE guild_id = ?"
    val = (guild.id,)
    with sqlite3.connect('./database.sqlite3') as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        cursor.execute(query, val)
        m_db = cursor.fetchone()
    if m_db is None:
        return False
    return m_db['count']

async def getchannel(guild):
    query = "SELECT * FROM  panel WHERE guild_id = ?"
    val = (guild.id,)
    with sqlite3.connect('./database.sqlite3') as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        cursor.execute(query, val)
        m_db = cursor.fetchone()
    if m_db is None:
        return None
    r = discord.utils.get(guild.categories, id=m_db['channel_id'])
    return r

async def getopencategory(guild):
    query = "SELECT * FROM  panel WHERE guild_id = ?"
    val = (guild.id,)
    with sqlite3.connect('./database.sqlite3') as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        cursor.execute(query, val)
        m_db = cursor.fetchone()
    if m_db is None:
        return None
    r = discord.utils.get(guild.categories, id=m_db['opencategory'])
    return r

async def getclosedcategory(guild):
    query = "SELECT * FROM  panel WHERE guild_id = ?"
    val = (guild.id,)
    with sqlite3.connect('./database.sqlite3') as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        cursor.execute(query, val)
        m_db = cursor.fetchone()
    if m_db is None:
        return None
    r = discord.utils.get(guild.categories, id=m_db['closedcategory'])
    return r

async def getclaimedrole(guild):
    query = "SELECT * FROM  panel WHERE guild_id = ?"
    val = (guild.id,)
    with sqlite3.connect('./database.sqlite3') as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        cursor.execute(query, val)
        m_db = cursor.fetchone()
    if m_db is None:
        return None
    r = discord.utils.get(guild.roles, id=m_db['claimedrole'])
    return r

async def getsupportrole(guild):
    query = "SELECT * FROM  panel WHERE guild_id = ?"
    val = (guild.id,)
    with sqlite3.connect('./database.sqlite3') as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        cursor.execute(query, val)
        m_db = cursor.fetchone()
    if m_db is None:
        return None
    r = discord.utils.get(guild.roles, id=m_db['supportrole'])
    return r

async def getpingrole(guild):
    query = "SELECT * FROM  panel WHERE guild_id = ?"
    val = (guild.id,)
    with sqlite3.connect('./database.sqlite3') as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        cursor.execute(query, val)
        m_db = cursor.fetchone()
    if m_db is None:
        return None
    r = discord.utils.get(guild.roles, id=m_db['pingrole'])
    return r

async def checkuser(guild, user):
    query = "SELECT * FROM  ticket WHERE guild_id = ?"
    val = (guild.id,)
    with sqlite3.connect('./database.sqlite3') as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        cursor.execute(query, val)
        m_db = cursor.fetchone()
    if m_db is None:
        return False
    xd = literal_eval(m_db['opendata'])
    for i in xd:
        if xd[i][0] == user.id:
            return xd[i][1]
    return False
    
async def adddata(guild, count, data):
    query = "SELECT * FROM  ticket WHERE guild_id = ?"
    val = (guild.id,)
    with sqlite3.connect('./database.sqlite3') as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        cursor.execute(query, val)
        m_db = cursor.fetchone()
    count = int(count)
    xd = literal_eval(m_db['opendata'])
    try:
        if xd[count] == data:
            pass
        else:
            xd[count] = data
    except:
        xd[count] = data
    sql = (f"UPDATE ticket SET opendata = ? WHERE guild_id = ?")
    val = (f"{xd}", guild.id)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()

async def updateopendata(guild, count, data):
    query = "SELECT * FROM  ticket WHERE guild_id = ?"
    val = (guild.id,)
    with sqlite3.connect('./database.sqlite3') as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        cursor.execute(query, val)
        m_db = cursor.fetchone()
    count = int(count)
    xd = literal_eval(m_db['opendata'])
    xdd = literal_eval(m_db['closeddata'])
    try:
        if xdd[count] == data:
                del xdd[count]
    except:
        pass
    xd[count] = data
    sql = (f"UPDATE ticket SET opendata = ? WHERE guild_id = ?")
    val = (f"{xd}", guild.id)
    cursor.execute(sql, val)
    sql = (f"UPDATE ticket SET closeddata = ? WHERE guild_id = ?")
    val = (f"{xdd}", guild.id)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()

async def updatecloseddata(guild, count, data):
    query = "SELECT * FROM  ticket WHERE guild_id = ?"
    val = (guild.id,)
    with sqlite3.connect('./database.sqlite3') as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        cursor.execute(query, val)
        m_db = cursor.fetchone()
    count = int(count)
    xd = literal_eval(m_db['opendata'])
    xdd = literal_eval(m_db['closeddata'])
    try:
        if xd[count] == data:
                del xd[count]
    except:
        pass
    xdd[count] = data
    sql = (f"UPDATE ticket SET opendata = ? WHERE guild_id = ?")
    val = (f"{xd}", guild.id)
    cursor.execute(sql, val)
    sql = (f"UPDATE ticket SET closeddata = ? WHERE guild_id = ?")
    val = (f"{xdd}", guild.id)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()

async def deleteudata(guild, count, data):
    query = "SELECT * FROM  ticket WHERE guild_id = ?"
    val = (guild.id,)
    with sqlite3.connect('./database.sqlite3') as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        cursor.execute(query, val)
        m_db = cursor.fetchone()
    count = int(count)
    xd = literal_eval(m_db['opendata'])
    xdd = literal_eval(m_db['closeddata'])
    try:
        if xd[count] == data:
            del xd[count]
    except:
        pass
    try:
        if xdd[count] == data:
            del xdd[count]
    except:
        pass
    sql = (f"UPDATE ticket SET opendata = ? WHERE guild_id = ?")
    val = (f"{xd}", guild.id)
    sql = (f"UPDATE ticket SET closeddata = ? WHERE guild_id = ?")
    val = (f"{xdd}", guild.id)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()
    
async def updatecount(guild, count):
    query = "SELECT * FROM  ticket WHERE guild_id = ?"
    val = (guild.id,)
    with sqlite3.connect('./database.sqlite3') as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        cursor.execute(query, val)
        m_db = cursor.fetchone()
    count = int(count)
    sql = (f"UPDATE ticket SET count = ? WHERE guild_id = ?")
    val = (count, guild.id)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()

async def deletedata(guild: discord.Guild):
    query = "SELECT * FROM  panel WHERE guild_id = ?"
    val = (guild.id,)
    with sqlite3.connect('./database.sqlite3') as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        cursor.execute(query, val)
        m_db = cursor.fetchone()
    if m_db is None:
        return False
    else:
        query = "DELETE FROM  panel WHERE guild_id = ?"
        val = (guild.id,)
        cursor.execute(query, val)
        query = "DELETE FROM  ticket WHERE guild_id = ?"
        val = (guild.id,)
        cursor.execute(query, val)
    db.commit()
    cursor.close()
    db.close()
    return True
    

async def configdata(guild: discord.Guild):
    query = "SELECT * FROM  panel WHERE guild_id = ?"
    val = (guild.id,)
    with sqlite3.connect('./database.sqlite3') as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        cursor.execute(query, val)
        m_db = cursor.fetchone()
    if m_db is None:
        return None
    embed = discord.Embed(title=f"{m_db['name']} Ticket panel setup", color=0xc283fe).set_footer(text=guild.me.name, icon_url=guild.me.avatar.url)
    opencat = discord.utils.get(guild.categories, id=m_db['opencategory'])
    closedcat = discord.utils.get(guild.categories, id=m_db['closedcategory'])
    channel = discord.utils.get(guild.channels, id=m_db['channel_id'])
    support = discord.utils.get(guild.roles, id=m_db['supportrole'])
    claimed = discord.utils.get(guild.roles, id=m_db['pingrole'])
    embmsg = m_db['msg']
    if channel is None:
        channel = None
    else:
        channel = channel.mention
    if opencat is None:
        opencat = None
    else:
        opencat = opencat.mention
    if closedcat is None:
        closedcat = None
    else:
        closedcat = closedcat.mention
    if support is None:
        support = None
    else:
        support = support.mention
    if claimed is None:
        claimed = None
    else:
        claimed = claimed.mention
    embed.add_field(name="Ticket Channel:", value=channel, inline=True)
    embed.add_field(name="Support Role:", value=support, inline=True)
    embed.add_field(name="Ping Role:", value=claimed, inline=True)
    embed.add_field(name="Open Tickets Category:", value=opencat, inline=True)
    embed.add_field(name="Closed Tickets Category:", value=closedcat, inline=True)
    embed.add_field(name="Ticket's Embed Title:", value=f"`{m_db['name']} Panel`", inline=True)
    embed.add_field(name="Ticket's Embed description:", value=f"`{embmsg}`", inline=True)
    embed.timestamp = datetime.datetime.now()
    return embed

class tickredel(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="Reopen", emoji="🔓", custom_id="open", style=discord.ButtonStyle.green)
    async def _treopen(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        guild = interaction.guild
        srole = await getsupportrole(guild)
        user = await getuser(guild, interaction.channel)
        count = await getucount(guild, interaction.channel)
        cat = await getopencategory(guild)
        if count < 10:
            count = "000" + str(count)
        elif count < 100:
            count = "00" + str(count)
        elif count < 1000:
            count = "0" + str(count)
        else:
            count = str(count)
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel = False),
            user: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files = True, embed_links = True),
            guild.me: discord.PermissionOverwrite(view_channel = True, send_messages = True, read_message_history = True)
        }
        if srole:
            overwrites[srole] =  discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files = True, embed_links = True)
        await interaction.channel.edit(name=f"ticket-{count}", overwrites=overwrites, category=cat, reason= f"Ticket Reopened by {str(interaction.user)} [{interaction.user.id}]")
        data = [user.id, interaction.channel.id]
        await updateopendata(guild, int(count), data)
        await updatecloseddata(guild, int(count), data)
        p = await getpingrole(guild)
        if p is not None:
            message = f"{user.mention} Welcome Back! The ticket is reopened\n{p.mention}"
        else:
            message = f"{user.mention} Welcome Back! The ticket is reopened"
        embed = discord.Embed(description="You will be provided with support shortly\nTo close this ticket click the <:ticket_close:1041629937951588352> button.", color=0xc283fe).set_footer(text=f"{guild.me.name} Ticket System", icon_url=guild.me.avatar.url)
        v = ticketchannelpanel(self.bot)
        await interaction.channel.send(message, embed=embed, view=v)
        self.bot.add_view(v)
        await interaction.message.edit(view=None)

    @discord.ui.button(label="Delete", emoji="<:gateway_delete:1041640522487451658>", custom_id="delete", style=discord.ButtonStyle.red)
    async def _delete(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        guild = interaction.guild
        user = await getuser(guild, interaction.channel)
        count = await getucount(guild, interaction.channel)
        data = [user.id, interaction.channel.id]
        await deleteudata(guild, count, data)
        await interaction.channel.delete(reason=f"Ticket Deleted by {str(interaction.user)} [{interaction.user.id}]")

class ticketchannelpanel(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="Close", emoji="<:ticket_close:1041629937951588352>", custom_id="close", style=discord.ButtonStyle.red)
    async def _ticketchannel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        guild = interaction.guild
        srole = await getsupportrole(guild)
        user = await getuser(guild, interaction.channel)
        count = await getucount(guild, interaction.channel)
        if count < 10:
            count = "000" + str(count)
        elif count < 100:
            count = "00" + str(count)
        elif count < 1000:
            count = "0" + str(count)
        else:
            count = str(count)
        cat = await getclosedcategory(guild)
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel = False),
            user: discord.PermissionOverwrite(view_channel = False, send_messages = True, attach_files = True, embed_links = True),
            guild.me: discord.PermissionOverwrite(view_channel = True, send_messages = True, read_message_history = True)
        }
        if srole:
            overwrites[srole] =  discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files = True, embed_links = True)
        await interaction.channel.edit(overwrites=overwrites, category=cat, reason= f"Ticket Closed by {str(interaction.user)}")
        data = [user.id, interaction.message.channel.id]
        await updateopendata(guild, int(count), data)
        await updatecloseddata(guild, int(count), data)
        v = tickredel(self.bot)
        em = discord.Embed(title="<:ticket_close:1041629937951588352> Ticket Closed", description=f"{interaction.channel.mention} is closed by {str(interaction.user)}", color=0xc283fe).set_footer(text=f"{guild.me.name} Ticket System", icon_url=guild.me.avatar.url)
        await interaction.message.channel.send(embed=em, view=v)
        self.bot.add_view(v)
        await interaction.message.edit(view=None)

class ticketpanel(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot
    async def interaction_check(self, interaction: discord.Interaction):
        c = await checkuser(interaction.guild, interaction.user)
        if c is False:
            return True
        else:
            c = discord.utils.get(interaction.guild.channels, id=c)
            await interaction.response.send_message(f"Umm Looks like you already have a ticket {c.mention}", ephemeral=True)

    @discord.ui.button(label="Create Ticket", emoji="📩", custom_id="panel", style=discord.ButtonStyle.gray)
    async def _ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        guild = interaction.guild
        user = interaction.user
        count = await getcount(guild) + 1
        if count < 10:
            count = "000" + str(count)
        elif count < 100:
            count = "00" + str(count)
        elif count < 1000:
            count = "0" + str(count)
        else:
            count = str(count)
        cat = await getopencategory(guild)
        srole = await getsupportrole(guild)
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel = False),
            user: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files = True, embed_links = True),
            guild.me: discord.PermissionOverwrite(view_channel = True, send_messages = True, read_message_history = True)
        }
        if srole:
            overwrites[srole] =  discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files = True, embed_links = True)
        channel = await interaction.guild.create_text_channel(name=f"ticket-{count}", overwrites=overwrites, category=cat, reason= f"Ticket Created for {interaction.user} [{interaction.user.id}]")
        data = [user.id, channel.id]
        await adddata(guild, int(count), data)
        await updatecount(guild, int(count))
        p = await getpingrole(guild)
        if p is not None:
            message = f"{interaction.user.mention} Welcome\n{p.mention}"
        else:
            message = f"{interaction.user.mention} Welcome"
        embed = discord.Embed(description="You will be provided with support shortly\nTo close this ticket click the <:ticket_close:1041629937951588352> button.", color=0xc283fe).set_footer(text=f"{guild.me.name} Ticket System", icon_url=guild.me.avatar.url)
        v = ticketchannelpanel(self.bot)
        await channel.send(message, embed=embed, view=v)
        self.bot.add_view(v)
        
class roledropdownmenu(discord.ui.RoleSelect):
    def __init__(self, ctx: commands.Context, opt: str, place:str):
        super().__init__(placeholder=place,
            min_values=1,
            max_values=1,
        )
        self.ctx = ctx
        self.opt = opt

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False, thinking=False)
        guild = self.ctx.guild
        query = "SELECT * FROM  panel WHERE guild_id = ?"
        val = (guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            m_db = cursor.fetchone()
        sql = (f"UPDATE panel SET {self.opt} = ? WHERE guild_id = ?")
        val = (self.values[0].id, guild.id)
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        self.view.stop()

class rolemenuview(discord.ui.View):
    def __init__(self, ctx: commands.Context, opt: str, place: str):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.add_item(roledropdownmenu(self.ctx, opt, place))
    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and interaction.user.id not in  [978930369392951366, 979353019235840000]:
            await interaction.response.send_message(f"Um, Looks like you are not the author of the command...", ephemeral=True)
            return False
        return True
        
class channeldropdownmenu(discord.ui.ChannelSelect):
    def __init__(self, ctx: commands.Context, opt: str, place:str):
        super().__init__(placeholder=place,
            min_values=1,
            max_values=1,
            channel_types=[discord.ChannelType.text]
        )
        self.ctx = ctx
        self.opt = opt

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False, thinking=False)
        guild = self.ctx.guild
        query = "SELECT * FROM  panel WHERE guild_id = ?"
        val = (guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            m_db = cursor.fetchone()
        sql = (f"UPDATE panel SET {self.opt} = ? WHERE guild_id = ?")
        val = (self.values[0].id, guild.id)
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        self.view.stop()

class channelmenuview(discord.ui.View):
    def __init__(self, ctx: commands.Context, opt: str, place: str):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.add_item(channeldropdownmenu(self.ctx, opt, place))
    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and interaction.user.id not in  [978930369392951366, 979353019235840000]:
            await interaction.response.send_message(f"Um, Looks like you are not the author of the command...", ephemeral=True)
            return False
        return True
        
class catdropdownmenu(discord.ui.ChannelSelect):
    def __init__(self, ctx: commands.Context, opt: str, place:str):
        super().__init__(placeholder=place,
            min_values=1,
            max_values=1,
            channel_types=[discord.ChannelType.category]
        )
        self.ctx = ctx
        self.opt = opt

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False, thinking=False)
        guild = self.ctx.guild
        query = "SELECT * FROM  panel WHERE guild_id = ?"
        val = (guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            m_db = cursor.fetchone()
        sql = (f"UPDATE panel SET {self.opt} = ? WHERE guild_id = ?")
        val = (self.values[0].id, guild.id)
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        self.view.stop()

class catmenuview(discord.ui.View):
    def __init__(self, ctx: commands.Context, opt: str, place: str):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.add_item(catdropdownmenu(self.ctx, opt, place))
    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and interaction.user.id not in  [978930369392951366, 979353019235840000]:
            await interaction.response.send_message(f"Um, Looks like you are not the author of the command...", ephemeral=True)
            return False
        return True

class embmsg(discord.ui.Modal, title="Embed Message"):
    emb = discord.ui.TextInput(
        label='What Should be The Embed Message?',
        style=discord.TextStyle.long,
        placeholder='Type your Embed message here...',
        required=False,
    )

    async def on_submit(self, interaction: discord.Interaction):
        des = self.emb.value + "\nTo create a ticket interact with the button below 📩"
        query = "SELECT * FROM  panel WHERE guild_id = ?"
        val = (interaction.guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            m_db = cursor.fetchone()
        sql = (f"UPDATE panel SET msg = ? WHERE guild_id = ?")
        val = (des, interaction.guild.id)
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        await interaction.response.send_message('Updated Embed Message', ephemeral=True)
        self.stop()


    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)

class editpanelview(discord.ui.View):
    def __init__(self, bot: commands.Bot, ctx: commands.Context, name):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.bot = bot
        self.name = name
    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and interaction.user.id not in  [978930369392951366, 979353019235840000]:
            await interaction.response.send_message(f"Um, Looks like you are not the author of the command...", ephemeral=True)
            return False
        return True
    @discord.ui.button(label="Support Role", custom_id='support', style=discord.ButtonStyle.blurple)
    async def support(self, interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        xd = {}
        for i in interaction.guild.roles:
            if not i.is_bot_managed() and not i.is_premium_subscriber():
                xd[i.name] = i.id
        if len(xd) == 0:
            await interaction.message.edit(embed = discord.Embed(title=f"{self.name} Ticket panel setup", description="There are no Roles in the Server", color=0xc283fe).set_footer(text=f"{self.bot.user.name} Ticket", icon_url=self.bot.user.avatar.url))
            await asyncio.sleep(10)
        else:
            x = rolemenuview(self.ctx, "supportrole", "Select the Support Role")
            embed = discord.Embed(title=f"{self.name} Ticket panel setup", description="Select a role which should be allowed to view the ticket channels\nIf a role is not listed below just start typing it's name in select menu box it will be shown as a option", color=0xc283fe).set_footer(text=f"{self.bot.user.name} Ticket", icon_url=self.bot.user.avatar.url)
            await interaction.edit_original_response(embed=embed, view=x)
            await x.wait()
        emb = await configdata(interaction.guild)
        await interaction.edit_original_response(embed=emb, view=self)

    @discord.ui.button(label="Ping Role", custom_id='ping', style=discord.ButtonStyle.blurple)
    async def pingrole(self, interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        xd = {}
        for i in interaction.guild.roles:
            if not i.is_bot_managed() and not i.is_premium_subscriber():
                xd[i.name] = i.id
        if len(xd) == 0:
            await interaction.edit_original_response(embed = discord.Embed(title=f"{self.name} Ticket panel setup", description="There are no Roles in the Server", color=0xc283fe).set_footer(text=f"{self.bot.user.name} Ticket", icon_url=self.bot.user.avatar.url))
            await asyncio.sleep(10)
        else:
            x = rolemenuview(self.ctx, "pingrole", "Select the Ping Role")
            embed = discord.Embed(title=f"{self.name} Ticket panel setup", description="Select a role which should be pinged as a ticket is created\nIf a role is not listed below just start typing it's name in select menu box it will be shown as a option", color=0xc283fe).set_footer(text=f"{self.bot.user.name} Ticket", icon_url=self.bot.user.avatar.url)
            await interaction.message.edit(embed=embed, view=x)
            await x.wait()
        emb = await configdata(interaction.guild)
        await interaction.edit_original_response(embed=emb, view=self)

    @discord.ui.button(label="Open Ticket Category", custom_id='open', style=discord.ButtonStyle.blurple)
    async def open(self, interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        xd = {}
        for i in interaction.guild.categories:
                xd[i.name] = i.id
        if len(xd) == 0:
            await interaction.edit_original_response(embed = discord.Embed(title=f"{self.name} Ticket panel setup", description="There are no category in the Server", color=0xc283fe).set_footer(text=f"{self.bot.user.name} Ticket", icon_url=self.bot.user.avatar.url))
            await asyncio.sleep(10)
        else:
            x = catmenuview(self.ctx, "opencategory", "Select the Open ticket's category")
            embed = discord.Embed(title=f"{self.name} Ticket panel setup", description="Select a category for open tickets\nIf a category is not listed below just start typing it's name in select menu box it will be shown as a option", color=0xc283fe).set_footer(text=f"{self.bot.user.name} Ticket", icon_url=self.bot.user.avatar.url)
            await interaction.edit_original_response(embed=embed, view=x)
            await x.wait()
        emb = await configdata(interaction.guild)
        await interaction.edit_original_response(embed=emb, view=self)

    @discord.ui.button(label="Closed Ticket Category", custom_id='closed', style=discord.ButtonStyle.blurple)
    async def closed(self, interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        xd = {}
        for i in interaction.guild.categories:
                xd[i.name] = i.id
        if len(xd) == 0:
            await interaction.edit_original_response(embed = discord.Embed(title=f"{self.name} Ticket panel setup", description="There are no category in the Server", color=0xc283fe).set_footer(text=f"{self.bot.user.name} Ticket", icon_url=self.bot.user.avatar.url))
            await asyncio.sleep(10)
        else:
            x = catmenuview(self.ctx, "closedcategory", "Select the Closed ticket's category")
            embed = discord.Embed(title=f"{self.name} Ticket panel setup", description="Select a category for open tickets\nIf a category is not listed below just start typing it's name in select menu box it will be shown as a option", color=0xc283fe).set_footer(text=f"{self.bot.user.name} Ticket", icon_url=self.bot.user.avatar.url)
            await interaction.edit_original_response(embed=embed, view=x)
            await x.wait()
        emb = await configdata(interaction.guild)
        await interaction.edit_original_response(embed=emb, view=self)

    @discord.ui.button(label="Embed Message", custom_id='emb', style=discord.ButtonStyle.blurple)
    async def embmsg(self, interaction, button):
        embed = discord.Embed(title=f"{self.name} Ticket panel setup", description=f"What should be the Embed message for {self.name}'s Panel", color=0xc283fe).set_footer(text=f"{self.bot.user.name} Ticket", icon_url=self.bot.user.avatar.url)
        def check(message):
            return message.author == self.ctx.author and message.channel == self.ctx.channel
        m = embmsg()
        await interaction.response.send_modal(m)
        await m.wait()
        emb = await configdata(interaction.guild)
        await interaction.edit_original_response(embed=emb, view=self)

    @discord.ui.button(label="Done", custom_id='done', style=discord.ButtonStyle.green)
    async def done(self, interaction, button):
        query = "SELECT * FROM  panel WHERE guild_id = ?"
        val = (interaction.guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            m_db = cursor.fetchone()
        emb = discord.Embed(title=f"{m_db['name']} Panel", description=m_db['msg'], color=0xc283fe).set_footer(text=f"{str(self.bot.user.name)} Ticket System", icon_url=self.bot.user.avatar.url)
        emb.timestamp = datetime.datetime.now()
        view = ticketpanel(self.bot)
        try:
            c = self.bot.get_channel(m_db["channel_id"])
            m = await c.fetch_message(m_db['msg_id'])
            await m.edit(embed=emb, view=view)
        except:
            pass
        await interaction.message.delete()
        self.stop

class panelview(discord.ui.View):
    def __init__(self, bot: commands.Bot, ctx: commands.Context, name):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.bot = bot
        self.name = name
    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and interaction.user.id not in  [978930369392951366, 979353019235840000]:
            await interaction.response.send_message(f"Um, Looks like you are not the author of the command...", ephemeral=True)
            return False
        return True
    @discord.ui.button(label="Ticket Channel", custom_id='channel', style=discord.ButtonStyle.blurple)
    async def channel(self, interaction: discord.Interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        xd = {}
        for i in interaction.guild.channels:
            if isinstance(i, discord.TextChannel):
                xd[i.name] = i.id
        x = channelmenuview(self.ctx, "channel_id", "Select the channel")
        embed = discord.Embed(title=f"{self.name} Ticket panel setup", description="Where should I setup the ticket panel?\nIf a channel is not listed below just start typing it's name in select menu box it will be shown as a option", color=0xc283fe).set_footer(text=f"{self.bot.user.name} Ticket", icon_url=self.bot.user.avatar.url)
        await interaction.edit_original_response(embed=embed, view=x)
        await x.wait()
        for i in self.children:
            if i.disabled is True:
                i.disabled = False
        emb = await configdata(interaction.guild)
        await interaction.edit_original_response(embed=emb, view=self)

    @discord.ui.button(label="Support Role", custom_id='support', disabled=True, style=discord.ButtonStyle.blurple)
    async def support(self, interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        xd = {}
        for i in interaction.guild.roles[1:]:
            if not i.is_bot_managed() and not i.is_premium_subscriber():
                xd[i.name] = i.id
        if len(xd) == 0:
            await interaction.edit_original_response(embed = discord.Embed(title=f"{self.name} Ticket panel setup", description="There are no Roles in the Server", color=0xc283fe).set_footer(text=f"{self.bot.user.name} Ticket", icon_url=self.bot.user.avatar.url))
            await asyncio.sleep(10)
        else:
            x = rolemenuview(self.ctx, "supportrole", "Select the Support Role")
            embed = discord.Embed(title=f"{self.name} Ticket panel setup", description="Select a role which should be allowed to view the ticket channels\nIf a role is not listed below just start typing it's name in select menu box it will be shown as a option", color=0xc283fe).set_footer(text=f"{self.bot.user.name} Ticket", icon_url=self.bot.user.avatar.url)
            await interaction.edit_original_response(embed=embed, view=x)
            await x.wait()
        emb = await configdata(interaction.guild)
        await interaction.message.edit(embed=emb, view=self)
        pass

    @discord.ui.button(label="Ping Role", custom_id='ping', disabled=True, style=discord.ButtonStyle.blurple)
    async def pingrole(self, interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        xd = {}
        for i in interaction.guild.roles[1:]:
            if not i.is_bot_managed() and not i.is_premium_subscriber():
                xd[i.name] = i.id
        if len(xd) == 0:
            await interaction.edit_original_response(embed = discord.Embed(title=f"{self.name} Ticket panel setup", description="There are no Roles in the Server", color=0xc283fe).set_footer(text=f"{self.bot.user.name} Ticket", icon_url=self.bot.user.avatar.url))
            await asyncio.sleep(10)
        else:
            x = rolemenuview(self.ctx, "pingrole", "Select the Ping Role")
            embed = discord.Embed(title=f"{self.name} Ticket panel setup", description="Select a role which should be pinged as a ticket is created\nIf a role is not listed below just start typing it's name in select menu box it will be shown as a option", color=0xc283fe).set_footer(text=f"{self.bot.user.name} Ticket", icon_url=self.bot.user.avatar.url)
            await interaction.edit_original_response(embed=embed, view=x)
            await x.wait()
        emb = await configdata(interaction.guild)
        await interaction.edit_original_response(embed=emb, view=self)

    @discord.ui.button(label="Open Ticket Category", custom_id='open', disabled=True, style=discord.ButtonStyle.blurple)
    async def open(self, interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        xd = {}
        for i in interaction.guild.categories:
                xd[i.name] = i.id
        if len(xd) == 0:
            await interaction.edit_original_response(embed = discord.Embed(title=f"{self.name} Ticket panel setup", description="There are no category in the Server", color=0xc283fe).set_footer(text=f"{self.bot.user.name} Ticket", icon_url=self.bot.user.avatar.url))
            await asyncio.sleep(10)
        else:
            x = catmenuview(self.ctx, "opencategory", "Select the Open ticket's category")
            embed = discord.Embed(title=f"{self.name} Ticket panel setup", description="Select a category for open tickets\nIf a category is not listed below just start typing it in select menu box it's name will be shown as a option", color=0xc283fe).set_footer(text=f"{self.bot.user.name} Ticket", icon_url=self.bot.user.avatar.url)
            await interaction.edit_original_response(embed=embed, view=x)
            await x.wait()
        emb = await configdata(interaction.guild)
        await interaction.edit_original_response(embed=emb, view=self)

    @discord.ui.button(label="Closed Ticket Category", custom_id='closed', disabled=True, style=discord.ButtonStyle.blurple)
    async def closed(self, interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        xd = {}
        for i in interaction.guild.categories:
                xd[i.name] = i.id
        if len(xd) == 0:
            await interaction.edit_original_response(embed = discord.Embed(title=f"{self.name} Ticket panel setup", description="There are no category in the Server", color=0xc283fe).set_footer(text=f"{self.bot.user.name} Ticket", icon_url=self.bot.user.avatar.url))
            await asyncio.sleep(10)
        else:
            x = catmenuview(self.ctx, "closedcategory", "Select the Closed ticket's category")
            embed = discord.Embed(title=f"{self.name} Ticket panel setup", description="Select a category for open tickets\nIf a category is not listed below just start typing it's name in select menu box it will be shown as a option", color=0xc283fe).set_footer(text=f"{self.bot.user.name} Ticket", icon_url=self.bot.user.avatar.url)
            await interaction.edit_original_response(embed=embed, view=x)
            await x.wait()
        emb = await configdata(interaction.guild)
        await interaction.edit_original_response(embed=emb, view=self)

    @discord.ui.button(label="Embed Message", custom_id='emb', disabled=True, style=discord.ButtonStyle.blurple)
    async def embmsg(self, interaction: discord.Interaction, button):
        embed = discord.Embed(title=f"{self.name} Ticket panel setup", description=f"What should be the Embed message for {self.name}'s Panel", color=0xc283fe).set_footer(text=f"{self.bot.user.name} Ticket", icon_url=self.bot.user.avatar.url)
        def check(message):
            return message.author == self.ctx.author and message.channel == self.ctx.channel
        m = embmsg()
        await interaction.response.send_modal(m)
        await m.wait()
        emb = await configdata(interaction.guild)
        await interaction.edit_original_response(embed=emb, view=self)

    @discord.ui.button(label="Abort", custom_id='cancel', style=discord.ButtonStyle.red)
    async def cancel(self, interaction, button):
        await deletedata(interaction.guild)
        await interaction.message.delete()
        self.stop()

    @discord.ui.button(label="Done", custom_id='done', disabled=True, style=discord.ButtonStyle.green)
    async def done(self, interaction, button):
        query = "SELECT * FROM  panel WHERE guild_id = ?"
        val = (interaction.guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            m_db = cursor.fetchone()
        emb = discord.Embed(title=f"{m_db['name']} Panel", description=m_db['msg'], color=0xc283fe).set_footer(text=f"{str(self.bot.user.name)} Ticket System", icon_url=self.bot.user.avatar.url)
        emb.timestamp = datetime.datetime.now()
        chan = discord.utils.get(interaction.guild.channels, id=m_db['channel_id'])
        view = ticketpanel(self.bot)
        self.bot.add_view(view)
        init = await chan.send(embed=emb, view=view)
        sql = (f"UPDATE panel SET msg_id = ? WHERE guild_id = ?")
        val = (init.id, interaction.guild.id)
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        await interaction.message.delete()
        self.stop

class ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(
        invoke_without_command=True, description="Shows the help menu for ticket commands"
    )
    async def ticket(self, ctx):
        prefix = ctx.prefix
        if prefix == f"<@{self.bot.user.id}> ":
            prefix = f"@{str(self.bot.user)} "
        anay = discord.utils.get(self.bot.users, id=978930369392951366)
        ls = ["ticket", "ticket create", "ticket delete", "ticket edit", "ticket info", "ticket reopen"]
        des = ""
        for i in sorted(ls):
            cmd = self.bot.get_command(i)
            des += f"`{prefix}{i}`\n{cmd.description}\n\n"
        listem = discord.Embed(title=f"<:gateway_ticket:1041628723851579485> Ticket Commands", colour=0xc283fe,
                                     description=f"<...> Duty | [...] Optional\n\n{des}")
        listem.set_author(name=f"{str(ctx.author)}", icon_url=ctx.author.display_avatar.url)
        listem.set_footer(text=f"Made by stars.gg" ,  icon_url=anay.avatar.url)
        await ctx.send(embed=listem)
    
    @ticket.command(description="Reopens a ticket panel for the server")
    @commands.has_guild_permissions(administrator=True)
    async def reopen(self, ctx: commands.Context, *, channel:discord.TextChannel):
        guild = ctx.guild
        srole = await getsupportrole(guild)
        user = await getcloseduser(guild, channel)
        count = await getucount(guild, channel)
        cat = await getclosedcategory(guild)
        if count < 10:
            count = "000" + str(count)
        elif count < 100:
            count = "00" + str(count)
        elif count < 1000:
            count = "0" + str(count)
        else:
            count = str(count)
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel = False),
            user: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files = True, embed_links = True),
            guild.me: discord.PermissionOverwrite(view_channel = True, send_messages = True, read_message_history = True)
        }
        if srole:
            overwrites[srole] =  discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files = True, embed_links = True)
        await channel.edit(name=f"ticket-{count}", overwrites=overwrites, category=cat, reason= f"Ticket Reopened by {str(ctx.author)} [{ctx.author.id}]")
        data = [user.id, channel.id]
        await updateopendata(guild, int(count), data)
        await updatecloseddata(guild, int(count), data)
        p = await getpingrole(guild)
        if p is not None:
            message = f"{user.mention} Welcome Back! The ticket is reopened\n{p.mention}"
        else:
            message = f"{user.mention} Welcome Back! The ticket is reopened"
        embed = discord.Embed(description="You will be provided with support shortly\nTo close this ticket click the <:ticket_close:1041629937951588352> button.", color=0xc283fe).set_footer(text=f"{guild.me.name} Ticket System", icon_url=guild.me.avatar.url)
        v = ticketchannelpanel(self.bot)
        await channel.send(message, embed=embed, view=v)
        self.bot.add_view(v)
    
    @ticket.command(description="Creates a ticket panel for the server")
    @commands.has_guild_permissions(administrator=True)
    async def create(self, ctx: commands.Context):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 979353019235840000]:
                em = discord.Embed(description=f"<:error:1153009680428318791>You must Have Higher Role than Bot To run This Command", color=0xff0000)
                return await ctx.send(embed=em)
        name = "Ticket"
        guild = ctx.guild
        query = "SELECT * FROM  panel WHERE guild_id = ?"
        val = (guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            m_db = cursor.fetchone()
        if m_db is None:
            sql = (f"INSERT INTO panel(guild_id, name) VALUES(?, ?)")
            val = (ctx.guild.id, f"{name.title()}")
            cursor.execute(sql, val)
            sql = (f"INSERT INTO ticket(guild_id, name) VALUES(?, ?)")
            val = (ctx.guild.id, f"{name.title()}")
            cursor.execute(sql, val)
        else:
            return await ctx.send(embed=discord.Embed(description=f"You can create only one panel at the moment. ", color=0xc283fe).set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url))
        db.commit()
        cursor.close()
        db.close()
        v = panelview(self.bot, ctx, name)
        emb = await configdata(ctx.guild)
        await ctx.reply(embed=emb, view=v)
        await v.wait()
    
    @ticket.command(description="Deletes a ticket panel for the server")
    @commands.has_guild_permissions(administrator=True)
    async def delete(self, ctx: commands.Context):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 979353019235840000]:
                em = discord.Embed(description=f"<:error:1153009680428318791>You must Have Higher Role than Bot To run This Command", color=0xff0000)
                return await ctx.send(embed=em)
        guild = ctx.guild
        name = "Ticket"
        query = "SELECT * FROM  panel WHERE guild_id = ?"
        val = (guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            m_db = cursor.fetchone()
        if m_db is None:
            return await ctx.send(embed=discord.Embed(description=f"No ticket panel found with the name `{name}`", color=0xc283fe).set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url))
        try:
            c = self.bot.get_channel(m_db["channel_id"])
            m = await c.fetch_message(m_db['msg_id'])
            await m.edit(view=None)
        except:
            pass
        await deletedata(ctx.guild)
        return await ctx.send(embed=discord.Embed(description=f"Successfully deleted ticket panel with name `{name}`", color=0xc283fe).set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url))
    
    @ticket.command(description="Gets the information of the ticket")
    @commands.has_guild_permissions(administrator=True)
    async def info(self, ctx: commands.Context):
        name = "Ticket"
        guild = ctx.guild
        query = "SELECT * FROM  panel WHERE guild_id = ?"
        val = (guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            m_db = cursor.fetchone()
        if m_db is None:
            return await ctx.send(embed=discord.Embed(description=f"No ticket panel found with the name `{name}`", color=0xc283fe).set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url))
        if m_db['name'] != name.title():
            return await ctx.send(embed=discord.Embed(description=f"No ticket panel found with the name `{name}`", color=0xc283fe).set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url))
        em = await configdata(ctx.guild)
        await ctx.reply(embed=em)

    @ticket.command(description="Let you edit the ticket")
    @commands.has_guild_permissions(administrator=True)
    async def edit(self, ctx: commands.Context):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 979353019235840000]:
                em = discord.Embed(description=f"<:error:1153009680428318791>You must Have Higher Role than Bot To run This Command", color=0xff0000)
                return await ctx.send(embed=em)
        name = "Ticket"
        guild = ctx.guild
        query = "SELECT * FROM  panel WHERE guild_id = ?"
        val = (guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            m_db = cursor.fetchone()
        if m_db is None:
            return await ctx.send(embed=discord.Embed(description=f"No ticket panel found with the name `{name}`", color=0xc283fe).set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url))
        if m_db['name'] != name.title():
            return await ctx.send(embed=discord.Embed(description=f"No ticket panel found with the name `{name}`", color=0xc283fe).set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url))
        v = editpanelview(self.bot, ctx, name)
        emb = await configdata(ctx.guild)
        await ctx.reply(embed=emb, view=v)
        await v.wait()
    
    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel) -> None:
        await self.bot.wait_until_ready()

        guild = channel.guild
        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        query = "SELECT * FROM  panel WHERE guild_id = ?"
        val = (guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            m_db = cursor.fetchone()
        if m_db is None:
            return
        if m_db['channel_id'] == channel.id:
            await deletedata(guild)
        query = "SELECT * FROM  ticket WHERE guild_id = ?"
        val = (guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            m_db = cursor.fetchone()
        xd = literal_eval(m_db['opendata'])
        for i in xd:
            if xd[i][1] == channel.id:
                await deleteudata(guild, i, xd[i])
        xd = literal_eval(m_db['closeddata'])
        for i in xd:
            if xd[i][1] == channel.id:
                await deleteudata(guild, i, xd[i])
            
    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        guild = message.guild
        if not guild:
            return
        query = "SELECT * FROM  panel WHERE guild_id = ?"
        val = (guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            m_db = cursor.fetchone()
        if m_db is not None:
            if m_db['msg_id'] == message.id:
                await deletedata(guild)

async def setup(bot):
	await bot.add_cog(ticket(bot))
