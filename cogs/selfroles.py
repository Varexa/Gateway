from re import I
from tempfile import TemporaryFile
import discord
import datetime
from discord.ext import commands, tasks
from ast import literal_eval
import sqlite3
import asyncio
from cogs.premium import check_upgraded
from paginators import PaginationView, PaginatorView
from typing import Union
from embed import *
from dump.converter import *

        
xd = {}
async def getchannel(guild_id):
    if guild_id not in xd:
        return 0
    else:
        return xd[guild_id]

async def updatechannel(guild_id, channel_id):
    xd[guild_id] = channel_id
    return True

async def delchannel(guild_id):
    del xd[guild_id]
    return True

xdd = {}
async def getrole(guild_id):
    if guild_id not in xdd:
        return 0
    else:
        return xdd[guild_id]

async def updaterole(guild_id, role_id):
    xdd[guild_id] = role_id
    return True

async def delrole(guild_id):
    del xdd[guild_id]
    return True
class BasicView(discord.ui.View):
    def __init__(self, ctx: commands.Context, timeout = 60):
        super().__init__(timeout=timeout)
        self.ctx = ctx
      
    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and interaction.user.id not in  [978930369392951366, 979353019235840000]:
            await interaction.response.send_message(f"Um, Looks like you are not the author of the command...", ephemeral=True)
            return False
        return True

class embedm_edit(BasicView):
    def __init__(self, bot, ctx: commands.Context, id):
        super().__init__(ctx, timeout=120)
        self.add_item(embedMenu(bot, ctx, id))
        self.value = None

    @discord.ui.button(label="Done", style=discord.ButtonStyle.green)
    async def _send(self, interaction: discord.Interaction, button):
        self.stop()
        
class OnOrOff(BasicView):
    def __init__(self, ctx: commands.Context):
        super().__init__(ctx, timeout=60)
        self.value = None

    @discord.ui.button(label="Same", custom_id='Yes', style=discord.ButtonStyle.green)
    async def dare(self, interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        self.value = 'same'
        self.stop()

    @discord.ui.button(label="Custom", custom_id='No', style=discord.ButtonStyle.danger)
    async def truth(self, interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        self.value = 'custom'
        self.stop()

class SelectRoleButton(discord.ui.Select):
    def __init__(self, place, max, stuff: list, reqrole):
        options = []
        for x in stuff:
            options.append(discord.SelectOption(label=x["label"], emoji=x["emo"], description=x["des"], value=x["role"]))
        super().__init__(placeholder=place, min_values=1, max_values=max, options=options, custom_id='selfrole-dropdown')
        self.reqrole = reqrole

    async def callback(self, interaction: discord.Interaction):
        if self.reqrole is not None:
            rr = discord.utils.get(interaction.guild.roles, id=self.reqrole)
            if rr is not None:
                if rr not in interaction.user.roles:
                    await interaction.message.edit(view=self.view)
                    return await interaction.response.send_message(f"You require {rr.mention} role in order to interact with..", ephemeral=True)
        given = []
        removed = []
        for i in self.values:
            r = discord.utils.get(interaction.guild.roles, id=int(i))
            if r is None:
                continue
            if r in interaction.user.roles:
                await interaction.user.remove_roles(r, reason="Gateway Selfroles")
                removed.append(r.mention)
            else:
                await interaction.user.add_roles(r, reason="Gateway Selfroles")
                given.append(r.mention)
        if len(given) != 0 and len(removed) != 0:
            xd = ','.join(given)
            xdd = ','.join(removed)
            await interaction.response.send_message(f"Gave you the {xd} role(s) and removed {xdd} role(s) from you.", ephemeral=True)
        elif len(given) != 0:
            xd = ','.join(given)
            await interaction.response.send_message(f"Gave you the {xd} role(s).", ephemeral=True)
        elif len(removed) != 0:
            xd = ','.join(removed)
            await interaction.response.send_message(f"Removed the {xd} role(s).", ephemeral=True)
        query = "SELECT * FROM srmain WHERE guild_id = ?"
        val = (interaction.guild.id,)
        with sqlite3.connect('./database.sqlite3') as db1:
            db1.row_factory = sqlite3.Row
            cursor1 = db1.cursor()
            cursor1.execute(query, val)
            self_db = cursor1.fetchone()
        dbd = literal_eval(self_db['data_dropdown'])
        for i in dbd:
            if i['message_id'] == interaction.message.id:
                dd = i['data']
                reqrole = dd[0]["reqrole"]
                v = DropdownSelfRoleView(place=i["placeholder"], max=i["max_options"], stuff=i["data"], reqrole=reqrole)
                await interaction.message.edit(view=v)

class DropdownSelfRoleView(discord.ui.View):
    def __init__(self, place, max, stuff: list, reqrole):
        super().__init__(timeout=None)
        self.add_item(SelectRoleButton(place, max, stuff, reqrole))

class SelfRoleButton(discord.ui.Button):
    def __init__(self, b_type, label, emoji, role_id: int, reqrole):
        if b_type == "p":
            t = discord.ButtonStyle.blurple
        elif b_type == "p2":
            t = discord.ButtonStyle.green
        elif b_type == "secondary":
            t = discord.ButtonStyle.secondary
        else:
            t = discord.ButtonStyle.danger
        super().__init__(label=label, emoji=emoji, style=t, custom_id=str(role_id))
        self.emoji = emoji
        self.role = role_id
        self.reqrole = reqrole

    async def callback(self, interaction: discord.Interaction):
        r = discord.utils.get(interaction.guild.roles, id=self.role)
        if r is None:
            return
        if self.reqrole is not None:
            rr = discord.utils.get(interaction.guild.roles, id=self.reqrole)
            if rr is not None:
                if rr not in interaction.user.roles:
                    return await interaction.response.send_message(f"You require {rr.mention} role in order to interact with..", ephemeral=True)
        if r in interaction.user.roles:
            await interaction.user.remove_roles(r, reason="Gateway Selfroles")
            await interaction.response.send_message(f"Removed the {r.mention} role.", ephemeral=True)
        else:
            await interaction.user.add_roles(r, reason="Gateway Selfroles")
            await interaction.response.send_message(f"Gave you the {r.mention} role.", ephemeral=True)


class ButtonSelfRoleView(discord.ui.View):
    def __init__(self, stuff: list):
        super().__init__(timeout=None)
        for x in stuff:
            button = SelfRoleButton(x['b_type'], x['label'], x['emo'], x['role'], x['reqrole'])
            self.add_item(button)
            
class BasicView(discord.ui.View):
    def __init__(self, ctx: commands.Context, timeout = 60):
        super().__init__(timeout=timeout)
        self.ctx = ctx

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and interaction.user.id not in  [978930369392951366, 979353019235840000]:
            await interaction.response.send_message(f"Um, Looks like you are not the author of the command...", ephemeral=True)
            return False
        return True

class ButtonOrDropdown(BasicView):
    def __init__(self, ctx: commands.Context):
        super().__init__(ctx, timeout=60)
        self.value = None

    @discord.ui.button(label="Button", custom_id='button', style=discord.ButtonStyle.green)
    async def dare(self, interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        self.value = 'button'
        self.stop()
    @discord.ui.button(label="DropDown", custom_id='dropdown', style=discord.ButtonStyle.blurple)
    async def truth(self, interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        self.value = 'dropdown'
        self.stop()
        
class embormsg(BasicView):
    def __init__(self, ctx: commands.Context):
        super().__init__(ctx, timeout=60)
        self.value = None

    @discord.ui.button(label="Embed", custom_id='emb', style=discord.ButtonStyle.green)
    async def dare(self, interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        self.value = True
        self.stop()
    @discord.ui.button(label="Simple", custom_id='msg', style=discord.ButtonStyle.blurple)
    async def truth(self, interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        self.value = False
        self.stop()
class choosebutton(BasicView):
    def __init__(self, ctx: commands.Context, x):
        super().__init__(ctx, timeout=60)
        self.value = None
        if x == 0:
            self.remove_item(self.done)

    @discord.ui.button(label="Primary", custom_id='b1', style=discord.ButtonStyle.blurple)
    async def dare(self, interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        self.value = 'p'
        self.stop()
    @discord.ui.button(label="Primary Success", custom_id='b2', style=discord.ButtonStyle.green)
    async def truthhh(self, interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        self.value = 'p2'
        self.stop()
    @discord.ui.button(label="Secondary", custom_id='b3', style=discord.ButtonStyle.secondary)
    async def truthhhhh(self, interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        self.value = 'secondary'
        self.stop()
    @discord.ui.button(label="Danger", custom_id='b4', style=discord.ButtonStyle.danger)
    async def hhh(self, interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        self.value = 'danger'
        self.stop()
                         
    @discord.ui.button(style=discord.ButtonStyle.green, label="Done", custom_id="done")
    async def done(self, interaction: discord.Interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        self.value = "done"
        self.stop()

class chooselabeloremoji(BasicView):
    def __init__(self, ctx: commands.Context, x, xx=None):
        super().__init__(ctx, timeout=60)
        self.value = None
        if xx is not None:
            self.remove_item(self.truthh)
        if not x:
            self.remove_item(self.done)
    
    
    @discord.ui.button(style=discord.ButtonStyle.green, label="Label & Emoji", emoji="<:Gateway_trans:1097074266165489674>", custom_id="L&E")
    async def dare(self, interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        self.value = 'L&E'
        self.stop()
    @discord.ui.button(style=discord.ButtonStyle.green, label="Only Label", custom_id="L")
    async def truth(self, interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        self.value = 'L'
        self.stop()
    @discord.ui.button(style=discord.ButtonStyle.green, label="Only Emoji", emoji="<:Gateway_trans:1097074266165489674>", custom_id="E")
    async def truthh(self, interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        self.value = 'E'
        self.stop()
                 
    @discord.ui.button(style=discord.ButtonStyle.green, label="Done", custom_id="done")
    async def done(self, interaction: discord.Interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        self.value = "done"
        self.stop()
           
class customordefault(BasicView):
    def __init__(self, bot, ctx: commands.Context, x):
        super().__init__(ctx, timeout=None)
        self.value = None
        self.ctx = ctx
        self.x = x
        self.bot = bot
    
    @discord.ui.button(style=discord.ButtonStyle.green, label="Default", custom_id="NAME")
    async def dare(self, interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        des = ""
        for i in self.x:
            r = discord.utils.get(self.ctx.guild.roles, id=i["role"])
            if r is not None:
                if i['emo'] is not None and i['label'] is not None:
                    des += f"> {i['emo']} {i['label']}: {r.mention}\n"
                elif i['emo'] is not None and i['label'] is None:
                    des += f"> {i['emo']}: {r.mention}\n"
                else:
                    des += f"> {i['label']}: {r.mention}\n"
        des = "Interact with the following for getting or removing the role that follows\n\n" + des
        self.value = des
        self.stop()
       
    @discord.ui.button(style=discord.ButtonStyle.blurple, label="Custom Message", custom_id="CUSTOM")
    async def custom(self, interaction: discord.Interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        self.value = "custom"
        self.stop()

class placeholdm(discord.ui.Modal, title="Custom Placeholder"):
    emb = discord.ui.TextInput(
        label="What Should be The custom placeholder?",
        style=discord.TextStyle.short,
        placeholder='Type the placeholder here',
        max_length=100,
        required=True,
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message('Custom placeholder set', ephemeral=True)
        self.stop()

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)
           
class placehold(BasicView):
    def __init__(self, ctx: commands.Context):
        super().__init__(ctx, timeout=60)
        self.value = None
    
    @discord.ui.button(style=discord.ButtonStyle.green, label="Default", custom_id="NAME")
    async def dare(self, interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        self.value = 'Select the roles from the dropdown'
        self.stop()
       
    @discord.ui.button(style=discord.ButtonStyle.blurple, label="Custom Placeholder", custom_id="CUSTOM")
    async def custom(self, interaction: discord.Interaction, button):
        m = placeholdm()
        await interaction.response.send_modal(m)
        await m.wait()
        self.value = m.emb.value  
        self.stop()

class dex(discord.ui.Modal, title="Custom Description"):
    emb = discord.ui.TextInput(
        label="What Should be The custom description?",
        style=discord.TextStyle.short,
        placeholder='Type {name} for role name',
        max_length=100,
        required=True,
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message('Custom Description set', ephemeral=True)
        self.stop()

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)
           
class desornone(BasicView):
    def __init__(self, ctx: commands.Context):
        super().__init__(ctx, timeout=60)
        self.value = None
    
    @discord.ui.button(style=discord.ButtonStyle.danger, label="None", custom_id="NAME")
    async def dare(self, interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        self.value = None
        self.stop()
       
    @discord.ui.button(style=discord.ButtonStyle.blurple, label="Custom Description", custom_id="CUSTOM")
    async def custom(self, interaction: discord.Interaction, button):
        m = dex()
        await interaction.response.send_modal(m)
        await m.wait()
        self.value = m.emb.value  
        self.stop()

class embmsg(discord.ui.Modal, title="Custom label"):
    emb = discord.ui.TextInput(
        label="What Should be The custom label?",
        style=discord.TextStyle.short,
        placeholder='Type {name} for role name',
        max_length=80,
        required=True,
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message('Custom label set', ephemeral=True)
        self.stop()

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)
           
class label(BasicView):
    def __init__(self, ctx: commands.Context, x):
        super().__init__(ctx, timeout=60)
        self.value = None
        if not x:
            self.remove_item(self.done)
    
    @discord.ui.button(style=discord.ButtonStyle.blurple, label="Role name", custom_id="NAME")
    async def dare(self, interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        self.value = '{name}'
        self.stop()
       
    @discord.ui.button(style=discord.ButtonStyle.blurple, label="Custom Label", custom_id="CUSTOM")
    async def custom(self, interaction: discord.Interaction, button):
        m = embmsg()
        await interaction.response.send_modal(m)
        await m.wait()
        self.value = m.emb.value  
        self.stop()
                 
    @discord.ui.button(style=discord.ButtonStyle.green, label="Done", custom_id="done")
    async def done(self, interaction: discord.Interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        self.value = "done"
        self.stop()
           
class xddd(BasicView):
    def __init__(self, ctx: commands.Context, c):
        super().__init__(ctx, timeout=60)
        self.value = None
        if c == 0:
            self.done.disabled = True
                 
    @discord.ui.button(style=discord.ButtonStyle.green, label="Done", custom_id="done")
    async def done(self, interaction: discord.Interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        self.value = "done"
        self.stop()

class roledropdownmenu(discord.ui.RoleSelect):
    def __init__(self, ctx: commands.Context):
        super().__init__(placeholder="Select the role",
            min_values=1,
            max_values=1,
        )
        self.ctx = ctx
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False, thinking=False)
        await updaterole(self.ctx.guild.id, self.values[0].id)
        self.view.stop()

class rolemenuview(discord.ui.View):
    def __init__(self, ctx: commands.Context):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.add_item(roledropdownmenu(self.ctx))

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and interaction.user.id not in  [978930369392951366, 979353019235840000]:
            await interaction.response.send_message(f"Um, Looks like you are not the author of the command...", ephemeral=True)
            return False
        return True

        
class requiredrole(discord.ui.View):
    def __init__(self, ctx: commands.Context):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.add_item(roledropdownmenu(self.ctx))
        self.value = None

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and interaction.user.id not in  [978930369392951366, 979353019235840000]:
            await interaction.response.send_message(f"Um, Looks like you are not the author of the command...", ephemeral=True)
            return False
        return True
                     
    @discord.ui.button(style=discord.ButtonStyle.red, label="None", custom_id="none")
    async def done(self, interaction: discord.Interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        self.value = False
        self.stop()
        
class channeldropdownmenu(discord.ui.ChannelSelect):
    def __init__(self, ctx: commands.Context):
        super().__init__(placeholder="Select channel for selfrole panel",
            min_values=1,
            max_values=1,
            channel_types=[discord.ChannelType.text]
        )
        self.ctx = ctx
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False, thinking=False)
        await updatechannel(self.ctx.guild.id, self.values[0].id)
        self.view.stop()

class channelmenuview(discord.ui.View):
    def __init__(self, ctx: commands.Context):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.value = None
        self.add_item(channeldropdownmenu(self.ctx))

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and interaction.user.id not in  [978930369392951366, 979353019235840000]:
            await interaction.response.send_message(f"Um, Looks like you are not the author of the command...", ephemeral=True)
            return False
        return True

class selfroles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.group(invoke_without_command=True, name="selfrole", aliases=['selfroles', 'reactionrole', 'sr', 'rr'], description="Show's the help menu for selfroles")
    async def selfrole(self, ctx: commands.Context):
        prefix = ctx.prefix
        if prefix == f"<@{self.bot.user.id}> ":
            prefix = f"@{str(self.bot.user)} "
        anay = discord.utils.get(self.bot.users, id=978930369392951366)
        ls = ["selfroles", "selfroles create", "selfroles delete", "selfroles list"]
        des = ""
        for i in sorted(ls):
            cmd = self.bot.get_command(i)
            if cmd.description is None:
                cmd.description = "No Description"
            des += f"`{prefix}{i}`\n{cmd.description}\n\n"
        listem = discord.Embed(title=f"<:selfroles:1048653295041921045> Selfroles Commands", colour=0xc283fe,
                                     description=f"<...> Duty | [...] Optional\n\n{des}")
        listem.set_author(name=f"{str(ctx.author)}", icon_url=ctx.author.display_avatar.url)
        listem.set_footer(text=f"Made by stars.gg" ,  icon_url=anay.avatar.url)
        await ctx.send(embed=listem)
    
    @selfrole.command(name="list", aliases=['show'], description="Shows you the current selfrole panels of the server")
    @commands.has_guild_permissions(administrator=True)
    async def show(self, ctx: commands.Context):
        no_panel = discord.Embed(description=f"There are no selfrole panels in this server", color=0xc283fe).set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        query = "SELECT * FROM srmain WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('./database.sqlite3') as db1:
            db1.row_factory = sqlite3.Row
            cursor1 = db1.cursor()
            cursor1.execute(query, val)
            self_db = cursor1.fetchone()
        if self_db is None:
            return await ctx.reply(embed=no_panel)
        else:
            lsb = literal_eval(self_db['data_button'])
            lsd = literal_eval(self_db['data_dropdown'])
            lsm = lsb + lsd
            if len(lsm) == 0:
                return await ctx.reply(embed=no_panel)
            else:
                em = discord.Embed(title=f"Selfrole panels for {ctx.guild.name}", color=0xc283fe).set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
                d = ""
                for i in lsm:
                    if "placeholder" in i:
                        x = "DropDown"
                    else:
                        x = "Button"
                    t = i['data']
                    t = len(t)
                    try:
                        channel = self.bot.get_channel(i["channel_id"])
                        try:
                            message = await channel.fetch_message(i['message_id'])
                            d += f"[{message.id}]({message.jump_url}) Type: `{x}` Total Roles: {t} roles\n"
                        except:
                            d += f"{i['message_id']} (The message is deleted) Type: `{x}` Total Roles: {t} roles\n"
                    except:
                        d += f"{i['message_id']} (The channel is deleted) Type: `{x}` Total Roles: {t} roles\n"
                em.title = f"Selfrole panels for {ctx.guild.name} - {len(lsm)}"
                em.description = d
                await ctx.reply(embed=em)

    @selfrole.command(name="create", aliases=["add"], description="Create a selfrole panel")
    @commands.cooldown(1, 15, commands.BucketType.guild)
    @commands.has_guild_permissions(administrator=True)
    async def create(self, ctx: commands.Context):
        c = await check_upgraded(ctx.guild.id)
        if ctx.author.id == ctx.guild.owner.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 979353019235840000]:
                em = discord.Embed(description=f"<:error:1153009680428318791>You must Have Higher Role than Bot To run This Command", color=0xff0000)
                return await ctx.send(embed=em)
        query = "SELECT * FROM srmain WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('./database.sqlite3') as db1:
            db1.row_factory = sqlite3.Row
            cursor1 = db1.cursor()
            cursor1.execute(query, val)
            self_db = cursor1.fetchone()
        if self_db is None:
            lsb = []
            lsd = []
        else:
            lsb = literal_eval(self_db['data_button'])
            lsd = literal_eval(self_db['data_dropdown'])
        if not c:
            lsm = lsb+lsd
            if len(lsm) >= 3:
                em = discord.Embed(description=f"You just tried to create more than 3 selfrole panels but this guild is not upgarded\nYou can buy bot's premium from the link given below or by creating a ticket in the [Support Server](https://discord.gg/6Q9D7R8hYc)", color=0xc283fe).set_footer(text=f"{self.bot.user.name} Premium feature", icon_url=self.bot.user.avatar.url)
                v = discord.ui.View()
                v.add_item(discord.ui.Button(label="Patreon", url="https://www.patreon.com/gateway_bot"))
                v.add_item(discord.ui.Button(label="Support Server", url="https://discord.gg/6Q9D7R8hYc"))
                return await ctx.reply(embed=em, view=v)
        em = discord.Embed(description=f"Where should i send the panel of selfrole?\nIf you can't see any channel in the dropdown type its name in the dropdown selection box.", color=0xc283fe).set_footer(text=f"{self.bot.user.name} Selfroles", icon_url=self.bot.user.avatar.url)
        v = channelmenuview(ctx)
        init = await ctx.reply(embed=em, view=v)
        await v.wait()
        c = await getchannel(ctx.guild.id)
        c = discord.utils.get(ctx.guild.channels, id=c)
        em.description = f"Which type of interaction you want in selfroles panel?"
        v2 = ButtonOrDropdown(ctx)
        await init.edit(embed=em, view=v2)
        await v2.wait()
        if v2.value is None:
            return await init.delete()
        else:
            val = v2.value
        if val is None:
            await delchannel(ctx.guild.id)
            return await init.delete()
        elif val == "button":
            em.description = f"What type of message you want?"
            v5 = embormsg(ctx)
            await init.edit(embed=em, view=v5)
            await v5.wait()
            if v5.value is None:
                await delchannel(ctx.guild.id)
                return await init.delete()
            emb = v5.value
            x = []
            samecl = False
            samecb = False
            mcheck = True
            while mcheck:
                await init.clear_reactions()
                if len(x) == 25:
                    mcheck = False
                    break
                d = {}
                if not samecb:
                    em.description = f"Which types of button you want in the panel?"
                    v3 = choosebutton(ctx, len(x))
                    await init.edit(embed=em, view=v3)
                    await v3.wait()
                    if v3.value is None:
                        await delchannel(ctx.guild.id)
                        return await init.delete()
                    if v3.value == "done":
                        mcheck = False
                        break
                    d['b_type'] = v3.value
                else:
                    d['b_type'] = m_b_type
                if len(x) == 0:
                    em.description = f"Do you want the same type of buttons for all or you want to custom each one?"
                    v_yes_no = OnOrOff(ctx)
                    await init.edit(embed=em, view=v_yes_no)
                    await v_yes_no.wait()
                    if v_yes_no.value is None:
                        return await init.delete()
                    if v_yes_no.value == "same":
                        samecb = True
                        m_b_type = v3.value
                    else:
                        samecb = False
                if not samecl:
                    em.description = f"What should be written or given on the button?"
                    if samecb and len(x) != 0:
                        v4 = chooselabeloremoji(ctx, True)
                    else:
                        v4 = chooselabeloremoji(ctx, False)
                    await init.edit(embed=em, view=v4)
                    await v4.wait()
                    if v4.value is None:
                        await delchannel(ctx.guild.id)
                        return await init.delete()
                    if v4.value == "done":
                        mcheck = False
                        break
                    ty = v4.value
                else:
                    ty = m_l_type
                if len(x) == 0:
                    em.description = f"Do you want the same type of writings on all buttons or you want to custom each one?"
                    v_yes_no = OnOrOff(ctx)
                    await init.edit(embed=em, view=v_yes_no)
                    await v_yes_no.wait()
                    if v_yes_no.value is None:
                        return await init.delete()
                    if v_yes_no.value == "same":
                        samecl = True
                        m_l_type = v4.value
                    else:
                        samecl = False
                if ty == "L&E":
                    if samecb and samecl and len(x) != 0:
                        em.description = f"You want a custom label or only role name as a label\nClick on done if you dont want more buttons"
                        v_label = label(ctx, True)
                    else:
                        em.description = f"You want a custom label or only role name as a label"
                        v_label = label(ctx, False)
                    await init.edit(embed=em, view=v_label)
                    await v_label.wait()
                    if v_label.value is None:
                        await delchannel(ctx.guild.id)
                        return await init.delete()
                    if v_label.value == "done":
                        mcheck = False
                        break
                    d['label'] = v_label.value
                    em.description = f"React with the emoji on this message for the button"
                    await init.edit(embed=em, view=None)
                    def check(reaction, user):
                        return user == ctx.author
                    try:
                        reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
                    except asyncio.TimeoutError:
                        await delchannel(ctx.guild.id)
                        return await init.delete()
                    else:
                        pass
                    while True:
                        if isinstance(reaction.emoji, str):
                            d['emo'] = str(reaction.emoji)
                            break
                        elif isinstance(reaction.emoji, discord.Emoji):
                            d['emo'] = str(reaction.emoji)
                            break
                        else:
                            await init.clear_reactions()
                            em.description = f"The emoji you reacted with can't accessed by the bot as it's not in any of the server where bot is added. Try again or write `cancel` to stop process"
                            await init.edit(embed=em)
                            try:
                                reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
                            except asyncio.TimeoutError:
                                await delchannel(ctx.guild.id)
                                return await init.delete()
                    await init.clear_reactions()
                    check2 = True
                    em.description = f"Select the role for this button\nIf you can't see any role in the dropdown, type its name in the dropdown selection box."
                    v_role = rolemenuview(ctx)
                    await init.edit(embed=em, view=v_role)
                    await v_role.wait()
                    while check2:
                        r = await getrole(ctx.guild.id)
                        r = discord.utils.get(ctx.guild.roles, id=r)
                        if not r.is_assignable():
                            em.description = f"I cannot assign that role to anyone select another role"
                            await init.edit(embed=em, view=v_role)
                            await v_role.wait()
                        else:
                            d["role"] = r.id
                            check2 = False
                    x.append(d)
                elif ty == "L":
                    if samecb and samecl and len(x) != 0:
                        em.description = f"You want a custom label or only role name as a label\nClick on done if you dont want more buttons"
                        v_label = label(ctx, True)
                    else:
                        em.description = f"You want a custom label or only role name as a label"
                        v_label = label(ctx, False)
                    await init.edit(embed=em, view=v_label)
                    await v_label.wait()
                    if v_label.value is None:
                        await delchannel(ctx.guild.id)
                        return await init.delete()
                    if v_label.value == "done":
                        mcheck = False
                        break
                    d['label'] = v_label.value
                    check2 = True
                    em.description = f"Select the role for this button\nIf you can't see any role in the dropdown, type its name in the dropdown selection box."
                    v_role = rolemenuview(ctx)
                    await init.edit(embed=em, view=v_role)
                    await v_role.wait()
                    while check2:
                        r = await getrole(ctx.guild.id)
                        r = discord.utils.get(ctx.guild.roles, id=r)
                        if not r.is_assignable():
                            em.description = f"I cannot assign that role to anyone select another role"
                            await init.edit(embed=em, view=v_role)
                            await v_role.wait()
                        else:
                            d["role"] = r.id
                            check2 = False
                    d["emo"] = None
                    x.append(d)
                elif ty == "E":
                    if samecb and samecl and len(x) != 0:
                        em.description = f"React with the emoji on this message for the button\nReact with <:ticky:1154027584020021278> if you dont want more buttons"
                        t = await init.add_reaction("<:ticky:1154027584020021278>")
                    else:
                        em.description = f"React with the emoji on this message for the button"
                    await init.edit(embed=em, view=None)
                    def check(reaction, user):
                        return user == ctx.author
                    try:
                        reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
                    except asyncio.TimeoutError:
                        await delchannel(ctx.guild.id)
                        return await init.delete()
                    if reaction.emoji.id == 1036691761269063740:
                        mcheck = False
                        break
                    else:
                        pass
                    while True:
                        if isinstance(reaction.emoji, str):
                            d['emo'] = str(reaction.emoji)
                            break
                        elif isinstance(reaction.emoji, discord.Emoji):
                            d['emo'] = str(reaction.emoji)
                            break
                        else:
                            await init.clear_reactions()
                            em.description = f"The emoji you reacted with can't accessed by the bot as it's not in any of the server where bot is added. Try again or write `cancel` to stop process"
                            await init.edit(embed=em)
                            try:
                                reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
                            except asyncio.TimeoutError:
                                await delchannel(ctx.guild.id)
                                return await init.delete()
                    check2 = True
                    await init.clear_reactions()
                    em.description = f"Select the role for this button\nIf you can't see any role in the dropdown, type its name in the dropdown selection box."
                    v_role = rolemenuview(ctx)
                    await init.edit(embed=em, view=v_role)
                    await v_role.wait()
                    while check2:
                        r = await getrole(ctx.guild.id)
                        r = discord.utils.get(ctx.guild.roles, id=r)
                        if not r.is_assignable():
                            em.description = f"I cannot assign that role to anyone select another role"
                            await init.edit(embed=em, view=v_role)
                            await v_role.wait()
                        else:
                            d["role"] = r.id
                            check2 = False
                    d["label"] = None
                    x.append(d)
            await init.clear_reactions()
            em.description = f"Select the role required to interact with the self role panel\nIf you can't see any role in the dropdown, type its name in the dropdown selection box."
            v6 = requiredrole(ctx)
            await init.edit(embed=em, view=v6)
            await v6.wait()
            if v6.value is False:
                reqrole = None
            else:
                reqrole = await getrole(ctx.guild.id)
            em.description = f"What should be the message for the panel"
            for i in x:
                l = i['label']
                r_r = discord.utils.get(ctx.guild.roles, id=i['role'])
                if l is not None:
                    l = l.replace("{name}", r_r.name)
                    i['label'] = l
                i['reqrole'] = reqrole
            v7 = customordefault(self.bot, ctx, x)
            await init.edit(embed=em, view=v7)
            await v7.wait()
            if v7.value is None:
                return await init.delete()
            elif v7.value == "custom":
                if emb:
                    des = ""
                    for i in x:
                        r = discord.utils.get(ctx.guild.roles, id=i["role"])
                        if r is not None:
                            if i['emo'] is not None and i['label'] is not None:
                                des += f"> {i['emo']} {i['label']}: {r.mention}\n"
                            elif i['emo'] is not None and i['label'] is None:
                                des += f"> {i['emo']}: {r.mention}\n"
                            else:
                                des += f"> {i['label']}: {r.mention}\n"
                    des = "Interact with the following for getting or removing the role that follows\n\n" + des
                    emb = discord.Embed(description=des, color=0xc283fe)
                    r_no = round(random.random()*100000)
                    await updateembed(r_no, emb.to_dict())
                    vxdxd = embedm_edit(self.bot, ctx, r_no)
                    okok=await ctx.reply(content="This is a sample of selfrole embed you have updated till now", embed=emb, view=vxdxd)
                    await vxdxd.wait()
                    await okok.delete()
                    xx = await getembed(ctx.guild, ctx.author, r_no)
                    main_embed = discord.Embed.from_dict(xx)
                    msg = None
                else:
                    em.description = f"Type your custom message"
                    await init.edit(embed=em, view=None)
                    def check(message):
                        return message.author == ctx.author and message.channel == ctx.channel
                    try:
                            user_response = await self.bot.wait_for("message", timeout=120, check=check)
                            await user_response.delete()
                    except asyncio.TimeoutError:
                        await init.delete()
                        return
                    main_embed = None
                    msg = user_response.content
            else:
                if emb:
                    main_embed = discord.Embed(description=v7.value, color=0xc283fe)
                    msg = None
                else:
                    main_embed = None
                    msg = v7.value
            v_main = ButtonSelfRoleView(x)
            if emb:
                m = await c.send(embed=main_embed, view=v_main)
            else:
                m = await c.send(msg, view=v_main, allowed_mentions=discord.AllowedMentions.none())
            self.bot.add_view(v_main)
            em.description = f"Successfully created the selfrole panel"
            vv = discord.ui.View()
            vv.add_item(discord.ui.Button(label="Jump to panel", url=m.jump_url))
            await init.edit(embed=em, view=vv)
            if emb:
                emb = main_embed.to_dict()
            else:
                emb = None
            ok = {
                "channel_id": c.id,
                "message_id": m.id,
                "message": msg,
                "embed": emb,
                "data": x
            }
            lsb.append(ok)
        elif val == "dropdown":
            em.description = f"What type of message you want?"
            v5 = embormsg(ctx)
            await init.edit(embed=em, view=v5)
            await v5.wait()
            if v5.value is None:
                await delchannel(ctx.guild.id)
                return await init.delete()
            emb = v5.value
            x = []
            samecl = False
            mcheck = True
            while mcheck:
                await init.clear_reactions()
                if len(x) == 25:
                    mcheck = False
                    break
                d = {}
                if not samecl:
                    em.description = f"What should be written or given on the select option?"
                    if len(x) != 0:
                        v4 = chooselabeloremoji(ctx, True, True)
                    else:
                        v4 = chooselabeloremoji(ctx, False, True)
                    await init.edit(embed=em, view=v4)
                    await v4.wait()
                    if v4.value is None:
                        await delchannel(ctx.guild.id)
                        return await init.delete()
                    if v4.value == "done":
                        mcheck = False
                        break
                    ty = v4.value
                else:
                    ty = m_l_type
                if len(x) == 0:
                    em.description = f"Do you want the same type of writings on all select options or you want to custom each one?"
                    v_yes_no = OnOrOff(ctx)
                    await init.edit(embed=em, view=v_yes_no)
                    await v_yes_no.wait()
                    if v_yes_no.value is None:
                        return await init.delete()
                    if v_yes_no.value == "same":
                        samecl = True
                        m_l_type = v4.value
                    else:
                        samecl = False
                if ty == "L&E":
                    if samecl and len(x) != 0:
                        em.description = f"You want a custom label or only role name as a label\nClick on done if you dont want more buttons"
                        v_label = label(ctx, True)
                    else:
                        em.description = f"You want a custom label or only role name as a label"
                        v_label = label(ctx, False)
                    await init.edit(embed=em, view=v_label)
                    await v_label.wait()
                    if v_label.value is None:
                        await delchannel(ctx.guild.id)
                        return await init.delete()
                    if v_label.value == "done":
                        mcheck = False
                        break
                    d['label'] = v_label.value
                    em.description = f"React with the emoji on this message for the button"
                    await init.edit(embed=em, view=None)
                    def check(reaction, user):
                        return user == ctx.author
                    try:
                        reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
                    except asyncio.TimeoutError:
                        await delchannel(ctx.guild.id)
                        return await init.delete()
                    else:
                        pass
                    while True:
                        if isinstance(reaction.emoji, str):
                            d['emo'] = str(reaction.emoji)
                            break
                        elif isinstance(reaction.emoji, discord.Emoji):
                            d['emo'] = str(reaction.emoji)
                            break
                        else:
                            await init.clear_reactions()
                            em.description = f"The emoji you reacted with can't accessed by the bot as it's not in any of the server where bot is added. Try again or write `cancel` to stop process"
                            await init.edit(embed=em)
                            try:
                                reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
                            except asyncio.TimeoutError:
                                await delchannel(ctx.guild.id)
                                return await init.delete()
                    await init.clear_reactions()
                    check2 = True
                    em.description = f"Select the role for this button\nIf you can't see any role in the dropdown, type its name in the dropdown selection box."
                    v_role = rolemenuview(ctx)
                    await init.edit(embed=em, view=v_role)
                    await v_role.wait()
                    while check2:
                        r = await getrole(ctx.guild.id)
                        r = discord.utils.get(ctx.guild.roles, id=r)
                        if not r.is_assignable():
                            em.description = f"I cannot assign that role to anyone select another role"
                            await init.edit(embed=em, view=v_role)
                            await v_role.wait()
                        else:
                            d["role"] = r.id
                            check2 = False
                elif ty == "L":
                    if samecl and len(x) != 0:
                        em.description = f"You want a custom label or only role name as a label\nClick on done if you dont want more buttons"
                        v_label = label(ctx, True)
                    else:
                        em.description = f"You want a custom label or only role name as a label"
                        v_label = label(ctx, False)
                    await init.edit(embed=em, view=v_label)
                    await v_label.wait()
                    if v_label.value is None:
                        await delchannel(ctx.guild.id)
                        return await init.delete()
                    if v_label.value == "done":
                        mcheck = False
                        break
                    d['label'] = v_label.value
                    check2 = True
                    em.description = f"Select the role for this button\nIf you can't see any role in the dropdown, type its name in the dropdown selection box."
                    v_role = rolemenuview(ctx)
                    await init.edit(embed=em, view=v_role)
                    await v_role.wait()
                    while check2:
                        r = await getrole(ctx.guild.id)
                        r = discord.utils.get(ctx.guild.roles, id=r)
                        if not r.is_assignable():
                            em.description = f"I cannot assign that role to anyone select another role"
                            await init.edit(embed=em, view=v_role)
                            await v_role.wait()
                        else:
                            d["role"] = r.id
                            check2 = False
                    d["emo"] = None
                em.description = f"What should be the description for this option"
                vvv = desornone(ctx)
                await init.edit(embed=em, view=vvv)
                await vvv.wait()
                d['des'] = vvv.value
                x.append(d)
            await init.clear_reactions()
            em.description = f"Select the role required to interact with the self role panel\nIf you can't see any role in the dropdown, type its name in the dropdown selection box."
            v6 = requiredrole(ctx)
            await init.edit(embed=em, view=v6)
            await v6.wait()
            if v6.value is False:
                reqrole = None
            else:
                reqrole = await getrole(ctx.guild.id)
            for i in x:
                l = i['label']
                r_r = discord.utils.get(ctx.guild.roles, id=i['role'])
                if l is not None:
                    l = l.replace("{name}", r_r.name)
                    i['label'] = l
                dd = i['des']
                if dd is not None:
                    dd = dd.replace("{name}", r_r.name)
                    i['des'] = dd
                i['reqrole'] = reqrole
            em.description = f"What should be the placeholder for the dropdown"
            v7 = placehold(ctx)
            await init.edit(embed=em, view=v7)
            await v7.wait()
            if v7.value is None:
                return await init.delete()
            else:
                place = v7.value
            em.description = f"How many roles can a user select at one time from the dropdown"
            await init.edit(embed=em, view=None)
            def check(message):
                    return message.author == ctx.author and message.channel == ctx.channel
            try:
                    user_response = await self.bot.wait_for("message", timeout=120, check=check)
                    await user_response.delete()
            except asyncio.TimeoutError:
                await init.delete()
                return
            chhh = True
            while chhh:
                if user_response.content.isdigit():
                    if abs(int(user_response.content)) > len(x):
                        em.description = f"You have entered a digit more than roles available for the user to select\nType a number below {len(x)}"
                    else:
                        max_opt = abs(int(user_response.content))
                        break
                else:
                    em.description = f"You have not entered a digit\nPlease type a digit only"
                await init.edit(embed=em)
                try:
                    user_response = await self.bot.wait_for("message", timeout=120, check=check)
                    await user_response.delete()
                except asyncio.TimeoutError:
                    await init.delete()
                    return
            em.description = f"What should be the message for the panel"
            v7 = customordefault(self.bot, ctx, x)
            await init.edit(embed=em, view=v7)
            await v7.wait()
            if v7.value is None:
                return await init.delete()
            elif v7.value == "custom":
                if emb:
                    des = ""
                    for i in x:
                        r = discord.utils.get(ctx.guild.roles, id=i["role"])
                        if r is not None:
                            if i['emo'] is not None and i['label'] is not None:
                                des += f"> {i['emo']} {i['label']}: {r.mention}\n"
                            elif i['emo'] is not None and i['label'] is None:
                                des += f"> {i['emo']}: {r.mention}\n"
                            else:
                                des += f"> {i['label']}: {r.mention}\n"
                    des = "Interact with the following for getting or removing the role that follows\n\n" + des
                    emb = discord.Embed(description=des, color=0xc283fe)
                    r_no = round(random.random()*100000)
                    await updateembed(r_no, emb.to_dict())
                    vxdxd = embedm_edit(self.bot, ctx, r_no)
                    okok=await ctx.reply(content="This is a sample of selfrole embed you have updated till now", embed=emb, view=vxdxd)
                    await vxdxd.wait()
                    await okok.delete()
                    xx = await getembed(ctx.guild, ctx.author, r_no)
                    main_embed = discord.Embed.from_dict(xx)
                    msg = None
                else:
                    em.description = f"Type your custom message"
                    await init.edit(embed=em, view=None)
                    def check(message):
                        return message.author == ctx.author and message.channel == ctx.channel
                    try:
                            user_response = await self.bot.wait_for("message", timeout=120, check=check)
                            await user_response.delete()
                    except asyncio.TimeoutError:
                        await init.delete()
                        return
                    main_embed = None
                    msg = user_response.content
            else:
                if emb:
                    main_embed = discord.Embed(description=v7.value, color=0xc283fe)
                    msg = None
                else:
                    main_embed = None
                    msg = v7.value
            v_main = DropdownSelfRoleView(place, max_opt, x, reqrole)
            if emb:
                m = await c.send(embed=main_embed, view=v_main)
            else:
                m = await c.send(msg, view=v_main, allowed_mentions=discord.AllowedMentions.none())
            self.bot.add_view(v_main)
            em.description = f"Successfully created the selfrole panel"
            vv = discord.ui.View()
            vv.add_item(discord.ui.Button(label="Jump to panel", url=m.jump_url))
            await init.edit(embed=em, view=vv)
            if emb:
                emb = main_embed.to_dict()
            else:
                emb = None
            ok = {
                "channel_id": c.id,
                "message_id": m.id,
                "message": msg,
                "embed": emb,
                "placeholder": place,
                "max_options": max_opt,
                "data": x
            }
            lsd.append(ok)
        if self_db is None:
            sql = (f"INSERT INTO srmain(guild_id, 'data_button', 'data_dropdown') VALUES(?, ?, ?)")
            val = (ctx.guild.id, f"{lsb}", f"{lsd}",)
            cursor1.execute(sql, val)
        else:
            sql = (f"UPDATE 'srmain' SET 'data_button' = ? WHERE guild_id = ?")
            val = (f"{lsb}", ctx.guild.id)
            cursor1.execute(sql, val)
            sql = (f"UPDATE 'srmain' SET 'data_dropdown' = ? WHERE guild_id = ?")
            val = (f"{lsd}", ctx.guild.id)
            cursor1.execute(sql, val)
        db1.commit()
        cursor1.close()
        db1.close()
        
    @selfrole.command(name="edit", description="Edis a selfrole panel from the server")
    @commands.has_guild_permissions(administrator=True)
    async def edit(self, ctx:commands.Context, *, message_id):
        if ctx.author.id == ctx.guild.owner.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 979353019235840000]:
                em = discord.Embed(description=f"<:error:1153009680428318791>You must Have Higher Role than Bot To run This Command", color=0xff0000)
                return await ctx.send(embed=em)
        if not message_id.isdigit():
            return await ctx.send("Message id must be an integer")
        no_panel = discord.Embed(description=f"There are no selfrole panels in this server", color=0xc283fe).set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        query = "SELECT * FROM srmain WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('./database.sqlite3') as db1:
            db1.row_factory = sqlite3.Row
            cursor1 = db1.cursor()
            cursor1.execute(query, val)
            self_db = cursor1.fetchone()
        if self_db is None:
            return await ctx.reply(embed=no_panel)
        else:
            lsb = literal_eval(self_db['data_button'])
            lsd = literal_eval(self_db['data_dropdown'])
            lsm = lsb + lsd
            if len(lsm) == 0:
                return await ctx.reply(embed=no_panel)
            c = False
            INDEX = 0
            for i in lsb:
                INDEX +=1
                if i["message_id"] == int(message_id):
                    c_id = i["channel_id"]
                    msg = i["message"]
                    em_main = i["embed"]
                    c = True
                    b = True
                    break
            for i in lsd:
                INDEX +=1
                if i["message_id"] == int(message_id):
                    c_id = i["channel_id"]
                    msg = i["message"]
                    em_main = i["embed"]
                    c = True
                    b = False
                    break
            if c == False:
                no_panel.description = f"There are no selfrole panels with message id `{message_id}` in this server"
                return await ctx.send(embed=no_panel)
            else:
                channel = self.bot.get_channel(c_id)
                sr_msg = await channel.fetch_message(int(message_id))
                if msg is not None:
                    em = discord.Embed(title="Selfrole edit panel", color=0xc283fe)
                    em.description = f"Type your custom message"
                    init=await ctx.reply(embed=em, view=None)
                    def check(message):
                        return message.author == ctx.author and message.channel == ctx.channel
                    try:
                            user_response = await self.bot.wait_for("message", timeout=120, check=check)
                            await user_response.delete()
                    except asyncio.TimeoutError:
                        await init.delete()
                        return
                    msg = user_response.content
                    await sr_msg.edit(content=msg)
                else:
                    r_no = round(random.random()*100000)
                    await updateembed(r_no, em_main)
                    vxdxd = embedm_edit(self.bot, ctx, r_no)
                    init=await ctx.reply(content="This is a sample of selfrole embed you have updated till now", embed=discord.Embed.from_dict(em_main), view=vxdxd)
                    await vxdxd.wait()
                    em_main = await getembed(ctx.guild, ctx.author, r_no)
                    await sr_msg.edit(embed=discord.Embed.from_dict(em_main))
                if b:
                    lsb[INDEX-1]["message"] = msg
                    lsb[INDEX-1]["embed"] = em_main
                else:
                    lsd[INDEX-1]["message"] = msg
                    lsd[INDEX-1]["embed"] = em_main
        sql = (f"UPDATE ' srmain' SET 'data_button' = ? WHERE guild_id = ?")
        val = (f"{lsb}", ctx.guild.id)
        cursor1.execute(sql, val)
        sql = (f"UPDATE ' srmain' SET 'data_dropdown' = ? WHERE guild_id = ?")
        val = (f"{lsd}", ctx.guild.id)
        cursor1.execute(sql, val)
        db1.commit()
        cursor1.close()
        db1.close()
        no_panel.description = f"Successfully edited selfrole panel with message id `{message_id}`"
        await init.edit(content=None, embed=no_panel, view=None)
        
    @selfrole.command(name="delete", description="Deletes a selfrole panel from the server")
    @commands.has_guild_permissions(administrator=True)
    async def delete(self, ctx:commands.Context, *, message_id):
        if ctx.author.id == ctx.guild.owner.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 979353019235840000]:
                em = discord.Embed(description=f"<:error:1153009680428318791>You must Have Higher Role than Bot To run This Command", color=0xff0000)
                return await ctx.send(embed=em)
        if not message_id.isdigit():
            return await ctx.send("Message id must be an integer")
        no_panel = discord.Embed(description=f"There are no selfrole panels in this server", color=0xc283fe).set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        query = "SELECT * FROM srmain WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('./database.sqlite3') as db1:
            db1.row_factory = sqlite3.Row
            cursor1 = db1.cursor()
            cursor1.execute(query, val)
            self_db = cursor1.fetchone()
        if self_db is None:
            return await ctx.reply(embed=no_panel)
        else:
            lsb = literal_eval(self_db['data_button'])
            lsd = literal_eval(self_db['data_dropdown'])
            lsm = lsb + lsd
            if len(lsm) == 0:
                return await ctx.reply(embed=no_panel)
            c = False
            for i in lsb:
                if i["message_id"] == int(message_id):
                    try:
                        channel = self.bot.get_channel(i["channel_id"])
                        try:
                            message = await channel.fetch_message(i['message_id'])
                            await message.edit(view=None)
                        except:
                            pass
                    except:
                        pass
                    lsb.remove(i)
                    c = True
            for i in lsd:
                if i["message_id"] == int(message_id):
                    try:
                        channel = self.bot.get_channel(i["channel_id"])
                        try:
                            message = await channel.fetch_message(i['message_id'])
                            await message.edit(view=None)
                        except:
                            pass
                    except:
                        pass
                    lsd.remove(i)
                    c = True
            if c == False:
                no_panel.description = f"There are no selfrole panels with message id `{message_id}` in this server"
                return await ctx.send(embed=no_panel)
        sql = (f"UPDATE ' srmain' SET 'data_button' = ? WHERE guild_id = ?")
        val = (f"{lsb}", ctx.guild.id)
        cursor1.execute(sql, val)
        sql = (f"UPDATE ' srmain' SET 'data_dropdown' = ? WHERE guild_id = ?")
        val = (f"{lsd}", ctx.guild.id)
        cursor1.execute(sql, val)
        db1.commit()
        cursor1.close()
        db1.close()
        no_panel.description = f"Successfully deleted selfrole panel with message id `{message_id}`"
        await ctx.reply(embed=no_panel)

async def setup(bot):
	await bot.add_cog(selfroles(bot))
