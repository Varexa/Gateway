from enum import auto
from math import isqrt
from xml.dom.pulldom import parseString
import discord
from discord.ext import commands, tasks
import platform
from discord import *
import datetime
import time
import os
import sqlite3
import random
from cogs.premium import check_upgraded
from paginators import PaginationView, PaginatorView
from ast import literal_eval

class BasicView(discord.ui.View):
    def __init__(self, ctx: commands.Context, timeout = 60):
        super().__init__(timeout=timeout)
        self.ctx = ctx

    
      
    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and interaction.user.id not in  [978930369392951366, 979353019235840000]:
            await interaction.response.send_message(f"Um, Looks like you are not the author of the command...", ephemeral=True)
            return False
        return True

class OnOrOff(BasicView):
    def __init__(self, ctx: commands.Context):
        super().__init__(ctx, timeout=60)
        self.value = None

    

    @discord.ui.button(emoji="<:confirm:1156150922200748053>", custom_id='Yes', style=discord.ButtonStyle.green)
    async def dare(self, interaction, button):
        self.value = 'Yes'
        self.stop()

    @discord.ui.button(emoji="<:cross:1156150663802265670>", custom_id='No', style=discord.ButtonStyle.danger)
    async def truth(self, interaction, button):
        self.value = 'No'
        self.stop()

class PngOrGif(BasicView):
    def __init__(self, ctx: commands.Context):
        super().__init__(ctx, timeout=60)
        self.value = None
        
    @discord.ui.button(label="PNG", custom_id='png', style=discord.ButtonStyle.green)
    async def png(self, interaction, button):
        self.value = 'png'
        self.stop()

    @discord.ui.button(label="GIF", custom_id='gif', style=discord.ButtonStyle.green)
    async def gif(self, interaction, button):
        self.value = 'gif'
        self.stop()

    @discord.ui.button(label="MIX", custom_id='mix', style=discord.ButtonStyle.green)
    async def mix(self, interaction, button):
        self.value = 'mix'
        self.stop()

    @discord.ui.button(label="STOP", custom_id='stop', style=discord.ButtonStyle.danger)
    async def cancel(self, interaction, button):
        self.value = 'stop'
        self.stop()

class night(BasicView):
    def __init__(self, ctx: commands.Context):
        super().__init__(ctx, timeout=120)
        self.value = None

    

    @discord.ui.button(label="Simple Roles Only", custom_id='simple', style=discord.ButtonStyle.green)
    async def simple(self, interaction, button):
        self.value = 'simple'
        self.stop()
    @discord.ui.button(label="Bot Roles Only", custom_id='bot', style=discord.ButtonStyle.green)
    async def bot(self, interaction, button):
        self.value = 'bot'
        self.stop()

    @discord.ui.button(label="Both", custom_id='both', style=discord.ButtonStyle.danger)
    async def both(self, interaction, button):
        self.value = 'both'
        self.stop()
   
    @discord.ui.button(label="Cancel", custom_id='cancel', style=discord.ButtonStyle.gray)
    async def cancel(self, interaction, button):
        self.value = 'cancel'
        self.stop()

async def autopfp(self, c_id, type):
    if len(self.bot.users) < 1000:
        u = random.sample(self.bot.users, len(self.bot.users))
    else:
        u = random.sample(self.bot.users, 1000)
    c = 1
    channel = self.bot.get_channel(c_id)
    if channel is None:
        return
    if not channel.permissions_for(channel.guild.me).send_messages:
        return
    for i in u:
        if i.avatar and c <= 10:
          if type != 'mix':
            if type in i.avatar.url:
                try:
                    await channel.send(i.avatar.url)
                except:
                    return
                c += 1
          else:
                try:
                    await channel.send(i.avatar.url)
                except:
                    return
                c += 1

async def get_prefix(message: discord.Message):
    with sqlite3.connect('database.sqlite3') as db:
      db.row_factory = sqlite3.Row
      cursor = db.cursor()
      cursor.execute(f'SELECT prefix FROM prefixes WHERE guild_id = {message.guild.id}')
      res = cursor.fetchone()
    if res:
      prefix = str(res[0])
    if not res:
      prefix = '-'
    try:
        cursor.execute(f'SELECT * FROM noprefix WHERE user_id = {message.author.id}')
        res1 = cursor.fetchone()
        if res1 is not None:
            if res1['servers'] is not None:
                no_prefix = literal_eval(res1['servers'])
                if message.guild.id in no_prefix:
                    return [f"<@{message.guild.me.id}>", prefix, ""]
            if res1['main'] is not None:
                if res1['main'] == 1:
                    return [f"<@{message.guild.me.id}>", prefix, ""]
    except:
        pass
    db.commit()
    cursor.close()
    db.close()
    return [f"<@{message.guild.me.id}>", prefix]
async def by_cmd(ctx, user: discord.Member, cmd):
    c = await check_upgraded(ctx.guild.id)
    if not c:
        return False
    query = "SELECT * FROM  bypass WHERE guild_id = ?"
    val = (ctx.guild.id,)
    with sqlite3.connect('database.sqlite3') as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        cursor.execute(query, val)
        ig_db = cursor.fetchone()
    if ig_db is None:
        return False
    xd = literal_eval(ig_db['bypass_users'])
    xdd = literal_eval(ig_db['bypass_roles'])
    xddd = literal_eval(ig_db['bypass_channels'])
    if user.id not in xd:
        pass
    else:
        ls = xd[user.id]
        if 'cmd' in ls:
          lss = ls['cmd']
          if lss == "all":
              return True
          elif cmd in lss:
              return True
          else:
              pass
    for i in user.roles:
        if i.id in xdd:
            ls = xdd[i.id]
            if 'cmd' in ls:
              lss = ls['cmd']
              if lss == "all":
                  return True
              elif cmd in lss:
                  return True
              else:
                  pass
    if ctx.channel.id not in xddd:
      pass
    else:
        ls = xddd[ctx.channel.id]
        if 'cmd' in ls:
          lss = ls['cmd']
          if lss == "all":
              return True
          elif cmd in lss:
              return True
          else:
              pass
    return False

async def by_module(ctx, user: discord.Member, module):
    c = await check_upgraded(ctx.guild.id)
    if not c:
        return False
    query = "SELECT * FROM  bypass WHERE guild_id = ?"
    val = (ctx.guild.id,)
    with sqlite3.connect('database.sqlite3') as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        cursor.execute(query, val)
        ig_db = cursor.fetchone()
    if ig_db is None:
        return False
    xd = literal_eval(ig_db['bypass_users'])
    xdd = literal_eval(ig_db['bypass_roles'])
    xddd = literal_eval(ig_db['bypass_channels'])
    if user.id not in xd:
        pass
    else:
        ls = xd[user.id]
        if 'module' in ls:
          lss = ls['module']
          if lss == "all":
              return True
          elif module in lss:
              return True
          else:
              pass
    for i in user.roles:
        if i.id in xdd:
            ls = xdd[i.id]
            if 'module' in ls:
              lss = ls['module']
              if lss == "all":
                  return True
              elif module in lss:
                  return True
              else:
                  pass
    if ctx.channel.id not in xddd:
      pass
    else:
        ls = xddd[ctx.channel.id]
        if 'module' in ls:
          lss = ls['module']
          if lss == "all":
              return True
          elif module in lss:
              return True
          else:
              pass
    return False

async def by_channel(ctx, user: discord.Member, channel: discord.TextChannel):
    c = await check_upgraded(ctx.guild.id)
    if not c:
        return False
    query = "SELECT * FROM  bypass WHERE guild_id = ?"
    val = (ctx.guild.id,)
    with sqlite3.connect('database.sqlite3') as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        cursor.execute(query, val)
        ig_db = cursor.fetchone()
    if ig_db is None:
        return False
    xd = literal_eval(ig_db['bypass_users'])
    xdd = literal_eval(ig_db['bypass_roles'])
    if user.id not in xd:
        pass
    else:
        ls = xd[user.id]
        if 'channel' in ls:
          lss = ls['channel']
          if lss == "all":
              return True
          elif channel.id in lss:
              return True
          else:
              pass
    try:
        for i in user.roles:
            if i.id in xdd:
                ls = xdd[i.id]
                if 'channel' in ls:
                    lss = ls['channel']
                    if lss == "all":
                        return True
                    elif channel.id in lss:
                        return True
                    else:
                        pass
    except:
        pass
    return False

async def by_role(ctx, user: discord.Member, role: discord.Role):
    c = await check_upgraded(ctx.guild.id)
    if not c:
        return False
    query = "SELECT * FROM  bypass WHERE guild_id = ?"
    val = (ctx.guild.id,)
    with sqlite3.connect('database.sqlite3') as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        cursor.execute(query, val)
        ig_db = cursor.fetchone()
    if ig_db is None:
        return False
    xd = literal_eval(ig_db['bypass_users'])
    xdd = literal_eval(ig_db['bypass_roles'])
    xddd = literal_eval(ig_db['bypass_channels'])
    if user.id not in xd:
        pass
    else:
        ls = xd[user.id]
        if 'role' in ls:
          lss = ls['role']
          if lss == "all":
              return True
          elif role.id in lss:
              return True
          else:
              pass
    for i in user.roles:
        if i.id in xdd:
            ls = xdd[i.id]
            if 'role' in ls:
              lss = ls['role']
              if lss == "all":
                  return True
              elif role.id in lss:
                  return True
              else:
                  pass
    if ctx.channel.id not in xddd:
      pass
    else:
        ls = xddd[ctx.channel.id]
        if 'role' in ls:
          lss = ls['role']
          if role.id in lss:
              return True
          elif lss == "all":
              return True
          else:
              pass
    return False

class extra(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.autopfp_task.start()

    @tasks.loop(minutes=10)
    async def autopfp_task(self):
        await self.bot.wait_until_ready()
        query = "SELECT * FROM  pfp"
        with sqlite3.connect('./database.sqlite3') as db:
                    db.row_factory = sqlite3.Row
                    cursor = db.cursor()
                    cursor.execute(query)
                    pfp_db = cursor.fetchall()
        for i, j, k in pfp_db:
            await autopfp(self, j, k)

    @commands.group(
        invoke_without_command=True, description="Shows The help menu for pfp"
    )
    async def pfp(self, ctx):
        prefix = ctx.prefix
        if prefix == f"<@{self.bot.user.id}> ":
            prefix = f"@{str(self.bot.user)} "
        xd = discord.utils.get(self.bot.users, id=978930369392951366)
        anay = str(xd)
        pfp = xd.display_avatar.url
        listem = discord.Embed(colour=0xc283fe,
                                     description=f"<...> Duty | [...] Optional\n\n" 
                                                  f"`{prefix}pfp`\n" 
                                                  f"Shows The help menu for pfp\n\n" 
                                                  f"`{prefix}pfp auto enable <channel>`\n" 
                                                  f"Sends pfp automatically every 2 mins\n\n"
                                                  f"`{prefix}pfp auto disable`\n"
                                                  f"Stops sending pfp\n\n"
                                                  f"`{prefix}pfp random <number>`\n" 
                                                  f"Sends random pfps\n\n")
        listem.set_author(name=f"{str(ctx.author)}", icon_url=ctx.author.display_avatar.url)
        listem.set_footer(text=f"Made by stars.gg" ,  icon_url=pfp)
        await ctx.send(embed=listem)
    
    @pfp.group(invoke_without_command=True, description="Shows The help menu for pfp auto")
    async def auto(self, ctx):
        with sqlite3.connect('database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(f"SELECT * FROM prefixes WHERE guild_id = {ctx.guild.id}")
            res = cursor.fetchone()
        prefix = res["prefix"]
        xd = discord.utils.get(self.bot.users, id=978930369392951366)
        anay = str(xd)
        pfp = xd.display_avatar.url
        listem = discord.Embed(colour=0xc283fe,
                                     description=f"<...> Duty | [...] Optional\n\n" 
                                                  f"`{prefix}pfp auto`\n" 
                                                  f"Shows The help menu for pfp auto\n\n" 
                                                  f"`{prefix}pfp auto enable <channel>`\n" 
                                                  f"Sends pfp automatically every 2 mins\n\n"
                                                  f"`{prefix}pfp auto disable`\n"
                                                  f"Stops sending pfp\n\n")
        listem.set_author(name=f"{str(ctx.author)}", icon_url=ctx.author.display_avatar.url)
        listem.set_footer(text=f"Made by stars.gg" ,  icon_url=pfp)
        await ctx.send(embed=listem)

    @auto.command()
    @commands.has_permissions(administrator=True)
    async def enable(self, ctx: commands.Context, *, channel: discord.TextChannel):
        view = PngOrGif(ctx)
        em = discord.Embed(description="Which type of pfp you want?\n**Note: The profile pictures may include expicit content as we are giving you profile picture of random users, So if you dont agree to it you can cancel the command.**", color=0xc283fe).set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        init = await ctx.reply(embed=em, view=view)
        await view.wait()
        if view.value == 'stop':
            return await init.delete()
        query = "SELECT * FROM  pfp WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
                    db.row_factory = sqlite3.Row
                    cursor = db.cursor()
                    cursor.execute(query, val)
                    pfp_db = cursor.fetchone()
        if pfp_db is None:
            sql = (f"INSERT INTO pfp(guild_id, channel_id, 'type') VALUES(?, ?, ?)")
            val = (ctx.guild.id, channel.id, view.value)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
        else:
            return await ctx.reply("It is already enabled")
        await init.delete()
        await ctx.reply(f"Now 5-10 profile pictures will be send in every 10 minutes in {channel.mention}.")
        await autopfp(self, channel.id, view.value)

    @auto.command()
    @commands.has_permissions(administrator=True)
    async def disable(self, ctx: commands.Context):
        query = "SELECT * FROM  pfp WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
                    db.row_factory = sqlite3.Row
                    cursor = db.cursor()
                    cursor.execute(query, val)
                    pfp_db = cursor.fetchone()
        if pfp_db is not None:
            sql = (f"DELETE FROM pfp WHERE guild_id = ?")
            val = (ctx.guild.id,)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
        else:
            return await ctx.reply(f"It was already disabled")
        await ctx.reply(f"Now no profile pictures will be send.")

    @pfp.command()
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def random(self, ctx: commands.Context, *, number):
        if number.isdigit():
            number = int(number)
        else:
            return await ctx.reply("Please provide a valid number")
        if abs(number) > 15:
            return await ctx.reply("The limit is only for 15 profile pictures")
        view = PngOrGif(ctx)
        em = discord.Embed(description="Which type of pfp you want?\n**Note: The profile pictures may include expicit content as we are giving you profile picture of random users, So if you dont agree to it you can cancel the command.**", color=0xc283fe).set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        init = await ctx.reply(embed=em, view=view)
        await view.wait()
        if view.value == 'stop':
            return await init.delete()
        if view.value == 'mix':
            await init.delete()
            u = random.sample(self.bot.users, 10000)
            c = 1
            for i in u:
                if i.avatar and c <= abs(number):
                        await ctx.send(i.avatar.url)
                        c += 1
        if view.value == 'png':
            await init.delete()
            u = random.sample(self.bot.users, 10000)
            c = 1
            for i in u:
                if i.avatar and c <= abs(number):
                    if 'png' in i.avatar.url:
                        await ctx.send(i.avatar.url)
                        c += 1
        if view.value == 'gif':
            await init.delete()
            u = random.sample(self.bot.users, 10000)
            c = 1
            for i in u:
                if i.avatar and c <= abs(number):
                    if 'gif' in i.avatar.url:
                        await ctx.send(i.avatar.url)
                        c += 1

    @commands.group(
        invoke_without_command=True, description="Shows The help menu for nightmode"
    )
    async def nightmode(self, ctx):
        prefix = ctx.prefix
        if prefix == f"<@{self.bot.user.id}> ":
            prefix = f"@{str(self.bot.user)} "
        xd = discord.utils.get(self.bot.users, id=978930369392951366)
        anay = str(xd)
        pfp = xd.display_avatar.url
        listem = discord.Embed(colour=0xc283fe,
                                     description=f"<...> Duty | [...] Optional\n\n" 
                                                  f"`{prefix}nightmode`\n" 
                                                  f"Shows The help menu for nightmode\n\n" 
                                                  f"`{prefix}nightmode enable <perm>`\n" 
                                                  f"Take perms from every role that is below the bot\n\n"
                                                  f"`{prefix}nightmode disable`\n"
                                                  f"Give the role their permissions back\n\n")
        listem.set_author(name=f"{str(ctx.author)}", icon_url=ctx.author.display_avatar.url)
        listem.set_footer(text=f"Made by stars.gg" ,  icon_url=pfp)
        await ctx.send(embed=listem)

    @nightmode.command(name="enable", aliases=['on'], description="Enables nightmode for the server")
    @commands.has_permissions(administrator=True)
    async def _enable(self, ctx, *, perms):
        c = await check_upgraded(ctx.guild.id)
        if not c:
            em = discord.Embed(description=f"You just tried to execute a premium command but this guild is not upgarded\nYou can buy bot's premium from the link given below or by creating a ticket in the [Support Server](https://discord.gg/6Q9D7R8hYc)", color=0xc283fe).set_footer(text=f"{self.bot.user.name} Premium feature", icon_url=self.bot.user.avatar.url)
            v = discord.ui.View()
            v.add_item(discord.ui.Button(label="Patreon", url="https://www.patreon.com/gateway_bot"))
            v.add_item(discord.ui.Button(label="Support Server", url="https://discord.gg/6Q9D7R8hYc"))
            return await ctx.reply(embed=em, view=v)
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 979353019235840000]:
                em = discord.Embed(description=f"<:error:1153009680428318791>You must Have Higher Role than Bot To run This Command", color=0xff0000)
                return await ctx.send(embed=em)
        if not ctx.guild.me.guild_permissions.administrator:
            return await ctx.reply(embed=discord.Embed(description="Gateway lacks certain permissions to run this function properly kindly refer to [our documentation for more](https://docs.gatewaybot.xyz/faqs/#gateway-lacks-certain-permissions-to-run-this-function-properly)", color=0xc283fe))
        valid = ['All', 'Admin', 'Kick', 'Ban', 'Manage server', 'Manage channels', 'Manage roles', 'Mention everyone']
        if perms.capitalize() not in valid:
            return await ctx.reply(f"Please give a valid perm to remove\nValid perms are {', '.join(valid)}")
        perms = perms.lower()
        with sqlite3.connect('database.sqlite3') as db1:
            db1.row_factory = sqlite3.Row
            cursor1 = db1.cursor()
            cursor1.execute(f"SELECT * FROM prefixes WHERE guild_id = {ctx.guild.id}")
            res = cursor1.fetchone()
        prefix = res["prefix"]
        query = "SELECT * FROM  imp WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            imp_db = cursor.fetchone()
        valid = ['all', 'admin', 'kick', 'ban', 'manage server', 'manage channels', 'manage roles', 'mention everyone']
        if imp_db['cmd'] in valid:
            em = discord.Embed(description=f"Nightmode is already enabled please kindly do `{prefix}nightmode off`", color=0xff0000)
            return await ctx.reply(embed=em, mention_author=False)
        adm, ki, ba, server, ch, ro, every = [], [], [], [], [], [], []
        view = night(ctx)
        em = discord.Embed(description="From which type of roles you want to remove Perms\nNote: Be sure that the top role of Bot has **Adminstrator Perms** and is **Whitelisted** from every anti-nuke bot Before clicking any of the buttons because during turning on the nightmode if bot gets kick/ban the changes wont be reversed", color=0xc283fe)
        ok = await ctx.reply(embed=em, view=view, mention_author=False)
        await view.wait()
        if not view.value:
            await ok.delete()
            return await ctx.reply("Timed out!", mention_author=True)
        if view.value == 'cancel':
            await ok.delete()
            em = discord.Embed(description=f"Successfully cancelled the command", color=0xc283fe)
            return await ctx.reply(embed=em)
        if view.value == 'simple':
            await ok.delete()
            if perms == 'all':
                for role in ctx.guild.roles:
                  if role.is_bot_managed() is False:
                    if role.position < ctx.guild.me.top_role.position:
                        if role.permissions.administrator:
                            adm.append(role.id)
                        if role.permissions.kick_members:
                            ki.append(role.id)
                        if role.permissions.ban_members:
                            ba.append(role.id)
                        if role.permissions.manage_guild:
                            server.append(role.id)
                        if role.permissions.manage_channels:
                            ch.append(role.id)
                        if role.permissions.manage_roles:
                            ro.append(role.id)
                        if role.permissions.mention_everyone:
                            every.append(role.id)
                        permission = role.permissions
                        permission.update(kick_members=False, ban_members=False, manage_guild=False, mention_everyone=False, administrator = False, manage_roles=False, manage_channels=False)
                        await role.edit(permissions=permission, reason="Enabled Nightmode")
                await ctx.reply(embed=discord.Embed(description=f"Removed every Dangerous perms from every Role that is Below me\nRun `{prefix}nightmode off` to give back permissions to the roles", color=0xc283fe),mention_author=False)
            if perms == 'admin':
                for role in ctx.guild.roles:
                  if role.is_bot_managed() is False:
                    if role.position < ctx.guild.me.top_role.position:
                        if role.permissions.administrator:
                            adm.append(role.id)
                        permission = role.permissions
                        permission.update(administrator=False)
                        await role.edit(permissions=permission, reason="Enabled Nightmode")
                await ctx.reply(embed=discord.Embed(description=f"Removed admin perms from every Role that is Below me\nRun `{prefix}nightmode off` to give back permissions to the roles", color=0xc283fe),mention_author=False)
            if perms == 'kick':
                for role in ctx.guild.roles:
                  if role.is_bot_managed() is False:
                    if role.position < ctx.guild.me.top_role.position:
                        if role.permissions.kick_members:
                            ki.append(role.id)
                        permission = role.permissions
                        permission.update(kick_members=False)
                        await role.edit(permissions=permission, reason="Enabled Nightmode")
                await ctx.reply(embed=discord.Embed(description=f"Removed Kick perms from every Role that is Below me\nRun `{prefix}nightmode off` to give back permissions to the roles", color=0xc283fe),mention_author=False)
            if perms == 'ban':
                for role in ctx.guild.roles:
                  if role.is_bot_managed() is False:
                    if role.position < ctx.guild.me.top_role.position:
                        if role.permissions.ban_members:
                            ba.append(role.id)
                        permission = role.permissions
                        permission.update(ban_members=False)
                        await role.edit(permissions=permission, reason="Enabled Nightmode")
                await ctx.reply(embed=discord.Embed(description=f"Removed Ban perms from every Role that is Below me\nRun `{prefix}nightmode off` to give back permissions to the roles", color=0xc283fe),mention_author=False)
            if perms == 'manage server':
                for role in ctx.guild.roles:
                  if role.is_bot_managed() is False:
                    if role.position < ctx.guild.me.top_role.position:
                        if role.permissions.manage_guild:
                            server.append(role.id)
                        permission = role.permissions
                        permission.update(manage_guild=False)
                        await role.edit(permissions=permission, reason="Enabled Nightmode")
                await ctx.reply(embed=discord.Embed(description=f"Removed Manage server perms from every Role that is Below me\nRun `{prefix}nightmode off` to give back permissions to the roles", color=0xc283fe),mention_author=False)
            if perms == 'manage channels':
                for role in ctx.guild.roles:
                  if role.is_bot_managed() is False:
                    if role.position < ctx.guild.me.top_role.position:
                        if role.permissions.manage_channels:
                            ch.append(role.id)
                        permission = role.permissions
                        permission.update(manage_channels=False)
                        await role.edit(permissions=permission, reason="Enabled Nightmode")
                await ctx.reply(embed=discord.Embed(description=f"Removed Manage Channels perms from every Role that is Below me\nRun `{prefix}nightmode off` to give back permissions to the roles", color=0xc283fe),mention_author=False)
            if perms == 'manage roles':
                for role in ctx.guild.roles:
                  if role.is_bot_managed() is False:
                    if role.position < ctx.guild.me.top_role.position:
                        if role.permissions.manage_roles:
                            ro.append(role.id)
                        permission = role.permissions
                        permission.update(manage_roles=False)
                        await role.edit(permissions=permission, reason="Enabled Nightmode")
                await ctx.reply(embed=discord.Embed(description=f"Removed Manage Roles perms from every Role that is Below me\nRun `{prefix}nightmode off` to give back permissions to the roles", color=0xc283fe),mention_author=False)
            if perms == 'mention everyone':
                for role in ctx.guild.roles:
                  if role.is_bot_managed() is False:
                    if role.position < ctx.guild.me.top_role.position:
                        if role.permissions.mention_everyone:
                            every.append(role.id)
                        permission = role.permissions
                        permission.update(mention_everyone=False)
                        await role.edit(permissions=permission, reason="Enabled Nightmode")
                await ctx.reply(embed=discord.Embed(description=f"Removed Mention everyone perms from every Role that is Below me\nRun `{prefix}nightmode off` to give back permissions to the roles", color=0xc283fe),mention_author=False)
        if view.value == 'bot':
            await ok.delete()
            if perms == 'all':
                for role in ctx.guild.roles:
                  if role.is_bot_managed() is True:
                    if role.position < ctx.guild.me.top_role.position:
                        if role.permissions.administrator:
                            adm.append(role.id)
                        if role.permissions.kick_members:
                            ki.append(role.id)
                        if role.permissions.ban_members:
                            ba.append(role.id)
                        if role.permissions.manage_guild:
                            server.append(role.id)
                        if role.permissions.manage_channels:
                            ch.append(role.id)
                        if role.permissions.manage_roles:
                            ro.append(role.id)
                        if role.permissions.mention_everyone:
                            every.append(role.id)
                        permission = role.permissions
                        permission.update(kick_members=False, ban_members=False, manage_guild=False, mention_everyone=False, administrator = False, manage_roles=False, manage_channels=False)
                        await role.edit(permissions=permission, reason="Enabled Nightmode")
                await ctx.reply(embed=discord.Embed(description=f"Removed every Dangerous perms from every Role that is Below me\nRun `{prefix}nightmode off` to give back permissions to the roles", color=0xc283fe),mention_author=False)
            if perms == 'admin':
                for role in ctx.guild.roles:
                  if role.is_bot_managed() is True:
                    if role.position < ctx.guild.me.top_role.position:
                        if role.permissions.administrator:
                            adm.append(role.id)
                        permission = role.permissions
                        permission.update(administrator=False)
                        await role.edit(permissions=permission, reason="Enabled Nightmode")
                await ctx.reply(embed=discord.Embed(description=f"Removed admin perms from every Role that is Below me\nRun `{prefix}nightmode off` to give back permissions to the roles", color=0xc283fe),mention_author=False)
            if perms == 'kick':
                for role in ctx.guild.roles:
                  if role.is_bot_managed() is True:
                    if role.position < ctx.guild.me.top_role.position:
                        if role.permissions.kick_members:
                            ki.append(role.id)
                        permission = role.permissions
                        permission.update(kick_members=False)
                        await role.edit(permissions=permission, reason="Enabled Nightmode")
                await ctx.reply(embed=discord.Embed(description=f"Removed Kick perms from every Role that is Below me\nRun `{prefix}nightmode off` to give back permissions to the roles", color=0xc283fe),mention_author=False)
            if perms == 'ban':
                for role in ctx.guild.roles:
                  if role.is_bot_managed() is True:
                    if role.position < ctx.guild.me.top_role.position:
                        if role.permissions.ban_members:
                            ba.append(role.id)
                        permission = role.permissions
                        permission.update(ban_members=False)
                        await role.edit(permissions=permission, reason="Enabled Nightmode")
                await ctx.reply(embed=discord.Embed(description=f"Removed Ban perms from every Role that is Below me\nRun `{prefix}nightmode off` to give back permissions to the roles", color=0xc283fe),mention_author=False)
            if perms == 'manage server':
                for role in ctx.guild.roles:
                  if role.is_bot_managed() is True:
                    if role.position < ctx.guild.me.top_role.position:
                        if role.permissions.manage_guild:
                            server.append(role.id)
                        permission = role.permissions
                        permission.update(manage_guild=False)
                        await role.edit(permissions=permission, reason="Enabled Nightmode")
                await ctx.reply(embed=discord.Embed(description=f"Removed Manage server perms from every Role that is Below me\nRun `{prefix}nightmode off` to give back permissions to the roles", color=0xc283fe),mention_author=False)
            if perms == 'manage channels':
                for role in ctx.guild.roles:
                  if role.is_bot_managed() is True:
                    if role.position < ctx.guild.me.top_role.position:
                        if role.permissions.manage_channels:
                            ch.append(role.id)
                        permission = role.permissions
                        permission.update(manage_channels=False)
                        await role.edit(permissions=permission, reason="Enabled Nightmode")
                await ctx.reply(embed=discord.Embed(description=f"Removed Manage Channels perms from every Role that is Below me\nRun `{prefix}nightmode off` to give back permissions to the roles", color=0xc283fe),mention_author=False)
            if perms == 'manage roles':
                for role in ctx.guild.roles:
                  if role.is_bot_managed() is True:
                    if role.position < ctx.guild.me.top_role.position:
                        if role.permissions.manage_roles:
                            ro.append(role.id)
                        permission = role.permissions
                        permission.update(manage_roles=False)
                        await role.edit(permissions=permission, reason="Enabled Nightmode")
                await ctx.reply(embed=discord.Embed(description=f"Removed Manage Roles perms from every Role that is Below me\nRun `{prefix}nightmode off` to give back permissions to the roles", color=0xc283fe),mention_author=False)
            if perms == 'mention everyone':
                for role in ctx.guild.roles:
                  if role.is_bot_managed() is True:
                    if role.position < ctx.guild.me.top_role.position:
                        if role.permissions.mention_everyone:
                            every.append(role.id)
                        permission = role.permissions
                        permission.update(mention_everyone=False)
                        await role.edit(permissions=permission, reason="Enabled Nightmode")
                await ctx.reply(embed=discord.Embed(description=f"Removed Mention everyone perms from every Role that is Below me\nRun `{prefix}nightmode off` to give back permissions to the roles", color=0xc283fe),mention_author=False)
        if view.value == 'both':
            await ok.delete()
            if perms == 'all':
                for role in ctx.guild.roles:
                    if role.position < ctx.guild.me.top_role.position:
                        if role.permissions.administrator:
                            adm.append(role.id)
                        if role.permissions.kick_members:
                            ki.append(role.id)
                        if role.permissions.ban_members:
                            ba.append(role.id)
                        if role.permissions.manage_guild:
                            server.append(role.id)
                        if role.permissions.manage_channels:
                            ch.append(role.id)
                        if role.permissions.manage_roles:
                            ro.append(role.id)
                        if role.permissions.mention_everyone:
                            every.append(role.id)
                        permission = role.permissions
                        permission.update(kick_members=False, ban_members=False, manage_guild=False, mention_everyone=False, administrator = False, manage_roles=False, manage_channels=False)
                        await role.edit(permissions=permission, reason="Enabled Nightmode")
                await ctx.reply(embed=discord.Embed(description=f"Removed every Dangerous perms from every Role that is Below me\nRun `{prefix}nightmode off` to give back permissions to the roles", color=0xc283fe),mention_author=False)
            if perms == 'admin':
                for role in ctx.guild.roles:
                    if role.position < ctx.guild.me.top_role.position:
                        if role.permissions.administrator:
                            adm.append(role.id)
                        permission = role.permissions
                        permission.update(administrator=False)
                        await role.edit(permissions=permission, reason="Enabled Nightmode")
                await ctx.reply(embed=discord.Embed(description=f"Removed admin perms from every Role that is Below me\nRun `{prefix}nightmode off` to give back permissions to the roles", color=0xc283fe),mention_author=False)
            if perms == 'kick':
                for role in ctx.guild.roles:
                    if role.position < ctx.guild.me.top_role.position:
                        if role.permissions.kick_members:
                            ki.append(role.id)
                        permission = role.permissions
                        permission.update(kick_members=False)
                        await role.edit(permissions=permission, reason="Enabled Nightmode")
                await ctx.reply(embed=discord.Embed(description=f"Removed Kick perms from every Role that is Below me\nRun `{prefix}nightmode off` to give back permissions to the roles", color=0xc283fe),mention_author=False)
            if perms == 'ban':
                for role in ctx.guild.roles:
                    if role.position < ctx.guild.me.top_role.position:
                        if role.permissions.ban_members:
                            ba.append(role.id)
                        permission = role.permissions
                        permission.update(ban_members=False)
                        await role.edit(permissions=permission, reason="Enabled Nightmode")
                await ctx.reply(embed=discord.Embed(description=f"Removed Ban perms from every Role that is Below me\nRun `{prefix}nightmode off` to give back permissions to the roles", color=0xc283fe),mention_author=False)
            if perms == 'manage server':
                for role in ctx.guild.roles:
                    if role.position < ctx.guild.me.top_role.position:
                        if role.permissions.manage_guild:
                            server.append(role.id)
                        permission = role.permissions
                        permission.update(manage_guild=False)
                        await role.edit(permissions=permission, reason="Enabled Nightmode")
                await ctx.reply(embed=discord.Embed(description=f"Removed Manage server perms from every Role that is Below me\nRun `{prefix}nightmode off` to give back permissions to the roles", color=0xc283fe),mention_author=False)
            if perms == 'manage channels':
                for role in ctx.guild.roles:
                    if role.position < ctx.guild.me.top_role.position:
                        if role.permissions.manage_channels:
                            ch.append(role.id)
                        permission = role.permissions
                        permission.update(manage_channels=False)
                        await role.edit(permissions=permission, reason="Enabled Nightmode")
                await ctx.reply(embed=discord.Embed(description=f"Removed Manage Channels perms from every Role that is Below me\nRun `{prefix}nightmode off` to give back permissions to the roles", color=0xc283fe),mention_author=False)
            if perms == 'manage roles':
                for role in ctx.guild.roles:
                    if role.position < ctx.guild.me.top_role.position:
                        if role.permissions.manage_roles:
                            ro.append(role.id)
                        permission = role.permissions
                        permission.update(manage_roles=False)
                        await role.edit(permissions=permission, reason="Enabled Nightmode")
                await ctx.reply(embed=discord.Embed(description=f"Removed Manage Roles perms from every Role that is Below me\nRun `{prefix}nightmode off` to give back permissions to the roles", color=0xc283fe),mention_author=False)
            if perms == 'mention everyone':
                for role in ctx.guild.roles:
                    if role.position < ctx.guild.me.top_role.position:
                        if role.permissions.mention_everyone:
                            every.append(role.id)
                        permission = role.permissions
                        permission.update(mention_everyone=False)
                        await role.edit(permissions=permission, reason="Enabled Nightmode")
                await ctx.reply(embed=discord.Embed(description=f"Removed Mention everyone perms from every Role that is Below me\nRun `{prefix}nightmode off` to give back permissions to the roles", color=0xc283fe),mention_author=False)
        hm = []
        sql = "UPDATE imp SET cmd = ? WHERE guild_id = ?"
        val = (f"{perms}", ctx.guild.id)
        cursor.execute(sql, val)
        if adm != hm:
            sql1 = "UPDATE imp SET admin = ? WHERE guild_id = ?"
            val1 = (f"{adm}", ctx.guild.id)
            cursor.execute(sql1, val1)
        if ki != hm:
            sql2 = "UPDATE imp SET kick = ? WHERE guild_id = ?"
            val2 = (f"{ki}", ctx.guild.id)
            cursor.execute(sql2, val2)
        if ba != hm:
            sql3 = "UPDATE imp SET ban = ? WHERE guild_id = ?"
            val3 = (f"{ba}", ctx.guild.id)
            cursor.execute(sql3, val3)
        if server != hm:
            sql4 = "UPDATE imp SET mgn = ? WHERE guild_id = ?"
            val4 = (f"{server}", ctx.guild.id)
            cursor.execute(sql4, val4)
        if ch != hm:
            sql5 = "UPDATE imp SET mgnch = ? WHERE guild_id = ?"
            val5 = (f"{ch}", ctx.guild.id)
            cursor.execute(sql5, val5)
        if ro != hm:
            sql6 = "UPDATE imp SET mgnro = ? WHERE guild_id = ?"
            val6 = (f"{ro}", ctx.guild.id)
            cursor.execute(sql6, val6)
        if every != hm:
            sql7 = "UPDATE imp SET mention = ? WHERE guild_id = ?"
            val7 = (f"{every}", ctx.guild.id)
            cursor.execute(sql7, val7)
        db.commit()
        cursor.close()
        db.close()

    @nightmode.command(name='disable', aliases=['off'], description="Disables nightmode for the server")
    @commands.has_permissions(administrator=True)
    async def _disable(self, ctx):
        c = await check_upgraded(ctx.guild.id)
        if not c:
            em = discord.Embed(description=f"You just tried to execute a premium command but this guild is not upgarded\nYou can buy bot's premium from the link given below or by creating a ticket in the [Support Server](https://discord.gg/6Q9D7R8hYc)", color=0xc283fe).set_footer(text=f"{self.bot.user.name} Premium feature", icon_url=self.bot.user.avatar.url)
            v = discord.ui.View()
            v.add_item(discord.ui.Button(label="Patreon", url="https://www.patreon.com/gateway_bot"))
            v.add_item(discord.ui.Button(label="Support Server", url="https://discord.gg/6Q9D7R8hYc"))
            return await ctx.reply(embed=em, view=v)
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 979353019235840000]:
                em = discord.Embed(description=f"<:error:1153009680428318791>You must Have Higher Role than Bot To run This Command", color=0xff0000)
                return await ctx.send(embed=em)
        if not ctx.guild.me.guild_permissions.administrator:
            return await ctx.reply(embed=discord.Embed(description="Gatewaylacks certain permissions to run this function properly kindly refer to [our documentation for more](https://docs.gatewaybot.xyz/faqs/#gateway-lacks-certain-permissions-to-run-this-function-properly)", color=0xc283fe))
        with sqlite3.connect('database.sqlite3') as db1:
            db1.row_factory = sqlite3.Row
            cursor1 = db1.cursor()
            cursor1.execute(f"SELECT * FROM prefixes WHERE guild_id = {ctx.guild.id}")
            res = cursor1.fetchone()
        prefix = res["prefix"]
        query = "SELECT * FROM  imp WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            imp_db = cursor.fetchone()
        valid = ['all', 'admin', 'kick', 'ban', 'manage server', 'manage channels', 'manage roles', 'mention everyone']
        if imp_db['cmd'] not in valid:
            em = discord.Embed(description=f"Nightmode is already disabled please kindly do `{ctx.prefix}nightmode on <perm>`", color=0xff0000)
            return await ctx.reply(embed=em, mention_author=False)
        adm = imp_db['admin']
        ki = imp_db['kick']
        ba = imp_db['ban']
        server = imp_db['mgn']
        ch = imp_db['mgnch']
        ro = imp_db['mgnro']
        every = imp_db['mention']
        cm = imp_db['cmd']
        if cm == 'all':
            for role in ctx.guild.roles:
                if f"{role.id}" in adm:
                    if role.position < ctx.guild.me.top_role.position:
                        if not role.permissions.administrator:
                            permission = role.permissions
                            permission.update(administrator=True)
                            await role.edit(permissions=permission, reason="Disabled Nightmode")
                if f"{role.id}" in ki:
                    if role.position < ctx.guild.me.top_role.position:
                        if not role.permissions.kick_members:
                            permission = role.permissions
                            permission.update(kick_members=True)
                            await role.edit(permissions=permission, reason="Disabled Nightmode")
                if f"{role.id}" in ba:
                    if role.position < ctx.guild.me.top_role.position:
                        if not role.permissions.ban_members:
                            permission = role.permissions
                            permission.update(ban_members=True)
                            await role.edit(permissions=permission, reason="Disabled Nightmode")
                if f"{role.id}" in server:
                    if role.position < ctx.guild.me.top_role.position:
                        if not role.permissions.manage_guild:
                            permission = role.permissions
                            permission.update(manage_guild=True)
                            await role.edit(permissions=permission, reason="Disabled Nightmode")
                if f"{role.id}" in ch:
                    if role.position < ctx.guild.me.top_role.position:
                        if not role.permissions.manage_channels:
                            permission = role.permissions
                            permission.update(manage_channels=True)
                            await role.edit(permissions=permission, reason="Disabled Nightmode")
                if f"{role.id}" in ro:
                    if role.position < ctx.guild.me.top_role.position:
                        if not role.permissions.manage_roles:
                            permission = role.permissions
                            permission.update(manage_roles=True)
                            await role.edit(permissions=permission, reason="Disabled Nightmode")
                if f"{role.id}" in every:
                    if role.position < ctx.guild.me.top_role.position:
                        if not role.permissions.mention_everyone:
                            permission = role.permissions
                            permission.update(mention_everyone=True)
                            await role.edit(permissions=permission, reason="Disabled Nightmode")
            await ctx.reply(embed=discord.Embed(description=f"Given permissions back to All the roles Below me\nRun `{prefix}nighmode enable <perms>` to Enable Night Mode", color=0xc283fe), mention_author=False)
        if cm == 'admin':
            for role in ctx.guild.roles:
                if f"{role.id}" in adm:
                    if role.position < ctx.guild.me.top_role.position:
                        if not role.permissions.administrator:
                            permission = role.permissions
                            permission.update(administrator=True)
                            await role.edit(permissions=permission, reason="Disabled Nightmode")
            await ctx.reply(embed=discord.Embed(description=f"Given Admin permissions back to All the roles Below me\nRun `{prefix}nighmode enable <perms>` to Enable Night Mode", color=0xc283fe), mention_author=False)
        if cm == 'kick':
            for role in ctx.guild.roles:
                if f"{role.id}" in ki:
                    if role.position < ctx.guild.me.top_role.position:
                        if not role.permissions.kick_members:
                            permission = role.permissions
                            permission.update(kick_members=True)
                            await role.edit(permissions=permission, reason="Disabled Nightmode")
            await ctx.reply(embed=discord.Embed(description=f"Given Kick permissions back to All the roles Below me\nRun `{prefix}nighmode enable <perms>` to Enable Night Mode", color=0xc283fe), mention_author=False)
        if cm == 'ban':
            for role in ctx.guild.roles:
                if f"{role.id}" in ba:
                    if role.position < ctx.guild.me.top_role.position:
                        if not role.permissions.ban_members:
                            permission = role.permissions
                            permission.update(ban_members=True)
                            await role.edit(permissions=permission, reason="Disabled Nightmode")
            await ctx.reply(embed=discord.Embed(description=f"Given Ban permissions back to All the roles Below me\nRun `{prefix}nighmode enable <perms>` to Enable Night Mode", color=0xc283fe), mention_author=False)
        if cm == 'manage server':
            for role in ctx.guild.roles:
                if f"{role.id}" in server:
                    if role.position < ctx.guild.me.top_role.position:
                        if not role.permissions.manage_guild:
                            permission = role.permissions
                            permission.update(manage_guild=True)
                            await role.edit(permissions=permission, reason="Disabled Nightmode")
            await ctx.reply(embed=discord.Embed(description=f"Given Manage server permissions back to All the roles Below me\nRun `{prefix}nighmode enable <perms>` to Enable Night Mode", color=0xc283fe), mention_author=False)
        if cm == 'manage channels':
            for role in ctx.guild.roles:
                if f"{role.id}" in ch:
                    if role.position < ctx.guild.me.top_role.position:
                        if not role.permissions.manage_channels:
                            permission = role.permissions
                            permission.update(manage_channels=True)
                            await role.edit(permissions=permission, reason="Disabled Nightmode")
            await ctx.reply(embed=discord.Embed(description=f"Given Manage channels permissions back to All the roles Below me\nRun `{prefix}nighmode enable <perms>` to Enable Night Mode", color=0xc283fe), mention_author=False)
        if cm == 'manage roles':
            for role in ctx.guild.roles:
                if f"{role.id}" in ro:
                    if role.position < ctx.guild.me.top_role.position:
                        if not role.permissions.manage_roles:
                            permission = role.permissions
                            permission.update(manage_roles=True)
                            await role.edit(permissions=permission, reason="Disabled Nightmode")
            await ctx.reply(embed=discord.Embed(description=f"Given Manage roles permissions back to All the roles Below me\nRun `{prefix}nighmode enable <perms>` to Enable Night Mode", color=0xc283fe), mention_author=False)
        if cm == 'manage everyone':
            for role in ctx.guild.roles:
                if f"{role.id}" in every:
                    if role.position < ctx.guild.me.top_role.position:
                        if not role.permissions.mention_everyone:
                            permission = role.permissions
                            permission.update(mention_everyone=True)
                            await role.edit(permissions=permission, reason="Disabled Nightmode")
            await ctx.reply(embed=discord.Embed(description=f"Given Mention everyone permissions back to All the roles Below me\nRun `{prefix}nighmode enable <perms>` to Enable Night Mode", color=0xc283fe), mention_author=False)
        hm = []
        sql8 = "UPDATE imp SET cmd = ? WHERE guild_id = ?"
        val8 = (f"0", ctx.guild.id)
        cursor.execute(sql8, val8)
        if cm == 'all':
            sql1 = "UPDATE imp SET admin = ? WHERE guild_id = ?"
            val1 = (f"0", ctx.guild.id)
            cursor.execute(sql1, val1)
            sql2 = "UPDATE imp SET kick = ? WHERE guild_id = ?"
            val2 = (f"0", ctx.guild.id)
            cursor.execute(sql2, val2)
            sql3 = "UPDATE imp SET ban = ? WHERE guild_id = ?"
            val3 = (f"0", ctx.guild.id)
            cursor.execute(sql3, val3)
            sql4 = "UPDATE imp SET mgn = ? WHERE guild_id = ?"
            val4 = (f"0", ctx.guild.id)
            cursor.execute(sql4, val4)
            sql5 = "UPDATE imp SET mgnch = ? WHERE guild_id = ?"
            val5 = (f"0", ctx.guild.id)
            cursor.execute(sql5, val5)
            sql6 = "UPDATE imp SET mgnro = ? WHERE guild_id = ?"
            val6 = (f"0", ctx.guild.id)
            sql7 = "UPDATE imp SET mention = ? WHERE guild_id = ?"
            val7 = (f"0", ctx.guild.id)
            cursor.execute(sql7, val7)
        if cm == 'admin':
            sql1 = "UPDATE imp SET admin = ? WHERE guild_id = ?"
            val1 = (f"0", ctx.guild.id)
            cursor.execute(sql1, val1)
        if cm == 'kick':
            sql2 = "UPDATE imp SET kick = ? WHERE guild_id = ?"
            val2 = (f"0", ctx.guild.id)
            cursor.execute(sql2, val2)
        if cm == 'ban':
            sql3 = "UPDATE imp SET ban = ? WHERE guild_id = ?"
            val3 = (f"0", ctx.guild.id)
            cursor.execute(sql3, val3)
        if cm == 'manage server':
            sql4 = "UPDATE imp SET mgn = ? WHERE guild_id = ?"
            val4 = (f"0", ctx.guild.id)
            cursor.execute(sql4, val4)
        if cm == 'manage channels':
            sql5 = "UPDATE imp SET mgnch = ? WHERE guild_id = ?"
            val5 = (f"0", ctx.guild.id)
            cursor.execute(sql5, val5)
        if cm == 'manage roles':
            sql6 = "UPDATE imp SET mgnro = ? WHERE guild_id = ?"
            val6 = (f"0", ctx.guild.id)
            cursor.execute(sql6, val6)
        if cm == 'mention everyone':
            sql7 = "UPDATE imp SET mention = ? WHERE guild_id = ?"
            val7 = (f"0", ctx.guild.id)
            cursor.execute(sql7, val7)
        db.commit()
        cursor.close()
        db.close()

    @commands.group(invoke_without_command=True, description="Custom role setup for the server")
    async def setup(self, ctx):
        prefix = ctx.prefix
        if prefix == f"<@{self.bot.user.id}> ":
            prefix = f"@{str(self.bot.user)} "
        anay = discord.utils.get(self.bot.users, id=978930369392951366)
        setupem = discord.Embed(colour=0xc283fe,
                                     description=f"<...> Duty | [...] Optional\n\n" 
                                                 f"`{prefix}setup`\n"
                                                 f"This Command Will Show This Page\n\n"
                                                 f"`{prefix}setup reqrole`\n"
                                                 f"It will setup the required role to run some custom role commands\n\n"
                                                 f"`{prefix}setup create`\n"
                                                 f"To add an alias for giving and taking specific roles\n\n"
                                                 f"`{prefix}setup delete`\n"
                                                 f"To remove an alias from giving and taking specific roles\n\n"
                                                 f"`{prefix}setup official`\n"
                                                 f"Set The Official role\n\n"
                                                 f"`{prefix}setup tag`\n"
                                                 f"Set The Tag for Official role\n\n"
                                                 f"`{prefix}setup stag`\n"
                                                 f"Set The Small Tag for Official role\n\n"
                                                 f"`{prefix}setup friend`\n"
                                                 f"Set The Friend role\n\n"
                                                 f"`{prefix}setup guest`\n"
                                                 f"Set the Guest role\n\n"
                                                 f"`{prefix}setup vip`\n"
                                                 f"Set the Vip role.\n\n"
                                                 f"`{prefix}setup girl`\n"
                                                 f"Set the Girl role\n\n"
                                                 f"`{prefix}setup config`\n" 
                                                 f"Shows The current Custom role Settings For the server\n\n"
                                                 f"`{prefix}setup reset`\n" 
                                                 f"Resets the Custom Role Settings For the server")
        setupem.set_author(name=f"{str(ctx.author)}", icon_url=ctx.author.display_avatar.url)
        setupem.set_footer(text=f"Made by stars.gg" ,  icon_url=anay.avatar.url)
        query = "SELECT * FROM  roles WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
          db.row_factory = sqlite3.Row
          cursor = db.cursor()
          cursor.execute(query, val)
          setup_db = cursor.fetchone()
        official = setup_db['official']
        friend = setup_db['friend']
        guest = setup_db['guest']
        vip = setup_db['vip']
        girl = setup_db['girls']
        if official == 0:
          off = f"Official role is not set"
          roff = f"Official role is not set"
        else:
          off = f"Gives <@&{official}> to member"
          roff = f"Removes <@&{official}> from member"
        if friend == 0:
          fr = f"Friend role is not set"
          rfr = f"Friend role is not set"
        else:
          fr = f"Gives <@&{friend}> to member"
          rfr = f"Removes <@&{friend}> from member"
        if guest == 0:
          gu = f"Guest role is not set"
          rgu = f"Guest role is not set"
        else:
          gu = f"Gives <@&{guest}> to member"
          rgu = f"Removes <@&{guest}> from member"
        if vip == 0:
          vi = f"Vip role is not set"
          rvi = f"Vip role is not set"
        else:
          vi = f"Gives <@&{vip}> to member"
          rvi = f"Removes <@&{vip}> from member"
        if girl == 0:
          gir = f"Girl role is not set"
          rgir = f"Girl role is not set"
        else:
          gir = f"Gives <@&{girl}> to member"
          rgir = f"Removes <@&{girl}> from member"
        setupem1 = discord.Embed(colour=0xc283fe,
                                     description=f"<...> Duty | [...] Optional\n\n" 
                                                 f"`{prefix}official <member>`\n"
                                                 f"{off}\n\n"
                                                 f"`{prefix}applied`\n"
                                                 f"{off} but only if your name has tag\n\n"
                                                 f"`{prefix}friend <member>`\n"
                                                 f"{fr}\n\n"
                                                 f"`{prefix}guest <member>`\n"
                                                 f"{gu}\n\n"
                                                 f"`{prefix}vip <member>`\n"
                                                 f"{vi}\n\n"
                                                 f"`{prefix}girl <member>`\n"
                                                 f"{gir}\n\n"
                                                 f"`{prefix}rofficial <member>`\n"
                                                 f"{roff}\n\n"
                                                 f"`{prefix}rfriend <member>`\n"
                                                 f"{rfr}\n\n"
                                                 f"`{prefix}rguest <member>`\n"
                                                 f"{rgu}\n\n"
                                                 f"`{prefix}rvip <member>`\n"
                                                 f"{rvi}\n\n"
                                                 f"`{prefix}rgirl <member>`\n"
                                                 f"{rgir}\n\n")
        setupem1.set_author(name=f"{str(ctx.author)}", icon_url=ctx.author.display_avatar.url)
        setupem1.set_footer(text=f"Made by stars.gg" ,  icon_url=anay.avatar.url)
        em_list = []
        em_list.append(setupem)
        em_list.append(setupem1)
        page = PaginationView(embed_list=em_list, ctx=ctx)
        await page.start(ctx)
            
    @setup.command(name="reset", description="Reset custom role settings for the server")
    @commands.has_permissions(administrator=True)
    async def reset(self, ctx, *, option):
            if ctx.guild.owner.id == ctx.author.id:
                pass
            else:
                if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 979353019235840000]:
                    em = discord.Embed(description=f"<:error:1153009680428318791>You must Have Higher Role than Bot To run This Command", color=0xff0000)
                    return await ctx.send(embed=em)
            if not option:
                await ctx.reply("Mention a badge to Remove")
            msg = option
            msg = msg.lower()
            valid = ["all", "reqrole", "custom", "official", "officials", "staff", "staffs", "tag", "stag", "friend", "friends", "guest", "guests", "girls", "girl", "vip", "vips"]
            if msg not in valid:
                return await ctx.send("Please send A valid Option\nValid Options ARE: All, Reqrole, Custom, Official/Staff, Tag, Stag, Friend, Guest, Vip, Girl")
            if msg == "reqrole":
              msg = "role"
            if msg == "staff":
              msg = "official"
            if msg == "staffs":
              msg = "official"
            if msg == "officials":
              msg = "official"
            if msg == "friends":
              msg = "friend"
            if msg == "girl":
              msg = "girls"
            if msg == "vips":
              msg = "vip"
            if msg == "guests":
              msg = "guest"
            if msg == "all":
              query = f"SELECT * FROM  roles WHERE guild_id = ?"
              val = (ctx.guild.id,)
              with sqlite3.connect('./database.sqlite3') as db:
                db.row_factory = sqlite3.Row
                cursor = db.cursor()
                cursor.execute(query, val)
                welcome_db = cursor.fetchone()
              if welcome_db == 0:
                msg = msg.upper()
                return await ctx.send(f"{msg} Is Not set")
              else:
                cursor.execute(f"UPDATE roles SET role = 0 WHERE guild_id = {ctx.guild.id}")
                cursor.execute(f"UPDATE roles SET official = 0 WHERE guild_id = {ctx.guild.id}")
                sql1 = (f"UPDATE roles SET tag = ? WHERE guild_id = ?")
                val1 = (None, ctx.guild.id)
                cursor.execute(sql1, val1)
                sql1 = (f"UPDATE roles SET stag = ? WHERE guild_id = ?")
                val1 = (None, ctx.guild.id)
                cursor.execute(sql1, val1)
                cursor.execute(f"UPDATE roles SET friend = 0 WHERE guild_id = {ctx.guild.id}")
                cursor.execute(f"UPDATE roles SET guest = 0 WHERE guild_id = {ctx.guild.id}")
                cursor.execute(f"UPDATE roles SET vip = 0 WHERE guild_id = {ctx.guild.id}")
                cursor.execute(f"UPDATE roles SET girls = 0 WHERE guild_id = {ctx.guild.id}")
                cursor.execute(f"UPDATE roles SET ar = 0 WHERE guild_id = {ctx.guild.id}")
                sql1 = (f"UPDATE roles SET custom = ? WHERE guild_id = ?")
                val1 = ("{}", ctx.guild.id)
                cursor.execute(sql1, val1)
              db.commit()
              cursor.close()
              db.close()
              return await ctx.send(f"{ctx.author.mention} I Reset The Custom Role settings for : {ctx.guild.name}")
            query = f"SELECT {msg} FROM  roles WHERE guild_id = ?"
            val = (ctx.guild.id,)
            with sqlite3.connect('./database.sqlite3') as db:
              db.row_factory = sqlite3.Row
              cursor = db.cursor()
              cursor.execute(query, val)
              welcome_db = cursor.fetchone()
            if welcome_db == 0 or welcome_db is None:
              msg = msg.upper()
              return await ctx.send(f"{msg} Is Not set")
            else:
              if msg == "tag" or msg == "official"or msg == "stag" or msg == "custom":
                if msg == "tag":
                  sql1 = (f"UPDATE roles SET tag = ? WHERE guild_id = ?")
                  val1 = (None, ctx.guild.id)
                  cursor.execute(sql1, val1)
                  sql1 = (f"UPDATE roles SET ar = ? WHERE guild_id = ?")
                  val1 = (0, ctx.guild.id)
                  cursor.execute(sql1, val1)
                elif msg == "stag":
                  sql1 = (f"UPDATE roles SET stag = ? WHERE guild_id = ?")
                  val1 = (None, ctx.guild.id)
                  cursor.execute(sql1, val1)
                  sql1 = (f"UPDATE roles SET ar = ? WHERE guild_id = ?")
                  val1 = (0, ctx.guild.id)
                  cursor.execute(sql1, val1)
                elif msg == "official":
                  sql1 = (f"UPDATE roles SET tag = ? WHERE guild_id = ?")
                  val1 = (None, ctx.guild.id)
                  cursor.execute(sql1, val1)
                  sql1 = (f"UPDATE roles SET stag = ? WHERE guild_id = ?")
                  val1 = (None, ctx.guild.id)
                  cursor.execute(sql1, val1)
                  sql1 = (f"UPDATE roles SET ar = ? WHERE guild_id = ?")
                  val1 = (0, ctx.guild.id)
                  cursor.execute(sql1, val1)
                  sql1 = (f"UPDATE roles SET official = ? WHERE guild_id = ?")
                  val1 = (0, ctx.guild.id)
                  cursor.execute(sql1, val1)
                elif msg == "custom":
                  sql1 = (f"UPDATE roles SET custom = ? WHERE guild_id = ?")
                  val1 = ("{}", ctx.guild.id)
                  cursor.execute(sql1, val1)
              else:
                sql = (f"UPDATE roles SET {msg} = ? WHERE guild_id = ?")
                val = (0, ctx.guild.id)
                cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
            msg = msg.title()
            return await ctx.send(f"{ctx.author.mention} I Reset {msg} for : {ctx.guild.name}")

    @setup.command(name="config", description="Shows the current custom role settings for the server")
    @commands.has_permissions(administrator=True)
    async def config(self, ctx):
            query = "SELECT * FROM  roles WHERE guild_id = ?"
            val = (ctx.guild.id,)
            with sqlite3.connect('./database.sqlite3') as db:
              db.row_factory = sqlite3.Row
              cursor = db.cursor()
              cursor.execute(query, val)
              welcome_db = cursor.fetchone()
            if welcome_db is None:
              return await ctx.reply('First setup Your required role by Running `-setup reqrole @role/id`')
            reqrole = welcome_db['role']
            official = welcome_db['official']
            friend = welcome_db['friend']
            guest = welcome_db['guest']
            vip = welcome_db['vip']
            girl = welcome_db['girls']
            if welcome_db['stag'] is not None and welcome_db['tag'] is not None:
                tag = f"{welcome_db['tag']} or {welcome_db['stag']}"
                pass
            elif welcome_db['stag'] is None:
                tag = f"{welcome_db['tag']}"
                pass
            elif welcome_db['tag'] is None:
                tag = f"{welcome_db['stag']}"
                pass
            else:
                tag = None
            if reqrole == 0:
              rr = f"Required Role is not set"
            else:
              rr = f"<@&{reqrole}>"
            if official == 0:
              off = f"Official role is not set"
            else:
              if tag is None:
                off = f"<@&{official}>"
              else:
                off = f"<@&{official}> ({tag})"
            if friend == 0:
              fr = f"Friend Role is not set"
            else:
              fr = f"<@&{friend}>"
            if guest == 0:
              gu = f"Guest role is not set"
            else:
              gu = f"<@&{guest}>"
            if vip == 0:
              vi = f"Vip role is not set"
            else:
              vi = f"<@&{vip}>"
            if girl == 0:
              gir = f"Girl role is not set"
            else:
              gir = f"<@&{girl}>"
            embed = discord.Embed(title=f"Custom roles Settings For {ctx.guild.name}", color=0xc283fe)
            embed.add_field(name="Required Role:", value=rr)
            embed.add_field(name="Friend Role:", value=fr)
            embed.add_field(name="Official Role:", value=off)
            embed.add_field(name="Guest Role:", value=gu)
            embed.add_field(name="Vip Role:", value=vi)
            embed.add_field(name="Girl Role:", value=gir)
            c = await check_upgraded(ctx.guild.id)
            if c:
                ls = literal_eval(welcome_db['custom'])
                des = ""
                for i in ls:
                    r = discord.utils.get(ctx.guild.roles, id=ls[i])
                    if r is None:
                        ro = "Role was deleted"
                    else:
                        ro = r.mention
                    des+=f"{i.capitalize()}: {ro}\n"
                if des == "":
                    des = "No custom alias"
                embed.add_field(name="Custom Aliases", value=des, inline=False)
            await ctx.send(embed=embed)

    @setup.group(aliases=["requiredrole", "modrole"], description="Setups the required role for the server")
    @commands.has_permissions(administrator=True)
    async def reqrole(self, ctx, *,role: discord.Role):
            if ctx.guild.owner.id == ctx.author.id:
                pass
            else:
                if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 979353019235840000]:
                    em = discord.Embed(description=f"<:error:1153009680428318791>You must Have Higher Role than Bot To run This Command", color=0xff0000)
                    return await ctx.send(embed=em)

            query = "SELECT * FROM  roles WHERE guild_id = ?"
            val = (ctx.guild.id,)
            with sqlite3.connect('./database.sqlite3') as db:
              db.row_factory = sqlite3.Row
              cursor = db.cursor()
              cursor.execute(query, val)
              welcome_db = cursor.fetchone()

            if welcome_db is None:
              hm = [role.id]
              sql = (f"INSERT INTO roles(guild_id, role) VALUES(?, ?)")
              val = (ctx.guild.id, hm)
            else:
              sql = (f"UPDATE roles SET role = ? WHERE guild_id = ?")
              val = (role.id, ctx.guild.id)
              em = discord.Embed(description=f"Reqiured role role to run custom role commands is set to {role.mention}", color=0xc283fe)
              await ctx.reply(embed=em, mention_author=False)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

    @setup.command(name="tag", description="Setups the tag for the server")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def setup_tag(self, ctx, *, tag: str):
            if ctx.guild.owner.id == ctx.author.id:
                pass
            else:
                if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 979353019235840000]:
                    em = discord.Embed(description=f"<:error:1153009680428318791>You must Have Higher Role than Bot To run This Command", color=0xff0000)
                    return await ctx.send(embed=em)
            query = "SELECT tag, official, ar FROM  roles WHERE guild_id = ?"
            val = (ctx.guild.id,)
            with sqlite3.connect('./database.sqlite3') as db:
              db.row_factory = sqlite3.Row
              cursor = db.cursor()
              cursor.execute(query, val)
              welcome_db = cursor.fetchone()
            if welcome_db['official'] == 0:
              return await ctx.reply('First setup Your Staff/Official role by Running `-setup staff/official @role/id`')
            else:
                sql = (f"UPDATE roles SET tag = ? WHERE guild_id = ?")
                val = (tag, ctx.guild.id)
                cursor.execute(sql, val)
                view = OnOrOff(ctx)
                em = discord.Embed(description=f'Should there be an autorespond for "tag"', color=0xc283fe)
                test = await ctx.reply(embed=em, view=view, mention_author=False)
                await view.wait()
                if not view.value:
                    await test.delete()
                    return await ctx.reply(content="Timed out!", mention_author=False)
                if view.value == 'Yes':
                    await test.delete()
                    if welcome_db['ar'] == 0:
                        sql = (f"UPDATE roles SET ar = ? WHERE guild_id = ?")
                        val = (1, ctx.guild.id)
                        cursor.execute(sql, val)
                        em = discord.Embed(description=f"Tag setup successful with autoresponding on", color=0xc283fe)
                        await ctx.reply(embed=em, mention_author=False)
                    else:
                        em = discord.Embed(description=f"Tag setup successful with autoresponding on", color=0xc283fe)
                        await ctx.reply(embed=em, mention_author=False)
                if view.value == 'No':
                    await test.delete()
                    if welcome_db['ar'] == 1:
                        sql = (f"UPDATE roles SET ar = ? WHERE guild_id = ?")
                        val = (0, ctx.guild.id)
                        cursor.execute(sql, val)
                        em = discord.Embed(description=f"Tag setup successful with autoresponding off", color=0xc283fe)
                        await ctx.reply(embed=em, mention_author=False)
                    else:
                        em = discord.Embed(description=f"Tag setup successful with autoresponding off", color=0xc283fe)
                        await ctx.reply(embed=em, mention_author=False)
            db.commit()
            cursor.close()
            db.close()  

    @setup.command(name="stag", description="Setups the small tag for the server")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def setup_stag(self, ctx, *, tag: str):
            if ctx.guild.owner.id == ctx.author.id:
                pass
            else:
                if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 979353019235840000]:
                    em = discord.Embed(description=f"<:error:1153009680428318791>You must Have Higher Role than Bot To run This Command", color=0xff0000)
                    return await ctx.send(embed=em)
            query = "SELECT stag, official, ar FROM  roles WHERE guild_id = ?"
            val = (ctx.guild.id,)
            with sqlite3.connect('./database.sqlite3') as db:
              db.row_factory = sqlite3.Row
              cursor = db.cursor()
              cursor.execute(query, val)
              welcome_db = cursor.fetchone()
            if welcome_db['official'] == 0:
              return await ctx.reply('First setup Your Staff/Official role by Running `-setup staff/official @role/id`')
            else:
                sql = (f"UPDATE roles SET stag = ? WHERE guild_id = ?")
                val = (tag, ctx.guild.id)
                cursor.execute(sql, val)
                view = OnOrOff(ctx)
                em = discord.Embed(description=f'Should there be an autorespond for "tag"', color=0xc283fe)
                test = await ctx.reply(embed=em, view=view, mention_author=False)
                await view.wait()
                if not view.value:
                    await test.delete()
                    return await ctx.reply(content="Timed out!", mention_author=False)
                if view.value == 'Yes':
                    await test.delete()
                    if welcome_db['ar'] == 0:
                        sql = (f"UPDATE roles SET ar = ? WHERE guild_id = ?")
                        val = (1, ctx.guild.id)
                        cursor.execute(sql, val)
                        em = discord.Embed(description=f"Small Tag setup successful with autoresponding on", color=0xc283fe)
                        await ctx.reply(embed=em, mention_author=False)
                    else:
                        em = discord.Embed(description=f"Small Tag setup successful with autoresponding on", color=0xc283fe)
                        await ctx.reply(embed=em, mention_author=False)
                if view.value == 'No':
                    await test.delete()
                    if welcome_db['ar'] == 1:
                        sql = (f"UPDATE roles SET ar = ? WHERE guild_id = ?")
                        val = (0, ctx.guild.id)
                        cursor.execute(sql, val)
                        em = discord.Embed(description=f"Small Tag setup successful with autoresponding off", color=0xc283fe)
                        await ctx.reply(embed=em, mention_author=False)
                    else:
                        em = discord.Embed(description=f"Small Tag setup successful with autoresponding off", color=0xc283fe)
                        await ctx.reply(embed=em, mention_author=False)
            db.commit()
            cursor.close()
            db.close()
            
    @setup.command(name="create", aliases=['add'], description="To add alias for giving and taking specific roles")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def setup_create(self, ctx: commands.Context, alias, *, role: discord.Role):
        c = await check_upgraded(ctx.guild.id)
        if not c:
            em = discord.Embed(description=f"You just tried to execute a premium command but this guild is not upgarded\nYou can buy bot's premium from the link given below or by creating a ticket in the [Support Server](https://discord.gg/6Q9D7R8hYc)", color=0xc283fe).set_footer(text=f"{self.bot.user.name} Premium feature", icon_url=self.bot.user.avatar.url)
            v = discord.ui.View()
            v.add_item(discord.ui.Button(label="Patreon", url="https://www.patreon.com/gateway_bot"))
            v.add_item(discord.ui.Button(label="Support Server", url="https://discord.gg/6Q9D7R8hYc"))
            return await ctx.reply(embed=em, view=v)
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 979353019235840000]:
                em = discord.Embed(description=f"<:error:1153009680428318791>You must Have Higher Role than Bot To run This Command", color=0xff0000)
                return await ctx.send(embed=em)
        if role.position >= ctx.guild.me.top_role.position:
            em = discord.Embed(description=f"{role.mention} is above my top role, move my role above the {role.mention} and run the command again", color=0xff0000)
            return await ctx.reply(embed=em, mention_author=False)
        if not role.is_assignable():
            em = discord.Embed(description=f"{role.mention} can't be assigned to any user by the bot Please try again with different role.", color=0xff0000)
            return await ctx.reply(embed=em, mention_author=False)
        query = "SELECT custom, role FROM  roles WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            welcome_db = cursor.fetchone()
        if welcome_db['role'] == 0:
            return await ctx.reply('First setup Your required role by Running `-setup reqrole @role/id`')
        else:
            ls = literal_eval(welcome_db['custom'])
            if alias.lower() in ls:
                r = ls[alias.lower()]
                return await ctx.reply(embed=discord.Embed(description=f"There is already a custom alias with {alias} which is assigning {r.mention}", color=0xc283fe))
            elif self.bot.get_command(alias.lower()):
                return await ctx.reply(embed=discord.Embed(description=f"There is a bot command with {alias} try with any other alias", color=0xc283fe))
            else:
                ls[alias.lower()] = role.id
                sql = (f"UPDATE roles SET custom = ? WHERE guild_id = ?")
                val = (f"{ls}", ctx.guild.id)
            em = discord.Embed(description=f"Custom alias {alias.capitalize()} is set to {role.mention}\nJust type `{alias.lower()} <member>` to give or `r{alias.lower()} <member>` to take {role.mention}", color=0xc283fe)
            await ctx.reply(embed=em, mention_author=False)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
            
    @setup.command(name="delete", aliases=['remove'], description="To remove alias for giving and taking specific roles")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def setup_delete(self, ctx: commands.Context, alias):
        c = await check_upgraded(ctx.guild.id)
        if not c:
            em = discord.Embed(description=f"You just tried to execute a premium command but this guild is not upgarded\nYou can buy bot's premium from the link given below or by creating a ticket in the [Support Server](https://discord.gg/6Q9D7R8hYc)", color=0xc283fe).set_footer(text=f"{self.bot.user.name} Premium feature", icon_url=self.bot.user.avatar.url)
            v = discord.ui.View()
            v.add_item(discord.ui.Button(label="Patreon", url="https://www.patreon.com/gateway_bot"))
            v.add_item(discord.ui.Button(label="Support Server", url="https://discord.gg/6Q9D7R8hYc"))
            return await ctx.reply(embed=em, view=v)
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 979353019235840000]:
                em = discord.Embed(description=f"<:error:1153009680428318791>You must Have Higher Role than Bot To run This Command", color=0xff0000)
                return await ctx.send(embed=em)
        query = "SELECT custom, role FROM  roles WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            welcome_db = cursor.fetchone()
        if welcome_db['role'] == 0:
            return await ctx.reply('First setup Your required role by Running `-setup reqrole @role/id`')
        else:
            ls = literal_eval(welcome_db['custom'])
            if alias.lower() not in ls:
                r = ls[alias.lower()]
                return await ctx.reply(embed=discord.Embed(description=f"There is not a custom alias with {alias} which is assigning any role", color=0xc283fe))
            elif len(ls) >= 20:
                return await ctx.reply(embed=discord.Embed(description=f"Only 20 custom aliases can be added in the server", color=0xc283fe))
            else:
                del ls[alias.lower()]
                sql = (f"UPDATE roles SET custom = ? WHERE guild_id = ?")
                val = (f"{ls}", ctx.guild.id)
            em = discord.Embed(description=f"Custom alias {alias.capitalize()} is removed from assigning any role", color=0xc283fe)
            await ctx.reply(embed=em, mention_author=False)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

    @setup.command(name="staff", aliases=['staffs', 'official', 'officials'], description="Setups the staff role for the server")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def setup_staff(self, ctx, *,role: discord.Role):
            if ctx.guild.owner.id == ctx.author.id:
                pass
            else:
                if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 979353019235840000]:
                    em = discord.Embed(description=f"<:error:1153009680428318791>You must Have Higher Role than Bot To run This Command", color=0xff0000)
                    return await ctx.send(embed=em)
            if role.position >= ctx.guild.me.top_role.position:
                em = discord.Embed(description=f"{role.mention} is above my top role, move my role above the {role.mention} and run the command again", color=0xff0000)
                return await ctx.reply(embed=em, mention_author=False)
            if not role.is_assignable():
                em = discord.Embed(description=f"{role.mention} can't be assigned to any user by the bot Please try again with different role.", color=0xff0000)
                return await ctx.reply(embed=em, mention_author=False)
            query = "SELECT official, role FROM  roles WHERE guild_id = ?"
            val = (ctx.guild.id,)
            with sqlite3.connect('./database.sqlite3') as db:
              db.row_factory = sqlite3.Row
              cursor = db.cursor()
              cursor.execute(query, val)
              welcome_db = cursor.fetchone()
            if welcome_db['role'] == 0:
              return await ctx.reply('First setup Your required role by Running `-setup reqrole @role/id`')
            else:
              sql = (f"UPDATE roles SET official = ? WHERE guild_id = ?")
              val = (role.id, ctx.guild.id)
              em = discord.Embed(description=f"Official role is set to {role.mention}\nJust type `official <member>` to give or `rofficial <member>` to take {role.mention}", color=0xc283fe)
              await ctx.reply(embed=em, mention_author=False)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

    @setup.command(name="friend", aliases=['firends'], description="Setups the friend role for the server")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def setup_friend(self, ctx, *,role: discord.Role):
            if ctx.guild.owner.id == ctx.author.id:
                pass
            else:
                if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 979353019235840000]:
                    em = discord.Embed(description=f"<:error:1153009680428318791>You must Have Higher Role than Bot To run This Command", color=0xff0000)
                    return await ctx.send(embed=em)
            if role.position >= ctx.guild.me.top_role.position:
                em = discord.Embed(description=f"{role.mention} is above my top role, move my role above the {role.mention} and run the command again", color=0xff0000)
                return await ctx.reply(embed=em, mention_author=False)
            if not role.is_assignable():
                em = discord.Embed(description=f"{role.mention} can't be assigned to any user by the bot Please try again with different role.", color=0xff0000)
                return await ctx.reply(embed=em, mention_author=False)
            query = "SELECT friend, role FROM  roles WHERE guild_id = ?"
            val = (ctx.guild.id,)
            with sqlite3.connect('./database.sqlite3') as db:
              db.row_factory = sqlite3.Row
              cursor = db.cursor()
              cursor.execute(query, val)
              welcome_db = cursor.fetchone()
            if welcome_db['role'] == 0:
              return await ctx.reply('First setup Your required role by Running `-setup reqrole @role/id`')
            else:
              sql = (f"UPDATE roles SET friend = ? WHERE guild_id = ?")
              val = (role.id, ctx.guild.id)
              em = discord.Embed(description=f"Friend role is set to {role.mention}\nJust type `friend <member>` to give or `rfriend <member>` to take {role.mention}", color=0xc283fe)
              await ctx.reply(embed=em, mention_author=False)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

    @setup.command(name="vip", aliases=['vips'], description="Setups the vip role for the server")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def setup_vip(self, ctx, *,role: discord.Role):
            if ctx.guild.owner.id == ctx.author.id:
                pass
            else:
                if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 979353019235840000]:
                    em = discord.Embed(description=f"<:error:1153009680428318791>You must Have Higher Role than Bot To run This Command", color=0xff0000)
                    return await ctx.send(embed=em)
            if role.position >= ctx.guild.me.top_role.position:
                em = discord.Embed(description=f"{role.mention} is above my top role, move my role above the {role.mention} and run the command again", color=0xff0000)
                return await ctx.reply(embed=em, mention_author=False)
            if not role.is_assignable():
                em = discord.Embed(description=f"{role.mention} can't be assigned to any user by the bot Please try again with different role.", color=0xff0000)
                return await ctx.reply(embed=em, mention_author=False)
            query = "SELECT vip, role FROM  roles WHERE guild_id = ?"
            val = (ctx.guild.id,)
            with sqlite3.connect('./database.sqlite3') as db:
              db.row_factory = sqlite3.Row
              cursor = db.cursor()
              cursor.execute(query, val)
              welcome_db = cursor.fetchone()
            if welcome_db['role'] == 0:
              return await ctx.reply('First setup Your required role by Running `-setup reqrole @role/id`', mention_author=False)
            else:
              sql = (f"UPDATE roles SET vip = ? WHERE guild_id = ?")
              val = (role.id, ctx.guild.id)
              em = discord.Embed(description=f"Vip role is set to {role.mention}\nJust type `vip <member>` to give or `rvip <member>` to take {role.mention}", color=0xc283fe)
              await ctx.reply(embed=em, mention_author=False)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

    @setup.command(name="guest", aliases=['guests'], description="Setups the guest role for the server")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def setup_guest(self, ctx, *,role: discord.Role):
            if ctx.guild.owner.id == ctx.author.id:
                pass
            else:
                if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 979353019235840000]:
                    em = discord.Embed(description=f"<:error:1153009680428318791>You must Have Higher Role than Bot To run This Command", color=0xff0000)
                    return await ctx.send(embed=em)
            if role.position >= ctx.guild.me.top_role.position:
                em = discord.Embed(description=f"{role.mention} is above my top role, move my role above the {role.mention} and run the command again", color=0xff0000)
                return await ctx.reply(embed=em, mention_author=False)
            if not role.is_assignable():
                em = discord.Embed(description=f"{role.mention} can't be assigned to any user by the bot Please try again with different role.", color=0xff0000)
                return await ctx.reply(embed=em, mention_author=False)
            query = "SELECT guest, role FROM  roles WHERE guild_id = ?"
            val = (ctx.guild.id,)
            with sqlite3.connect('./database.sqlite3') as db:
              db.row_factory = sqlite3.Row
              cursor = db.cursor()
              cursor.execute(query, val)
              welcome_db = cursor.fetchone()
            if welcome_db['role'] == 0:
              return await ctx.reply('First setup Your required role by Running `-setup reqrole @role/id`')
            else:
              sql = (f"UPDATE roles SET guest = ? WHERE guild_id = ?")
              val = (role.id, ctx.guild.id)
              em = discord.Embed(description=f"Guest role is set to {role.mention}\nJust type `guest <member>` to give or `rguest <member>` to take {role.mention}", color=0xc283fe)
              await ctx.reply(embed=em, mention_author=False)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

    @setup.command(name="girl", aliases=['girls'], description="Setups the girl role for the server")
    @commands.bot_has_guild_permissions(manage_roles=True)
    @commands.has_permissions(administrator=True)
    async def setup_girl(self, ctx, *,role: discord.Role):
            if ctx.guild.owner.id == ctx.author.id:
                pass
            else:
                if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 979353019235840000]:
                    em = discord.Embed(description=f"<:error:1153009680428318791>You must Have Higher Role than Bot To run This Command", color=0xff0000)
                    return await ctx.send(embed=em)
            if role.position >= ctx.guild.me.top_role.position:
                em = discord.Embed(description=f"{role.mention} is above my top role, move my role above the {role.mention} and run the command again", color=0xff0000)
                return await ctx.reply(embed=em, mention_author=False)
            if not role.is_assignable():
                em = discord.Embed(description=f"{role.mention} can't be assigned to any user by the bot Please try again with different role.", color=0xff0000)
                return await ctx.reply(embed=em, mention_author=False)
            query = "SELECT girls, role FROM  roles WHERE guild_id = ?"
            val = (ctx.guild.id,)
            with sqlite3.connect('./database.sqlite3') as db:
              db.row_factory = sqlite3.Row
              cursor = db.cursor()
              cursor.execute(query, val)
              welcome_db = cursor.fetchone()
            if welcome_db['role'] == 0:
              return await ctx.reply('First setup Your required role by Running `-setup reqrole @role/id`')
            if welcome_db['girls'] is not None:
              sql = (f"UPDATE roles SET girls = ? WHERE guild_id = ?")
              val = (role.id, ctx.guild.id)
              em = discord.Embed(description=f"Girl role is set to {role.mention}\nJust type `girl <member>` to give or `rgirl <member>` to take {role.mention}", color=0xc283fe)
              await ctx.reply(embed=em, mention_author=False)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

    @commands.command(name="staff", aliases=['staffs', 'official', 'officials'], description="Gives the staff role to the user")
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def _staff(self, ctx, user: discord.Member):
            if user.id == ctx.author.id:
                return await ctx.reply("You cant change your own roles")
            query = "SELECT role, official FROM  roles WHERE guild_id = ?"
            val = (ctx.guild.id,)
            with sqlite3.connect('./database.sqlite3') as db:
              db.row_factory = sqlite3.Row
              cursor = db.cursor()
              cursor.execute(query, val)
              welcome_db = cursor.fetchone()
            if welcome_db['official'] == 0:
                em = discord.Embed(description=f"<:error:1153009680428318791>Official Role Is Not Set.", color=0xff0000)
                return await ctx.send(embed=em)
            RRole = discord.utils.get(ctx.guild.roles, id=welcome_db['role'])
            if ctx.guild.owner.id == ctx.author.id:
                pass
            else:
                if RRole not in ctx.author.roles:
                  em = discord.Embed(description=f"<:error:1153009680428318791>You need {RRole.mention} role to use this command.", color=0xff0000)
                  return await ctx.send(embed=em)
            Role = discord.utils.get(ctx.guild.roles, id=welcome_db['official'])
            if Role.position >= ctx.guild.me.top_role.position:
                  em = discord.Embed(description=f"<:error:1153009680428318791>{Role.mention} is above my top role.", color=0xff0000)
                  return await ctx.send(embed=em)
            if Role in user.roles:
                await user.remove_roles(Role)
                em=discord.Embed(description=f"<:ticky:1154027584020021278> Successfully Removed {Role.mention} from {user.mention}", color=ctx.author.color)
                return await ctx.send(embed=em)
            await user.add_roles(Role)
            em=discord.Embed(description=f"<:ticky:1154027584020021278> Successfully Given {Role.mention} to {user.mention}", color=ctx.author.color)
            await ctx.send(embed=em)

    @commands.command(name="friend", aliases=['friends'], description="Gives the friend role to the user")
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def _friend(self, ctx, user: discord.Member):
            if user.id == ctx.author.id:
                return await ctx.reply("You cant change your own roles")
            query = "SELECT role, friend FROM  roles WHERE guild_id = ?"
            val = (ctx.guild.id,)
            with sqlite3.connect('./database.sqlite3') as db:
              db.row_factory = sqlite3.Row
              cursor = db.cursor()
              cursor.execute(query, val)
              welcome_db = cursor.fetchone()
            if welcome_db['friend'] == 0:
                em = discord.Embed(description=f"<:error:1153009680428318791>Friend Role Is Not Set.", color=0xff0000)
                return await ctx.send(embed=em)
            RRole = discord.utils.get(ctx.guild.roles, id=welcome_db['role'])
            if ctx.guild.owner.id == ctx.author.id:
                pass
            else:
                if RRole not in ctx.author.roles:
                  em = discord.Embed(description=f"<:error:1153009680428318791>You need {RRole.mention} role to use this command.", color=0xff0000)
                  return await ctx.send(embed=em)
            Role = discord.utils.get(ctx.guild.roles, id=welcome_db['friend'])
            if Role.position >= ctx.guild.me.top_role.position:
                  em = discord.Embed(description=f"<:error:1153009680428318791>{Role.mention} is above my top role.", color=0xff0000)
                  return await ctx.send(embed=em)
            if Role in user.roles:
                await user.remove_roles(Role)
                em=discord.Embed(description=f"<:ticky:1154027584020021278> Successfully Removed {Role.mention} from {user.mention}", color=ctx.author.color)
                return await ctx.send(embed=em)
            await user.add_roles(Role)
            em=discord.Embed(description=f"<:ticky:1154027584020021278> Successfully Given {Role.mention} to {user.mention}", color=ctx.author.color)
            await ctx.send(embed=em)

    @commands.command(name="vip", aliases=['vips'], description="Gives vip role to the user")
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def _vip(self, ctx, user: discord.Member):
            if user.id == ctx.author.id:
                return await ctx.reply("You cant change your own roles")
            query = "SELECT role, vip FROM  roles WHERE guild_id = ?"
            val = (ctx.guild.id,)
            with sqlite3.connect('./database.sqlite3') as db:
              db.row_factory = sqlite3.Row
              cursor = db.cursor()
              cursor.execute(query, val)
              welcome_db = cursor.fetchone()
            if welcome_db['vip'] == 0:
                em = discord.Embed(description=f"<:error:1153009680428318791>Vip Role Is Not Set.", color=0xff0000)
                return await ctx.send(embed=em)
            RRole = discord.utils.get(ctx.guild.roles, id=welcome_db['role'])
            if ctx.guild.owner.id == ctx.author.id:
                pass
            else:
                if RRole not in ctx.author.roles:
                  em = discord.Embed(description=f"<:error:1153009680428318791>You need {RRole.mention} role to use this command.", color=0xff0000)
                  return await ctx.send(embed=em)
            Role = discord.utils.get(ctx.guild.roles, id=welcome_db['vip'])
            if Role.position >= ctx.guild.me.top_role.position:
                  em = discord.Embed(description=f"<:error:1153009680428318791>{Role.mention} is above my top role.", color=0xff0000)
                  return await ctx.send(embed=em)
            if Role in user.roles:
                await user.remove_roles(Role)
                em=discord.Embed(description=f"<:ticky:1154027584020021278> Successfully Removed {Role.mention} from {user.mention}", color=ctx.author.color)
                return await ctx.send(embed=em)
            await user.add_roles(Role)
            em=discord.Embed(description=f"<:ticky:1154027584020021278> Successfully Given {Role.mention} to {user.mention}", color=ctx.author.color)
            await ctx.send(embed=em)

    @commands.command(name="guest", aliases=['guests'], description="Gives guest role to the user")
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def _guest(self, ctx, user: discord.Member):
            if user.id == ctx.author.id:
                return await ctx.reply("You cant change your own roles")
            query = "SELECT role, guest FROM  roles WHERE guild_id = ?"
            val = (ctx.guild.id,)
            with sqlite3.connect('./database.sqlite3') as db:
              db.row_factory = sqlite3.Row
              cursor = db.cursor()
              cursor.execute(query, val)
              welcome_db = cursor.fetchone()
            if welcome_db['guest'] == 0:
                em = discord.Embed(description=f"<:error:1153009680428318791>Guest Role Is Not Set.", color=0xff0000)
                return await ctx.send(embed=em)
            RRole = discord.utils.get(ctx.guild.roles, id=welcome_db['role'])
            if ctx.guild.owner.id == ctx.author.id:
                pass
            else:
                if RRole not in ctx.author.roles:
                  em = discord.Embed(description=f"<:error:1153009680428318791>You need {RRole.mention} role to use this command.", color=0xff0000)
                  return await ctx.send(embed=em)
            Role = discord.utils.get(ctx.guild.roles, id=welcome_db['guest'])
            if Role.position >= ctx.guild.me.top_role.position:
                  em = discord.Embed(description=f"<:error:1153009680428318791>{Role.mention} is above my top role.", color=0xff0000)
                  return await ctx.send(embed=em)
            if Role in user.roles:
                await user.remove_roles(Role)
                em=discord.Embed(description=f"<:ticky:1154027584020021278> Successfully Removed {Role.mention} from {user.mention}", color=ctx.author.color)
                return await ctx.send(embed=em)
            await user.add_roles(Role)
            em=discord.Embed(description=f"<:ticky:1154027584020021278> Successfully Given {Role.mention} to {user.mention}", color=ctx.author.color)
            await ctx.send(embed=em)

    @commands.command(name="girl", aliases=['girls'], description="Gives girl role to the user")
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def _girls(self, ctx, user: discord.Member):
            if user.id == ctx.author.id:
                return await ctx.reply("You cant change your own roles")
            query = "SELECT role, girls FROM  roles WHERE guild_id = ?"
            val = (ctx.guild.id,)
            with sqlite3.connect('./database.sqlite3') as db:
              db.row_factory = sqlite3.Row
              cursor = db.cursor()
              cursor.execute(query, val)
              welcome_db = cursor.fetchone()
            if welcome_db['girls'] == 0:
                em = discord.Embed(description=f"<:error:1153009680428318791>Girl Role Is Not Set.", color=0xff0000)
                return await ctx.send(embed=em)
            RRole = discord.utils.get(ctx.guild.roles, id=welcome_db['role'])
            if ctx.guild.owner.id == ctx.author.id:
                pass
            else:
                if RRole not in ctx.author.roles:
                  em = discord.Embed(description=f"<:error:1153009680428318791>You need {RRole.mention} role to use this command.", color=0xff0000)
                  return await ctx.send(embed=em)
            Role = discord.utils.get(ctx.guild.roles, id=welcome_db['girls'])
            if Role.position >= ctx.guild.me.top_role.position:
                  em = discord.Embed(description=f"<:error:1153009680428318791>{Role.mention} is above my top role.", color=0xff0000)
                  return await ctx.send(embed=em)
            if Role in user.roles:
                await user.remove_roles(Role)
                em=discord.Embed(description=f"<:ticky:1154027584020021278> Successfully Removed {Role.mention} from {user.mention}", color=ctx.author.color)
                return await ctx.send(embed=em)
            await user.add_roles(Role)
            em=discord.Embed(description=f"<:ticky:1154027584020021278> Successfully Given {Role.mention} to {user.mention}", color=ctx.author.color)
            await ctx.send(embed=em)

    @commands.command(aliases=['rstaffs', 'rofficial', 'rofficials'], description="Removes the staff role from the user")
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def rstaff(self, ctx, user: discord.Member):
            if user.id == ctx.author.id:
                return await ctx.reply("You cant change your own roles")
            query = "SELECT role, official FROM  roles WHERE guild_id = ?"
            val = (ctx.guild.id,)
            with sqlite3.connect('./database.sqlite3') as db:
              db.row_factory = sqlite3.Row
              cursor = db.cursor()
              cursor.execute(query, val)
              welcome_db = cursor.fetchone()
            if welcome_db['official'] == 0:
                em = discord.Embed(description=f"<:error:1153009680428318791>Official Role Is Not Set.", color=0xff0000)
                return await ctx.send(embed=em)
            RRole = discord.utils.get(ctx.guild.roles, id=welcome_db['role'])
            if ctx.guild.owner.id == ctx.author.id:
                pass
            else:
                if RRole not in ctx.author.roles:
                  em = discord.Embed(description=f"<:error:1153009680428318791>You need {RRole.mention} role to use this command.", color=0xff0000)
                  return await ctx.send(embed=em)
            Role = discord.utils.get(ctx.guild.roles, id=welcome_db['official'])
            if Role.position >= ctx.guild.me.top_role.position:
                  em = discord.Embed(description=f"<:error:1153009680428318791>{Role.mention} is above my top role.", color=0xff0000)
                  return await ctx.send(embed=em)
            await user.remove_roles(Role)
            em=discord.Embed(description=f"<:ticky:1154027584020021278> Successfully Removed {Role.mention} from {user.mention}", color=ctx.author.color)
            await ctx.send(embed=em)

    @commands.command(aliases=['rfriends'], description="Removes the friend role from the user")
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def rfriend(self, ctx, user: discord.Member):
            if user.id == ctx.author.id:
                return await ctx.reply("You cant change your own roles")
            query = "SELECT role, friend FROM  roles WHERE guild_id = ?"
            val = (ctx.guild.id,)
            with sqlite3.connect('./database.sqlite3') as db:
              db.row_factory = sqlite3.Row
              cursor = db.cursor()
              cursor.execute(query, val)
              welcome_db = cursor.fetchone()
            if welcome_db['friend'] == 0:
                em = discord.Embed(description=f"<:error:1153009680428318791>Official Role Is Not Set.", color=0xff0000)
                return await ctx.send(embed=em)
            RRole = discord.utils.get(ctx.guild.roles, id=welcome_db['role'])
            if ctx.guild.owner.id == ctx.author.id:
                pass
            else:
                if RRole not in ctx.author.roles:
                  em = discord.Embed(description=f"<:error:1153009680428318791>You need {RRole.mention} role to use this command.", color=0xff0000)
                  return await ctx.send(embed=em)
            Role = discord.utils.get(ctx.guild.roles, id=welcome_db['friend'])
            if Role.position >= ctx.guild.me.top_role.position:
                  em = discord.Embed(description=f"<:error:1153009680428318791>{Role.mention} is above my top role.", color=0xff0000)
                  return await ctx.send(embed=em)
            await user.remove_roles(Role)
            em=discord.Embed(description=f"<:ticky:1154027584020021278> Successfully Removed {Role.mention} from {user.mention}", color=ctx.author.color)
            await ctx.send(embed=em)
            
    @commands.command(aliases=["rvips"], description="Removes the vip role from the user")
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def rvip(self, ctx, user: discord.Member):
            if user.id == ctx.author.id:
                return await ctx.reply("You cant change your own roles")
            query = "SELECT role, vip FROM  roles WHERE guild_id = ?"
            val = (ctx.guild.id,)
            with sqlite3.connect('./database.sqlite3') as db:
              db.row_factory = sqlite3.Row
              cursor = db.cursor()
              cursor.execute(query, val)
              welcome_db = cursor.fetchone()
            if welcome_db['vip'] == 0:
                em = discord.Embed(description=f"<:error:1153009680428318791>Vip Role Is Not Set.", color=0xff0000)
                return await ctx.send(embed=em)
            RRole = discord.utils.get(ctx.guild.roles, id=welcome_db['role'])
            if ctx.guild.owner.id == ctx.author.id:
                pass
            else:
                if RRole not in ctx.author.roles:
                  em = discord.Embed(description=f"<:error:1153009680428318791>You need {RRole.mention} role to use this command.", color=0xff0000)
                  return await ctx.send(embed=em)
            Role = discord.utils.get(ctx.guild.roles, id=welcome_db['vip'])
            if Role.position >= ctx.guild.me.top_role.position:
                  em = discord.Embed(description=f"<:error:1153009680428318791>{Role.mention} is above my top role.", color=0xff0000)
                  return await ctx.send(embed=em)
            await user.remove_roles(Role)
            em=discord.Embed(description=f"<:ticky:1154027584020021278> Successfully Removed {Role.mention} from {user.mention}", color=ctx.author.color)
            await ctx.send(embed=em)

    @commands.command(aliases=["rguests"], description="Removes the guest role from the user")
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def rguest(self, ctx, user: discord.Member):
            if user.id == ctx.author.id:
                return await ctx.reply("You cant change your own roles")
            query = "SELECT role, guest FROM  roles WHERE guild_id = ?"
            val = (ctx.guild.id,)
            with sqlite3.connect('./database.sqlite3') as db:
              db.row_factory = sqlite3.Row
              cursor = db.cursor()
              cursor.execute(query, val)
              welcome_db = cursor.fetchone()
            if welcome_db['guest'] == 0:
                em = discord.Embed(description=f"<:error:1153009680428318791>Guest Role Is Not Set.", color=0xff0000)
                return await ctx.send(embed=em)
            RRole = discord.utils.get(ctx.guild.roles, id=welcome_db['role'])
            if ctx.guild.owner.id == ctx.author.id:
                pass
            else:
                if RRole not in ctx.author.roles:
                  em = discord.Embed(description=f"<:error:1153009680428318791>You need {RRole.mention} role to use this command.", color=0xff0000)
                  return await ctx.send(embed=em)
            Role = discord.utils.get(ctx.guild.roles, id=welcome_db['guest'])
            if Role.position >= ctx.guild.me.top_role.position:
                  em = discord.Embed(description=f"<:error:1153009680428318791>{Role.mention} is above my top role.", color=0xff0000)
                  return await ctx.send(embed=em)
            await user.remove_roles(Role)
            em=discord.Embed(description=f"<:ticky:1154027584020021278> Successfully Removed {Role.mention} from {user.mention}", color=ctx.author.color)
            await ctx.send(embed=em)

    @commands.command(aliases=["rgirls"], description="Removes the girls role from the user")
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def rgirl(self, ctx, user: discord.Member):
            if user.id == ctx.author.id:
                return await ctx.reply("You cant change your own roles")
            query = "SELECT role, girls FROM  roles WHERE guild_id = ?"
            val = (ctx.guild.id,)
            with sqlite3.connect('./database.sqlite3') as db:
              db.row_factory = sqlite3.Row
              cursor = db.cursor()
              cursor.execute(query, val)
              welcome_db = cursor.fetchone()
            if welcome_db['girls'] == 0:
                em = discord.Embed(description=f"<:error:1153009680428318791>Girl Role Is Not Set.", color=0xff0000)
                return await ctx.send(embed=em)
            RRole = discord.utils.get(ctx.guild.roles, id=welcome_db['role'])
            if ctx.guild.owner.id == ctx.author.id:
                pass
            else:
                if RRole not in ctx.author.roles:
                  em = discord.Embed(description=f"<:error:1153009680428318791>You need {RRole.mention} role to use this command.", color=0xff0000)
                  return await ctx.send(embed=em)
            Role = discord.utils.get(ctx.guild.roles, id=welcome_db['girls'])
            if Role.position >= ctx.guild.me.top_role.position:
                  em = discord.Embed(description=f"<:error:1153009680428318791>{Role.mention} is above my top role.", color=0xff0000)
                  return await ctx.send(embed=em)
            await user.remove_roles(Role)
            em=discord.Embed(description=f"<:ticky:1154027584020021278> Successfully Removed {Role.mention} from {user.mention}", color=ctx.author.color)
            await ctx.send(embed=em)
    
    @commands.command()
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def applied(self, ctx):
            query = "SELECT * FROM  roles WHERE guild_id = ?"
            val = (ctx.guild.id,)
            with sqlite3.connect('./database.sqlite3') as db:
              db.row_factory = sqlite3.Row
              cursor = db.cursor()
              cursor.execute(query, val)
              welcome_db = cursor.fetchone()
            if welcome_db['official'] == 0:
                em = discord.Embed(description=f"<:error:1153009680428318791>Official Role Is Not Set.", color=0xff0000)
                return await ctx.send(embed=em)
            if welcome_db['tag'] is None and welcome_db['stag'] is None:
                em = discord.Embed(description=f"<:error:1153009680428318791>Tag Is Not Set.", color=0xff0000)
                return await ctx.send(embed=em)
            check = False
            if welcome_db['tag'] is not None:
                if welcome_db['stag'] is None:
                    if welcome_db['tag'] not in ctx.author.name:
                        check = True
                else:
                    if welcome_db['stag'] not in ctx.author.name and welcome_db['tag'] not in ctx.author.name:
                        check = True
            elif welcome_db['stag'] is not None:
                if welcome_db['tag'] is None:
                    if welcome_db['stag'] not in ctx.author.name:
                        check = True
                else:
                    if welcome_db['stag'] not in ctx.author.name and welcome_db['tag'] not in ctx.author.name:
                        check = True
            else:
                pass
            if check:
                if welcome_db['stag'] is not None and welcome_db['tag'] is not None:
                    tag = f"'{welcome_db['tag']}' or '{welcome_db['stag']}'"
                    pass
                elif welcome_db['stag'] is None:
                    tag = f"'{welcome_db['tag']}'"
                    pass
                elif welcome_db['tag'] is None:
                    tag = f"'{welcome_db['stag']}'"
                    pass
                else:
                    tag = None
                return await ctx.reply(f"First apply {tag} in username to get official role")
            Role = discord.utils.get(ctx.guild.roles, id=welcome_db['official'])
            if Role in ctx.author.roles:
                em=discord.Embed(description=f"You already have {Role.mention}", color=ctx.author.color)
                return await ctx.send(embed=em)
            if Role.position >= ctx.guild.me.top_role.position:
                  em = discord.Embed(description=f"<:error:1153009680428318791>{Role.mention} is above my top role.", color=0xff0000)
                  return await ctx.send(embed=em)
            await ctx.author.add_roles(Role)
            em=discord.Embed(description=f"<:ticky:1154027584020021278> Successfully Given {Role.mention}", color=ctx.author.color)
            await ctx.send(embed=em)


    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        await self.bot.wait_until_ready()
        if message.guild is None:
            return
        ctx = await self.bot.get_context(message)
        if isinstance(message.channel, discord.DMChannel):
            return
        if not message.guild.me.guild_permissions.read_messages:
            return
        if not message.guild.me.guild_permissions.read_message_history:
            return
        if not message.guild.me.guild_permissions.view_channel:
            return
        if not message.guild.me.guild_permissions.send_messages:
            return
        query = "SELECT * FROM  roles WHERE guild_id = ?"
        val = (message.guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            welcome_db = cursor.fetchone()
        content = ""
        if welcome_db is not None:
            tag = welcome_db['tag']
            stag = welcome_db['stag']
            official = welcome_db['official']
            ls = literal_eval(welcome_db['custom'])
            content = message.content.lower()
        else:
            return
        c = await check_upgraded(message.guild.id)
        if message.guild.me.guild_permissions.manage_roles:
            if not c:
                pass
            else:
                query1 = "SELECT * FROM  ignore WHERE guild_id = ?"
                val1 = (message.guild.id,)
                with sqlite3.connect('database.sqlite3') as db1:
                    db1.row_factory = sqlite3.Row
                    cursor1 = db1.cursor()
                    cursor1.execute(query1, val1)
                    ig_db = cursor1.fetchone()
                if ig_db is not None:
                    xd = literal_eval(ig_db['user'])
                    if message.author.id in xd:
                        return
                    xdd = literal_eval(ig_db['channel'])
                    c_channel = await by_channel(ctx, message.author, message.channel)
                    if message.channel.id in xdd and not c_channel:
                        return
                    xddd = literal_eval(ig_db['role'])
                    oke = discord.utils.get(message.guild.members, id=message.author.id)
                    if oke is not None:
                        for i in message.author.roles:
                            if i.id in xddd:
                                c_role = await by_role(ctx, message.author, i)
                                if not c_role:
                                    return
                pre = await get_prefix(message)
                check = False
                for k in pre:
                    if content.startswith(k):
                        content = content.replace(k, "").strip()
                        check = True
                        prefix = k
                for i in ls:
                    if content.startswith(i) and check:
                        u = None
                        for j in message.mentions:
                            if j.bot:
                                continue
                            else:
                                u = j
                                break
                        if u is None:
                            xx = message.guild.get_member(int(content.replace(i, "").strip()))
                            if xx is None:
                                em = discord.Embed(description=f"<:error:1153009680428318791>You forgot to mention the user argument.\nDo it like: `{prefix}{i} <user>`", color=0xff0000)
                                return await ctx.reply(embed=em, delete_after=7)
                            u = xx
                        if u.id == message.author.id:
                            em = discord.Embed(description=f"<:error:1153009680428318791>You cant change your own roles", color=0xff0000)
                            return await ctx.reply(embed=em, delete_after=7)
                        else:
                            r = discord.utils.get(message.guild.roles, id=welcome_db['role'])
                            if r is None:
                                pass
                            else:
                                if r not in message.author.roles:
                                    em = discord.Embed(description=f"<:error:1153009680428318791>You need {r.mention} role to use this command.", color=0xff0000)
                                    return await ctx.reply(embed=em)
                                Role = discord.utils.get(ctx.guild.roles, id=ls[i])
                                if Role.position >= ctx.guild.me.top_role.position:
                                    em = discord.Embed(description=f"<:error:1153009680428318791>{Role.mention} is above my top role.", color=0xff0000)
                                    return await ctx.reply(embed=em)
                                if Role in u.roles:
                                    await u.remove_roles(Role)
                                    em=discord.Embed(description=f"<:ticky:1154027584020021278> Successfully Removed {Role.mention} from {u.mention}", color=ctx.author.color)
                                    return await ctx.reply(embed=em)
                                else:
                                    await u.add_roles(Role)
                                    em=discord.Embed(description=f"<:ticky:1154027584020021278> Successfully Given {Role.mention} to {u.mention}", color=ctx.author.color)
                                    return await ctx.reply(embed=em)
        if content == "tag" or content == "stag":
            if welcome_db['ar'] == 0:
                return
            with sqlite3.connect('database.sqlite3') as db:
                db.row_factory = sqlite3.Row
                cursor = db.cursor()
                cursor.execute(f"SELECT * FROM prefixes WHERE guild_id = {message.guild.id}")
                res = cursor.fetchone()
            prefix = res["prefix"]
            if welcome_db['stag'] is not None and welcome_db['tag'] is not None:
                tg = f"'{welcome_db['tag']}' or '{welcome_db['stag']}'"
                pass
            elif welcome_db['stag'] is None:
                tg = f"'{welcome_db['tag']}'"
                pass
            elif welcome_db['tag'] is None:
                tg = f"'{welcome_db['stag']}'"
                pass
            else:
                tg = None
            return await message.channel.send(embed=discord.Embed(description=f"Tag for becoming official/staff of the server is: {tg} \nAfter applying tag in username just write `{prefix}applied` to get <@&{official}> role", color=0xc283fe), delete_after=60)

async def setup(bot):
    await bot.add_cog(extra(bot))
