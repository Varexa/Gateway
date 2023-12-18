from ast import literal_eval
from cmath import e
from glob import iglob
import discord
from discord.ext import commands
from discord import Webhook
from typing import Union, Optional
import re
import sqlite3
import asyncio
from collections import Counter
import aiohttp
import datetime
import requests
import random
from io import BytesIO
from botinfo import *
from paginators import PaginationView, PaginatorView
from cogs.premium import check_upgraded
import matplotlib

def getigdata(guild_id):
    query = "SELECT * FROM  ignore WHERE guild_id = ?"
    val = (guild_id,)
    with sqlite3.connect('database.sqlite3') as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        cursor.execute(query, val)
        ig_db = cursor.fetchone()
    return ig_db

def getbydata(guild_id):
    query = "SELECT * FROM  bypass WHERE guild_id = ?"
    val = (guild_id,)
    with sqlite3.connect('database.sqlite3') as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        cursor.execute(query, val)
        ig_db = cursor.fetchone()
    return ig_db

class roledropdownmenu(discord.ui.Select):
    def __init__(self, ctx: commands.Context, opt: list, user: Union[discord.Member, discord.Role, discord.TextChannel]):
        options = []
        for i in opt:
            c = discord.utils.get(ctx.guild.roles, id=i)
            options.append(discord.SelectOption(label=f"{c.name}", value=c.id))
        if len(opt) == 0:
            super().__init__(placeholder="Select the roles to bypass",
                min_values=1,
                max_values=1,
                options=[discord.SelectOption(label=f"Gateway", value="Gateway")],
                disabled=True
            )
        else:
            super().__init__(placeholder="Select the roles to bypass",
                min_values=1,
                max_values=len(opt),
                options=options,
                disabled=False
            )
        self.ctx = ctx
        self.user = user
        self.opt = opt

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False, thinking=False)
        guild = self.ctx.guild
        query = "SELECT * FROM  bypass WHERE guild_id = ?"
        val = (guild.id,)
        with sqlite3.connect('database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            ig_db = cursor.fetchone()
        if ig_db is None:
            xd = {}
            xd[self.user.id] = {}
            xd[self.user.id]['role'] = [i for i in self.values]
            
            if isinstance(self.user, discord.Member):
                sql = f"INSERT INTO bypass(guild_id, bypass_users) VALUES(?, ?)"
            if isinstance(self.user, discord.Role):
                sql = f"INSERT INTO bypass(guild_id, bypass_roles) VALUES(?, ?)"
            if isinstance(self.user, discord.TextChannel):
                sql = f"INSERT INTO bypass(guild_id, bypass_channels) VALUES(?, ?)"
            val = (guild.id, f"{xd}")
            cursor.execute(sql, val)
        else:
            if isinstance(self.user, discord.Member):
                xd = literal_eval(ig_db['bypass_users'])
            if isinstance(self.user, discord.Role):
                xd = literal_eval(ig_db['bypass_roles'])
            if isinstance(self.user, discord.TextChannel):
                xd = literal_eval(ig_db['bypass_channels'])
            if self.user.id in xd:
                if 'role' in xd[self.user.id]:
                    ls = xd[self.user.id]['role']
                    for i in self.values:
                        ls.append(i)
                    xd[self.user.id]['role'] = ls
                else:
                    xd[self.user.id]['role'] = [i for i in self.values]
            else:
                xd[self.user.id] = {}
                xd[self.user.id]['role'] = [i for i in self.values]
            if isinstance(self.user, discord.Member):
                sql = (f"UPDATE bypass SET 'bypass_users' = ? WHERE guild_id = ?")
            if isinstance(self.user, discord.Role):
                sql = (f"UPDATE bypass SET 'bypass_roles' = ? WHERE guild_id = ?")
            if isinstance(self.user, discord.TextChannel):
                sql = (f"UPDATE bypass SET 'bypass_channels' = ? WHERE guild_id = ?")
            val = (f"{xd}", guild.id)
            cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        ls = []
        for i in self.values:
            c = discord.utils.get(self.ctx.guild.roles, id=i)
            ls.append(c.mention)
        em = discord.Embed(description=f"Successfully allowed {self.user.mention} to bypass `{', '.join(ls)}` roles", color=0xc283fe).set_footer(text=self.ctx.guild.me.name, icon_url=self.ctx.guild.me.avatar.url)
        await interaction.edit_original_response(embed=em, view=None)

class rolemenuview(discord.ui.View):
    def __init__(self, ctx: commands.Context, opt: list, user: Union[discord.Member, discord.Role, discord.TextChannel]):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.user = user
        self.add_item(channeldropdownmenu(self.ctx, opt, user))
    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and interaction.user.id not in  [978930369392951366, 979353019235840000]:
            await interaction.response.send_message(f"Um, Looks like you are not the author of the command...", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="Bypass All Ignored roles", custom_id='all', style=discord.ButtonStyle.blurple)
    async def okkkkkk(self, interaction: discord.Interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        guild = self.ctx.guild
        query = "SELECT * FROM  bypass WHERE guild_id = ?"
        val = (guild.id,)
        with sqlite3.connect('database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            ig_db = cursor.fetchone()
        if ig_db is None:
            xd = {}
            xd[self.user.id] = {}
            xd[self.user.id]['role'] = "all"
            
            if isinstance(self.user, discord.Member):
                sql = f"INSERT INTO bypass(guild_id, bypass_users) VALUES(?, ?)"
            if isinstance(self.user, discord.Role):
                sql = f"INSERT INTO bypass(guild_id, bypass_roles) VALUES(?, ?)"
            if isinstance(self.user, discord.TextChannel):
                sql = f"INSERT INTO bypass(guild_id, bypass_channels) VALUES(?, ?)"
            val = (guild.id, f"{xd}")
            cursor.execute(sql, val)
        else:
            if isinstance(self.user, discord.Member):
                xd = literal_eval(ig_db['bypass_users'])
            if isinstance(self.user, discord.Role):
                xd = literal_eval(ig_db['bypass_roles'])
            if isinstance(self.user, discord.TextChannel):
                xd = literal_eval(ig_db['bypass_channels'])
            if self.user.id in xd:
                xd[self.user.id]['role'] = "all"
            else:
                xd[self.user.id] = {}
                xd[self.user.id]['role'] = "all"
            
            if isinstance(self.user, discord.Member):
                sql = (f"UPDATE bypass SET 'bypass_users' = ? WHERE guild_id = ?")
            if isinstance(self.user, discord.Role):
                sql = (f"UPDATE bypass SET 'bypass_roles' = ? WHERE guild_id = ?")
            if isinstance(self.user, discord.TextChannel):
                sql = (f"UPDATE bypass SET 'bypass_channels' = ? WHERE guild_id = ?")
            val = (f"{xd}", guild.id)
            cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        em = discord.Embed(description=f"Successfully allowed {self.user.mention} to bypass all ignored roles", color=0xc283fe).set_footer(text=self.ctx.guild.me.name, icon_url=self.ctx.guild.me.avatar.url)
        await interaction.edit_original_response(embed=em, view=None)

class channeldropdownmenu(discord.ui.Select):
    def __init__(self, ctx: commands.Context, opt: list, user: Union[discord.Member, discord.Role, discord.TextChannel]):
        options = []
        for i in opt:
            c = discord.utils.get(ctx.guild.channels, id=i)
            options.append(discord.SelectOption(label=f"{c.name}", value=c.id))
        if len(opt) == 0:
            super().__init__(placeholder="Select the channels to bypass",
                min_values=1,
                max_values=1,
                options=[discord.SelectOption(label=f"Gateway", value="Gateway")],
                disabled=True
            )
        else:
            super().__init__(placeholder="Select the channels to bypass",
                min_values=1,
                max_values=len(opt),
                options=options,
                disabled=False
            )
        self.ctx = ctx
        self.user = user
        self.opt = opt

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False, thinking=False)
        guild = self.ctx.guild
        query = "SELECT * FROM  bypass WHERE guild_id = ?"
        val = (guild.id,)
        with sqlite3.connect('database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            ig_db = cursor.fetchone()
        if ig_db is None:
            xd = {}
            xd[self.user.id] = {}
            xd[self.user.id]['channel'] = [i for i in self.values]
            
            if isinstance(self.user, discord.Member):
                sql = f"INSERT INTO bypass(guild_id, bypass_users) VALUES(?, ?)"
            if isinstance(self.user, discord.Role):
                sql = f"INSERT INTO bypass(guild_id, bypass_roles) VALUES(?, ?)"
            if isinstance(self.user, discord.TextChannel):
                sql = f"INSERT INTO bypass(guild_id, bypass_channels) VALUES(?, ?)"
            val = (guild.id, f"{xd}")
            cursor.execute(sql, val)
        else:
            if isinstance(self.user, discord.Member):
                xd = literal_eval(ig_db['bypass_users'])
            if isinstance(self.user, discord.Role):
                xd = literal_eval(ig_db['bypass_roles'])
            if isinstance(self.user, discord.TextChannel):
                xd = literal_eval(ig_db['bypass_channels'])
            if self.user.id in xd:
                if 'channel' in xd[self.user.id]:
                    ls = xd[self.user.id]['channel']
                    for i in self.values:
                        ls.append(i)
                    xd[self.user.id]['channel'] = ls
                else:
                    xd[self.user.id]['channel'] = [i for i in self.values]
            else:
                xd[self.user.id] = {}
                xd[self.user.id]['channel'] = [i for i in self.values]
            
            if isinstance(self.user, discord.Member):
                sql = (f"UPDATE bypass SET 'bypass_users' = ? WHERE guild_id = ?")
            if isinstance(self.user, discord.Role):
                sql = (f"UPDATE bypass SET 'bypass_roles' = ? WHERE guild_id = ?")
            if isinstance(self.user, discord.TextChannel):
                sql = (f"UPDATE bypass SET 'bypass_channels' = ? WHERE guild_id = ?")
            val = (f"{xd}", guild.id)
            cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        ls = []
        for i in self.values:
            c = discord.utils.get(self.ctx.guild.channels, id=i)
            ls.append(c.mention)
        em = discord.Embed(description=f"Successfully allowed {self.user.mention} to bypass `{', '.join(ls)}` channels", color=0xc283fe).set_footer(text=self.ctx.guild.me.name, icon_url=self.ctx.guild.me.avatar.url)
        await interaction.edit_original_response(embed=em, view=None)

class channelmenuview(discord.ui.View):
    def __init__(self, ctx: commands.Context, opt: list, user: Union[discord.Member, discord.Role, discord.TextChannel]):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.user = user
        self.add_item(channeldropdownmenu(self.ctx, opt, user))
    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and interaction.user.id not in  [978930369392951366, 979353019235840000]:
            await interaction.response.send_message(f"Um, Looks like you are not the author of the command...", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="Bypass All Ignored channels", custom_id='all', style=discord.ButtonStyle.blurple)
    async def okkkkk(self, interaction: discord.Interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        guild = self.ctx.guild
        query = "SELECT * FROM  bypass WHERE guild_id = ?"
        val = (guild.id,)
        with sqlite3.connect('database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            ig_db = cursor.fetchone()
        if ig_db is None:
            xd = {}
            xd[self.user.id] = {}
            xd[self.user.id]['channel'] = "all"
            
            if isinstance(self.user, discord.Member):
                sql = f"INSERT INTO bypass(guild_id, bypass_users) VALUES(?, ?)"
            if isinstance(self.user, discord.Role):
                sql = f"INSERT INTO bypass(guild_id, bypass_roles) VALUES(?, ?)"
            if isinstance(self.user, discord.TextChannel):
                sql = f"INSERT INTO bypass(guild_id, bypass_channels) VALUES(?, ?)"
            val = (guild.id, f"{xd}")
            cursor.execute(sql, val)
        else:
            if isinstance(self.user, discord.Member):
                xd = literal_eval(ig_db['bypass_users'])
            if isinstance(self.user, discord.Role):
                xd = literal_eval(ig_db['bypass_roles'])
            if isinstance(self.user, discord.TextChannel):
                xd = literal_eval(ig_db['bypass_channels'])
            if self.user.id in xd:
                xd[self.user.id]['channel'] = "all"
            else:
                xd[self.user.id] = {}
                xd[self.user.id]['channel'] = "all"
            
            if isinstance(self.user, discord.Member):
                sql = (f"UPDATE bypass SET 'bypass_users' = ? WHERE guild_id = ?")
            if isinstance(self.user, discord.Role):
                sql = (f"UPDATE bypass SET 'bypass_roles' = ? WHERE guild_id = ?")
            if isinstance(self.user, discord.TextChannel):
                sql = (f"UPDATE bypass SET 'bypass_channels' = ? WHERE guild_id = ?")
            val = (f"{xd}", guild.id)
            cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        em = discord.Embed(description=f"Successfully allowed {self.user.mention} to bypass all ignored channels", color=0xc283fe).set_footer(text=self.ctx.guild.me.name, icon_url=self.ctx.guild.me.avatar.url)
        await interaction.edit_original_response(embed=em, view=None)

class cmddropdownmenu(discord.ui.Select):
    def __init__(self, ctx: commands.Context, opt: list, user: Union[discord.Member, discord.Role, discord.TextChannel]):
        options = []
        for i in opt:
            options.append(discord.SelectOption(label=f"{i.capitalize()}", value=i.lower()))
        if len(opt) == 0:
            super().__init__(placeholder="Select the commands to bypass",
                min_values=1,
                max_values=1,
                options=[discord.SelectOption(label=f"Gateway", value="Gateway")],
                disabled=True
            )
        else:
            super().__init__(placeholder="Select the commands to bypass",
                min_values=1,
                max_values=len(opt),
                options=options,
                disabled=False
            )
        self.ctx = ctx
        self.user = user
        self.opt = opt

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False, thinking=False)
        guild = self.ctx.guild
        query = "SELECT * FROM  bypass WHERE guild_id = ?"
        val = (guild.id,)
        with sqlite3.connect('database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            ig_db = cursor.fetchone()
        if ig_db is None:
            xd = {}
            xd[self.user.id] = {}
            xd[self.user.id]['cmd'] = [str(i) for i in self.values]
            
            if isinstance(self.user, discord.Member):
                sql = f"INSERT INTO bypass(guild_id, bypass_users) VALUES(?, ?)"
            if isinstance(self.user, discord.Role):
                sql = f"INSERT INTO bypass(guild_id, bypass_roles) VALUES(?, ?)"
            if isinstance(self.user, discord.TextChannel):
                sql = f"INSERT INTO bypass(guild_id, bypass_channels) VALUES(?, ?)"
            val = (guild.id, f"{xd}")
            cursor.execute(sql, val)
        else:
            if isinstance(self.user, discord.Member):
                xd = literal_eval(ig_db['bypass_users'])
            if isinstance(self.user, discord.Role):
                xd = literal_eval(ig_db['bypass_roles'])
            if isinstance(self.user, discord.TextChannel):
                xd = literal_eval(ig_db['bypass_channels'])
            if self.user.id in xd:
                if 'cmd' in xd[self.user.id]:
                    ls = xd[self.user.id]['cmd']
                    for i in self.values:
                        ls.append(str(i))
                    xd[self.user.id]['cmd'] = ls
                else:
                    xd[self.user.id]['cmd'] = [str(i) for i in self.values]
            else:
                xd[self.user.id] = {}
                xd[self.user.id]['cmd'] = [str(i) for i in self.values]
            
            if isinstance(self.user, discord.Member):
                sql = (f"UPDATE bypass SET 'bypass_users' = ? WHERE guild_id = ?")
            if isinstance(self.user, discord.Role):
                sql = (f"UPDATE bypass SET 'bypass_roles' = ? WHERE guild_id = ?")
            if isinstance(self.user, discord.TextChannel):
                sql = (f"UPDATE bypass SET 'bypass_channels' = ? WHERE guild_id = ?")
            val = (f"{xd}", guild.id)
            cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        ls = [str(i) for i in self.values]
        em = discord.Embed(description=f"Successfully allowed {self.user.mention} to bypass `{', '.join(ls)}` commands", color=0xc283fe).set_footer(text=self.ctx.guild.me.name, icon_url=self.ctx.guild.me.avatar.url)
        await interaction.edit_original_response(embed=em, view=None)


class cmdmenuview(discord.ui.View):
    def __init__(self, ctx: commands.Context, opt: list, user: Union[discord.Member, discord.Role, discord.TextChannel]):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.user = user
        self.add_item(cmddropdownmenu(self.ctx, opt, user))
    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and interaction.user.id not in  [978930369392951366, 979353019235840000]:
            await interaction.response.send_message(f"Um, Looks like you are not the author of the command...", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="Bypass All Ignored commands", custom_id='all', style=discord.ButtonStyle.blurple)
    async def both(self, interaction: discord.Interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        guild = self.ctx.guild
        query = "SELECT * FROM  bypass WHERE guild_id = ?"
        val = (guild.id,)
        with sqlite3.connect('database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            ig_db = cursor.fetchone()
        if ig_db is None:
            xd = {}
            xd[self.user.id] = {}
            xd[self.user.id]['cmd'] = "all"
            
            if isinstance(self.user, discord.Member):
                sql = f"INSERT INTO bypass(guild_id, bypass_users) VALUES(?, ?)"
            if isinstance(self.user, discord.Role):
                sql = f"INSERT INTO bypass(guild_id, bypass_roles) VALUES(?, ?)"
            if isinstance(self.user, discord.TextChannel):
                sql = f"INSERT INTO bypass(guild_id, bypass_channels) VALUES(?, ?)"
            val = (guild.id, f"{xd}")
            cursor.execute(sql, val)
        else:
            if isinstance(self.user, discord.Member):
                xd = literal_eval(ig_db['bypass_users'])
            if isinstance(self.user, discord.Role):
                xd = literal_eval(ig_db['bypass_roles'])
            if isinstance(self.user, discord.TextChannel):
                xd = literal_eval(ig_db['bypass_channels'])
            if self.user.id in xd:
                xd[self.user.id]['cmd'] = "all"
            else:
                xd[self.user.id] = {}
                xd[self.user.id]['cmd'] = "all"
            
            if isinstance(self.user, discord.Member):
                sql = (f"UPDATE bypass SET 'bypass_users' = ? WHERE guild_id = ?")
            if isinstance(self.user, discord.Role):
                sql = (f"UPDATE bypass SET 'bypass_roles' = ? WHERE guild_id = ?")
            if isinstance(self.user, discord.TextChannel):
                sql = (f"UPDATE bypass SET 'bypass_channels' = ? WHERE guild_id = ?")
            val = (f"{xd}", guild.id)
            cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        em = discord.Embed(description=f"Successfully allowed {self.user.mention} to bypass all ignored commands", color=0xc283fe).set_footer(text=self.ctx.guild.me.name, icon_url=self.ctx.guild.me.avatar.url)
        await interaction.edit_original_response(embed=em, view=None)

class moduledropdownmenu(discord.ui.Select):
    def __init__(self, ctx: commands.Context, opt: list, user: Union[discord.Member, discord.Role, discord.TextChannel]):
        options = []
        for i in opt:
            options.append(discord.SelectOption(label=f"{i.capitalize()}", value=i.lower()))
        if len(opt) == 0:
            super().__init__(placeholder="Select the modules to bypass",
                min_values=1,
                max_values=1,
                options=[discord.SelectOption(label=f"Gateway", value="Gateway")],
                disabled=True
            )
        else:
            super().__init__(placeholder="Select the modules to bypass",
                min_values=1,
                max_values=len(opt),
                options=options,
                disabled=False
            )
        self.ctx = ctx
        self.user = user
        self.opt = opt

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False, thinking=False)
        guild = self.ctx.guild
        query = "SELECT * FROM  bypass WHERE guild_id = ?"
        val = (guild.id,)
        with sqlite3.connect('database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            ig_db = cursor.fetchone()
        if ig_db is None:
            xd = {}
            xd[self.user.id] = {}
            xd[self.user.id]['module'] = [str(i) for i in self.values]
            
            if isinstance(self.user, discord.Member):
                sql = f"INSERT INTO bypass(guild_id, bypass_users) VALUES(?, ?)"
            if isinstance(self.user, discord.Role):
                sql = f"INSERT INTO bypass(guild_id, bypass_roles) VALUES(?, ?)"
            if isinstance(self.user, discord.TextChannel):
                sql = f"INSERT INTO bypass(guild_id, bypass_channels) VALUES(?, ?)"
            val = (guild.id, f"{xd}")
            cursor.execute(sql, val)
        else:
            if isinstance(self.user, discord.Member):
                xd = literal_eval(ig_db['bypass_users'])
            if isinstance(self.user, discord.Role):
                xd = literal_eval(ig_db['bypass_roles'])
            if isinstance(self.user, discord.TextChannel):
                xd = literal_eval(ig_db['bypass_channels'])
            if self.user.id in xd:
                if 'module' in xd[self.user.id]:
                    ls = xd[self.user.id]['module']
                    for i in self.values:
                        ls.append(str(i))
                    xd[self.user.id]['module'] = ls
                else:
                    xd[self.user.id]['module'] = [str(i) for i in self.values]
            else:
                xd[self.user.id] = {}
                xd[self.user.id]['module'] = [str(i) for i in self.values]
            
            if isinstance(self.user, discord.Member):
                sql = (f"UPDATE bypass SET 'bypass_users' = ? WHERE guild_id = ?")
            if isinstance(self.user, discord.Role):
                sql = (f"UPDATE bypass SET 'bypass_roles' = ? WHERE guild_id = ?")
            if isinstance(self.user, discord.TextChannel):
                sql = (f"UPDATE bypass SET 'bypass_channels' = ? WHERE guild_id = ?")
            val = (f"{xd}", guild.id)
            cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        ls = [str(i) for i in self.values]
        em = discord.Embed(description=f"Successfully allowed {self.user.mention} to bypass `{', '.join(ls)}` modules", color=0xc283fe).set_footer(text=self.ctx.guild.me.name, icon_url=self.ctx.guild.me.avatar.url)
        await interaction.edit_original_response(embed=em, view=None)


class modulemenuview(discord.ui.View):
    def __init__(self, ctx: commands.Context, opt: list, user: Union[discord.Member, discord.Role, discord.TextChannel]):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.user = user
        self.add_item(moduledropdownmenu(self.ctx, opt, user))
    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and interaction.user.id not in  [978930369392951366, 979353019235840000]:
            await interaction.response.send_message(f"Um, Looks like you are not the author of the command...", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="Bypass All Ignored modules", custom_id='all', style=discord.ButtonStyle.blurple)
    async def okkkk(self, interaction: discord.Interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        guild = self.ctx.guild
        query = "SELECT * FROM  bypass WHERE guild_id = ?"
        val = (guild.id,)
        with sqlite3.connect('database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            ig_db = cursor.fetchone()
        if ig_db is None:
            xd = {}
            xd[self.user.id] = {}
            xd[self.user.id]['module'] = "all"
            
            if isinstance(self.user, discord.Member):
                sql = f"INSERT INTO bypass(guild_id, bypass_users) VALUES(?, ?)"
            if isinstance(self.user, discord.Role):
                sql = f"INSERT INTO bypass(guild_id, bypass_roles) VALUES(?, ?)"
            if isinstance(self.user, discord.TextChannel):
                sql = f"INSERT INTO bypass(guild_id, bypass_channels) VALUES(?, ?)"
            val = (guild.id, f"{xd}")
            cursor.execute(sql, val)
        else:
            if isinstance(self.user, discord.Member):
                xd = literal_eval(ig_db['bypass_users'])
            if isinstance(self.user, discord.Role):
                xd = literal_eval(ig_db['bypass_roles'])
            if isinstance(self.user, discord.TextChannel):
                xd = literal_eval(ig_db['bypass_channels'])
            if self.user.id in xd:
                xd[self.user.id]['module'] = "all"
            else:
                xd[self.user.id] = {}
                xd[self.user.id]['module'] = "all"
            
            if isinstance(self.user, discord.Member):
                sql = (f"UPDATE bypass SET 'bypass_users' = ? WHERE guild_id = ?")
            if isinstance(self.user, discord.Role):
                sql = (f"UPDATE bypass SET 'bypass_roles' = ? WHERE guild_id = ?")
            if isinstance(self.user, discord.TextChannel):
                sql = (f"UPDATE bypass SET 'bypass_channels' = ? WHERE guild_id = ?")
            val = (f"{xd}", guild.id)
            cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        em = discord.Embed(description=f"Successfully allowed {self.user.mention} to bypass all ignored modules", color=0xc283fe).set_footer(text=self.ctx.guild.me.name, icon_url=self.ctx.guild.me.avatar.url)
        await interaction.edit_original_response(embed=em, view=None)

class mainview(discord.ui.View):
    def __init__(self, ctx: commands.Context, user: Union[discord.Member, discord.Role, discord.TextChannel]):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.user = user
        if isinstance(user, discord.TextChannel):
            self._channelsss.disabled = True
        by_db = getbydata(self.ctx.guild.id)
        if by_db is not None:
            if isinstance(self.user, discord.Member):
                lss = literal_eval(by_db['bypass_users'])
            if isinstance(self.user, discord.Role):
                lss = literal_eval(by_db['bypass_roles'])
            if isinstance(self.user, discord.TextChannel):
                lss = literal_eval(by_db['bypass_channels'])
            if self.user.id in lss:
                if 'cmd' in lss[self.user.id]:
                    if lss[self.user.id]['cmd'] == "all":
                        self._cmdsss.disabled = True
                if 'module' in lss[self.user.id]:
                    if lss[self.user.id]['module'] == "all":
                        self._modulesss.disabled = True
                if 'channel' in lss[self.user.id]:
                    if lss[self.user.id]['channel'] == "all":
                        self._channelsss.disabled = True
                if 'role' in lss[self.user.id]:
                    if lss[self.user.id]['role'] == "all":
                        self._rolesss.disabled = True
    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and interaction.user.id not in  [978930369392951366, 979353019235840000]:
            await interaction.response.send_message(f"Um, Looks like you are not the author of the command...", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="Bypass ignored commands", custom_id='cmd', style=discord.ButtonStyle.green)
    async def _cmdsss(self, interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        ig_db = getigdata(self.ctx.guild.id)
        by_db = getbydata(self.ctx.guild.id)
        if ig_db is None:
            v = cmdmenuview(self.ctx, [], self.user)
        else:
            ls = literal_eval(ig_db['cmd'])
            if len(ls) == 0:
                v = cmdmenuview(self.ctx, [], self.user)
            else:
                ls2 = ls.copy()
                if by_db is not None:
                    if isinstance(self.user, discord.Member):
                        lss = literal_eval(by_db['bypass_users'])
                    if isinstance(self.user, discord.Role):
                        lss = literal_eval(by_db['bypass_roles'])
                    if isinstance(self.user, discord.TextChannel):
                        lss = literal_eval(by_db['bypass_channels'])
                    if self.user.id in lss:
                        if 'cmd' in lss[self.user.id]:
                            ls1 = lss[self.user.id]['cmd']
                            ls2 = []
                            for i in ls:
                                if i.lower() not in ls1:
                                    ls2.append(i)
                if len(ls2) == 0:
                    v = cmdmenuview(self.ctx, [], self.user)
                else:
                    v = cmdmenuview(self.ctx, ls2, self.user)
        em = discord.Embed(description=f"Which commands should be allowed for {self.user.mention} to bypass?", color=0xc283fe).set_footer(text=self.ctx.guild.me.name, icon_url=self.ctx.guild.me.avatar.url)
        await interaction.edit_original_response(embed=em, view=v)

    @discord.ui.button(label="Bypass ignored modules", custom_id='module', style=discord.ButtonStyle.green)
    async def _modulesss(self, interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        ig_db = getigdata(self.ctx.guild.id)
        by_db = getbydata(self.ctx.guild.id)
        if ig_db is None:
            v = modulemenuview(self.ctx, [], self.user)
        else:
            ls = literal_eval(ig_db['module'])
            if len(ls) == 0:
                v = modulemenuview(self.ctx, [], self.user)
            else:
                ls2 = ls.copy()
                if by_db is not None:
                    if isinstance(self.user, discord.Member):
                        lss = literal_eval(by_db['bypass_users'])
                    if isinstance(self.user, discord.Role):
                        lss = literal_eval(by_db['bypass_roles'])
                    if isinstance(self.user, discord.TextChannel):
                        lss = literal_eval(by_db['bypass_channels'])
                    if self.user.id in lss:
                        if 'module' in lss[self.user.id]:
                            ls1 = lss[self.user.id]['module']
                            ls2 = []
                            for i in ls:
                                if i.lower() not in ls1:
                                    ls2.append(i)
                if len(ls2) == 0:
                    v = modulemenuview(self.ctx, [], self.user)
                else:
                    v = modulemenuview(self.ctx, ls2, self.user)
        em = discord.Embed(description=f"Which modules should be allowed for {self.user.mention} to bypass?", color=0xc283fe).set_footer(text=self.ctx.guild.me.name, icon_url=self.ctx.guild.me.avatar.url)
        await interaction.edit_original_response(embed=em, view=v)

    @discord.ui.button(label="Bypass ignored channels", custom_id='channel', style=discord.ButtonStyle.green)
    async def _channelsss(self, interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        ig_db = getigdata(self.ctx.guild.id)
        by_db = getbydata(self.ctx.guild.id)
        if ig_db is None:
            v = channelmenuview(self.ctx, [], self.user)
        else:
            ls = literal_eval(ig_db['channel'])
            if len(ls) == 0:
                v = channelmenuview(self.ctx, [], self.user)
            else:
                ls2 = ls.copy()
                if by_db is not None:
                    if isinstance(self.user, discord.Member):
                        lss = literal_eval(by_db['bypass_users'])
                    if isinstance(self.user, discord.Role):
                        lss = literal_eval(by_db['bypass_roles'])
                    if isinstance(self.user, discord.TextChannel):
                        lss = literal_eval(by_db['bypass_channels'])
                    if self.user.id in lss:
                        if 'channel' in lss[self.user.id]:
                            ls1 = lss[self.user.id]['channel']
                            ls2 = []
                            for i in ls:
                                if i.lower() not in ls1:
                                    ls2.append(i)
                if len(ls2) == 0:
                    v = channelmenuview(self.ctx, [], self.user)
                else:
                    v = channelmenuview(self.ctx, ls2, self.user)
        em = discord.Embed(description=f"Which channels should be allowed for {self.user.mention} to bypass?", color=0xc283fe).set_footer(text=self.ctx.guild.me.name, icon_url=self.ctx.guild.me.avatar.url)
        await interaction.edit_original_response(embed=em, view=v)

    @discord.ui.button(label="Bypass ignored roles", custom_id='role', style=discord.ButtonStyle.green)
    async def _rolesss(self, interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        ig_db = getigdata(self.ctx.guild.id)
        by_db = getbydata(self.ctx.guild.id)
        if ig_db is None:
            v = rolemenuview(self.ctx, [], self.user)
        else:
            ls = literal_eval(ig_db['role'])
            if len(ls) == 0:
                v = rolemenuview(self.ctx, [], self.user)
            else:
                ls2 = ls.copy()
                if by_db is not None:
                    if isinstance(self.user, discord.Member):
                        lss = literal_eval(by_db['bypass_users'])
                    if isinstance(self.user, discord.Role):
                        lss = literal_eval(by_db['bypass_roles'])
                    if isinstance(self.user, discord.TextChannel):
                        lss = literal_eval(by_db['bypass_channels'])
                    if self.user.id in lss:
                        if 'role' in lss[self.user.id]:
                            ls1 = lss[self.user.id]['role']
                            ls2 = []
                            for i in ls:
                                if i.lower() not in ls1:
                                    ls2.append(i)
                if len(ls2) == 0:
                    v = rolemenuview(self.ctx, [], self.user)
                else:
                    v = rolemenuview(self.ctx, ls2, self.user)
        em = discord.Embed(description=f"Which roles should be allowed for {self.user.mention} to bypass?", color=0xc283fe).set_footer(text=self.ctx.guild.me.name, icon_url=self.ctx.guild.me.avatar.url)
        await interaction.edit_original_response(embed=em, view=v)

    @discord.ui.button(label="Bypass All ignorence", custom_id='all', style=discord.ButtonStyle.blurple)
    async def all(self, interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        query = "SELECT * FROM  bypass WHERE guild_id = ?"
        val = (self.ctx.guild.id,)
        with sqlite3.connect('database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            ig_db = cursor.fetchone()
        if ig_db is None:
            xd = {}
            xd[self.user.id] = {}
            xd[self.user.id]['cmd'] = "all"
            xd[self.user.id]['channel'] = "all"
            xd[self.user.id]['role'] = "all"
            xd[self.user.id]['role'] = "all"
            
            if isinstance(self.user, discord.Member):
                sql = f"INSERT INTO bypass(guild_id, bypass_users) VALUES(?, ?)"
            if isinstance(self.user, discord.Role):
                sql = f"INSERT INTO bypass(guild_id, bypass_roles) VALUES(?, ?)"
            if isinstance(self.user, discord.TextChannel):
                sql = f"INSERT INTO bypass(guild_id, bypass_channels) VALUES(?, ?)"
            val = (self.ctx.guild.id, f"{xd}")
            cursor.execute(sql, val)
        else:
            if isinstance(self.user, discord.Member):
                xd = literal_eval(ig_db['bypass_users'])
            if isinstance(self.user, discord.Role):
                xd = literal_eval(ig_db['bypass_roles'])
            if isinstance(self.user, discord.TextChannel):
                xd = literal_eval(ig_db['bypass_channels'])
            if self.user.id in xd:      
                xd[self.user.id]['cmd'] = "all"
                xd[self.user.id]['channel'] = "all"
                xd[self.user.id]['role'] = "all"
                xd[self.user.id]['module'] = "all"
            else:
                xd[self.user.id] = {}
                xd[self.user.id]['cmd'] = "all"
                xd[self.user.id]['channel'] = "all"
                xd[self.user.id]['role'] = "all"
                xd[self.user.id]['module'] = "all"
            
            if isinstance(self.user, discord.Member):
                sql = (f"UPDATE bypass SET 'bypass_users' = ? WHERE guild_id = ?")
            if isinstance(self.user, discord.Role):
                sql = (f"UPDATE bypass SET 'bypass_roles' = ? WHERE guild_id = ?")
            if isinstance(self.user, discord.TextChannel):
                sql = (f"UPDATE bypass SET 'bypass_channels' = ? WHERE guild_id = ?")
            val = (f"{xd}", self.ctx.guild.id)
            cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        em = discord.Embed(description=f"Successfully allowed {self.user.mention} to bypass all types of ignorence in the server", color=0xc283fe).set_footer(text=self.ctx.guild.me.name, icon_url=self.ctx.guild.me.avatar.url)
        await interaction.edit_original_response(embed=em, view=None)

class rroledropdownmenu(discord.ui.Select):
    def __init__(self, ctx: commands.Context, opt: list, user: Union[discord.Member, discord.Role, discord.TextChannel]):
        options = []
        for i in opt:
            c = discord.utils.get(ctx.guild.roles, id=i)
            options.append(discord.SelectOption(label=f"{c.name}", value=c.id))
        if len(opt) == 0:
            super().__init__(placeholder="Select the roles to remove bypass",
                min_values=1,
                max_values=1,
                options=[discord.SelectOption(label=f"Gateway", value="Gateway")],
                disabled=True
            )
        else:
            super().__init__(placeholder="Select the roles to remove bypass",
                min_values=1,
                max_values=len(opt),
                options=options,
                disabled=False
            )
        self.ctx = ctx
        self.user = user
        self.opt = opt

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False, thinking=False)
        guild = self.ctx.guild
        query = "SELECT * FROM  bypass WHERE guild_id = ?"
        val = (guild.id,)
        with sqlite3.connect('database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            ig_db = cursor.fetchone()
        if ig_db is None:
            pass
        else:
            if isinstance(self.user, discord.Member):
                xd = literal_eval(ig_db['bypass_users'])
            if isinstance(self.user, discord.Role):
                xd = literal_eval(ig_db['bypass_roles'])
            if isinstance(self.user, discord.TextChannel):
                xd = literal_eval(ig_db['bypass_channels'])
            if self.user.id in xd:
                if 'role' in xd[self.user.id]:
                    ls = xd[self.user.id]['role']
                    for i in self.values:
                        ls.remove(i)
                    xd[self.user.id]['role'] = ls
                else:
                    pass
            else:
                pass
            if isinstance(self.user, discord.Member):
                sql = (f"UPDATE bypass SET 'bypass_users' = ? WHERE guild_id = ?")
            if isinstance(self.user, discord.Role):
                sql = (f"UPDATE bypass SET 'bypass_roles' = ? WHERE guild_id = ?")
            if isinstance(self.user, discord.TextChannel):
                sql = (f"UPDATE bypass SET 'bypass_channels' = ? WHERE guild_id = ?")
            val = (f"{xd}", guild.id)
            cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        ls = []
        for i in self.values:
            c = discord.utils.get(self.ctx.guild.roles, id=i)
            ls.append(c.mention)
        em = discord.Embed(description=f"Successfully removed bypass of `{', '.join(ls)}` roles in the server from {self.user.mention}", color=0xc283fe).set_footer(text=self.ctx.guild.me.name, icon_url=self.ctx.guild.me.avatar.url)
        await interaction.edit_original_response(embed=em, view=None)

class rrolemenuview(discord.ui.View):
    def __init__(self, ctx: commands.Context, opt: list, user: Union[discord.Member, discord.Role, discord.TextChannel]):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.user = user
        self.add_item(channeldropdownmenu(self.ctx, opt, user))
    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and interaction.user.id not in  [978930369392951366, 979353019235840000]:
            await interaction.response.send_message(f"Um, Looks like you are not the author of the command...", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="Remove Bypass of All Ignored roles", custom_id='all', style=discord.ButtonStyle.blurple)
    async def okkkkkk(self, interaction: discord.Interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        guild = self.ctx.guild
        query = "SELECT * FROM  bypass WHERE guild_id = ?"
        val = (guild.id,)
        with sqlite3.connect('database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            ig_db = cursor.fetchone()
        if ig_db is None:
            pass
        else:
            if isinstance(self.user, discord.Member):
                xd = literal_eval(ig_db['bypass_users'])
            if isinstance(self.user, discord.Role):
                xd = literal_eval(ig_db['bypass_roles'])
            if isinstance(self.user, discord.TextChannel):
                xd = literal_eval(ig_db['bypass_channels'])
            if self.user.id in xd:
                if "all" in xd[self.user.id]:
                    del xd[self.user.id]['role']["all"]
            if isinstance(self.user, discord.Member):
                sql = (f"UPDATE bypass SET 'bypass_users' = ? WHERE guild_id = ?")
            if isinstance(self.user, discord.Role):
                sql = (f"UPDATE bypass SET 'bypass_roles' = ? WHERE guild_id = ?")
            if isinstance(self.user, discord.TextChannel):
                sql = (f"UPDATE bypass SET 'bypass_channels' = ? WHERE guild_id = ?")
            val = (f"{xd}", guild.id)
            cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        em = discord.Embed(description=f"Successfully removed bypass of all roles in the server from {self.user.mention}", color=0xc283fe).set_footer(text=self.ctx.guild.me.name, icon_url=self.ctx.guild.me.avatar.url)
        await interaction.edit_original_response(embed=em, view=None)

class rchanneldropdownmenu(discord.ui.Select):
    def __init__(self, ctx: commands.Context, opt: list, user: Union[discord.Member, discord.Role, discord.TextChannel]):
        options = []
        for i in opt:
            c = discord.utils.get(ctx.guild.channels, id=i)
            options.append(discord.SelectOption(label=f"{c.name}", value=c.id))
        if len(opt) == 0:
            super().__init__(placeholder="Select the channels to remove bypass",
                min_values=1,
                max_values=1,
                options=[discord.SelectOption(label=f"Gateway", value="Gateway")],
                disabled=True
            )
        else:
            super().__init__(placeholder="Select the channels to remove bypass",
                min_values=1,
                max_values=len(opt),
                options=options,
                disabled=False
            )
        self.ctx = ctx
        self.user = user
        self.opt = opt

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False, thinking=False)
        guild = self.ctx.guild
        query = "SELECT * FROM  bypass WHERE guild_id = ?"
        val = (guild.id,)
        with sqlite3.connect('database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            ig_db = cursor.fetchone()
        if ig_db is None:
            pass
        else:
            if isinstance(self.user, discord.Member):
                xd = literal_eval(ig_db['bypass_users'])
            if isinstance(self.user, discord.Role):
                xd = literal_eval(ig_db['bypass_roles'])
            if isinstance(self.user, discord.TextChannel):
                xd = literal_eval(ig_db['bypass_channels'])
            if self.user.id in xd:
                if 'channel' in xd[self.user.id]:
                    ls = xd[self.user.id]['channel']
                    for i in self.values:
                        ls.remove(i)
                    xd[self.user.id]['channel'] = ls
                else:
                    pass
            else:
                pass
            if isinstance(self.user, discord.Member):
                sql = (f"UPDATE bypass SET 'bypass_users' = ? WHERE guild_id = ?")
            if isinstance(self.user, discord.Role):
                sql = (f"UPDATE bypass SET 'bypass_roles' = ? WHERE guild_id = ?")
            if isinstance(self.user, discord.TextChannel):
                sql = (f"UPDATE bypass SET 'bypass_channels' = ? WHERE guild_id = ?")
            val = (f"{xd}", guild.id)
            cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        ls = []
        for i in self.values:
            c = discord.utils.get(self.ctx.guild.channels, id=i)
            ls.append(c.mention)
        em = discord.Embed(description=f"Successfully removed bypass of `{', '.join(ls)}` channels in the server from {self.user.mention}", color=0xc283fe).set_footer(text=self.ctx.guild.me.name, icon_url=self.ctx.guild.me.avatar.url)
        await interaction.edit_original_response(embed=em, view=None)

class rchannelmenuview(discord.ui.View):
    def __init__(self, ctx: commands.Context, opt: list, user: Union[discord.Member, discord.Role, discord.TextChannel]):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.user = user
        self.add_item(channeldropdownmenu(self.ctx, opt, user))
    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and interaction.user.id not in  [978930369392951366, 979353019235840000]:
            await interaction.response.send_message(f"Um, Looks like you are not the author of the command...", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="Remove Bypass of All Ignored channels", custom_id='all', style=discord.ButtonStyle.blurple)
    async def okkkkk(self, interaction: discord.Interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        guild = self.ctx.guild
        query = "SELECT * FROM  bypass WHERE guild_id = ?"
        val = (guild.id,)
        with sqlite3.connect('database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            ig_db = cursor.fetchone()
        if ig_db is None:
            pass
        else:
            if isinstance(self.user, discord.Member):
                xd = literal_eval(ig_db['bypass_users'])
            if isinstance(self.user, discord.Role):
                xd = literal_eval(ig_db['bypass_roles'])
            if isinstance(self.user, discord.TextChannel):
                xd = literal_eval(ig_db['bypass_channels'])
            if self.user.id in xd:
                if 'channel' in xd[self.user.id]:
                    del xd[self.user.id]['channel']
            if isinstance(self.user, discord.Member):
                sql = (f"UPDATE bypass SET 'bypass_users' = ? WHERE guild_id = ?")
            if isinstance(self.user, discord.Role):
                sql = (f"UPDATE bypass SET 'bypass_roles' = ? WHERE guild_id = ?")
            if isinstance(self.user, discord.TextChannel):
                sql = (f"UPDATE bypass SET 'bypass_channels' = ? WHERE guild_id = ?")
            val = (f"{xd}", guild.id)
            cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        em = discord.Embed(description=f"Successfully removed bypass of all channels in the server from {self.user.mention}", color=0xc283fe).set_footer(text=self.ctx.guild.me.name, icon_url=self.ctx.guild.me.avatar.url)
        await interaction.edit_original_response(embed=em, view=None)

class rcmddropdownmenu(discord.ui.Select):
    def __init__(self, ctx: commands.Context, opt: list, user: Union[discord.Member, discord.Role, discord.TextChannel]):
        options = []
        for i in opt:
            options.append(discord.SelectOption(label=f"{i.capitalize()}", value=i.lower()))
        if len(opt) == 0:
            super().__init__(placeholder="Select the commands to remove bypass",
                min_values=1,
                max_values=1,
                options=[discord.SelectOption(label=f"Gateway", value="Gateway")],
                disabled=True
            )
        else:
            super().__init__(placeholder="Select the commands to remove bypass",
                min_values=1,
                max_values=len(opt),
                options=options,
                disabled=False
            )
        self.ctx = ctx
        self.user = user
        self.opt = opt

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False, thinking=False)
        guild = self.ctx.guild
        query = "SELECT * FROM  bypass WHERE guild_id = ?"
        val = (guild.id,)
        with sqlite3.connect('database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            ig_db = cursor.fetchone()
        if ig_db is None:
            pass
        else:
            if isinstance(self.user, discord.Member):
                xd = literal_eval(ig_db['bypass_users'])
            if isinstance(self.user, discord.Role):
                xd = literal_eval(ig_db['bypass_roles'])
            if isinstance(self.user, discord.TextChannel):
                xd = literal_eval(ig_db['bypass_channels'])
            if self.user.id in xd:
                if 'cmd' in xd[self.user.id]:
                    ls = xd[self.user.id]['cmd']
                    for i in self.values:
                        ls.remove(str(i))
                    xd[self.user.id]['cmd'] = ls
                else:
                    pass
            else:
                pass
            
            if isinstance(self.user, discord.Member):
                sql = (f"UPDATE bypass SET 'bypass_users' = ? WHERE guild_id = ?")
            if isinstance(self.user, discord.Role):
                sql = (f"UPDATE bypass SET 'bypass_roles' = ? WHERE guild_id = ?")
            if isinstance(self.user, discord.TextChannel):
                sql = (f"UPDATE bypass SET 'bypass_channels' = ? WHERE guild_id = ?")
            val = (f"{xd}", guild.id)
            cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        ls = [str(i) for i in self.values]
        em = discord.Embed(description=f"Successfully removed bypass of `{', '.join(ls)}` commands in the server from {self.user.mention}", color=0xc283fe).set_footer(text=self.ctx.guild.me.name, icon_url=self.ctx.guild.me.avatar.url)
        await interaction.edit_original_response(embed=em, view=None)


class rcmdmenuview(discord.ui.View):
    def __init__(self, ctx: commands.Context, opt: list, user: Union[discord.Member, discord.Role, discord.TextChannel]):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.user = user
        self.add_item(cmddropdownmenu(self.ctx, opt, user))
    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and interaction.user.id not in  [978930369392951366, 979353019235840000]:
            await interaction.response.send_message(f"Um, Looks like you are not the author of the command...", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="Remove Bypass of All Ignored commands", custom_id='all', style=discord.ButtonStyle.blurple)
    async def both(self, interaction: discord.Interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        guild = self.ctx.guild
        query = "SELECT * FROM  bypass WHERE guild_id = ?"
        val = (guild.id,)
        with sqlite3.connect('database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            ig_db = cursor.fetchone()
        if ig_db is None:
            pass
        else:
            if isinstance(self.user, discord.Member):
                xd = literal_eval(ig_db['bypass_users'])
            if isinstance(self.user, discord.Role):
                xd = literal_eval(ig_db['bypass_roles'])
            if isinstance(self.user, discord.TextChannel):
                xd = literal_eval(ig_db['bypass_channels'])
            if self.user.id in xd:
                if 'cmd' in xd[self.user.id]:
                    del xd[self.user.id]['cmd']
            if isinstance(self.user, discord.Member):
                sql = (f"UPDATE bypass SET 'bypass_users' = ? WHERE guild_id = ?")
            if isinstance(self.user, discord.Role):
                sql = (f"UPDATE bypass SET 'bypass_roles' = ? WHERE guild_id = ?")
            if isinstance(self.user, discord.TextChannel):
                sql = (f"UPDATE bypass SET 'bypass_channels' = ? WHERE guild_id = ?")
            val = (f"{xd}", guild.id)
            cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        em = discord.Embed(description=f"Successfully removed bypass of all commands in the server from {self.user.mention}", color=0xc283fe).set_footer(text=self.ctx.guild.me.name, icon_url=self.ctx.guild.me.avatar.url)
        await interaction.edit_original_response(embed=em, view=None)

class rmoduledropdownmenu(discord.ui.Select):
    def __init__(self, ctx: commands.Context, opt: list, user: Union[discord.Member, discord.Role, discord.TextChannel]):
        options = []
        for i in opt:
            options.append(discord.SelectOption(label=f"{i.capitalize()}", value=i.lower()))
        if len(opt) == 0:
            super().__init__(placeholder="Select the modules to remove bypass",
                min_values=1,
                max_values=1,
                options=[discord.SelectOption(label=f"Gateway", value="Gateway")],
                disabled=True
            )
        else:
            super().__init__(placeholder="Select the modules to remove bypass",
                min_values=1,
                max_values=len(opt),
                options=options,
                disabled=False
            )
        self.ctx = ctx
        self.user = user
        self.opt = opt

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False, thinking=False)
        guild = self.ctx.guild
        query = "SELECT * FROM  bypass WHERE guild_id = ?"
        val = (guild.id,)
        with sqlite3.connect('database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            ig_db = cursor.fetchone()
        if ig_db is None:
            pass
        else:
            if isinstance(self.user, discord.Member):
                xd = literal_eval(ig_db['bypass_users'])
            if isinstance(self.user, discord.Role):
                xd = literal_eval(ig_db['bypass_roles'])
            if isinstance(self.user, discord.TextChannel):
                xd = literal_eval(ig_db['bypass_channels'])
            if self.user.id in xd:
                if 'module' in xd[self.user.id]:
                    ls = xd[self.user.id]['module']
                    for i in self.values:
                        ls.remove(str(i))
                    xd[self.user.id]['module'] = ls
                else:
                    pass
            else:
                pass
            if isinstance(self.user, discord.Member):
                sql = (f"UPDATE bypass SET 'bypass_users' = ? WHERE guild_id = ?")
            if isinstance(self.user, discord.Role):
                sql = (f"UPDATE bypass SET 'bypass_roles' = ? WHERE guild_id = ?")
            if isinstance(self.user, discord.TextChannel):
                sql = (f"UPDATE bypass SET 'bypass_channels' = ? WHERE guild_id = ?")
            val = (f"{xd}", guild.id)
            cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        ls = [str(i) for i in self.values]
        em = discord.Embed(description=f"Successfully removed bypass of `{', '.join(ls)}` modules in the server from {self.user.mention}", color=0xc283fe).set_footer(text=self.ctx.guild.me.name, icon_url=self.ctx.guild.me.avatar.url)
        await interaction.edit_original_response(embed=em, view=None)


class rmodulemenuview(discord.ui.View):
    def __init__(self, ctx: commands.Context, opt: list, user: Union[discord.Member, discord.Role, discord.TextChannel]):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.user = user
        self.add_item(moduledropdownmenu(self.ctx, opt, user))
    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and interaction.user.id not in  [978930369392951366, 979353019235840000]:
            await interaction.response.send_message(f"Um, Looks like you are not the author of the command...", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="Remove Bypass of All Ignored modules", custom_id='all', style=discord.ButtonStyle.blurple)
    async def okkkasddskk(self, interaction: discord.Interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        guild = self.ctx.guild
        query = "SELECT * FROM  bypass WHERE guild_id = ?"
        val = (guild.id,)
        with sqlite3.connect('database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            ig_db = cursor.fetchone()
        if ig_db is None:
            pass
        else:
            if isinstance(self.user, discord.Member):
                xd = literal_eval(ig_db['bypass_users'])
            if isinstance(self.user, discord.Role):
                xd = literal_eval(ig_db['bypass_roles'])
            if isinstance(self.user, discord.TextChannel):
                xd = literal_eval(ig_db['bypass_channels'])
            if self.user.id in xd:
                if 'module' in xd[self.user.id]:
                    del xd[self.user.id]['module']
            if isinstance(self.user, discord.Member):
                sql = (f"UPDATE bypass SET 'bypass_users' = ? WHERE guild_id = ?")
            if isinstance(self.user, discord.Role):
                sql = (f"UPDATE bypass SET 'bypass_roles' = ? WHERE guild_id = ?")
            if isinstance(self.user, discord.TextChannel):
                sql = (f"UPDATE bypass SET 'bypass_channels' = ? WHERE guild_id = ?")
            val = (f"{xd}", guild.id)
            cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        em = discord.Embed(description=f"Successfully removed bypass of all modules in the server from {self.user.mention}", color=0xc283fe).set_footer(text=self.ctx.guild.me.name, icon_url=self.ctx.guild.me.avatar.url)
        await interaction.edit_original_response(embed=em, view=None)

class rmainview(discord.ui.View):
    def __init__(self, ctx: commands.Context, user: Union[discord.Member, discord.Role, discord.TextChannel]):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.user = user
        if isinstance(user, discord.TextChannel):
            self._channedfdsflsss.disabled = True
        by_db = getbydata(self.ctx.guild.id)
        if by_db is not None:
            if isinstance(self.user, discord.Member):
                lss = literal_eval(by_db['bypass_users'])
            if isinstance(self.user, discord.Role):
                lss = literal_eval(by_db['bypass_roles'])
            if isinstance(self.user, discord.TextChannel):
                lss = literal_eval(by_db['bypass_channels'])
            if self.user.id in lss:
                if 'cmd' not in lss[self.user.id]:
                    self._cmdsdffsss.disabled = True
                else:
                    ls = lss[self.user.id]['cmd']
                    if len(ls) == 0:
                        self._cmdsdffsss.disabled = True
                if 'module' not in lss[self.user.id]:
                    self._moduldfdsfesss.disabled = True
                else:
                    ls = lss[self.user.id]['module']
                    if len(ls) == 0:
                        self._moduldfdsfesss.disabled = True
                if 'channel' not in lss[self.user.id]:
                    self._channedfdsflsss.disabled = True
                else:
                    ls = lss[self.user.id]['channel']
                    if len(ls) == 0:
                        self._channedfdsflsss.disabled = True
                if 'role' not in lss[self.user.id]:
                    self._rolasfasfesss.disabled = True
                else:
                    ls = lss[self.user.id]['role']
                    if len(ls) == 0:
                        self._rolasfasfesss.disabled = True
    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and interaction.user.id not in  [978930369392951366, 979353019235840000]:
            await interaction.response.send_message(f"Um, Looks like you are not the author of the command...", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="Remove Bypass of ignored commands", custom_id='cmd', style=discord.ButtonStyle.green)
    async def _cmdsdffsss(self, interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        ig_db = getigdata(self.ctx.guild.id)
        by_db = getbydata(self.ctx.guild.id)
        if ig_db is None:
            v = rcmdmenuview(self.ctx, [], self.user)
        else:
            ls = literal_eval(ig_db['cmd'])
            if len(ls) == 0:
                v = rcmdmenuview(self.ctx, [], self.user)
            else:
                ls2 = ls.copy()
                if by_db is not None:
                    if isinstance(self.user, discord.Member):
                        lss = literal_eval(by_db['bypass_users'])
                    if isinstance(self.user, discord.Role):
                        lss = literal_eval(by_db['bypass_roles'])
                    if isinstance(self.user, discord.TextChannel):
                        lss = literal_eval(by_db['bypass_channels'])
                    if self.user.id in lss:
                        if 'cmd' in lss[self.user.id]:
                            ls1 = lss[self.user.id]['cmd']
                            ls2 = []
                            for i in ls:
                                if i.lower() in ls1:
                                    ls2.append(i)
                if len(ls2) == 0:
                    v = rcmdmenuview(self.ctx, [], self.user)
                else:
                    v = rcmdmenuview(self.ctx, ls2, self.user)
        em = discord.Embed(description=f"Which commands should be removed from being bypassed by {self.user.mention}?", color=0xc283fe).set_footer(text=self.ctx.guild.me.name, icon_url=self.ctx.guild.me.avatar.url)
        await interaction.edit_original_response(embed=em, view=v)

    @discord.ui.button(label="Remove Bypass of ignored modules", custom_id='module', style=discord.ButtonStyle.green)
    async def _moduldfdsfesss(self, interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        ig_db = getigdata(self.ctx.guild.id)
        by_db = getbydata(self.ctx.guild.id)
        if ig_db is None:
            v = rmodulemenuview(self.ctx, [], self.user)
        else:
            ls = literal_eval(ig_db['module'])
            if len(ls) == 0:
                v = rmodulemenuview(self.ctx, [], self.user)
            else:
                ls2 = ls.copy()
                if by_db is not None:
                    if isinstance(self.user, discord.Member):
                        lss = literal_eval(by_db['bypass_users'])
                    if isinstance(self.user, discord.Role):
                        lss = literal_eval(by_db['bypass_roles'])
                    if isinstance(self.user, discord.TextChannel):
                        lss = literal_eval(by_db['bypass_channels'])
                    if self.user.id in lss:
                        if 'module' in lss[self.user.id]:
                            ls1 = lss[self.user.id]['module']
                            ls2 = []
                            for i in ls:
                                if i.lower() in ls1:
                                    ls2.append(i)
                if len(ls2) == 0:
                    v = rmodulemenuview(self.ctx, [], self.user)
                else:
                    v = rmodulemenuview(self.ctx, ls2, self.user)
        em = discord.Embed(description=f"Which modules should be removed from being bypassed by {self.user.mention}?", color=0xc283fe).set_footer(text=self.ctx.guild.me.name, icon_url=self.ctx.guild.me.avatar.url)
        await interaction.edit_original_response(embed=em, view=v)

    @discord.ui.button(label="Remove Bypass of ignored channels", custom_id='channel', style=discord.ButtonStyle.green)
    async def _channedfdsflsss(self, interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        ig_db = getigdata(self.ctx.guild.id)
        by_db = getbydata(self.ctx.guild.id)
        if ig_db is None:
            v = rchannelmenuview(self.ctx, [], self.user)
        else:
            ls = literal_eval(ig_db['channel'])
            if len(ls) == 0:
                v = rchannelmenuview(self.ctx, [], self.user)
            else:
                ls2 = ls.copy()
                if by_db is not None:
                    if isinstance(self.user, discord.Member):
                        lss = literal_eval(by_db['bypass_users'])
                    if isinstance(self.user, discord.Role):
                        lss = literal_eval(by_db['bypass_roles'])
                    if isinstance(self.user, discord.TextChannel):
                        lss = literal_eval(by_db['bypass_channels'])
                    if self.user.id in lss:
                        if 'channel' in lss[self.user.id]:
                            ls1 = lss[self.user.id]['channel']
                            ls2 = []
                            for i in ls:
                                if i.lower() in ls1:
                                    ls2.append(i)
                if len(ls2) == 0:
                    v = rchannelmenuview(self.ctx, [], self.user)
                else:
                    v = rchannelmenuview(self.ctx, ls2, self.user)
        em = discord.Embed(description=f"Which channel should be removed from being bypassed by {self.user.mention}?", color=0xc283fe).set_footer(text=self.ctx.guild.me.name, icon_url=self.ctx.guild.me.avatar.url)
        await interaction.edit_original_response(embed=em, view=v)

    @discord.ui.button(label="Remove Bypass of ignored roles", custom_id='role', style=discord.ButtonStyle.green)
    async def _rolasfasfesss(self, interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        ig_db = getigdata(self.ctx.guild.id)
        by_db = getbydata(self.ctx.guild.id)
        if ig_db is None:
            v = rrolemenuview(self.ctx, [], self.user)
        else:
            ls = literal_eval(ig_db['role'])
            if len(ls) == 0:
                v = rrolemenuview(self.ctx, [], self.user)
            else:
                ls2 = ls.copy()
                if by_db is not None:
                    if isinstance(self.user, discord.Member):
                        lss = literal_eval(by_db['bypass_users'])
                    if isinstance(self.user, discord.Role):
                        lss = literal_eval(by_db['bypass_roles'])
                    if isinstance(self.user, discord.TextChannel):
                        lss = literal_eval(by_db['bypass_channels'])
                    if self.user.id in lss:
                        if 'role' in lss[self.user.id]:
                            ls1 = lss[self.user.id]['role']
                            ls2 = []
                            for i in ls:
                                if i.lower() in ls1:
                                    ls2.append(i)
                if len(ls2) == 0:
                    v = rrolemenuview(self.ctx, [], self.user)
                else:
                    v = rrolemenuview(self.ctx, ls2, self.user)
        em = discord.Embed(description=f"Which roles should be removed from being bypassed by {self.user.mention}?", color=0xc283fe).set_footer(text=self.ctx.guild.me.name, icon_url=self.ctx.guild.me.avatar.url)
        await interaction.edit_original_response(embed=em, view=v)

    @discord.ui.button(label="Remove All bypass ignorence", custom_id='all', style=discord.ButtonStyle.blurple)
    async def alfasfll(self, interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        query = "SELECT * FROM  bypass WHERE guild_id = ?"
        val = (self.ctx.guild.id,)
        with sqlite3.connect('database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            ig_db = cursor.fetchone()
        if ig_db is None:
            pass
        else:
            if isinstance(self.user, discord.Member):
                xd = literal_eval(ig_db['bypass_users'])
            if isinstance(self.user, discord.Role):
                xd = literal_eval(ig_db['bypass_roles'])
            if isinstance(self.user, discord.TextChannel):
                xd = literal_eval(ig_db['bypass_channels'])
            if self.user.id in xd:      
                del xd[self.user.id]
            if isinstance(self.user, discord.Member):
                sql = (f"UPDATE bypass SET 'bypass_users' = ? WHERE guild_id = ?")
            if isinstance(self.user, discord.Role):
                sql = (f"UPDATE bypass SET 'bypass_roles' = ? WHERE guild_id = ?")
            if isinstance(self.user, discord.TextChannel):
                sql = (f"UPDATE bypass SET 'bypass_channels' = ? WHERE guild_id = ?")
            val = (f"{xd}", self.ctx.guild.id)
            cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        em = discord.Embed(description=f"Successfully removed bypass of all types of ignorence in the server from {self.user.mention}", color=0xc283fe).set_footer(text=self.ctx.guild.me.name, icon_url=self.ctx.guild.me.avatar.url)
        await interaction.edit_original_response(embed=em, view=None)

class ignore(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, name="ignore", description="Shows The help menu for ignore")
    async def ignore(self, ctx:commands.Context):
        prefix = ctx.prefix
        if prefix == f"<@{self.bot.user.id}> ":
            prefix = f"@{str(self.bot.user)} "
        xd = discord.utils.get(self.bot.users, id=978930369392951366)
        anay = str(xd)
        pfp = xd.display_avatar.url
        listem = discord.Embed(colour=0xc283fe,
                                     description=f"<...> Duty | [...] Optional\n\n" 
                                                  f"`{prefix}ignore`\n" 
                                                  f"Shows The help menu for ignore\n\n" 
                                                  f"`{prefix}ignore user`\n" 
                                                  f"Ignores a user\n\n"
                                                  f"`{prefix}ignore channel`\n"
                                                  f"Ignores a channel\n\n"
                                                  f"`{prefix}ignore role`\n"
                                                  f"Ignores a role\n\n"
                                                  f"`{prefix}ignore command`\n"
                                                  f"Ignores a command\n\n"
                                                  f"`{prefix}ignore module`\n"
                                                  f"Ignores a module\n\n"
                                                  f"`{prefix}ignore bypass`\n"
                                                  f"Shows The help menu for ignore bypass\n\n")
        listem.set_author(name=f"{str(ctx.author)}", icon_url=ctx.author.display_avatar.url)
        listem.set_footer(text=f"Made by stars.gg" ,  icon_url=pfp)
        await ctx.send(embed=listem)
    
    @ignore.group(invoke_without_command=True, name="bypass", description="Shows The help menu for ignore bypass")
    async def _bypass(self, ctx: commands.Context):
        prefix = ctx.prefix
        if prefix == f"<@{self.bot.user.id}> ":
            prefix = f"@{str(self.bot.user)} "
        xd = discord.utils.get(self.bot.users, id=978930369392951366)
        anay = str(xd)
        pfp = xd.display_avatar.url
        listem = discord.Embed(colour=0xc283fe,
                                     description=f"<...> Duty | [...] Optional\n\n" 
                                                  f"`{prefix}ignore bypass`\n" 
                                                  f"Shows The help menu for ignore bypass\n\n" 
                                                  f"`{prefix}ignore bypass user`\n" 
                                                  f"Let a user bypass the ignore\n\n"
                                                  f"`{prefix}ignore bypass role`\n"
                                                  f"Let a role bypass the ignore\n\n"
                                                  f"`{prefix}ignore bypass channel`\n"
                                                  f"Let a channel bypass the ignore\n\n")
        listem.set_author(name=f"{str(ctx.author)}", icon_url=ctx.author.display_avatar.url)
        listem.set_footer(text=f"Made by stars.gg" ,  icon_url=pfp)
        await ctx.send(embed=listem)
    
    @_bypass.group(invoke_without_command=True, name="user", aliases=["users"], description="Let a user bypass the ignore")
    async def __user(self, ctx: commands.Context):
        prefix = ctx.prefix
        if prefix == f"<@{self.bot.user.id}> ":
            prefix = f"@{str(self.bot.user)} "
        xd = discord.utils.get(self.bot.users, id=978930369392951366)
        anay = str(xd)
        pfp = xd.display_avatar.url
        listem = discord.Embed(colour=0xc283fe,
                                     description=f"<...> Duty | [...] Optional\n\n" 
                                                  f"`{prefix}ignore bypass user`\n" 
                                                  f"Let a user bypass the ignore\n\n"
                                                  f"`{prefix}ignore bypass user add`\n"
                                                  f"Adds a user to ignore bypass list\n\n"
                                                  f"`{prefix}ignore bypass user remove`\n"
                                                  f"Removes a user from ignore bypass list\n\n")
                                                  #f"`{prefix}ignore bypass user show`\n"
                                                  #f"Shows you the current ignore bypass users list\n\n")
        listem.set_author(name=f"{str(ctx.author)}", icon_url=ctx.author.display_avatar.url)
        listem.set_footer(text=f"Made by stars.gg" ,  icon_url=pfp)
        await ctx.send(embed=listem)
    
    @__user.command(name="add", description="Adds a user to ignore bypass list")
    @commands.has_guild_permissions(administrator=True)
    async def __add(self, ctx: commands.Context, *, user: discord.Member):
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
        ig_db = getigdata(ctx.guild.id)
        by_db = getbydata(ctx.guild.id)
        c = 0
        if by_db is not None:
            lss = literal_eval(by_db['bypass_users'])
            if user.id in lss:
                if 'cmd' in lss[user.id]:
                    if lss[user.id]['cmd'] == "all":
                        c+=1
                if 'module' in lss[user.id]:
                    if lss[user.id]['module'] == "all":
                        c+=1
                if 'channel' in lss[user.id]:
                    if lss[user.id]['channel'] == "all":
                        c+=1
                if 'role' in lss[user.id]:
                    if lss[user.id]['role'] == "all":
                        c+=1
        if c == 4:
            return await ctx.reply(embed=discord.Embed(description=f"{user.mention} is already bypassed for all types of ignorance in the server", color=0xff0000))
        if ig_db is not None:
            xd = literal_eval(ig_db['user'])
            if user.id in xd:
                return await ctx.reply(embed=discord.Embed(description=f"{user.mention} is being ignored by the bot. In order to let him bypass the ignore first removed him from being ignored by typing `{ctx.prefix}ignore user remove {user.mention}`", color=0xff0000))
        em = discord.Embed(description=f"Which type of bypass should be given to {user.mention}", color=0xc283fe).set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        v = mainview(ctx, user)
        await ctx.reply(embed=em, view=v)
            
    @__user.command(name="remove", description="Removes a user from ignore bypass list")
    @commands.has_guild_permissions(administrator=True)
    async def __remove(self, ctx: commands.Context, *, user: discord.Member):
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
        ig_db = getigdata(ctx.guild.id)
        by_db = getbydata(ctx.guild.id)
        c = 0
        if by_db is not None:
            lss = literal_eval(by_db['bypass_users'])
            if user.id in lss:
                if 'cmd' not in lss[user.id]:
                    c+=1
                else:
                    ls = lss[user.id]['cmd']
                    if len(ls) == 0:
                        c+=1
                if 'module' not in lss[user.id]:
                    c+=1
                else:
                    ls = lss[user.id]['module']
                    if len(ls) == 0:
                        c+=1
                if 'channel' not in lss[user.id]:
                    c+=1
                else:
                    ls = lss[user.id]['channel']
                    if len(ls) == 0:
                        c+=1
                if 'role' not in lss[user.id]:
                    c+=1
                else:
                    ls = lss[user.id]['role']
                    if len(ls) == 0:
                        c+=1
            else:
                c = 4
        if c == 4:
            return await ctx.reply(embed=discord.Embed(description=f"{user.mention} is not bypassed for any type of ignorance in the server", color=0xff0000))
        em = discord.Embed(description=f"Which type of bypass should be remove from {user.mention}", color=0xc283fe).set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        v = rmainview(ctx, user)
        await ctx.reply(embed=em, view=v)

    @_bypass.group(invoke_without_command=True, name="role", aliases=["roles"], description="Let a role bypass the ignore")
    async def __role(self, ctx: commands.Context):
        prefix = ctx.prefix
        if prefix == f"<@{self.bot.user.id}> ":
            prefix = f"@{str(self.bot.user)} "
        xd = discord.utils.get(self.bot.users, id=978930369392951366)
        anay = str(xd)
        pfp = xd.display_avatar.url
        listem = discord.Embed(colour=0xc283fe,
                                     description=f"<...> Duty | [...] Optional\n\n" 
                                                  f"`{prefix}ignore bypass role`\n" 
                                                  f"Let a role bypass the ignore\n\n"
                                                  f"`{prefix}ignore bypass role add`\n"
                                                  f"Adds a role to ignore bypass list\n\n"
                                                  f"`{prefix}ignore bypass role remove`\n"
                                                  f"Removes a role from ignore bypass list\n\n")
                                                  #f"`{prefix}ignore bypass role show`\n"
                                                  #f"Shows you the current ignore bypass role list\n\n")
        listem.set_author(name=f"{str(ctx.author)}", icon_url=ctx.author.display_avatar.url)
        listem.set_footer(text=f"Made by stars.gg" ,  icon_url=pfp)
        await ctx.send(embed=listem)
            
    @__role.command(name="add", description="Adds a role to ignore bypass list")
    @commands.has_guild_permissions(administrator=True)
    async def __addd(self, ctx: commands.Context, *, role: discord.Role):
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
        ig_db = getigdata(ctx.guild.id)
        by_db = getbydata(ctx.guild.id)
        c = 0
        if by_db is not None:
            lss = literal_eval(by_db['bypass_roles'])
            if role.id in lss:
                if 'cmd' in lss[role.id]:
                    if lss[role.id]['cmd'] == "all":
                        c+=1
                if 'module' in lss[role.id]:
                    if lss[role.id]['module'] == "all":
                        c+=1
                if 'channel' in lss[role.id]:
                    if lss[role.id]['channel'] == "all":
                        c+=1
                if 'role' in lss[role.id]:
                    if lss[role.id]['role'] == "all":
                        c+=1
        if c == 4:
            return await ctx.reply(embed=discord.Embed(description=f"{role.mention} is already bypassed for all types of ignorance in the server", color=0xff0000))
        if ig_db is not None:
            xd = literal_eval(ig_db['role'])
            if role.id in xd:
                return await ctx.reply(embed=discord.Embed(description=f"{role.mention} is being ignored by the bot. In order to let him bypass the ignore first removed him from being ignored by typing `{ctx.prefix}ignore role remove {role.mention}`", color=0xff0000))
        em = discord.Embed(description=f"Which type of bypass should be given to {role.mention}", color=0xc283fe).set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        v = mainview(ctx, role)
        await ctx.reply(embed=em, view=v)

    @__role.command(name="remove", description="Removes a role from ignore bypass list")
    @commands.has_guild_permissions(administrator=True)
    async def __removee(self, ctx: commands.Context, *, role: discord.Role):
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
        ig_db = getigdata(ctx.guild.id)
        by_db = getbydata(ctx.guild.id)
        c = 0
        if by_db is not None:
            lss = literal_eval(by_db['bypass_roles'])
            if role.id in lss:
                if 'cmd' not in lss[role.id]:
                    c+=1
                else:
                    ls = lss[role.id]['cmd']
                    if len(ls) == 0:
                        c+=1
                if 'module' not in lss[role.id]:
                    c+=1
                else:
                    ls = lss[role.id]['module']
                    if len(ls) == 0:
                        c+=1
                if 'channel' not in lss[role.id]:
                    c+=1
                else:
                    ls = lss[role.id]['channel']
                    if len(ls) == 0:
                        c+=1
                if 'role' not in lss[role.id]:
                    c+=1
                else:
                    ls = lss[role.id]['role']
                    if len(ls) == 0:
                        c+=1
            else:
                c = 4
        if c == 4:
            return await ctx.reply(embed=discord.Embed(description=f"{role.mention} is not bypassed for any type of ignorance in the server", color=0xff0000))
        em = discord.Embed(description=f"Which type of bypass should be remove from {role.mention}", color=0xc283fe).set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        v = rmainview(ctx, role)
        await ctx.reply(embed=em, view=v)
        
    @_bypass.group(invoke_without_command=True, name="channel", aliases=["channels"], description="Let a channel bypass the ignore")
    async def __channel(self, ctx: commands.Context):
        prefix = ctx.prefix
        if prefix == f"<@{self.bot.user.id}> ":
            prefix = f"@{str(self.bot.user)} "
        xd = discord.utils.get(self.bot.users, id=978930369392951366)
        anay = str(xd)
        pfp = xd.display_avatar.url
        listem = discord.Embed(colour=0xc283fe,
                                     description=f"<...> Duty | [...] Optional\n\n" 
                                                  f"`{prefix}ignore bypass channel`\n" 
                                                  f"Let a channel bypass the ignore\n\n"
                                                  f"`{prefix}ignore bypass channel add`\n"
                                                  f"Adds a channel to ignore bypass list\n\n"
                                                  f"`{prefix}ignore bypass channel remove`\n"
                                                  f"Removes a chanel from ignore bypass list\n\n")
                                                  #f"`{prefix}ignore bypass channel show`\n"
                                                  #f"Shows you the current ignore bypass channel list\n\n")
        listem.set_author(name=f"{str(ctx.author)}", icon_url=ctx.author.display_avatar.url)
        listem.set_footer(text=f"Made by stars.gg" ,  icon_url=pfp)
        await ctx.send(embed=listem)
                
    @__channel.command(name="add", description="Adds a channel to ignore bypass list")
    @commands.has_guild_permissions(administrator=True)
    async def __addddd(self, ctx: commands.Context, *, channel: discord.TextChannel):
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
        ig_db = getigdata(ctx.guild.id)
        by_db = getbydata(ctx.guild.id)
        c = 0
        if by_db is not None:
            lss = literal_eval(by_db['bypass_channels'])
            if channel.id in lss:
                if 'cmd' in lss[channel.id]:
                    if lss[channel.id]['cmd'] == "all":
                        c+=1
                if 'module' in lss[channel.id]:
                    if lss[channel.id]['module'] == "all":
                        c+=1
                if 'role' in lss[channel.id]:
                    if lss[channel.id]['role'] == "all":
                        c+=1
        if c == 3:
            return await ctx.reply(embed=discord.Embed(description=f"{channel.mention} is already bypassed for all types of ignorance in the server", color=0xff0000))
        if ig_db is not None:
            xd = literal_eval(ig_db['channel'])
            if channel.id in xd:
                return await ctx.reply(embed=discord.Embed(description=f"{channel.mention} is being ignored by the bot. In order to let him bypass the ignore first removed him from being ignored by typing `{ctx.prefix}ignore channel remove {channel.mention}`", color=0xff0000))
        em = discord.Embed(description=f"Which type of bypass should be given to {channel.mention}", color=0xc283fe).set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        v = mainview(ctx, channel)
        await ctx.reply(embed=em, view=v)

    @__channel.command(name="remove", description="Removes a channel from ignore bypass list")
    @commands.has_guild_permissions(administrator=True)
    async def __removeee(self, ctx: commands.Context, *, channel: discord.TextChannel):
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
        ig_db = getigdata(ctx.guild.id)
        by_db = getbydata(ctx.guild.id)
        c = 0
        if by_db is not None:
            lss = literal_eval(by_db['bypass_channels'])
            if channel.id in lss:
                if 'cmd' not in lss[channel.id]:
                    c+=1
                else:
                    ls = lss[channel.id]['cmd']
                    if len(ls) == 0:
                        c+=1
                if 'module' not in lss[channel.id]:
                    c+=1
                else:
                    ls = lss[channel.id]['module']
                    if len(ls) == 0:
                        c+=1
                if 'role' not in lss[channel.id]:
                    c+=1
                else:
                    ls = lss[channel.id]['role']
                    if len(ls) == 0:
                        c+=1
            else:
                c = 3
        if c == 3:
            return await ctx.reply(embed=discord.Embed(description=f"{channel.mention} is not bypassed for any type of ignorance in the server", color=0xff0000))
        em = discord.Embed(description=f"Which type of bypass should be remove from {channel.mention}", color=0xc283fe).set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        v = rmainview(ctx, channel)
        await ctx.reply(embed=em, view=v)

    @ignore.group(invoke_without_command=True, name="user", aliases=["users"], description="Shows The help menu for ignore user")
    async def _user(self, ctx: commands.Context):
        prefix = ctx.prefix
        if prefix == f"<@{self.bot.user.id}> ":
            prefix = f"@{str(self.bot.user)} "
        xd = discord.utils.get(self.bot.users, id=978930369392951366)
        anay = str(xd)
        pfp = xd.display_avatar.url
        listem = discord.Embed(colour=0xc283fe,
                                     description=f"<...> Duty | [...] Optional\n\n" 
                                                  f"`{prefix}ignore user`\n" 
                                                  f"Shows The help menu for ignore user\n\n"
                                                  f"`{prefix}ignore user add`\n"
                                                  f"Adds a user to ignore list\n\n"
                                                  f"`{prefix}ignore user remove`\n"
                                                  f"Removes a user from ignore list\n\n"
                                                  f"`{prefix}ignore user show`\n"
                                                  f"Shows you the current list\n\n")
        listem.set_author(name=f"{str(ctx.author)}", icon_url=ctx.author.display_avatar.url)
        listem.set_footer(text=f"Made by stars.gg" ,  icon_url=pfp)
        await ctx.send(embed=listem)
    
    @_user.command(name="add", description="Adds a user to ignore list")
    @commands.has_guild_permissions(administrator=True)
    async def _add(self, ctx: commands.Context, *, user: discord.Member):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 979353019235840000]:
                em = discord.Embed(description=f"<:error:1153009680428318791>You must Have Higher Role than Bot To run This Command", color=0xff0000)
                return await ctx.send(embed=em)
        query = "SELECT * FROM  ignore WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            ig_db = cursor.fetchone()
        if ig_db is None:
            xd = [user.id]
            sql = (f"INSERT INTO ignore(guild_id, user) VALUES(?, ?)")
            val = (ctx.guild.id, f"{xd}")
            cursor.execute(sql, val)
        else:
            xd = literal_eval(ig_db['user'])
            if user.id in xd:
                return await ctx.reply(embed=discord.Embed(description=f"{user.mention} is already being ignored by the bot", color=0xff0000))
            else:
                xd.append(user.id)
            sql = (f"UPDATE ignore SET user = ? WHERE guild_id = ?")
            val = (f"{xd}", ctx.guild.id)
            cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        return await ctx.reply(embed=discord.Embed(description=f"Now onwards {user.mention} will be ignored by the bot.", color=0xc283fe))
    
    @_user.command(name="remove", description="Removes a user from ignore list")
    @commands.has_guild_permissions(administrator=True)
    async def _remove(self, ctx: commands.Context, *, user: discord.Member):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 979353019235840000]:
                em = discord.Embed(description=f"<:error:1153009680428318791>You must Have Higher Role than Bot To run This Command", color=0xff0000)
                return await ctx.send(embed=em)
        query = "SELECT * FROM  ignore WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            ig_db = cursor.fetchone()
        if ig_db is None:
            return await ctx.reply(embed=discord.Embed(description=f"{user.mention} is already not being ignored by the bot", color=0xff0000))
        else:
            xd = literal_eval(ig_db['user'])
            if user.id not in xd:
                return await ctx.reply(embed=discord.Embed(description=f"{user.mention} is already not being ignored by the bot", color=0xff0000))
            else:
                xd.remove(user.id)
            sql = (f"UPDATE ignore SET user = ? WHERE guild_id = ?")
            val = (f"{xd}", ctx.guild.id)
            cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        return await ctx.reply(embed=discord.Embed(description=f"Now onwards {user.mention} will not be ignored by the bot.", color=0xc283fe))
    
    @_user.command(name="show", aliases=['list'], description="Shows you the current ignored users list")
    @commands.has_guild_permissions(administrator=True)
    async def _show(self, ctx: commands.Context):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 979353019235840000]:
                em = discord.Embed(description=f"<:error:1153009680428318791>You must Have Higher Role than Bot To run This Command", color=0xff0000)
                return await ctx.send(embed=em)
        query = "SELECT * FROM  ignore WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            ig_db = cursor.fetchone()
        if ig_db is None:
            return await ctx.reply(embed=discord.Embed(description=f"No users are being ignored in the server", color=0xff0000))
        else:
            xd = literal_eval(ig_db['user'])
            if len(xd) == 0:
                return await ctx.reply(embed=discord.Embed(description=f"No users are being ignored in the server", color=0xff0000))
        ls = []
        for i in xd:
            u = discord.utils.get(ctx.guild.members, id=i)
            if u is not None:
                ls.append(u.mention)
        em = discord.Embed(title=f"Ignored users - {len(xd)}", description="\n".join(ls), color=0xc283fe).set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        await ctx.reply(embed=em)

    @ignore.group(invoke_without_command=True, name="channel", aliases=["channels"], description="Shows The help menu for ignore channel")
    async def _channel(self, ctx: commands.Context):
        prefix = ctx.prefix
        if prefix == f"<@{self.bot.user.id}> ":
            prefix = f"@{str(self.bot.user)} "
        xd = discord.utils.get(self.bot.users, id=978930369392951366)
        anay = str(xd)
        pfp = xd.display_avatar.url
        listem = discord.Embed(colour=0xc283fe,
                                     description=f"<...> Duty | [...] Optional\n\n" 
                                                  f"`{prefix}ignore channel`\n" 
                                                  f"Shows The help menu for ignore channel\n\n"
                                                  f"`{prefix}ignore channel add`\n"
                                                  f"Adds a channel to ignore list\n\n"
                                                  f"`{prefix}ignore channel remove`\n"
                                                  f"Removes a channel from ignore list\n\n"
                                                  f"`{prefix}ignore channel show`\n"
                                                  f"Shows you the current list\n\n")
        listem.set_author(name=f"{str(ctx.author)}", icon_url=ctx.author.display_avatar.url)
        listem.set_footer(text=f"Made by stars.gg" ,  icon_url=pfp)
        await ctx.send(embed=listem)
    
    @_channel.command(name="add", description="Adds a channel to ignore list")
    @commands.has_guild_permissions(administrator=True)
    async def _addd(self, ctx: commands.Context, *, channel: discord.TextChannel):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 979353019235840000]:
                em = discord.Embed(description=f"<:error:1153009680428318791>You must Have Higher Role than Bot To run This Command", color=0xff0000)
                return await ctx.send(embed=em)
        query = "SELECT * FROM  ignore WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            ig_db = cursor.fetchone()
        if ig_db is None:
            xd = [channel.id]
            sql = (f"INSERT INTO ignore(guild_id, channel) VALUES(?, ?)")
            val = (ctx.guild.id, f"{xd}")
            cursor.execute(sql, val)
        else:
            xd = literal_eval(ig_db['channel'])
            if channel.id in xd:
                return await ctx.reply(embed=discord.Embed(description=f"{channel.mention} is already being ignored by the bot", color=0xff0000))
            else:
                xd.append(channel.id)
            sql = (f"UPDATE ignore SET channel = ? WHERE guild_id = ?")
            val = (f"{xd}", ctx.guild.id)
            cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        return await ctx.reply(embed=discord.Embed(description=f"Now onwards {channel.mention} will be ignored by the bot.", color=0xc283fe))
    
    @_channel.command(name="remove", description="Removes a channel to ignore list")
    @commands.has_guild_permissions(administrator=True)
    async def _removee(self, ctx: commands.Context, *, channel: discord.TextChannel):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 979353019235840000]:
                em = discord.Embed(description=f"<:error:1153009680428318791>You must Have Higher Role than Bot To run This Command", color=0xff0000)
                return await ctx.send(embed=em)
        query = "SELECT * FROM  ignore WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            ig_db = cursor.fetchone()
        if ig_db is None:
            return await ctx.reply(embed=discord.Embed(description=f"{channel.mention} is already not being ignored by the bot", color=0xff0000))
        else:
            xd = literal_eval(ig_db['channel'])
            if channel.id not in xd:
                return await ctx.reply(embed=discord.Embed(description=f"{channel.mention} is already not being ignored by the bot", color=0xff0000))
            else:
                xd.remove(channel.id)
            sql = (f"UPDATE ignore SET channel = ? WHERE guild_id = ?")
            val = (f"{xd}", ctx.guild.id)
            cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        return await ctx.reply(embed=discord.Embed(description=f"Now onwards {channel.mention} will not be ignored by the bot.", color=0xc283fe))
    
    @_channel.command(name="show", aliases=['list'], description="Shows you the current ignored channels list")
    @commands.has_guild_permissions(administrator=True)
    async def _showw(self, ctx: commands.Context):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 979353019235840000]:
                em = discord.Embed(description=f"<:error:1153009680428318791>You must Have Higher Role than Bot To run This Command", color=0xff0000)
                return await ctx.send(embed=em)
        query = "SELECT * FROM  ignore WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            ig_db = cursor.fetchone()
        if ig_db is None:
            return await ctx.reply(embed=discord.Embed(description=f"No channels are being ignored in the server", color=0xff0000))
        else:
            xd = literal_eval(ig_db['channel'])
            if len(xd) == 0:
                return await ctx.reply(embed=discord.Embed(description=f"No channels are being ignored in the server", color=0xff0000))
        ls = []
        for i in xd:
            u = discord.utils.get(ctx.guild.channels, id=i)
            if u is not None:
                ls.append(u.mention)
        em = discord.Embed(title=f"Ignored channels - {len(xd)}", description="\n".join(ls), color=0xc283fe).set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        await ctx.reply(embed=em)

    @ignore.group(invoke_without_command=True, name="role", aliases=["roles"], description="Shows The help menu for ignore role")
    async def _role(self, ctx: commands.Context):
        prefix = ctx.prefix
        if prefix == f"<@{self.bot.user.id}> ":
            prefix = f"@{str(self.bot.user)} "
        xd = discord.utils.get(self.bot.users, id=978930369392951366)
        anay = str(xd)
        pfp = xd.display_avatar.url
        listem = discord.Embed(colour=0xc283fe,
                                     description=f"<...> Duty | [...] Optional\n\n" 
                                                  f"`{prefix}ignore role`\n" 
                                                  f"Shows The help menu for ignore role\n\n"
                                                  f"`{prefix}ignore role add`\n"
                                                  f"Adds a role to ignore list\n\n"
                                                  f"`{prefix}ignore role remove`\n"
                                                  f"Removes a role from ignore list\n\n"
                                                  f"`{prefix}ignore role show`\n"
                                                  f"Shows you the current list\n\n")
        listem.set_author(name=f"{str(ctx.author)}", icon_url=ctx.author.display_avatar.url)
        listem.set_footer(text=f"Made by stars.gg" ,  icon_url=pfp)
        await ctx.send(embed=listem)
    
    @_role.command(name="add", description="Adds a role to ignore list")
    @commands.has_guild_permissions(administrator=True)
    async def _adddd(self, ctx: commands.Context, *, role: discord.Role):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 979353019235840000]:
                em = discord.Embed(description=f"<:error:1153009680428318791>You must Have Higher Role than Bot To run This Command", color=0xff0000)
                return await ctx.send(embed=em)
        query = "SELECT * FROM  ignore WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            ig_db = cursor.fetchone()
        if ig_db is None:
            xd = [role.id]
            sql = (f"INSERT INTO ignore(guild_id, role) VALUES(?, ?)")
            val = (ctx.guild.id, f"{xd}")
            cursor.execute(sql, val)
        else:
            xd = literal_eval(ig_db['role'])
            if role.id in xd:
                return await ctx.reply(embed=discord.Embed(description=f"{role.mention} is already being ignored by the bot", color=0xff0000))
            else:
                xd.append(role.id)
            sql = (f"UPDATE ignore SET role = ? WHERE guild_id = ?")
            val = (f"{xd}", ctx.guild.id)
            cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        return await ctx.reply(embed=discord.Embed(description=f"Now onwards {role.mention} will be ignored by the bot.", color=0xc283fe))
    
    @_role.command(name="remove", description="Removes a role from ignore list")
    @commands.has_guild_permissions(administrator=True)
    async def _removeee(self, ctx: commands.Context, *, role: discord.Role):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 979353019235840000]:
                em = discord.Embed(description=f"<:error:1153009680428318791>You must Have Higher Role than Bot To run This Command", color=0xff0000)
                return await ctx.send(embed=em)
        query = "SELECT * FROM  ignore WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            ig_db = cursor.fetchone()
        if ig_db is None:
            return await ctx.reply(embed=discord.Embed(description=f"{role.mention} is already not being ignored by the bot", color=0xff0000))
        else:
            xd = literal_eval(ig_db['role'])
            if role.id not in xd:
                return await ctx.reply(embed=discord.Embed(description=f"{role.mention} is already not being ignored by the bot", color=0xff0000))
            else:
                xd.remove(role.id)
            sql = (f"UPDATE ignore SET role = ? WHERE guild_id = ?")
            val = (f"{xd}", ctx.guild.id)
            cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        return await ctx.reply(embed=discord.Embed(description=f"Now onwards {role.mention} will not be ignored by the bot.", color=0xc283fe))
    
    @_role.command(name="show", aliases=['list'], description="Shows you the current ignored roles list")
    @commands.has_guild_permissions(administrator=True)
    async def _showww(self, ctx: commands.Context):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 979353019235840000]:
                em = discord.Embed(description=f"<:error:1153009680428318791>You must Have Higher Role than Bot To run This Command", color=0xff0000)
                return await ctx.send(embed=em)
        query = "SELECT * FROM  ignore WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            ig_db = cursor.fetchone()
        if ig_db is None:
            return await ctx.reply(embed=discord.Embed(description=f"No roles are being ignored in the server", color=0xff0000))
        else:
            xd = literal_eval(ig_db['role'])
            if len(xd) == 0:
                return await ctx.reply(embed=discord.Embed(description=f"No roles are being ignored in the server", color=0xff0000))
        ls = []
        for i in xd:
            u = discord.utils.get(ctx.guild.roles, id=i)
            if u is not None:
                ls.append(u.mention)
        em = discord.Embed(title=f"Ignored roles - {len(xd)}", description="\n".join(ls), color=0xc283fe).set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        await ctx.reply(embed=em)

    @ignore.group(invoke_without_command=True, name="command", aliases=["commands", "cmd", "cmds"], description="Shows The help menu for ignore command")
    async def _cmd(self, ctx: commands.Context):
        prefix = ctx.prefix
        if prefix == f"<@{self.bot.user.id}> ":
            prefix = f"@{str(self.bot.user)} "
        xd = discord.utils.get(self.bot.users, id=978930369392951366)
        anay = str(xd)
        pfp = xd.display_avatar.url
        listem = discord.Embed(colour=0xc283fe,
                                     description=f"<...> Duty | [...] Optional\n\n" 
                                                  f"`{prefix}ignore command`\n" 
                                                  f"Shows The help menu for ignore command\n\n"
                                                  f"`{prefix}ignore command add`\n"
                                                  f"Adds a command to ignore list\n\n"
                                                  f"`{prefix}ignore command remove`\n"
                                                  f"Removes a command from ignore list\n\n"
                                                  f"`{prefix}ignore command show`\n"
                                                  f"Shows you the current list\n\n")
        listem.set_author(name=f"{str(ctx.author)}", icon_url=ctx.author.display_avatar.url)
        listem.set_footer(text=f"Made by stars.gg" ,  icon_url=pfp)
        await ctx.send(embed=listem)
        
    @_cmd.command(name="add", description="Adds a command to ignore list")
    @commands.has_guild_permissions(administrator=True)
    async def _addddd(self, ctx: commands.Context, *, command: str):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 979353019235840000]:
                em = discord.Embed(description=f"<:error:1153009680428318791>You must Have Higher Role than Bot To run This Command", color=0xff0000)
                return await ctx.send(embed=em)
        query = "SELECT * FROM  ignore WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            ig_db = cursor.fetchone()
        cmd = self.bot.get_command(command)
        if cmd is None:
            return await ctx.reply(embed=discord.Embed(description=f"No command found named `{command}`", color=0xff0000), mention_author=False)
        if str(cmd.cog_name.lower()) == "ignore":
            return await ctx.reply(embed=discord.Embed(description=f"Ignore commands cant be ignored", color=0xff0000), mention_author=False)
        if ig_db is None:
            xd = [cmd.qualified_name]
            sql = (f"INSERT INTO ignore(guild_id, cmd) VALUES(?, ?)")
            val = (ctx.guild.id, f"{xd}")
            cursor.execute(sql, val)
        else:
            xd = literal_eval(ig_db['cmd'])
            if cmd.qualified_name in xd:
                return await ctx.reply(embed=discord.Embed(description=f"`{cmd.qualified_name}` command is already being ignored by the bot", color=0xff0000))
            else:
                xd.append(cmd.qualified_name)
            sql = (f"UPDATE ignore SET cmd = ? WHERE guild_id = ?")
            val = (f"{xd}", ctx.guild.id)
            cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        return await ctx.reply(embed=discord.Embed(description=f"Now onwards `{cmd.qualified_name}` command will be ignored by the bot.", color=0xc283fe))
    
    @_cmd.command(name="remove", description="Removes a command from ignore list")
    @commands.has_guild_permissions(administrator=True)
    async def _removeeee(self, ctx: commands.Context, *, command: str):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 979353019235840000]:
                em = discord.Embed(description=f"<:error:1153009680428318791>You must Have Higher Role than Bot To run This Command", color=0xff0000)
                return await ctx.send(embed=em)
        cmd = self.bot.get_command(command)
        if cmd is None:
            return await ctx.reply(embed=discord.Embed(description=f"No command found named `{command}`", color=0xff0000), mention_author=False)
        if str(cmd.cog_name.lower()) == "ignore":
            return await ctx.reply(embed=discord.Embed(description=f"Ignore commands cant be ignored", color=0xff0000), mention_author=False)
        query = "SELECT * FROM  ignore WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            ig_db = cursor.fetchone()
        if ig_db is None:
            return await ctx.reply(embed=discord.Embed(description=f"`{cmd.qualified_name}` command is already not being ignored by the bot", color=0xff0000))
        else:
            xd = literal_eval(ig_db['cmd'])
            if cmd.qualified_name not in xd:
                return await ctx.reply(embed=discord.Embed(description=f"`{cmd.qualified_name}` command is already not being ignored by the bot", color=0xff0000))
            else:
                xd.remove(cmd.qualified_name)
            sql = (f"UPDATE ignore SET cmd = ? WHERE guild_id = ?")
            val = (f"{xd}", ctx.guild.id)
            cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        return await ctx.reply(embed=discord.Embed(description=f"Now onwards `{cmd.qualified_name}` command will not be ignored by the bot.", color=0xc283fe))
    
    @_cmd.command(name="show", aliases=['list'], description="Shows you the current ignored commands list")
    @commands.has_guild_permissions(administrator=True)
    async def _showwww(self, ctx: commands.Context):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 979353019235840000]:
                em = discord.Embed(description=f"<:error:1153009680428318791>You must Have Higher Role than Bot To run This Command", color=0xff0000)
                return await ctx.send(embed=em)
        query = "SELECT * FROM  ignore WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            ig_db = cursor.fetchone()
        if ig_db is None:
            return await ctx.reply(embed=discord.Embed(description=f"No commands are being ignored in the server", color=0xff0000))
        else:
            xd = literal_eval(ig_db['cmd'])
            if len(xd) == 0:
                return await ctx.reply(embed=discord.Embed(description=f"No commands are being ignored in the server", color=0xff0000))
        ls = []
        for i in xd:
            ls.append(i.capitalize())
        em = discord.Embed(title=f"Ignored command - {len(xd)}", description="\n".join(ls), color=0xc283fe).set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        await ctx.reply(embed=em)

    @ignore.group(invoke_without_command=True, name="module", aliases=["modules", "cog", "cogs"], description="Shows The help menu for ignore module")
    async def _module(self, ctx: commands.Context):
        prefix = ctx.prefix
        if prefix == f"<@{self.bot.user.id}> ":
            prefix = f"@{str(self.bot.user)} "
        xd = discord.utils.get(self.bot.users, id=978930369392951366)
        anay = str(xd)
        pfp = xd.display_avatar.url
        listem = discord.Embed(colour=0xc283fe,
                                     description=f"<...> Duty | [...] Optional\n\n" 
                                                  f"`{prefix}ignore module`\n" 
                                                  f"Shows The help menu for ignore module\n\n"
                                                  f"`{prefix}ignore module add`\n"
                                                  f"Adds a module to ignore list\n\n"
                                                  f"`{prefix}ignore module remove`\n"
                                                  f"Removes a module from ignore list\n\n"
                                                  f"`{prefix}ignore module show`\n"
                                                  f"Shows you the current list\n\n")
        listem.set_author(name=f"{str(ctx.author)}", icon_url=ctx.author.display_avatar.url)
        listem.set_footer(text=f"Made by stars.gg" ,  icon_url=pfp)
        await ctx.send(embed=listem)

    @_module.command(name="add", description="Adds a module to ignore list")
    @commands.has_guild_permissions(administrator=True)
    async def _adddddd(self, ctx: commands.Context, *, module: str):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 979353019235840000]:
                em = discord.Embed(description=f"<:error:1153009680428318791>You must Have Higher Role than Bot To run This Command", color=0xff0000)
                return await ctx.send(embed=em)
        if module.lower() == "ignore":
            return await ctx.reply(embed=discord.Embed(description=f"Ignore module cant be ignored", color=0xff0000), mention_author=False)
        dc = {
            "mod": "moderation",
            "mods": "moderation",
            "security": "antinuke",
            "gw": "giveaway",
            "giveaways": "giveaway",
            "logs": "logging",
            "log": "logging",
            "tickets": "ticket",
            "welcomer": "welcome",
            "vc": "voice",
            "invc roles": "invc",
        }
        for i in dc:
            if module.lower() == i:
                module = dc[i]
        query = "SELECT * FROM  ignore WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            ig_db = cursor.fetchone()
        m_name = module
        module = self.bot.get_cog(module.lower())
        if module is None:
            return await ctx.reply(embed=discord.Embed(description=f"No module found named `{m_name}`", color=0xff0000), mention_author=False)
        if ig_db is None:
            xd = [module.qualified_name]
            sql = (f"INSERT INTO ignore(guild_id, module) VALUES(?, ?)")
            val = (ctx.guild.id, f"{xd}")
            cursor.execute(sql, val)
        else:
            xd = literal_eval(ig_db['module'])
            if module.qualified_name in xd:
                return await ctx.reply(embed=discord.Embed(description=f"`{module.qualified_name}` module is already being ignored by the bot", color=0xff0000))
            else:
                xd.append(module.qualified_name)
            sql = (f"UPDATE ignore SET module = ? WHERE guild_id = ?")
            val = (f"{xd}", ctx.guild.id)
            cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        return await ctx.reply(embed=discord.Embed(description=f"Now onwards `{module.qualified_name}` command will be ignored by the bot.", color=0xc283fe))
    
    @_module.command(name="remove", description="Removes a Module from ignore list")
    @commands.has_guild_permissions(administrator=True)
    async def _removeeeee(self, ctx: commands.Context, *, module: str):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 979353019235840000]:
                em = discord.Embed(description=f"<:error:1153009680428318791>You must Have Higher Role than Bot To run This Command", color=0xff0000)
                return await ctx.send(embed=em)
        if module.lower() == "ignore":
            return await ctx.reply(embed=discord.Embed(description=f"Ignore module cant be ignored", color=0xff0000), mention_author=False)
        dc = {
            "mod": "moderation",
            "mods": "moderation",
            "security": "antinuke",
            "gw": "giveaway",
            "giveaways": "giveaway",
            "logs": "logging",
            "log": "logging",
            "tickets": "ticket",
            "welcomer": "welcome",
            "vc": "voice",
            "invc roles": "invc",
        }
        for i in dc:
            if module.lower() == i:
                module = dc[i]
        m_name = module
        module = self.bot.get_cog(module.lower())
        if module is None:
            return await ctx.reply(embed=discord.Embed(description=f"No module found named `{m_name}`", color=0xff0000), mention_author=False)
        query = "SELECT * FROM  ignore WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            ig_db = cursor.fetchone()
        if ig_db is None:
            return await ctx.reply(embed=discord.Embed(description=f"`{module.qualified_name}` module is already not being ignored by the bot", color=0xff0000))
        else:
            xd = literal_eval(ig_db['module'])
            if module.qualified_name not in xd:
                return await ctx.reply(embed=discord.Embed(description=f"`{module.qualified_name}` module is already not being ignored by the bot", color=0xff0000))
            else:
                xd.remove(module.qualified_name)
            sql = (f"UPDATE ignore SET module = ? WHERE guild_id = ?")
            val = (f"{xd}", ctx.guild.id)
            cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        return await ctx.reply(embed=discord.Embed(description=f"Now onwards `{module.qualified_name}` module will not be ignored by the bot.", color=0xc283fe))
    
    @_module.command(name="show", aliases=['list'], description="Shows you the current ignored module list")
    @commands.has_guild_permissions(administrator=True)
    async def _showwwww(self, ctx: commands.Context):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 979353019235840000]:
                em = discord.Embed(description=f"<:error:1153009680428318791>You must Have Higher Role than Bot To run This Command", color=0xff0000)
                return await ctx.send(embed=em)
        query = "SELECT * FROM  ignore WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            ig_db = cursor.fetchone()
        if ig_db is None:
            return await ctx.reply(embed=discord.Embed(description=f"No module are being ignored in the server", color=0xff0000))
        else:
            xd = literal_eval(ig_db['module'])
            if len(xd) == 0:
                return await ctx.reply(embed=discord.Embed(description=f"No module are being ignored in the server", color=0xff0000))
        ls = []
        for i in xd:
            ls.append(i.capitalize())
        em = discord.Embed(title=f"Ignored module - {len(xd)}", description="\n".join(ls), color=0xc283fe).set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        await ctx.reply(embed=em)

async def setup(bot):
    await bot.add_cog(ignore(bot))