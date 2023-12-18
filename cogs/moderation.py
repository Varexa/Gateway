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
import matplotlib
from embed import *

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


class BasicView(discord.ui.View):
    def __init__(self, ctx: commands.Context, timeout = 60):
        super().__init__(timeout=timeout)
        self.ctx = ctx

    

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and interaction.user.id not in  [978930369392951366, 933738517845118976]:
            await interaction.response.send_message(f"Um, Looks like you are not the author of the command...", ephemeral=True)
            return False
        return True
class channeldropdownmenu(discord.ui.ChannelSelect):
    def __init__(self, ctx: commands.Context):
        super().__init__(placeholder="Select channel",
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
        if interaction.user.id != self.ctx.author.id and interaction.user.id not in  [978930369392951366, 933738517845118976]:
            await interaction.response.send_message(f"Um, Looks like you are not the author of the command...", ephemeral=True)
            return False
        return True

class embedSend(discord.ui.View):
    def __init__(self, bot, ctx: commands.Context, id):
        super().__init__()
        self.add_item(embedMenu(bot, ctx, id))
        self.bot = bot
        self.ctx = ctx
        self.id = id

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and interaction.user.id not in  [978930369392951366, 933738517845118976]:
            await interaction.response.send_message(f"Um, Looks like you are not the author of the command...", ephemeral=True)
            return False
        return True

    async def on_timeout(self) -> None:
        try:
            if self.message:
                await self.message.edit(view=None)
        except:
            pass

    @discord.ui.button(label="Send", style=discord.ButtonStyle.green)
    async def _send(self, interaction: discord.Interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        embed = await getembed(self.ctx.guild, self.ctx.author, self.id)
        embed = discord.Embed.from_dict(embed)
        v = channelmenuview(self.ctx)
        await interaction.message.edit(content=f"Please select the channel where you want to send this embed\nIf you can't see any channel in the dropdown type its name in the dropdown selection box.", view=v)
        await v.wait()
        c = await getchannel(self.ctx.guild.id)
        c = discord.utils.get(self.ctx.guild.channels, id=c)
        ii = await c.send(embed=embed)
        em = discord.Embed(color=0xc283fe)
        em.description = f"Successfully sent the embed in {c.mention}"
        vv = discord.ui.View()
        vv.add_item(discord.ui.Button(label="Jump to embed", url=ii.jump_url))
        await interaction.message.edit(content=None, embed=em, view=vv)
        await delembed(self.id)
        self.stop()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.danger)
    async def _cancel(self, interaction: discord.Interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        em = discord.Embed(color=0xc283fe)
        em.description = f"Cancelled the command"
        await interaction.edit_original_response(embed=em, view=None)
        await delembed(self.id)
        self.stop()

class xddd(BasicView):
    def __init__(self, ctx: commands.Context):
        super().__init__(ctx, timeout=60)
        self.value = None

    @discord.ui.button(label="All", style=discord.ButtonStyle.gray)
    async def a(self, interaction, button):
        self.value = 'all'
        self.stop()
    @discord.ui.button(label="Server update", style=discord.ButtonStyle.gray)
    async def server(self, interaction, button):
        self.value = 'update'
        self.stop()
    @discord.ui.button(label="Ban", style=discord.ButtonStyle.gray)
    async def _b(self, interaction, button):
        self.value = 'ban'
        self.stop()
    @discord.ui.button(label="Kick", style=discord.ButtonStyle.gray)
    async def _k(self, interaction, button):
        self.value = 'kick'
        self.stop()

class channeloption(BasicView):
    def __init__(self, ctx: commands.Context):
        super().__init__(ctx, timeout=60)
        self.value = None

    @discord.ui.button(label="Text", style=discord.ButtonStyle.gray)
    async def a(self, interaction, button):
        self.value = 'text'
        self.stop()
    @discord.ui.button(label="Voice", style=discord.ButtonStyle.gray)
    async def server(self, interaction, button):
        self.value = 'voice'
        self.stop()
    @discord.ui.button(label="Category", style=discord.ButtonStyle.gray)
    async def _b(self, interaction, button):
        self.value = 'category'
        self.stop()

class nice(BasicView):
    def __init__(self, ctx: commands.Context):
        super().__init__(ctx, timeout=120)
        self.value = None

    

    @discord.ui.button(label="1", style=discord.ButtonStyle.gray)
    async def _one(self, interaction, button):
        self.value = 1
        self.stop()
    @discord.ui.button(label="10", style=discord.ButtonStyle.gray)
    async def _two(self, interaction, button):
        self.value = 10
        self.stop()
    @discord.ui.button(label="20", style=discord.ButtonStyle.gray)
    async def _third(self, interaction, button):
        self.value = 20
        self.stop()
    @discord.ui.button(label="100", style=discord.ButtonStyle.gray)
    async def _four(self, interaction, button):
        self.value = 100
        self.stop()
    @discord.ui.button(label="Custom", style=discord.ButtonStyle.gray)
    async def _five(self, interaction, button):
        self.value = "custom"
        self.stop()

class OnOrOff(BasicView):
    def __init__(self, ctx: commands.Context):
        super().__init__(ctx, timeout=60)
        self.value = None

    

    @discord.ui.button(emoji="<:confirm:1156150922200748053> ", custom_id='Yes', style=discord.ButtonStyle.green)
    async def dare(self, interaction, button):
        self.value = 'Yes'
        self.stop()

    @discord.ui.button(emoji="<:cross:1156150663802265670> ", custom_id='No', style=discord.ButtonStyle.danger)
    async def truth(self, interaction, button):
        self.value = 'No'
        self.stop()

class create(BasicView):
    def __init__(self, ctx: commands.Context):
        super().__init__(ctx, timeout=120)
        self.value = None

    

    @discord.ui.button(label="Users only", custom_id='users', style=discord.ButtonStyle.green)
    async def users(self, interaction, button):
        self.value = 'users'
        self.stop()
    @discord.ui.button(label="Bots Only", custom_id='bots', style=discord.ButtonStyle.green)
    async def bots(self, interaction, button):
        self.value = 'bots'
        self.stop()

    @discord.ui.button(label="Both", custom_id='both', style=discord.ButtonStyle.danger)
    async def both(self, interaction, button):
        self.value = 'both'
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

def convert(date):
    date.replace("second", "s")
    date.replace("seconds", "s")
    date.replace("minute", "m")
    date.replace("minutes", "m")
    date.replace("hour", "h")
    date.replace("hours", "h")
    date.replace("day", "d")
    date.replace("days", "d")
    pos = ["s", "m", "h", "d"]
    time_dic = {"s": 1, "m": 60, "h": 3600, "d": 3600 *24}
    i = {"s": "Secondes", "m": "Minutes", "h": "Heures", "d": "Jours"}
    unit = date[-1]
    if unit not in pos:
        return -1
    try:
        val = int(date[:-1])

    except:
        return -2

    if val == 1:
        return val * time_dic[unit], i[unit][:-1]
    else:
        return val * time_dic[unit], i[unit]

async def do_removal(ctx, limit, predicate, *, before=None, after=None):
    if limit > 2000:
        return await ctx.error(f"Too many messages to search given ({limit}/2000)")

    if before is None:
        before = ctx.message
    else:
        before = discord.Object(id=before)

    if after is not None:
        after = discord.Object(id=after)

    try:
        deleted = await ctx.channel.purge(limit=limit, before=before, after=after, check=predicate)
    except discord.Forbidden as e:
        return await ctx.error("I do not have permissions to delete messages.")
    except discord.HTTPException as e:
        return await ctx.error(f"Error: {e} (try a smaller search?)")

    spammers = Counter(m.author.display_name for m in deleted)
    deleted = len(deleted)
    messages = [f'{deleted} message{" was" if deleted == 1 else "s were"} removed.']
    if deleted:
        messages.append("")
        spammers = sorted(spammers.items(), key=lambda t: t[1], reverse=True)
        messages.extend(f"**{name}**: {count}" for name, count in spammers)

    to_send = "\n".join(messages)

    if len(to_send) > 2000:
        await ctx.send(f"Successfully removed {deleted} messages.", delete_after=10)
    else:
        await ctx.send(to_send, delete_after=10)

class moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.sniped_messages = {}
        self.bot.role_status = {}
        self.bot.rrole_status = {}
        self.color = 0xc283fe
    
    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        em = discord.Embed(title=f"Command runned in {ctx.guild.name}", description=f"Command name: `{ctx.command.qualified_name}`\nAuthor Name: {str(ctx.author)}\nGuild Id: {ctx.guild.id}\nCommand executed: `{ctx.message.content}`\nChannel name: {ctx.channel.name}\nChannel Id: {ctx.channel.id}\nJump Url: [Jump to]({ctx.message.jump_url})\nCommand runned without error: True", timestamp=ctx.message.created_at, color=0xc283fe)
        em.set_thumbnail(url=ctx.author.display_avatar.url)
        if ctx.author.id in [978930369392951366, 933738517845118976]:
            return
        else:
            webhook = discord.SyncWebhook.from_url(webhook_cmd_logs)
            webhook.send(embed=em, username=f"{str(self.bot.user)} | Command Logs", avatar_url=self.bot.user.avatar.url)
        
    @commands.command(description="Creates a embed")
    @commands.has_permissions(manage_guild=True)
    async def embed(self, ctx):
        em = discord.Embed(description="\u200B", color=0xc283fe)
        x = round(random.random()*100000)
        await updateembed(x, em.to_dict())
        v = embedSend(self.bot, ctx, x)
        await ctx.reply("This is a sample of embed you have created till now", embed=em, view=v)
        await v.wait()

    # @commands.command(description="Shows audit logs entry")
    # @commands.cooldown(1, 120, commands.BucketType.guild)
    # @commands.has_permissions(administrator=True)
    # async def audit(self, ctx):
    #     view = xddd(ctx)
    #     em = discord.Embed(description="Which type of Audit action you want to See?", color=0xc283fe)
    #     ok = await ctx.reply(embed=em, mention_author=False, view=view)
    #     await view.wait()
    #     action = view.value
    #     await ok.delete()
    #     view1 = nice(ctx)
    #     em = discord.Embed(description="How much Audit log entry you want", color=0xc283fe)
    #     ok = await ctx.reply(embed=em, mention_author=False, view=view1)
    #     await view1.wait()
    #     if view1.value == "custom":
    #         await ok.delete()
    #         em = discord.Embed(description="Type the no. of entries You want", color=0xc283fe)
    #         gud = await ctx.reply(embed=em, mention_author=False)
    #         def message_check(m):
    #          return ( 
    #              m.author.id == ctx.author.id
    #              and m.channel == ctx.channel
    #          )
             
    #         msg = await self.bot.wait_for("message", check=message_check)
    #         await gud.delete()
    #         try: 
    #            winners = abs(int(msg.content)) 
    #            if winners == 0: 
    #              await ctx.send("You did not enter an postive number.") 
    #              return 
    #         except ValueError: 
    #            return await ctx.send("You did not enter an integer.")
    #         no=int(msg.content)
    #     else:
    #         await ok.delete()
    #         no = view1.value
    #     ls, ok = [], []
    #     if action == 'ban':
    #         count = 1
    #         lol = "" 
    #         async for i in ctx.guild.audit_logs(limit=no, action=discord.AuditLogAction.ban):
    #             em = discord.Embed(title="Audit Log Entry", color=0xc283fe)
                
    #             des = f"Action Done: Ban\nAction Id: {i.id}\nAction Done By: {str(i.user)}\n"
    #             des+=f"Action Done to: {str(i.target)}[{i.target.id}]\n"
    #             if i.reason:
    #                     des+=f"Reason for Action: {i.reason}\n"
    #             if i.extra:
    #                     des+=f"Extra info for Action: {i.reason}\n"
    #             des+=f"Action Done At: <t:{round(i.created_at.timestamp())}:R>\n"
    #             em.description = des
    #             em.set_footer(text=f"Entry no. {count}", icon_url=self.bot.user.display_avatar.url)
    #             count+=1
    #             ok.append(em)
    #     if action == 'kick':
    #         count = 1
    #         lol = ""
    #         async for i in ctx.guild.audit_logs(limit=no, action=discord.AuditLogAction.kick):
    #             em = discord.Embed(title="Audit Log Entry", color=0xc283fe)
    #             lol = str(i.action)
    #             lol = lol.replace("AuditLogAction.", "").replace("_", " ")
    #             des = f"Action Done: {lol.capitalize()}\nAction Id: {i.id}\nAction Done By: {str(i.user)}\n"
    #             if lol == "ban":
    #                 des+=f"Action Done to: {str(i.target)}[{i.target.id}]\n"
    #                 if i.reason:
    #                     des+=f"Reason for Action: {i.reason}\n"
    #                 if i.extra:
    #                     des+=f"Extra info for Action: {i.reason}\n"
    #             des+=f"Action Done At: <t:{round(i.created_at.timestamp())}:R>\n"
    #             em.description = des
    #             em.set_footer(text=f"Entry no. {count}", icon_url=self.bot.user.display_avatar.url)
    #             count+=1
    #             ok.append(em)
    #     if action == 'update':
    #         count = 1
    #         lol = ""
    #         async for i in ctx.guild.audit_logs(limit=no, action=discord.AuditLogAction.guild_update):
    #                 em = discord.Embed(title="Audit Log Entry", color=0xc283fe)
    #                 des = f"Action Done: Server Update\nAction Id: {i.id}\nAction Done By: {str(i.user)}\n"
                
    #                 try:
    #                     des+=f"Server name Before: {i.before.name}\nServer name After: {i.after.name}\n"
    #                 except:
    #                     pass
    #                 try:
    #                     if i.before.icon != i.after.icon:
    #                         if i.before.icon is None:
    #                             des+=f"Server icon Before: None\n"
    #                         else:
    #                             des+=f"Server icon Before: [Icon Before]({i.befroe.icon.url})\n"
    #                         if i.after.icon is None:
    #                             des+=f"Server icon After: None\n"
    #                         else:
    #                             des+=f"Server icon After: [Icon After]({i.after.icon.url})\n"
    #                 except:
    #                     pass
    #                 try:
    #                     des+=f"Server vanity Before: {i.before.vanity_url_code}\nServer vanity After: {i.after.vanity_url_code}\n"
    #                 except:
    #                     pass
    #                 des+=f"Action Done At: <t:{round(i.created_at.timestamp())}:R>\n"
    #                 em.description = des
    #                 em.set_footer(text=f"Entry no. {count}", icon_url=self.bot.user.display_avatar.url)
    #                 count+=1
    #                 ok.append(em)
    #     if action == 'all':
    #         count = 1
    #         lol = ""
    #         async for i in ctx.guild.audit_logs(limit=no):
    #             em = discord.Embed(title="Audit Log Entry", color=0xc283fe)
    #             lol = str(i.action)
    #             lol = lol.replace("AuditLogAction.", "").replace("_", " ")
    #             des = f"Action Done: {lol.capitalize()}\nAction Id: {i.id}\nAction Done By: {str(i.user)}\n"
    #             if lol == "guild update":
    #                 try:
    #                     des+=f"Server name Before: {i.before.name}\nServer name After: {i.after.name}\n"
    #                 except:
    #                     pass
    #                 try:
    #                     if i.before.icon != i.after.icon:
    #                         if i.before.icon is None:
    #                             des+=f"Server icon Before: None\n"
    #                         else:
    #                             des+=f"Server icon Before: [Icon Before]({i.befroe.icon.url})\n"
    #                         if i.after.icon is None:
    #                             des+=f"Server icon After: None\n"
    #                         else:
    #                             des+=f"Server icon After: [Icon After]({i.after.icon.url})\n"
    #                 except:
    #                     pass
    #                 try:
    #                     des+=f"Server vanity Before: {i.before.vanity_url_code}\nServer vanity After: {i.after.vanity_url_code}\n"
    #                 except:
    #                     pass
    #             elif lol == "member prune":
    #                 des+=f"Members pruned for: {i.extra.delete_members_days}\nMembers pruned: {i.extra.members_removed} Members\n"
    #             elif lol == "member update":
    #                 try:
    #                     des+=f"Member nick Before: {i.before.nick}\nMember nick After: {i.after.nick}\n"
    #                 except:
    #                     pass
    #             elif lol == "member move":
    #                 des+=f"Move to: {i.extra.channel}\nNo. of members Moved: {i.extra.count}\n"
    #             elif lol == "webhook create":
    #                 des+=f"Webhook Created on: {i.changes.after.channel.name}\nWebhook Name: {i.changes.after.name}\n"
    #             elif lol == "webhook delete":
    #                 des+=f"Webhook Name: {i.changes.before.name}\n"
    #             elif lol == "ban":
    #                 des+=f"Action Done to: {str(i.target)}[{i.target.id}]\n"
    #                 if i.reason:
    #                     des+=f"Reason for Action: {i.reason}\n"
    #                 if i.extra:
    #                     des+=f"Extra info for Action: {i.extra}\n"
    #             elif lol == "unban":
    #                 des = f"Action Done to: {str(i.target)}[{i.target.id}]\n"
    #             elif lol == 'kick':
    #                 des+=f"Action Done to: {str(i.target)}[{i.target.id}]\n"
    #                 if i.reason:
    #                     des+=f"Reason for Action: {i.reason}\n"
    #                 if i.extra:
    #                     des+=f"Extra info for Action: {i.extra}\n"
    #             elif lol == 'channel create':
    #                 des+=f"Created Channel: {i.after.name} [{i.target.id}]\n"
    #                 if i.reason:
    #                     des+=f"Reason for Action: {i.reason}\n"
    #                 if i.extra:
    #                     des+=f"Extra info for Action: {i.extra}\n"
    #             elif lol == 'channel delete':
    #                 des+=f"Deleted Channel: {i.before.name} [{i.target.id}]\n"
    #                 if i.reason:
    #                     des+=f"Reason for Action: {i.reason}\n"
    #                 if i.extra:
    #                     des+=f"Extra info for Action: {i.extra}\n"
    #             elif lol == 'channel update':
    #                 try:
    #                     des+=f"Channel Name Before: {i.before.name}\nChannel Name After: {i.after.name}\n"
    #                 except:
    #                     des+=f"Channel Name: {i.target}\n"
        
    #                 if i.reason:
    #                     des+=f"Reason for Action: {i.reason}\n"
    #                 if i.extra:
    #                     des+=f"Extra info for Action: {i.extra}\n"
    #             elif lol == 'role create':
    #                 des+=f"Created Role: {i.after.name} [{i.target.id}]\n"
    #                 if i.reason:
    #                     des+=f"Reason for Action: {i.reason}\n"
    #                 if i.extra:
    #                     des+=f"Extra info for Action: {i.extra}\n"
    #             elif lol == 'role delete':
    #                 des+=f"Deleted Role: {i.before.name} [{i.target.id}]\n"
    #                 if i.reason:
    #                     des+=f"Reason for Action: {i.reason}\n"
    #                 if i.extra:
    #                     des+=f"Extra info for Action: {i.extra}\n"
    #             elif lol == 'role update':
    #                 try:
    #                     des+=f"Role Name Before: {i.before.name}\nRole Name After: {i.after.name}\n"
    #                 except:
    #                     pass
    #                 try:
    #                     des+=f"Role Hoist Before: {i.before.hoist}\nRole Hoist After: {i.after.hoist}\n"
    #                 except:
    #                     pass
    #                 try:
    #                     des+=f"Role Color Before: {i.before.color}\nRole Color After: {i.after.color}\n"
    #                 except:
    #                     pass
    #                 if i.reason:
    #                     des+=f"Reason for Action: {i.reason}\n"
    #                 if i.extra:
    #                     des+=f"Extra info for Action: {i.extra}\n"
    #             elif lol == "member role update":
    #                 des+=f"Action Done to: {str(i.target)}\n"
    #                 yo = []
    #                 if i.changes.before.roles != yo:
    #                     for op in i.changes.before.roles:
    #                         des+=f"Role removed: {op.name} [{op.id}]\n"
    #                 else:
    #                     for op in i.changes.after.roles:
    #                         des+=f"Role given: {op.name} [{op.id}]\n"
    #                 if i.reason:
    #                     des+=f"Reason for Action: {i.reason}\n"
    #                 if i.extra:
    #                     des+=f"Extra info for Action: {i.extra}\n"
    #             elif lol == "bot add":
    #                 des+=f"Bot added: {i.target.mention}\n"
    #             des+=f"Action Done At: <t:{round(i.created_at.timestamp())}:R>\n"
    #             em.description = des
    #             em.set_footer(text=f"Entry no. {count}", icon_url=self.bot.user.display_avatar.url)
    #             count+=1
    #             ok.append(em)
    #     if len(ok) < 1:
    #         return await ctx.reply("No Audit Entry Found")
    #     page = PaginationView(embed_list=ok, ctx=ctx)
    #     await page.start(ctx)
        
    @commands.command(description="Shows the current prefix")
    async def prefix(self, ctx):
        with sqlite3.connect('database.sqlite3') as db:
          db.row_factory = sqlite3.Row
          cursor = db.cursor()
          cursor.execute(f"SELECT * FROM prefixes WHERE guild_id = {ctx.guild.id}")
          res = cursor.fetchone()
        prefix = res["prefix"]
        if ctx.author.guild_permissions.administrator == True:
            em = discord.Embed(title=f"Current Prefix for {ctx.guild.name}", description=f"{prefix}\nYou can change it by typing {prefix}setprefix <prefix>", color=0xc283fe)
            await ctx.send(embed=em, mention_author=False)
        if ctx.author.guild_permissions.administrator == False:
            em = discord.Embed(title=f"Current Prefix for {ctx.guild.name}", description=f"{prefix}", color=0xc283fe)
            await ctx.send(embed=em, mention_author=False)
        db.commit()
        cursor.close()
        db.close()
        
    @commands.command(description="Changes the prefix for the bot")
    @commands.has_permissions(administrator=True)
    async def setprefix(self, ctx, *,prefix):
        with sqlite3.connect('database.sqlite3') as db:
          db.row_factory = sqlite3.Row
          cursor = db.cursor()
          cursor.execute(f"SELECT * FROM prefixes WHERE guild_id = {ctx.guild.id}")
          res = cursor.fetchone()
        pre = res["prefix"]
        if ctx.author.id == ctx.guild.owner.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 933738517845118976]:
                em = discord.Embed(description=f"<:cross:1156150663802265670>  You must Have Higher Role than Bot To run This Command", color=0xff0000)
                return await ctx.send(embed=em)
        if prefix is not None:
            if res is not None:
                sql = (f"UPDATE prefixes SET prefix = ? WHERE guild_id = ?") 
                val = (f"{prefix}", ctx.guild.id)
                cursor.execute(sql, val)
                await ctx.reply(embed=discord.Embed(description=f"Changed prefix to {prefix}", color=0xc283fe), mention_author=False)
        db.commit()
        cursor.close()
        db.close()

    @commands.command(aliases=['as', 'stealsticker'], description="Adds the sticker to the server")
    @commands.has_permissions(manage_emojis=True)
    async def addsticker(self, ctx: commands.Context, *, name=None):
        if ctx.message.reference is None:
            return await ctx.reply("No replied message found")
        msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        if len(msg.stickers) == 0:
            return await ctx.reply("No sticker found")
        n, url = "", ""
        for i in msg.stickers:
            n = i.name
            url = i.url
        if name is None:
            name = n
        try:
            response = requests.get(url)
            if url.endswith("gif"):
                fname = "Sticker.gif"
            else:
                fname = "Sticker.png"
            file = discord.File(BytesIO(response.content), fname)
            s = await ctx.guild.create_sticker(name=name, description= f"Sticker created by {str(self.bot.user)}", emoji="❤️", file=file)
            await ctx.reply(f"Sticker created with name `{name}`", stickers=[s])
        except:
            return await ctx.reply("Failed to create the sticker")

    @commands.command(aliases=["deletesticker", "removesticker"], description="Delete the sticker from the server")
    @commands.has_permissions(manage_emojis=True)
    async def delsticker(self, ctx: commands.Context, *, name=None):
        if ctx.message.reference is None:
            return await ctx.reply("No replied message found")
        msg = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        if len(msg.stickers) == 0:
            return await ctx.reply("No sticker found")
        try:
            name = ""
            for i in msg.stickers:
                name = i.name
                await ctx.guild.delete_sticker(i)
            await ctx.reply(f"Deleted Sticker named `{name}`")
        except:
            await ctx.reply("Failed to delete the sticker")
            
    @commands.command(aliases=["deleteemoji", "removeemoji"], description="Deletes the emoji from the server")
    @commands.has_permissions(manage_emojis=True)
    async def delemoji(self, ctx, emoji = None):
        init = await ctx.reply(f"<:loading:1060851548869107782> Processing the command...", mention_author=False)
        con = None
        if ctx.message.reference is not None:
            message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            con = str(message.content)
        else:
            con = str(ctx.message.content)
        if con is not None:
            x = r"<a?:[a-zA-Z0-9\_]+:([0-9]+)>"
            xxx = re.findall(x, con)
            count = 0
            if len(xxx) != 0:
                if len(xxx) >= 20:
                    await init.delete()
                    return await ctx.reply(f"Maximum 20 emojis can be deleted by the bot.")
                for i in xxx:
                    emo = discord.PartialEmoji.from_str(i)
                    if emo in ctx.guild.emojis:
                        emoo = await ctx.guild.fetch_emoji(emo.id)
                        await emoo.delete()
                        count+=1
                await init.delete()
                return await ctx.reply(f"Successfully deleted {count}/{len(xxx)} Emoji(s)")
        else:
            await init.delete()
            return await ctx.reply("No Emoji found")
        
    @commands.command(aliases=["steal", 'ae'], description="Adds the emoji to the server")
    @commands.has_permissions(manage_emojis=True)
    async def addemoji(self, ctx: commands.Context, emoji: Union[discord.Emoji, discord.PartialEmoji, str] = None,*,name=None):
        init = await ctx.reply(f"<:loading:1060851548869107782> Processing the command...", mention_author=False)
        con = None
        if ctx.message.reference is not None:
            message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
            con = str(message.content)
        else:
            con = str(ctx.message.content)
        x = r"<a?:[a-zA-Z0-9\_]+:([0-9]+)>"
        xxx = re.findall(x, con)
        if len(xxx) == 1:
            con = None
        if con is not None:
            count = 0
            if len(xxx) != 0:
                if len(xxx) >= 20:
                    await init.delete()
                    return await ctx.reply(f"Maximum 20 emojis can be added by the bot.")
                for i in xxx:
                    emo = discord.PartialEmoji.from_str(i)
                    if emo.animated:
                        url = f"https://cdn.discordapp.com/emojis/{emo.id}.gif"
                    else:
                        url = f"https://cdn.discordapp.com/emojis/{emo.id}.png"
                    try:
                        async with aiohttp.request("GET", url) as r:
                            img = await r.read()
                            emoji = await ctx.guild.create_custom_emoji(name=f"{emo.name}", image=img)
                            count+=1 
                            c = True
                    except:
                        c = False
                await init.delete()
                return await ctx.reply(f"Successfully created {count}/{len(xxx)} Emojis")
            else:
                if emoji is None:
                    return await ctx.reply(f"No emoji found")
            if not emoji.startswith("https://"):
                await init.delete()
                return await ctx.reply("Give a valid emoji to add")
            elif name is None:
                await init.delete()
                return await ctx.reply("Please provide a name for emoji")
            async with aiohttp.request("GET", f"{emoji}") as r:
                img = await r.read()
                try:
                  emo = await ctx.guild.create_custom_emoji(name=f"{name}", image=img)
                  await init.delete()
                  return await ctx.reply(f"Successfully created {emo}")
                except:
                  await init.delete()
                  return await ctx.reply(f"Failed to create emoji, it might be because the emoji slots are full.")        
        else:
            if name is None:
                name = f"{emoji.name}"
            c = False
            if emoji.animated:
                url = f"https://cdn.discordapp.com/emojis/{emoji.id}.gif"
            else:
                url = f"https://cdn.discordapp.com/emojis/{emoji.id}.png"
            try:
                async with aiohttp.request("GET", url) as r:
                    img = await r.read()
                    emo = await ctx.guild.create_custom_emoji(name=f"{name}", image=img)
                    await init.delete()
                    await ctx.reply(f"Successfully created {emo}")
                    c = True
            except:
                c = False
            if not c:
                await init.delete()
                return await ctx.reply("Failed to create emoji, it might be because the emoji slots are full.")
    
    @commands.command(description="Changes the icon for the role")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def roleicon(self, ctx: commands.Context, role: discord.Role, *, icon: Union[discord.Emoji, discord.PartialEmoji, str]=None):
        if role.position >= ctx.guild.me.top_role.position:
            em = discord.Embed(description=f"<:cross:1156150663802265670>  This role is higher than my role, move it to the top!", color=0xff0000)
        if ctx.author.top_role.position <= role.position:
            em = discord.Embed(description=f"<:cross:1156150663802265670>  That role has the same or higher position from your top role!", color=0xff0000)
            return await ctx.send(embed=em, delete_after=15)
        if icon is None:
            c = False
            url = None
            for xd in ctx.message.attachments:
                url = xd.url
                c = True
            if c:
                try:
                    async with aiohttp.request("GET", url) as r:
                        img = await r.read()
                        await role.edit(display_icon=img)
                    em = discord.Embed(description=f"Successfully changed icon of {role.mention}", color=0xc283fe)
                except:
                    return await ctx.reply("Failed to change the icon of the role")
            else:
                await role.edit(display_icon=None)
                em = discord.Embed(description=f"Successfully removed icon from {role.mention}", color=0xc283fe)
            return await ctx.reply(embed=em, mention_author=False)
        if isinstance(icon, discord.Emoji) or isinstance(icon, discord.PartialEmoji):
            png = f"https://cdn.discordapp.com/emojis/{icon.id}.png"
            try:
              async with aiohttp.request("GET", png) as r:
                img = await r.read()
            except:
              return await ctx.reply("Failed to change the icon of the role")
            await role.edit(display_icon=img)
            em = discord.Embed(description=f"Successfully changed the icon for {role.mention} to {icon}", color=0xc283fe)
            return await ctx.reply(embed=em, mention_author=False)
        else:
            if not icon.startswith("https://"):
                return await ctx.reply("Give a valid link")
            try:
              async with aiohttp.request("GET", icon) as r:
                img = await r.read()
            except:
              return await ctx.reply("An error occured while changing the icon for the role")
            await role.edit(display_icon=img)
            em = discord.Embed(description=f"Successfully changed the icon for {role.mention}", color=0xc283fe)
            return await ctx.reply(embed=em, mention_author=False)

    @commands.group(invoke_without_command=True, aliases=["purge"], description="Clears the messages")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, Choice: Union[discord.Member, int], Amount: int = None):
        """
        An all in one purge command.
        Choice can be a Member or a number
        """
        await ctx.message.delete()

        if isinstance(Choice, discord.Member):
            search = Amount or 5
            return await do_removal(ctx, search, lambda e: e.author == Choice)

        elif isinstance(Choice, int):
            return await do_removal(ctx, Choice, lambda e: True)

    @clear.command(description="Clears the messages containing embeds")
    @commands.has_permissions(manage_messages=True)
    async def embeds(self, ctx, search=100):
        """Removes messages that have embeds in them."""
        await ctx.message.delete()
        await do_removal(ctx, search, lambda e: len(e.embeds))

    @clear.command(description="Clears the messages containing files")
    @commands.has_permissions(manage_messages=True)
    async def files(self, ctx, search=100):
        """Removes messages that have attachments in them."""

        await ctx.message.delete()
        await do_removal(ctx, search, lambda e: len(e.attachments))

    @clear.command(description="Clears the messages containg images")
    @commands.has_permissions(manage_messages=True)
    async def images(self, ctx, search=100):
        """Removes messages that have embeds or attachments."""

        await ctx.message.delete()
        await do_removal(ctx, search, lambda e: len(e.embeds) or len(e.attachments))

    @clear.command(name="all", description="Clears all messages")
    @commands.has_permissions(manage_messages=True)
    async def _remove_all(self, ctx, search=100):
        """Removes all messages."""

        await ctx.message.delete()
        await do_removal(ctx, search, lambda e: True)

    @clear.command(description="Clears the messages of a specific user")
    @commands.has_permissions(manage_messages=True)
    async def user(self, ctx, member: discord.Member, search=100):
        """Removes all messages by the member."""

        await ctx.message.delete()
        await do_removal(ctx, search, lambda e: e.author == member)

    @clear.command(description="Clears the messages containing a specifix string")
    @commands.has_permissions(manage_messages=True)
    async def contains(self, ctx, *, string: str):
        """Removes all messages containing a substring.
        The substring must be at least 3 characters long.
        """

        await ctx.message.delete()
        if len(string) < 3:
            await ctx.error("The substring length must be at least 3 characters.")
        else:
            await do_removal(ctx, 100, lambda e: string in e.content)

    @clear.command(name="bot", aliases=["bots"], description="Clears the messages sent by bot")
    @commands.has_permissions(manage_messages=True)
    async def _bot(self, ctx, prefix=None, search=100):
        """Removes a bot user's messages and messages with their optional prefix."""

        await ctx.message.delete()

        def predicate(m):
            return (m.webhook_id is None and m.author.bot) or (prefix and m.content.startswith(prefix))

        await do_removal(ctx, search, predicate)

    @clear.command(name="emoji", aliases=["emojis"], description="Clears the messages having emojis")
    @commands.has_permissions(manage_messages=True)
    async def _emoji(self, ctx, search=100):
        """Removes all messages containing custom emoji."""

        await ctx.message.delete()
        custom_emoji = re.compile(r"<a?:[a-zA-Z0-9\_]+:([0-9]+)>")

        def predicate(m):
            return custom_emoji.search(m.content)

        await do_removal(ctx, search, predicate)

    @clear.command(name="reactions", description="Clears the reaction from the messages")
    @commands.has_permissions(manage_messages=True)
    async def _reactions(self, ctx, search=100):
        """Removes all reactions from messages that have them."""

        await ctx.message.delete()

        if search > 2000:
            return await ctx.send(f"Too many messages to search for ({search}/2000)")

        total_reactions = 0
        async for message in ctx.history(limit=search, before=ctx.message):
            if len(message.reactions):
                total_reactions += sum(r.count for r in message.reactions)
                await message.clear_reactions()

        await ctx.success(f"Successfully removed {total_reactions} reactions.")

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
      if not message.guild:
        return
      if not message.author.bot:
          if message.guild.me.guild_permissions.view_audit_log:
              async for i in message.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes=1, seconds=30), action=discord.AuditLogAction.message_delete):
                  url = None
                  for x in message.attachments:
                      url = x.url
                  if message.content == "":
                    content = "***Content Unavailable***"
                  else:
                    content = message.content
                  if i.target == message.author:
                      self.bot.sniped_messages[message.guild.id] = (content, url, message.author,
                                                        message.channel,
                                                        i.user,
                                                        message.created_at)
                  else:
                      self.bot.sniped_messages[message.guild.id] = (content, url, message.author,
                                                        message.channel,
                                                        None,
                                                        message.created_at)
          else:
              url = None
              for x in message.attachments:
                  url = x.url
              if message.content == "":
                  content = "***Content Unavailable***"
              else:
                  content = message.content
              self.bot.sniped_messages[message.guild.id] = (content, url, message.author, message.channel, None, message.created_at)

    @commands.command(description="Snipes the recent message deleted in the channel")
    async def snipe(self, ctx, channel: discord.TextChannel = None):
        if not channel:
            channel = ctx.channel
        try:
            contents, url, author, channel_xyz, mod, time = self.bot.sniped_messages[ctx.guild.id]
        except:
            await ctx.channel.send("<:cross:1156150663802265670>   Couldn't find a message to snipe!")
            return
        if channel_xyz.id == channel.id:
            embed = discord.Embed(description=f":put_litter_in_its_place: Message sent by {author.mention} deleted in {channel_xyz.mention}",
                                color=0xc283fe,
                                timestamp=time)
            embed.add_field(name="__Content__:",
                                  value=f"{contents}",
                                  inline=False)
            if mod is not None:
                embed.add_field(name="**Deleted By:**",
                                value=f"{mod.mention} (ID: {mod.id})")
            if url is not None:
                if url.startswith("http") or url.startswith("http"):
                    embed.set_image(url=url)
            embed.set_footer(text=f"Requested By {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
            return await ctx.channel.send(embed=embed)
        else:
            return await ctx.channel.send("<:cross:1156150663802265670>  Couldn't find a message to snipe!")

    @commands.command(description="Enables slowmode for the channel")
    @commands.bot_has_guild_permissions(manage_channels=True)
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, *, time=None):
        if time is None:
            await ctx.channel.edit(slowmode_delay=None, reason=f"Slowmode edited by {str(ctx.author)}")
            em = discord.Embed(description=f"<:confirm:1156150922200748053>  Successfully removed slowmode for channel {ctx.channel.mention}", color=0x00f7ff)
            return await ctx.channel.send(embed=em)
        t = "".join([ch for ch in time if ch.isalpha()])
        num = 0
        for c in time:
            if c.isdigit():
                num = num + int(c)
        if t == '':
            num = num
        elif t == 's' or t == 'seconds' or t == 'second':
            num = num
        elif t == 'm' or t == 'minutes' or t == 'minute':
            num = num*60
        elif t == 'h' or t == 'hours' or t == 'hour':
            num = num*60*60
        else:
            return await ctx.reply("Invalid time")
        try:
            await ctx.channel.edit(slowmode_delay=num, reason=f"Slowmode edited by {str(ctx.author)}")
        except:
            return await ctx.reply("Invalid time")
        em = discord.Embed(description=f"<:confirm:1156150922200748053>  Successfully changed slowmode for channel {ctx.channel.mention} to {t} seconds", color=0x00f7ff)
        await ctx.channel.send(embed=em)

    @commands.command(usage="[#channel/id]", name="lock", description="Locks the channel")
    @commands.has_permissions(administrator=True)
    async def lock(self, ctx, channel: discord.TextChannel = None, *, reason = None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        em = discord.Embed(description=f"Succesfully Locked Channel", color=0xc283fe)
        em.set_author(name="Channel Locked", icon_url="https://media.discordapp.net/attachments/1155964405129953391/1155964438332063854/verified.png?width=160&height=160")
        em.add_field(name="<:banhammer:1155963619691986944> Moderator", value=f"{ctx.author.mention} ( ID: {ctx.author.id} )", inline=True)
        await ctx.reply(embed=em)

    @commands.command(description="locks all channels in the server")
    @commands.cooldown(1, 60, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    async def lockall(self, ctx):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 933738517845118976]:
                em = discord.Embed(description=f"<:cross:1156150663802265670>  You must Have Higher Role than Bot To run This Command", color=0xff0000)
                return await ctx.send(embed=em)
        view = OnOrOff(ctx)
        em = discord.Embed(description=f"Would You Like To Lock all the channels of the Server", color=0xc283fe)
        try:
            em.set_author(name=str(ctx.author), icon_url=ctx.author.display_avatar.url)
        except:
            em.set_author(name=str(ctx.author))
        test = await ctx.reply(embed=em, view=view)
        await view.wait()
        if not view.value:
            await test.delete()
            return await ctx.reply(content="Timed out!", mention_author=False)
        if view.value == 'Yes':
            await test.delete()
            for channel in ctx.guild.channels:
                overwrite = channel.overwrites_for(ctx.guild.default_role)
                overwrite.send_messages = False
                await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite, reason=f"Lock all channels runned by {ctx.author}")
            em = discord.Embed(description=f"Succesfully Locked All Channel", color=0xc283fe)
            em.set_author(name="All Channel Locked", icon_url="https://media.discordapp.net/attachments/1155964405129953391/1155964438332063854/verified.png?width=160&height=160")
            em.add_field(name="<:banhammer:1155963619691986944> Moderator", value=f"{ctx.author.mention} ( ID: {ctx.author.id} )", inline=True)
            return await ctx.reply(embed=em, mention_author=False)
        if view.value == 'No':
            await test.delete()
            em = discord.Embed(description="Canceled The Command", color=0xff0000)
            return await ctx.reply(embed=em, mention_author=False)        

    @commands.command(usage="[#channel/id]", name="unlock", description="Unlocks the channel")
    @commands.has_permissions(administrator=True)
    async def unlock(self, ctx, channel: discord.TextChannel = None, *, reason = None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = True
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        em = discord.Embed(description=f"Succesfully Unlocked Channel", color=0xc283fe)
        em.set_author(name="Channel Unlocked", icon_url="https://media.discordapp.net/attachments/1155964405129953391/1155964438332063854/verified.png?width=160&height=160")
        em.add_field(name="<:banhammer:1155963619691986944> Moderator", value=f"{ctx.author.mention} ( ID: {ctx.author.id} )", inline=True)
        await ctx.reply(embed=em)
    
    @commands.command(description="Unlocks all channels in the server")
    @commands.cooldown(1, 60, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    async def unlockall(self, ctx):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 933738517845118976]:
                em = discord.Embed(description=f"<:cross:1156150663802265670>  You must Have Higher Role than Bot To run This Command", color=0xff0000)
                return await ctx.send(embed=em)
        view = OnOrOff(ctx)
        em = discord.Embed(description=f"Would You Like To Unlock all the channels of the Server", color=0xc283fe)
        try:
            em.set_author(name=str(ctx.author), icon_url=ctx.author.display_avatar.url)
        except:
            em.set_author(name=str(ctx.author))
        test = await ctx.reply(embed=em, view=view)
        await view.wait()
        if not view.value:
            await test.delete()
            return await ctx.reply(content="Timed out!", mention_author=False)
        if view.value == 'Yes':
            await test.delete()
            for channel in ctx.guild.channels:
                overwrite = channel.overwrites_for(ctx.guild.default_role)
                overwrite.send_messages = True
                await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite, reason=f"Lock all channels runned by {ctx.author}")
            em = discord.Embed(description=f"Succesfully Unlocked All Channel", color=0xc283fe)
            em.set_author(name="All Channel Unlocked", icon_url="https://media.discordapp.net/attachments/1155964405129953391/1155964438332063854/verified.png?width=160&height=160")
            em.add_field(name="<:banhammer:1155963619691986944> Moderator", value=f"{ctx.author.mention} ( ID: {ctx.author.id} )", inline=True)
            return await ctx.reply(embed=em, mention_author=False)
        if view.value == 'No':
            await test.delete()
            em = discord.Embed(description="Canceled The Command", color=0xff0000)
            return await ctx.reply(embed=em, mention_author=False)

    @commands.command(description="Hides the channel")
    @commands.has_permissions(administrator=True)
    async def hide(self, ctx, channel: discord.abc.GuildChannel = None, *, reason = None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.view_channel = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        em = discord.Embed(description=f"Succesfully Hidden Channel", color=0xc283fe)
        em.set_author(name="Channel Hidden", icon_url="https://media.discordapp.net/attachments/1155964405129953391/1155964438332063854/verified.png?width=160&height=160")
        em.add_field(name="<:banhammer:1155963619691986944> Moderator", value=f"{ctx.author.mention} ( ID: {ctx.author.id} )", inline=True)
        await ctx.reply(embed=em)
    
    @commands.command(description="Hide all channels in the server")
    @commands.cooldown(1, 60, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    async def hideall(self, ctx):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 933738517845118976]:
                em = discord.Embed(description=f"<:cross:1156150663802265670>  You must Have Higher Role than Bot To run This Command", color=0xff0000)
                return await ctx.send(embed=em)
        view = OnOrOff(ctx)
        em = discord.Embed(description=f"Would You Like To Hide all the channels of the Server", color=0xc283fe)
        try:
            em.set_author(name=str(ctx.author), icon_url=ctx.author.display_avatar.url)
        except:
            em.set_author(name=str(ctx.author))
        test = await ctx.reply(embed=em, view=view)
        await view.wait()
        if not view.value:
            await test.delete()
            return await ctx.reply(content="Timed out!", mention_author=False)
        if view.value == 'Yes':
            await test.delete()
            for channel in ctx.guild.channels:
                overwrite = channel.overwrites_for(ctx.guild.default_role)
                overwrite.view_channel = False
                await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite, reason=f"Lock all channels runned by {ctx.author}")
            em = discord.Embed(description=f"Succesfully Hidden Channel", color=0xc283fe)
            em.set_author(name="Channel Hidden", icon_url="https://media.discordapp.net/attachments/1155964405129953391/1155964438332063854/verified.png?width=160&height=160")
            em.add_field(name="<:banhammer:1155963619691986944> Moderator", value=f"{ctx.author.mention} ( ID: {ctx.author.id} )", inline=True)
            return await ctx.reply(embed=em, mention_author=False)
        if view.value == 'No':
            await test.delete()
            em = discord.Embed(description="Canceled The Command", color=0xff0000)
            return await ctx.reply(embed=em, mention_author=False)
        
    @commands.command(description="Unhides the channel")
    @commands.has_permissions(administrator=True)
    async def unhide(self, ctx, channel: discord.abc.GuildChannel = None, *, reason = None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.view_channel = True
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        em = discord.Embed(description=f"Succesfully Unhidden Channel", color=0xc283fe)
        em.set_author(name="Channel Unhidden", icon_url="https://media.discordapp.net/attachments/1155964405129953391/1155964438332063854/verified.png?width=160&height=160")
        em.add_field(name="<:banhammer:1155963619691986944> Moderator", value=f"{ctx.author.mention} ( ID: {ctx.author.id} )", inline=True)
        await ctx.reply(embed=em)
    
    @commands.command(description="Unhide all channels in the server")
    @commands.cooldown(1, 60, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    async def unhideall(self, ctx):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 933738517845118976]:
                em = discord.Embed(description=f"<:cross:1156150663802265670>  You must Have Higher Role than Bot To run This Command", color=0xff0000)
                return await ctx.send(embed=em)
        view = OnOrOff(ctx)
        em = discord.Embed(description=f"Would You Like To Unhide all the channels of the Server", color=0xc283fe)
        try:
            em.set_author(name=str(ctx.author), icon_url=ctx.author.display_avatar.url)
        except:
            em.set_author(name=str(ctx.author))
        test = await ctx.reply(embed=em, view=view)
        await view.wait()
        if not view.value:
            await test.delete()
            return await ctx.reply(content="Timed out!", mention_author=False)
        if view.value == 'Yes':
            await test.delete()
            for channel in ctx.guild.channels:
                overwrite = channel.overwrites_for(ctx.guild.default_role)
                overwrite.view_channel = True
            
                await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite, reason=f"Lock all channels runned by {ctx.author}")
                em = discord.Embed(description=f"Succesfully Unhidden All Channel", color=0xc283fe)
                em.set_author(name="All Channel Unhidden", icon_url="https://media.discordapp.net/attachments/1155964405129953391/1155964438332063854/verified.png?width=160&height=160")
                em.add_field(name="<:banhammer:1155963619691986944> Moderator", value=f"{ctx.author.mention} ( ID: {ctx.author.id} )", inline=True)
            return await ctx.reply(embed=em, mention_author=False)
        if view.value == 'No':
            await test.delete()
            em = discord.Embed(description="Canceled The Command", color=0xff0000)
            return await ctx.reply(embed=em, mention_author=False)

    @commands.group(invoke_without_command=True, aliases=['design', 'designs'], description="Shows the help menu for designer")
    @commands.has_permissions(administrator=True)
    async def designer(self, ctx: commands.Context):
        prefix = ctx.prefix
        if prefix == f"<@{self.bot.user.id}> ":
            prefix = f"@{str(self.bot.user)} "
        xd = discord.utils.get(self.bot.users, id=978930369392951366)
        anay = str(xd)
        pfp = xd.display_avatar.url
        listem = discord.Embed(colour=0xc283fe,
                                     description=f"<...> Duty | [...] Optional\n\n" 
                                                  f"`{prefix}designer`\n" 
                                                  f"Shows The help menu for designer\n\n" 
                                                  f"`{prefix}designer role <design>`\n" 
                                                  f"Changes the design for the roles in the server\n\n"
                                                  f"`{prefix}designer channel <design>`\n"
                                                  f"Changes the design for the channels in the server\n\n")
        listem.set_author(name=f"{str(ctx.author)}", icon_url=ctx.author.display_avatar.url)
        listem.set_footer(text=f"Made by stars.gg" ,  icon_url=pfp)
        await ctx.send(embed=listem)

    @designer.command(name="role", aliases=['roles'], description="Changes the design for the roles in the server")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 120, commands.BucketType.guild)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def r(self, ctx: commands.Context, *, design: str):
        if "{role}" in design:
            pass
        elif "{Role}" in design:
            design.replace("{Role}", "{role}")
        elif "{ROLE}" in design:
            design.replace("{ROLE}", "{role}")
        else:
            return await ctx.reply("Please specify where to write the name of the role in the design by `{role}`")
        v = OnOrOff(ctx)
        init = await ctx.reply(embed=discord.Embed(description=f"Are you sure you want me to change the design for roles in the server?", color=0xc283fe), view=v)
        await v.wait()
        if v.value == 'yes':
            await init.delete()
            for i in list(reversed(ctx.guild.roles[1:])):
                if i.is_assignable():
                    await i.edit(name=f'{design.replace("{role}", i.name)}')
            em = discord.Embed(description=f"Successfully changed the design for the roles in the server", color=0xc283fe)
            await ctx.reply(embed=em)
        else:
            await init.delete()
        
    @designer.command(name="channel", aliases=['channels'], description="Changes the design for the channels in the server")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 120, commands.BucketType.guild)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def cc(self, ctx: commands.Context, *, design: str):
        if "{channel}" in design:
            pass
        elif "{Channel}" in design:
            design.replace("{Channel}", "{channel}")
        elif "{CHANNEL}" in design:
            design.replace("{CHANNEL}", "{channel}")
        else:
            return await ctx.reply("Please specify where to write the name of the channel in the design by `{channel}`")
        emd = discord.Embed(description="Which types of channels should i edit?", color=0xc283fe)
        v = channeloption(ctx)
        init = await ctx.reply(embed=emd, view=v)
        await v.wait()
        vv = OnOrOff(ctx)
        await init.edit(embed=discord.Embed(description=f"Are you sure you want me to change the design for {v.value.capitalize()} channels in the server?", color=0xc283fe), view=vv)
        await vv.wait()
        if vv.value == 'yes':
            await init.delete()
            for i in ctx.guild.channels:
                if str(i.type) == v.value:
                    await i.edit(name=f'{design.replace("{channel}", i.name)}')
            em = discord.Embed(description=f"Successfully changed the design for the {v.value.capitalize()} channels in the server", color=0xc283fe)
            await ctx.reply(embed=em)
        else:
            await init.delete()

    @commands.command(name='enlarge', description='Enlarges an emoji.')
    async def enlarge(self, ctx, emoji: Union[discord.Emoji, discord.PartialEmoji, str]):
        if isinstance(emoji, discord.Emoji):
            await ctx.send(emoji.url)
        elif isinstance(emoji, discord.PartialEmoji):
            await ctx.send(emoji.url)
        elif isinstance(emoji, str) and not emoji.isalpha() and not emoji.isdigit():
            await ctx.send(emoji)

    #@commands.group(invoke_without_command=True, name="muterole", aliases=['muteroles'], description="Shows The help menu for muterole")
    async def muterole(self, ctx:commands.Context):
        prefix = ctx.prefix
        if prefix == f"<@{self.bot.user.id}> ":
            prefix = f"@{str(self.bot.user)} "
        xd = discord.utils.get(self.bot.users, id=978930369392951366)
        anay = str(xd)
        pfp = xd.display_avatar.url
        listem = discord.Embed(colour=0xc283fe,
                                     description=f"<...> Duty | [...] Optional\n\n" 
                                                  f"`{prefix}muterole`\n" 
                                                  f"Shows The help menu for muterole\n\n" 
                                                  f"`{prefix}muterole set <role>`\n" 
                                                  f"Sets the muterole of the server\n\n"
                                                  f"`{prefix}muterole reset`\n"
                                                  f"Resets the muterole of the server\n\n"
                                                  f"`{prefix}muterole show`\n"
                                                  f"Shows the muterole of the server\n\n")
        listem.set_author(name=f"{str(ctx.author)}", icon_url=ctx.author.display_avatar.url)
        listem.set_footer(text=f"Made by stars.gg" ,  icon_url=pfp)
        await ctx.send(embed=listem)

    #@muterole.command(name="set", description="Sets the muterole of the server")
    @commands.has_guild_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def adddd(self, ctx: commands.Context, *, role: discord.Role):
        query = "SELECT * FROM  'muteroles' WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('./muterole.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            m_db = cursor.fetchone()
        if m_db is None:
            xd = [role.id]
            sql = "INSERT INTO 'muteroles'(guild_id, muterole) VALUES(?, ?)"
            val = (ctx.guild.id, f"{xd}",)
            cursor.execute(sql, val)
        else:
            xd = literal_eval(m_db['muterole'])
            if len(xd) >= 1:
                return await ctx.reply(embed=discord.Embed(description=f"There can be only 1 muterole in the server", color=0xff0000))
            if role.id in xd:
                return await ctx.reply(embed=discord.Embed(description=f"{role.mention} is already added as muterole", color=0xff0000))
            xd.append(role.id)
            sql = "UPDATE 'muteroles' SET muterole = ? WHERE guild_id = ?"
            val = (f"{xd}", ctx.guild.id,)
            cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        await ctx.reply(embed=discord.Embed(description=f"Added {role.mention} to the muteroles of the server", color=0xc283fe))
        
    #@muterole.command(name="reset", description="Resets the muterole of the server")
    @commands.has_guild_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def removeeee(self, ctx: commands.Context):
        query = "SELECT * FROM  'muteroles' WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('./muterole.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            m_db = cursor.fetchone()
        if m_db is None:
            return await ctx.reply(embed=discord.Embed(description=f"There is no muterole in the server", color=0xff0000))
        else:
            xd = literal_eval(m_db['muterole'])
            if len(xd) == 0:
                return await ctx.reply(embed=discord.Embed(description=f"There is no muterole in the server", color=0xff0000))
            sql = "DELETE FROM 'muteroles' WHERE guild_id = ?"
            val = (ctx.guild.id,)
            cursor.execute(sql, val)
            sql = "DELETE FROM 'data' WHERE guild_id = ?"
            val = (ctx.guild.id,)
            cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        await ctx.reply(embed=discord.Embed(description=f"Removed muterole of the server", color=0xc283fe))
    
    #@muterole.command(name="show", aliases=['list'], description="Shows the muterole of the server")
    async def showww(self, ctx: commands.Context):
        query = "SELECT * FROM  'muteroles' WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('./muterole.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            m_db = cursor.fetchone()
        if m_db is None:
            return await ctx.reply(embed=discord.Embed(description=f"No muteroles are there in the server", color=0xff0000))
        else:
            xd = literal_eval(m_db['muterole'])
            if len(xd) == 0:
                return await ctx.reply(embed=discord.Embed(description=f"No muteroles are there in the server", color=0xff0000))
            else:
                des = ""
                for i in xd:
                    r = discord.utils.get(ctx.guild.roles, id=i)
                    des+=f"{r.mention}\n"
                em = discord.Embed(title=f"Muterole of the server", description=des, color=0xc283fe).set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
                await ctx.reply(embed=em)
    
    #@commands.Cog.listener()
    async def on_member_update(self, before: discord.Member,
                               after: discord.Member) -> None:
        if not after.guild:
            return
        if not after.guild.me.guild_permissions.manage_roles:
            return
        query = "SELECT * FROM  'muteroles' WHERE guild_id = ?"
        val = (after.guild.id,)
        with sqlite3.connect('./muterole.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            m_db = cursor.fetchone()
        if m_db is None:
            return
        else:
            xd = literal_eval(m_db['muterole'])
            if len(xd) == 1:
                role = discord.utils.get(after.guild.roles, id=xd[0])
                if role is None:
                    return
        query1 = "SELECT * FROM  'data' WHERE guild_id = ?"
        val1 = (after.guild.id,)
        with sqlite3.connect('./muterole.sqlite3') as db1:
            db1.row_factory = sqlite3.Row
            cursor1 = db1.cursor()
            cursor1.execute(query1, val1)
            m_db1 = cursor1.fetchone()
        if m_db1 is None:
            data = {}
            data1 = []
        else:
            data = literal_eval(m_db1['data'])
            if after.id in data:
                data1 = data[after.id]
            else:
                data1 = []
        if role in after.roles and role not in before.roles:
            for r in after.roles:
                if r.id == role.id:
                    continue
                else:
                    if r.is_assignable():
                        data1.append(r.id)
                        await after.remove_roles(r, reason="Muterole was assigned")
            data[after.id] = data1
        if role not in after.roles and role in before.roles:
            if after.id in data:
                data1 = data[after.id]
                for i in data1:
                    rr = discord.utils.get(after.guild.roles, id=i)
                    if rr.is_assignable():
                        await after.add_roles(rr, reason="Muterole was removed")
                del data[after.id]
        if m_db1 is None:
            sql = "INSERT OR IGNORE INTO 'data'(guild_id, data) VALUES(?, ?)"
            val = (after.guild.id, f"{data}",)
        else:
            sql = "UPDATE 'data' SET data = ? WHERE guild_id = ?"
            val = (f"{data}", after.guild.id,)
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()

    @commands.command(description="Created a role in the server")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def addrole(self, ctx, color, *,name):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 933738517845118976]:
                em = discord.Embed(description=f"<:cross:1156150663802265670>  You must Have Higher Role than Bot To run This Command", color=0xff0000)
                return await ctx.send(embed=em)
        try:
            color = matplotlib.colors.cnames[color.lower()]
        except:
            color = color
        color = str(color).replace("#", "")
        try:
            color = int(color, base=16)
        except:
            return await ctx.reply(f"Provide a specific color")
        role = await ctx.guild.create_role(name=name, color=color, reason=f"Role created by {str(ctx.author)}")
        em = discord.Embed(description=f"Created {role.mention} role", color=0xc283fe)
        await ctx.reply(embed=em, mention_author=False)
        
    @commands.command(description="Deletes a role in the server")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def delrole(self, ctx, *,role:discord.Role):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 933738517845118976]:
                em = discord.Embed(description=f"<:cross:1156150663802265670>  You must Have Higher Role than Bot To run This Command", color=0xff0000)
                return await ctx.send(embed=em)
        if role.position >= ctx.guild.me.top_role.position:
                em = discord.Embed(description=f"{role.mention} is above my top role, move my role above the {role.mention} and run the command again", color=0xff0000)
                return await ctx.reply(embed=em, mention_author=False)
        await role.delete()
        await ctx.reply(embed=discord.Embed(description="Successfully deleted the role", color=0xc283fe), mention_author=False)
    
    @commands.group(
        invoke_without_command=True,
        description="Adds a role to the user"
    )
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def role(self, ctx, user: discord.Member, *,role: discord.Role):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 933738517845118976]:
                em = discord.Embed(description=f"<:cross:1156150663802265670>  You must Have Higher Role than Bot To run This Command", color=0xff0000)
                return await ctx.send(embed=em, delete_after=15)
            if role.position >= ctx.author.top_role.position:
                em = discord.Embed(description=f"<:cross:1156150663802265670>  That role has the same or higher position from your top role!", color=0xff0000)
                return await ctx.send(embed=em, delete_after=15)

        if role.position >= ctx.guild.me.top_role.position:
            em = discord.Embed(description=f"<:cross:1156150663802265670>  This role is higher than my role, move it to the top!", color=0xff0000)
            return await ctx.send(embed=em, delete_after=15)
        if role.is_bot_managed() or role.is_premium_subscriber():
            return await ctx.reply("It is a integrated role. Please provide a different role", delete_after=15)
        if not role.is_assignable():
            return await ctx.reply("I cant assign this role to anyone so please check my permissions and position.", delete_after=15)
        if role in user.roles:
            await user.remove_roles(role, reason=f"Role removed by {ctx.author.name}")
            em=discord.Embed(description=f"<:confirm:1156150922200748053>  Successfully removed {role.mention} from {user.mention}", color=ctx.author.color)
            return await ctx.send(embed=em)
        await user.add_roles(role, reason=f"Role given by {ctx.author.name}")
        em=discord.Embed(description=f"<:confirm:1156150922200748053>  Successfully Given {role.mention} to {user.mention}", color=ctx.author.color)
        await ctx.reply(embed=em)

    @role.command(name="all", description="Gives a role to all the members in the server")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def role_all(self, ctx, *,role: discord.Role):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 933738517845118976]:
                em = discord.Embed(description=f"<:cross:1156150663802265670>  You must Have Higher Role than Bot To run This Command", color=0xff0000)
                return await ctx.send(embed=em, delete_after=15)
        try:
            if self.bot.role_status[ctx.guild.id] is not None:
                em = discord.Embed(description=f"<:cross:1156150663802265670>  Already a add role process is running", color=0xff0000)
                return await ctx.send(embed=em)
        except:
            pass
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:        
            if role.position >= ctx.author.top_role.position:
                em = discord.Embed(description=f"<:cross:1156150663802265670>  That role has the same or higher position as your top role!", color=0xff0000)
                return await ctx.send(embed=em, delete_after=15)

        if role.position >= ctx.guild.me.top_role.position:
            em = discord.Embed(description=f"<:cross:1156150663802265670>  This role is higher than my role, move it to the top!", color=0xff0000)
            return await ctx.send(embed=em, delete_after=15)
        if role.is_bot_managed() or role.is_premium_subscriber():
            return await ctx.reply("It is a integrated role. Please provide a different role", delete_after=15)
        if not role.is_assignable():
            return await ctx.reply("I cant assign this role to anyone so please check my permissions and position.", delete_after=15)
        test = [member for member in ctx.guild.members if not role in member.roles]
        if len(test) == 0:
            return await ctx.reply(embed=discord.Embed(description=f"{role.mention} is already given to all the members of the server", color=0xc283fe))
        emb=discord.Embed(description=f"Do you want to give __{role.mention}__ to {len(test)} Members?", color=ctx.author.color)
        v = OnOrOff(ctx)
        init = await ctx.send(embed=emb, view=v)
        await v.wait()
        if v.value == 'Yes':
            pass
        else:
            return await init.delete()
        self.bot.role_status[ctx.guild.id] = (0, len(test), True)
        em=discord.Embed(description=f"**<a:loading:988108755768062033>  |  Giving __{role.mention}__ to {len(test)} Members**", color=ctx.author.color)
        await init.edit(embed=em, view=None)
        for member in test:
            if self.bot.role_status[ctx.guild.id] is not None:
                count, total_count, sts = self.bot.role_status[ctx.guild.id]
                self.bot.role_status[ctx.guild.id] = (count+1, len(test), True)
                await member.add_roles(role, reason=f"Role all runned by {ctx.author.name}")
        if count+1 != total_count:
            em1=discord.Embed(description=f"**<:confirm:1156150922200748053>  |  Cancelled the process of Giving role | Given __{role.mention}__ to {count+1} members out of {total_count}**", color=ctx.author.color)
        else:
            em1=discord.Embed(description=f"**<:confirm:1156150922200748053>  |  Given __{role.mention}__ to {total_count} Members**", color=ctx.author.color)
        self.bot.role_status[ctx.guild.id] = None
        await init.delete()
        try:
            await ctx.reply(embed=em1)
        except:
            await ctx.send(embed=em1)

    @role.command(name="bots", description="Gives a role to all the bots in the server")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def role_bots(self, ctx, *,role: discord.Role):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 933738517845118976]:
                em = discord.Embed(description=f"<:cross:1156150663802265670>  You must Have Higher Role than Bot To run This Command", color=0xff0000)
                return await ctx.send(embed=em, delete_after=15)
        try:
            if self.bot.role_status[ctx.guild.id] is not None:
                em = discord.Embed(description=f"<:cross:1156150663802265670>  Already a add role process is running", color=0xff0000)
                return await ctx.send(embed=em, delete_after=15)
        except:
            pass
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:        
            if role.position >= ctx.author.top_role.position:
                em = discord.Embed(description=f"<:cross:1156150663802265670>  That role has the same or higher position as your top role!", color=0xff0000)
                return await ctx.send(embed=em, delete_after=15)

        if role.position >= ctx.guild.me.top_role.position:
            em = discord.Embed(description=f"<:cross:1156150663802265670>  This role is higher than my role, move it to the top!", color=0xff0000)
            return await ctx.send(embed=em, delete_after=15)
        if role.is_bot_managed() or role.is_premium_subscriber():
            return await ctx.reply("It is a integrated role. Please provide a different role", delete_after=15)
        if not role.is_assignable():
            return await ctx.reply("I cant assign this role to anyone so please check my permissions and position.", delete_after=15)
        test = [member for member in ctx.guild.members if all([member.bot, not role in member.roles])]
        if len(test) == 0:
            return await ctx.reply(embed=discord.Embed(description=f"{role.mention} is already given to all the bots of the server", color=0xc283fe))
        emb=discord.Embed(description=f"Do you want to give __{role.mention}__ to {len(test)} Bots?", color=ctx.author.color)
        v = OnOrOff(ctx)
        init = await ctx.send(embed=emb, view=v)
        await v.wait()
        if v.value == 'Yes':
            pass
        else:
            return await init.delete()
        self.bot.role_status[ctx.guild.id] = (0, len(test), True)
        em=discord.Embed(description=f"**<a:loading:988108755768062033>  |  Giving __{role.mention}__ to {len(set(test))} Bots**", color=ctx.author.color)
        await init.edit(embed=em, view=None)
        for bot_members in test:
            if self.bot.role_status[ctx.guild.id] is not None:
                count, total_count, sts = self.bot.role_status[ctx.guild.id]
                self.bot.role_status[ctx.guild.id] = (count+1, len(test), True)
                await bot_members.add_roles(role, reason=f"Role bots runned by {ctx.author.name}")
        if count+1 != total_count:
            em1=discord.Embed(description=f"**<:confirm:1156150922200748053>  |  Cancelled the process of Giving role | Given __{role.mention}__ to {count+1} Bots out of {total_count}**", color=ctx.author.color)
        else:
            em1=discord.Embed(description=f"**<:confirm:1156150922200748053>  |  Given __{role.mention}__ to {total_count} Bots**", color=ctx.author.color)
        self.bot.role_status[ctx.guild.id] = None
        await init.delete()
        try:
            await ctx.reply(embed=em1)
        except:
            await ctx.send(embed=em1)

    @role.command(name="humans", description="Gives a role to all the users in the server")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def role_humans(self, ctx, *,role: discord.Role):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 933738517845118976]:
                em = discord.Embed(description=f"<:cross:1156150663802265670>  You must Have Higher Role than Bot To run This Command", color=0xff0000)
                return await ctx.send(embed=em, delete_after=15)
        try:
            if self.bot.role_status[ctx.guild.id] is not None:
                em = discord.Embed(description=f"<:cross:1156150663802265670>  Already a add role process is running", color=0xff0000)
                return await ctx.send(embed=em, delete_after=15)
        except:
            pass
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:        
            if role.position >= ctx.author.top_role.position:
                em = discord.Embed(description=f"<:cross:1156150663802265670>  That role has the same or higher position as your top role!", color=0xff0000)
                return await ctx.send(embed=em, delete_after=15)

        if role.position >= ctx.guild.me.top_role.position:
            em = discord.Embed(description=f"<:cross:1156150663802265670>  This role is higher than my role, move it to the top!", color=0xff0000)
            return await ctx.send(embed=em, delete_after=15)
        if role.is_bot_managed() or role.is_premium_subscriber():
            return await ctx.reply("It is a integrated role. Please provide a different role", delete_after=15)
        if not role.is_assignable():
            return await ctx.reply("I cant assign this role to anyone so please check my permissions and position.", delete_after=15)
        test = [member for member in ctx.guild.members if all([not member.bot, not role in member.roles])]
        if len(test) == 0:
            return await ctx.reply(embed=discord.Embed(description=f"{role.mention} is already given to all the users of the server", color=0xc283fe))
        emb=discord.Embed(description=f"Do you want to give __{role.mention}__ to {len(test)} Users?", color=ctx.author.color)
        v = OnOrOff(ctx)
        init = await ctx.send(embed=emb, view=v)
        await v.wait()
        if v.value == 'Yes':
            pass
        else:
            return await init.delete()
        self.bot.role_status[ctx.guild.id] = (0, len(test), True)
        em=discord.Embed(description=f"**<a:loading:988108755768062033>  |  Giving __{role.mention}__ to {len(set(test))} Users**", color=ctx.author.color)
        await init.edit(embed=em, view=None)
        for humans in test:
            if self.bot.role_status[ctx.guild.id] is not None:
                count, total_count, sts = self.bot.role_status[ctx.guild.id]
                self.bot.role_status[ctx.guild.id] = (count+1, len(test), True)
                await humans.add_roles(role, reason=f"Role humans runned by {ctx.author.name}")
        if count+1 != total_count:
            em1=discord.Embed(description=f"**<:confirm:1156150922200748053>  |  Cancelled the process of Giving role | Given __{role.mention}__ to {count+1} Users out of {total_count}**", color=ctx.author.color)
        else:
            em1=discord.Embed(description=f"**<:confirm:1156150922200748053>  |  Given __{role.mention}__ to {total_count} Users**", color=ctx.author.color)
        self.bot.role_status[ctx.guild.id] = None
        await init.delete()
        try:
            await ctx.reply(embed=em1)
        except:
            await ctx.send(embed=em1)

    @role.command(name="status", description="Shows the status of current adding role process")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def role_status(self, ctx):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 933738517845118976]:
                em = discord.Embed(description=f"<:cross:1156150663802265670>  You must Have Higher Role than Bot To run This Command", color=0xff0000)
                return await ctx.send(embed=em, delete_after=15)
        try:
            if self.bot.role_status[ctx.guild.id] is None:
                em = discord.Embed(description=f"<:cross:1156150663802265670>  No add role process is running", color=0xff0000)
                return await ctx.send(embed=em, delete_after=15)
        except:
                em = discord.Embed(description=f"<:cross:1156150663802265670>  No add role process is running", color=0xff0000)
                return await ctx.send(embed=em, delete_after=15)
        count, total_count, sts = self.bot.role_status[ctx.guild.id]
        em = discord.Embed(description=f"Given roles to {count} users out of {total_count} users ({count/total_count * 100.0}%) of adding roles to {total_count} users", color=0xc283fe)
        em.set_footer(text=f"{str(self.bot.user)} Adding role", icon_url=self.bot.user.display_avatar.url)
        await ctx.send(embed=em)

    @role.command(name="cancel", description="Cancel the current adding role process")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def role_cancel(self, ctx):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 933738517845118976]:
                em = discord.Embed(description=f"<:cross:1156150663802265670>  You must Have Higher Role than Bot To run This Command", color=0xff0000)
                return await ctx.send(embed=em, delete_after=15)
        try:
            if self.bot.role_status[ctx.guild.id] is None:
                em = discord.Embed(description=f"<:cross:1156150663802265670>  No add role process is running", color=0xff0000)
                return await ctx.send(embed=em, delete_after=15)
        except:
                em = discord.Embed(description=f"<:cross:1156150663802265670>  No add role process is running", color=0xff0000)
                return await ctx.send(embed=em, delete_after=15)
        self.bot.role_status[ctx.guild.id] = None
        
    @commands.group(
        invoke_without_command=True,
        aliases=["removerole"], description="Removes a role from the user"
    )
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def rrole(self, ctx, user: discord.Member, *,role: discord.Role):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 933738517845118976]:
                em = discord.Embed(description=f"<:cross:1156150663802265670>  You must Have Higher Role than Bot To run This Command", color=0xff0000)
                return await ctx.send(embed=em, delete_after=15)

        if not role in user.roles:
            em = discord.Embed(description=f'<:cross:1156150663802265670>  The member do not has this role!', color=0xff0000)
            return await ctx.send(embed=em, delete_after=15)
            
        if role == ctx.author.top_role.position:
            em = discord.Embed(description=f"<:cross:1156150663802265670>  That role has the same position as your top role!", color=0xff0000)
            return await ctx.send(embed=em, delete_after=15)

        if role.position >= ctx.guild.me.top_role.position:
            em = discord.Embed(description=f"<:cross:1156150663802265670>  This role is higher than my role, move it to the top!", color=0xff0000)
            return await ctx.send(embed=em, delete_after=15)
        if role.is_bot_managed() or role.is_premium_subscriber():
            return await ctx.reply("It is a integrated role. Please provide a different role", delete_after=15)
        if not role.is_assignable():
            return await ctx.reply("I cant assign this role to anyone so please check my permissions and position.", delete_after=15)
        await user.remove_roles(role, reason=f"role removed by {ctx.author.name}")
        em=discord.Embed(description=f"<:confirm:1156150922200748053>  Successfully Removed {role.mention} From {user.mention}", color=ctx.author.color)
        await ctx.send(embed=em)

    @rrole.command(name="all", description="Removes a role from all the members in the server")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def rrole_all(self, ctx, *,role: discord.Role):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 933738517845118976]:
                em = discord.Embed(description=f"<:cross:1156150663802265670>  You must Have Higher Role than Bot To run This Command", color=0xff0000)
                return await ctx.send(embed=em, delete_after=15)
        try:
            if self.bot.rrole_status[ctx.guild.id] is not None:
                em = discord.Embed(description=f"<:cross:1156150663802265670>  Already a remove role process is running", color=0xff0000)
                return await ctx.send(embed=em, delete_after=15)
        except:
            pass
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:        
            if role.position >= ctx.author.top_role.position:
                em = discord.Embed(description=f"<:cross:1156150663802265670>  That role has the same or higher position as your top role!", color=0xff0000)
                return await ctx.send(embed=em, delete_after=15)

        if role.position >= ctx.guild.me.top_role.position:
            em = discord.Embed(description=f"<:cross:1156150663802265670>  This role is higher than my role, move it to the top!", color=0xff0000)
            return await ctx.send(embed=em, delete_after=15)
        if role.is_bot_managed() or role.is_premium_subscriber():
            return await ctx.reply("It is a integrated role. Please provide a different role", delete_after=15)
        if not role.is_assignable():
            return await ctx.reply("I cant assign this role to anyone so please check my permissions and position.", delete_after=15)
        test = [member for member in ctx.guild.members if role in member.roles]
        if len(test) == 0:
            return await ctx.reply(embed=discord.Embed(description=f"{role.mention} is already removed from all the members of the server", color=0xc283fe))
        emb=discord.Embed(description=f"Do you want to remove __{role.mention}__ from {len(test)} Members?", color=ctx.author.color)
        v = OnOrOff(ctx)
        init = await ctx.send(embed=emb, view=v)
        await v.wait()
        if v.value == 'Yes':
            pass
        else:
            return await init.delete()
        self.bot.rrole_status[ctx.guild.id] = (0, len(test), True)
        em=discord.Embed(description=f"**<a:loading:988108755768062033>  |  Removing __{role.mention}__ from {len(test)} Members**", color=ctx.author.color)
        await init.edit(embed=em, view=None)
        for member in test:
            if self.bot.rrole_status[ctx.guild.id] is not None:
                count, total_count, sts = self.bot.rrole_status[ctx.guild.id]
                self.bot.rrole_status[ctx.guild.id] = (count+1, len(test), True)
                await member.remove_roles(role, reason=f"Rrole all runned by {ctx.author.name}")
        if count+1 != total_count:
            em1=discord.Embed(description=f"**<:confirm:1156150922200748053>  |  Cancelled the process of Removing role | Removed __{role.mention}__ from {count+1} Users out of {total_count}**", color=ctx.author.color)
        else:
            em1=discord.Embed(description=f"**<:confirm:1156150922200748053>  |  Removed __{role.mention}__ from {total_count} Members**", color=ctx.author.color)
        self.bot.rrole_status[ctx.guild.id] = None
        await init.delete()
        try:
            await ctx.reply(embed=em1)
        except:
            await ctx.send(embed=em1)

    @rrole.command(name="bots", description="Removes a role from all the bots in the server")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def rrole_bots(self, ctx, *,role: discord.Role):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 933738517845118976]:
                em = discord.Embed(description=f"<:cross:1156150663802265670>  You must Have Higher Role than Bot To run This Command", color=0xff0000)
                return await ctx.send(embed=em, delete_after=15)
        try:
            if self.bot.rrole_status[ctx.guild.id] is not None:
                em = discord.Embed(description=f"<:cross:1156150663802265670>  Already a remove role process is running", color=0xff0000)
                return await ctx.send(embed=em, delete_after=15)
        except:
            pass
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:        
            if role.position >= ctx.author.top_role.position:
                em = discord.Embed(description=f"<:cross:1156150663802265670>  That role has the same or higher position as your top role!", color=0xff0000)
                return await ctx.send(embed=em, delete_after=15)

        if role.position >= ctx.guild.me.top_role.position:
            em = discord.Embed(description=f"<:cross:1156150663802265670>  This role is higher than my role, move it to the top!", color=0xff0000)
            return await ctx.send(embed=em, delete_after=15)
        if role.is_bot_managed() or role.is_premium_subscriber():
            return await ctx.reply("It is a integrated role. Please provide a different role", delete_after=15)
        if not role.is_assignable():
            return await ctx.reply("I cant assign this role to anyone so please check my permissions and position.", delete_after=15)
        test = [member for member in ctx.guild.members if all([member.bot, role in member.roles])]
        if len(test) == 0:
            return await ctx.reply(embed=discord.Embed(description=f"{role.mention} is already removed from all the bots of the server", color=0xc283fe))
        emb=discord.Embed(description=f"Do you want to remove __{role.mention}__ from {len(test)} Bots?", color=ctx.author.color)
        v = OnOrOff(ctx)
        init = await ctx.send(embed=emb, view=v)
        await v.wait()
        if v.value == 'Yes':
            pass
        else:
            return await init.delete()
        self.bot.rrole_status[ctx.guild.id] = (0, len(test), True)
        em=discord.Embed(description=f"**<a:loading:988108755768062033>  |  Removing __{role.mention}__ from {len(set(test))} Bots**", color=ctx.author.color)
        await init.edit(embed=em, view=None)
        for bot_members in test:
            if self.bot.rrole_status[ctx.guild.id] is not None:
                count, total_count, sts = self.bot.rrole_status[ctx.guild.id]
                self.bot.rrole_status[ctx.guild.id] = (count+1, len(test), True)
                await bot_members.remove_roles(role, reason=f"Rrole bots runned by {ctx.author.name}")
        if count+1 != total_count:
            em1=discord.Embed(description=f"**<:confirm:1156150922200748053>  |  Cancelled the process of Removing role | Removed __{role.mention}__ from {count+1} Bots out of {total_count}**", color=ctx.author.color)
        else:
            em1=discord.Embed(description=f"**<:confirm:1156150922200748053>  |  Removed __{role.mention}__ from {total_count} Bots**", color=ctx.author.color)
        self.bot.rrole_status[ctx.guild.id] = None
        await init.delete()
        try:
            await ctx.reply(embed=em1)
        except:
            await ctx.send(embed=em1)

    @rrole.command(name="humans", description="Removes a role from all the users in the server")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def rrole_humans(self, ctx, *,role: discord.Role):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 933738517845118976]:
                em = discord.Embed(description=f"<:cross:1156150663802265670>  You must Have Higher Role than Bot To run This Command", color=0xff0000)
                return await ctx.send(embed=em, delete_after=15)
        try:
            if self.bot.rrole_status[ctx.guild.id] is not None:
                em = discord.Embed(description=f"<:cross:1156150663802265670>  Already a remove role process is running", color=0xff0000)
                return await ctx.send(embed=em, delete_after=15)
        except:
            pass
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:        
            if role.position >= ctx.author.top_role.position:
                em = discord.Embed(description=f"<:cross:1156150663802265670>  That role has the same or higher position as your top role!", color=0xff0000)
                return await ctx.send(embed=em, delete_after=15)

        if role.position >= ctx.guild.me.top_role.position:
            em = discord.Embed(description=f"<:cross:1156150663802265670>  This role is higher than my role, move it to the top!", color=0xff0000)
            return await ctx.send(embed=em, delete_after=15)
        if role.is_bot_managed() or role.is_premium_subscriber():
            return await ctx.reply("It is a integrated role. Please provide a different role", delete_after=15)
        if not role.is_assignable():
            return await ctx.reply("I cant assign this role to anyone so please check my permissions and position.", delete_after=15)
        test = [member for member in ctx.guild.members if all([not member.bot, role in member.roles])]
        if len(test) == 0:
            return await ctx.reply(embed=discord.Embed(description=f"{role.mention} is already removed from all the users of the server", color=0xc283fe))
        emb=discord.Embed(description=f"Do you want to remove __{role.mention}__ from {len(test)} Users?", color=ctx.author.color)
        v = OnOrOff(ctx)
        init = await ctx.send(embed=emb, view=v)
        await v.wait()
        if v.value == 'Yes':
            pass
        else:
            return await init.delete()
        self.bot.rrole_status[ctx.guild.id] = (0, len(test), True)
        em=discord.Embed(description=f"**<a:loading:988108755768062033>  |  Removing __{role.mention}__ from {len(set(test))} Users**", color=ctx.author.color)
        await init.edit(embed=em, view=None)
        for humans in test:
            if self.bot.rrole_status[ctx.guild.id] is not None:
                count, total_count, sts = self.bot.rrole_status[ctx.guild.id]
                self.bot.rrole_status[ctx.guild.id] = (count+1, len(test), True)
                await humans.remove_roles(role, reason=f"Rrole humans runned by {ctx.author.name}")
        if count+1 != total_count:
            em1=discord.Embed(description=f"**<:confirm:1156150922200748053>  |  Cancelled the process of Removing role | Removed __{role.mention}__ from {count+1} Users out of {total_count}**", color=ctx.author.color)
        else:
            em1=discord.Embed(description=f"**<:confirm:1156150922200748053>  |  Removed __{role.mention}__ from {total_count} Users**", color=ctx.author.color)
        self.bot.rrole_status[ctx.guild.id] = None
        await init.delete()
        try:
            await ctx.reply(embed=em1)
        except:
            await ctx.send(embed=em1)

    @rrole.command(name="status", description="Shows the status of current remove role process")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def rrole_status(self, ctx):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 933738517845118976]:
                em = discord.Embed(description=f"<:cross:1156150663802265670>  You must Have Higher Role than Bot To run This Command", color=0xff0000)
                return await ctx.send(embed=em, delete_after=15)
        try:
            if self.bot.rrole_status[ctx.guild.id] is None:
                em = discord.Embed(description=f"<:cross:1156150663802265670>  No remove role process is running", color=0xff0000)
                return await ctx.send(embed=em, delete_after=15)
        except:
                em = discord.Embed(description=f"<:cross:1156150663802265670>  No remove role process is running", color=0xff0000)
                return await ctx.send(embed=em, delete_after=15)
        count, total_count, sts = self.bot.rrole_status[ctx.guild.id]
        em = discord.Embed(description=f"Removed roles from {count} users out of {total_count} users ({count/total_count * 100.0}%) of removing roles to {total_count} users", color=0xc283fe)
        em.set_footer(text=f"{str(self.bot.user)} Removing roles", icon_url=self.bot.user.display_avatar.url)
        await ctx.send(embed=em)

    @rrole.command(name="cancel", description="Cancel the current Remove role process")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def rrole_cancel(self, ctx):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 933738517845118976]:
                em = discord.Embed(description=f"<:cross:1156150663802265670>  You must Have Higher Role than Bot To run This Command", color=0xff0000)
                return await ctx.send(embed=em, delete_after=15)
        try:
            if self.bot.rrole_status[ctx.guild.id] is None:
                em = discord.Embed(description=f"<:cross:1156150663802265670>  No remove role process is running", color=0xff0000)
                return await ctx.send(embed=em, delete_after=15)
        except:
                em = discord.Embed(description=f"<:cross:1156150663802265670>  No remove role process is running", color=0xff0000)
                return await ctx.send(embed=em, delete_after=15)
        self.bot.rrole_status[ctx.guild.id] = None
        em = discord.Embed(description="Succesfully Cancelled the process", color=0xc283fe)
        await ctx.send(embed=em)

    @commands.command(aliases=["mute"], description="Timeouts a user for specific time\nIf you don't provide the time the user will be timeout for 5 minutes")
    @commands.bot_has_guild_permissions(manage_roles=True)
    @commands.has_permissions(manage_roles=True)
    async def timeout(self, ctx, member: discord.Member, *, time= None):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= member.top_role.position:
                em = discord.Embed(description=f"<:cross:1156150663802265670>  Your Top role should be above the top role of {str(member)}", color=0xff0000)
                return await ctx.reply(embed=em, mention_author=False)
        if member.id == ctx.guild.owner.id:
            em = discord.Embed(description=f"<:cross:1156150663802265670>  Idiot! You cannot mute owner of the server", color=0xff0000)
            return await ctx.send(embed=em)
        if ctx.guild.me.top_role.position == member.top_role.position:
            em = discord.Embed(description=f"<:cross:1156150663802265670>  My highest role is same as of {str(member)}!", color=0xff0000)
            return await ctx.send(embed=em)
        if member.top_role.position > ctx.guild.me.top_role.position:
            em = discord.Embed(description=f"<:cross:1156150663802265670>  My highest role is below {str(member)}!", color=0xff0000)
            return await ctx.send(embed=em)
        if time is None:
            time = "5m"
        converted_time = convert(time)
        if converted_time == -1 or converted_time == -2:
            em = discord.Embed(description=f"<:cross:1156150663802265670>  Provide specific time!", color=0xff0000)
            return await ctx.send(embed=em)
        timeout_until = discord.utils.utcnow() + datetime.timedelta(seconds=converted_time[0])
        await member.edit(timed_out_until=timeout_until, reason=f"Muted by {ctx.author}")
        em = discord.Embed(description=f"[{member}](https://discord.com/users/{member.id}) ( ID: {member.id} ) was successfully Muted.", color=0xc283fe)
        em.set_author(name="Successfully Muted", icon_url="https://media.discordapp.net/attachments/1155964405129953391/1155964438332063854/verified.png?width=160&height=160")
        em.add_field(name="<:banhammer:1155963619691986944> Moderator", value=f"{ctx.author.mention} ( ID: {ctx.author.id} )", inline=True)
        await ctx.channel.send(embed=em)
        em = discord.Embed(description=f'YOU HAVE BEEN MUTED FROM {ctx.guild.name}', color=0xc283fe)
        em.set_footer(text=f'Muted by {ctx.author.name}')
        return await member.send(embed=em)

    @commands.command(description="Removes the timeout from the user")
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def unmute(self, ctx, *,member: discord.Member):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= member.top_role.position:
                em = discord.Embed(description=f"<:cross:1156150663802265670>  Your Top role should be above the top role of {str(member)}", color=0xff0000)
                return await ctx.reply(embed=em, mention_author=False)
        if member.id == ctx.guild.owner.id:
            em = discord.Embed(description=f"<:cross:1156150663802265670>  Idiot! You cannot unmute owner of the server", color=0xff0000)
            return await ctx.send(embed=em)
        if ctx.guild.me.top_role.position == member.top_role.position:
            em = discord.Embed(description=f"<:cross:1156150663802265670>  My highest role is same as of {str(member)}!", color=0xff0000)
            return await ctx.send(embed=em)
        if member.top_role.position >= ctx.guild.me.top_role.position:
            em = discord.Embed(description=f"<:cross:1156150663802265670>  My highest role is below {str(member)}!", color=0xff0000)
            return await ctx.send(embed=em)
        guild = ctx.guild
        await member.edit(timed_out_until=None, reason=f"Unmuted by {ctx.author}")
        em = discord.Embed(description=f"[{member}](https://discord.com/users/{member.id}) ( ID: {member.id} ) was successfully Unmuted.", color=0xc283fe)
        em.set_author(name="Successfully Unmuted", icon_url="https://media.discordapp.net/attachments/1155964405129953391/1155964438332063854/verified.png?width=160&height=160")
        em.add_field(name="<:banhammer:1155963619691986944> Moderator", value=f"{ctx.author.mention} ( ID: {ctx.author.id} )", inline=True)
        await ctx.channel.send(embed=em)
        em = discord.Embed(description=f'YOU HAVE BEEN UNMUTED FROM {ctx.guild.name}', color=0xc283fe)
        em.set_footer(text=f'Unmuted by {ctx.author.name}')
        return await member.send(embed=em)

    @commands.command(aliases=["setnick"], description="Changes the user's nickname for the server")
    @commands.has_permissions(manage_nicknames=True)
    @commands.bot_has_guild_permissions(manage_nicknames=True)
    async def nick(self, ctx, member : discord.Member, *, Name=None):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:

            if ctx.author.top_role.position <= member.top_role.position:
                em = discord.Embed(description=f"<:cross:1156150663802265670>  Your Top role should be above the top role of {str(member)}", color=0xff0000)
                return await ctx.reply(embed=em, mention_author=False)
        if member.id == ctx.guild.owner.id:
            em = discord.Embed(description=f"<:cross:1156150663802265670>  Idiot! You cannot change nick of owner of the server", color=0xff0000)
            return await ctx.send(embed=em)
        if ctx.guild.me.top_role.position == member.top_role.position:
            em = discord.Embed(description=f"<:cross:1156150663802265670>  My highest role is same as of {str(member)}!", color=0xff0000)
            return await ctx.send(embed=em)
        if member.top_role.position >= ctx.guild.me.top_role.position:
            em = discord.Embed(description=f"<:cross:1156150663802265670>  My highest role is below {str(member)}!", color=0xff0000)
            return await ctx.send(embed=em)
        if Name is None:
            await member.edit(nick=None, reason=f"Nickname changed by {ctx.author.name}")
            em = discord.Embed(description=f"Successfully cleared nickname of {str(member)}", color=0xc283fe)
            return await ctx.reply(embed=em, mention_author=False)
        if Name is not None:
            await member.edit(nick=Name, reason=f"Nickname changed by {ctx.author.name}")
            em = discord.Embed(description=f"{member} ( ID: {member.id} ) was successfully Renamed.", color=0xc283fe)
            em.set_author(name="Successfully Changed Nick", icon_url="https://media.discordapp.net/attachments/1155964405129953391/1155964438332063854/verified.png?width=160&height=160")
            em.add_field(name="<:banhammer:1155963619691986944> Moderator", value=f"{ctx.author.mention} ( ID: {ctx.author.id} )", inline=True)
            return await ctx.reply(embed=em, mention_author=False)

    @commands.command(description="Kicks a member from the server")
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_guild_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 933738517845118976]:
                em = discord.Embed(description=f"<:cross:1156150663802265670>  You must Have Higher Role than me To run This command", color=0xff0000)
                return await ctx.send(embed=em)
            
        if member.id == ctx.guild.owner.id:
            em = discord.Embed(description=f"<:cross:1156150663802265670>  Idiot! You cannot kick owner of the server", color=0xff0000)
            return await ctx.send(embed=em)

        if ctx.guild.me.top_role.position == member.top_role.position:
            em = discord.Embed(description=f"<:cross:1156150663802265670>  My highest role is same as of {str(member)}!", color=0xff0000)
            return await ctx.send(embed=em)
        if member.top_role.position >= ctx.guild.me.top_role.position:
            em = discord.Embed(description=f"<:cross:1156150663802265670>  My highest role is below {str(member)}!", color=0xff0000)
            return await ctx.send(embed=em)
        rs = "No Reason Provided."

        if reason:
            rs = str(reason)[:500]

        await member.kick(reason=f"Kicked by {ctx.author.name} for {reason}")
        em = discord.Embed(description=f"[{member}](https://discord.com/users/{member.id}) ( ID: {member.id} ) was successfully kicked.", color=0xc283fe)
        em.set_author(name="Successfully Kicked", icon_url="https://media.discordapp.net/attachments/1155964405129953391/1155964438332063854/verified.png?width=160&height=160")
        em.add_field(name="<:gtpage:1155963628311289967> Reason", value=f"{rs}", inline=True)
        em.add_field(name="<:banhammer:1155963619691986944> Moderator", value=f"{ctx.author.mention} ( ID: {ctx.author.id} )", inline=True)
        await ctx.channel.send(embed=em)
        if reason:
            await member.send(embed=discord.Embed(description=f'You have been kicked from **{ctx.guild.name}** with the reason: `{rs}`', color=0xc283fe))
        else:
            await member.send(embed=discord.Embed(description=f'You have been kicked from **{ctx.guild.name}**', color=0xc283fe))


    @commands.command(description="Unbans a member from the server")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(ban_members=True)
    async def unban(self, ctx: commands.Context, user: discord.User):
        async for x in ctx.guild.bans():
            if x.id == user.id:
                await ctx.guild.unban(user, reason=f"Unbanned by {ctx.author.name}")
                return await ctx.send(f'<:confirm:1156150922200748053>  Unbanned **{str(user)}**!')
        await ctx.send(f'**{str(user)}** is not banned!')
    
    @commands.command(description="Unban all the banned members in the server")
    @commands.cooldown(1, 120, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(ban_members=True)
    async def unbanall(self, ctx):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [994130204949745705, 979353019235840000]:
                em = discord.Embed(description=f"<:cross:1156150663802265670> You must Have Higher Role than Bot To run This Command", color=0xff0000)
                return await ctx.send(embed=em)
        xd = [member async for member in ctx.guild.bans()]
        if len(xd) == 0:
            return await ctx.send("No Banned Users")
        view = OnOrOff(ctx)
        em = discord.Embed(description=f"Would You Like To Unban {len(xd)} Users", color=0xc283fe)
        try:
            em.set_author(name=str(ctx.author), icon_url=ctx.author.display_avatar.url)
        except:
            em.set_author(name=str(ctx.author))
        test = await ctx.reply(embed=em, view=view)
        await view.wait()
        if not view.value:
            return await test.edit(content="Timed out!", view=None)
        if view.value == 'Yes':
            await test.delete()
            count = 0
            async for member in ctx.guild.bans():
                await ctx.guild.unban(member.user, reason=f"Unbaned by {ctx.author.name}")
                count+=1
        em = discord.Embed(description=f"Succesfully Unbanned All.", color=0xc283fe)
        em.set_author(name="Successfully Unbanned All", icon_url="https://media.discordapp.net/attachments/1155964405129953391/1155964438332063854/verified.png?width=160&height=160")
        em.add_field(name="<:banhammer:1155963619691986944> Moderator", value=f"{ctx.author.mention} ( ID: {ctx.author.id} )", inline=True)
        return await ctx.reply(embed=em, mention_author=False)
        if view.value == 'No':
            await test.delete()
            em = discord.Embed(description="Canceled The Command", color=0xc283fe)
            return await ctx.reply(embed=em, mention_author=False)

    @commands.command(description="Warns the user")
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, user: discord.Member,*,reason=None):
        query = "SELECT * FROM  warn WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            w_db = cursor.fetchone()
        if w_db is None:
            count = 1
            data = {}
            ls = []
        else:
            data = literal_eval(w_db['data'])
            if user.id in data:
                ls = data[user.id]
            else:
                ls = []
            count = w_db['count'] + 1
        dic = {}
        if reason != None:
            try:
                await user.send(f'You have been warned from {ctx.guild.name} for {reason}')
                em = discord.Embed(description=f"<:confirm:1156150922200748053>  {user} Has been warned \n<:next:1154735525505269871> Reason: {reason}\n<:next:1154735525505269871> Warning id: {count}", color=0xc283fe)
                await ctx.send(embed=em)
            except:
                em = discord.Embed(description=f"<:confirm:1156150922200748053>  {user} Has been warned \n<:next:1154735525505269871> Reason: {reason}\n<:next:1154735525505269871> Warning id: {count}", color=0xc283fe)
                await ctx.send(embed=em)
            dic[count] = {}
            dic[count]['mod'] = ctx.author.id
            dic[count]['reason'] = reason
        if reason == None:
            try:
                await user.send(f'You have been warned from {ctx.guild.name}')
                em = discord.Embed(description=f"<:confirm:1156150922200748053>  {user} Has been warned\nWarning id: {count}", color=0x00f7ff)
                await ctx.send(embed=em)
            except:
                em = discord.Embed(description=f"<:confirm:1156150922200748053>  {user} Has been warned but the dm's are off\nWarning id: {count}", color=0x00f7ff)
                await ctx.send(embed=em)
            dic[count] = {}
            dic[count]['mod'] = ctx.author.id
            dic[count]['reason'] = 'None'
        ls.append(dic)
        data[user.id] = ls
        if w_db is None:
            sql = (f"INSERT INTO warn(guild_id, 'data', 'count') VALUES(?, ?, ?)")
            val = (ctx.guild.id, f"{data}", count)
            cursor.execute(sql, val)
        else:
            sql = (f"UPDATE warn SET data = ? WHERE guild_id = ?")
            val = (f"{data}", ctx.guild.id,)
            cursor.execute(sql, val)
            sql = (f"UPDATE warn SET count = ? WHERE guild_id = ?")
            val = (count, ctx.guild.id,)
            cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
    
    @commands.group(invoke_without_command=True, alias=['warnings'], description="Shows warnings of a specific user")
    @commands.has_guild_permissions(manage_messages=True)
    async def warning(self, ctx: commands.Context, *, user: discord.Member):
        no_warn_em = discord.Embed(description=f"There are no warnings for {user.mention}", color=0xc283fe).set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        query = "SELECT * FROM  warn WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            w_db = cursor.fetchone()
        if w_db is None:
            return await ctx.reply(embed=no_warn_em)
        else:
            data = literal_eval(w_db['data'])
            if user.id not in data:
                return await ctx.reply(embed=no_warn_em)
            else:
                ls = data[user.id]
                if len(ls) == 0:
                    return await ctx.reply(embed=no_warn_em)
                else:
                    pass
        ls1, warn = [], []
        count = 1
        for j in ls:
          for i in j:
            u = discord.utils.get(self.bot.users, id=j[i]['mod'])
            warn.append(f"`[{'0' + str(count) if count < 10 else count}]` | Warned by {u.mention} For the reason `{j[i]['reason']}` - Warning id: `{i}`")
            count += 1
        for i in range(0, len(warn), 15):
           ls1.append(warn[i: i + 15])
        em_list = []
        no = 1
        for k in ls1:
           embed =discord.Embed(color=0xc283fe)
           embed.title = f"Warning of {str(user)} - {count-1}"
           embed.description = "\n".join(k)
           embed.set_footer(text=f"{self.bot.user.name} • Page {no}/{len(ls1)}", icon_url=self.bot.user.display_avatar.url)
           em_list.append(embed)
           no+=1
        page = PaginationView(embed_list=em_list, ctx=ctx)
        await page.start(ctx)

    @warning.command(name="clear", description="Clears warning for a user")
    @commands.has_guild_permissions(manage_messages=True)
    async def _clear(self, ctx: commands.Context, *, user: discord.Member):
        no_warn_em = discord.Embed(description=f"<:next:1154735525505269871> {user.mention} has no warnings to be cleared", color=0xc283fe).set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        query = "SELECT * FROM  warn WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            w_db = cursor.fetchone()
        if w_db is None:
            return await ctx.reply(embed=no_warn_em)
        else:
            data = literal_eval(w_db['data'])
            if user.id not in data:
                return await ctx.reply(embed=no_warn_em)
            else:
                ls = data[user.id]
                if len(ls) == 0:
                    return await ctx.reply(embed=no_warn_em)
                else:
                    del data[user.id]
        sql = (f"UPDATE warn SET data = ? WHERE guild_id = ?")
        val = (f"{data}", ctx.guild.id,)
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        em = discord.Embed(description=f"<:confirm:1156150922200748053> Successfully cleared the warnings for {user.mention}", color=0xc283fe).set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        await ctx.reply(embed=em)

    @warning.command(name="remove", aliases=['delete'], description="Removes a warning from using its id")
    @commands.has_guild_permissions(manage_messages=True)
    async def _remove(self, ctx: commands.Context, id: str):
        if not id.isdigit():
            return await ctx.reply("Please provide the integer value")
        id = int(id)
        no_warn_em = discord.Embed(description=f"I was not able to find any warning with the id {id}", color=0xc283fe).set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        query = "SELECT * FROM  warn WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            w_db = cursor.fetchone()
        if w_db is None:
            return await ctx.reply(embed=no_warn_em)
        else:
            data = literal_eval(w_db['data'])
            c = False
            for i in data:
                for j in data[i]:
                    for k in j:
                        if k == id:
                            c = True
                            h = i
                            ls = data[i]
                            ls.remove(j)
                            data[i] = ls
                            break
            if not c:
                return await ctx.reply(embed=no_warn_em)
        sql = (f"UPDATE warn SET data = ? WHERE guild_id = ?")
        val = (f"{data}", ctx.guild.id,)
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        u = discord.utils.get(self.bot.users, id=h)
        em = discord.Embed(description=f"Successfully removed the warning of {u.mention} with the id `{id}`", color=0xc283fe).set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        await ctx.reply(embed=em)

    @commands.command(description="Bans the user from the server")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 933738517845118976]:
                em = discord.Embed(description=f"<:cross:1156150663802265670>  You must Have Higher Role than Bot To run This Command", color=0xff0000)
                return await ctx.send(embed=em)
            
        if member.id == ctx.guild.owner.id:
            em = discord.Embed(description=f"<:cross:1156150663802265670>  Idiot! You cannot ban owner of the server", color=0xff0000)
            return await ctx.send(embed=em)

        if ctx.guild.me.top_role.position == member.top_role.position:
            em = discord.Embed(description=f"<:cross:1156150663802265670>  My highest role is same as of {str(member)}!", color=0xff0000)
            return await ctx.send(embed=em)

        if member.top_role.position >= ctx.guild.me.top_role.position:
            em = discord.Embed(description=f"<:cross:1156150663802265670>  My highest role is below {str(member)}!", color=0xff0000)
            return await ctx.send(embed=em)
        await member.ban(reason=f"Banned by {ctx.author.name} for {reason}")
        em = discord.Embed(description=f"[{member}](https://discord.com/users/{member.id}) ( ID: {member.id} ) was successfully Banned.", color=0xc283fe)
        em.set_author(name="Successfully Banned", icon_url="https://media.discordapp.net/attachments/1155964405129953391/1155964438332063854/verified.png?width=160&height=160")
        em.add_field(name="<:gtpage:1155963628311289967> Reason", value=f"{reason}", inline=True)
        em.add_field(name="<:banhammer:1155963619691986944> Moderator", value=f"{ctx.author.mention} ( ID: {ctx.author.id} )", inline=True)
        await ctx.channel.send(embed=em)
        await member.send(embed=discord.Embed(description=f'You Have Been Banned From **{ctx.guild.name}** For The Reason: `{reason}`', color=0xc283fe))

    @commands.command(aliases=['nuke', 'clonechannel'], description="Clones the channel")
    @commands.cooldown(1, 15, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def clone(self, ctx, channel: discord.TextChannel = None):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 933738517845118976]:
                em = discord.Embed(description=f"<:cross:1156150663802265670>  You must Have Higher Role than Bot To run This Command", color=0xff0000)
                return await ctx.send(embed=em)
        if channel == None:
            channel = ctx.channel
        view = OnOrOff(ctx)
        em = discord.Embed(description=f"Would You Like To Clone {channel.mention} Channel", color=0xc283fe)
        try:
            em.set_author(name=str(ctx.author), icon_url=ctx.author.display_avatar.url)
        except:
            em.set_author(name=str(ctx.author))
        test = await ctx.reply(embed=em, view=view)
        await view.wait()
        if not view.value:
            return await test.edit(content="Timed out!", view=None)
        if view.value == 'Yes':
            await test.delete()
            channel_position = channel.position
            new = await channel.clone(reason=f"Channel nuked by {ctx.author.name}")
            await channel.delete(reason=f"Channel nuked by {ctx.author.name}")
            await new.edit(sync_permissions=True, position=channel_position)
            return await new.send(f"{ctx.author.mention}", embed=discord.Embed(title="Channel Nuked", description=f"<:confirm:1156150922200748053> Channel has been nuked by {ctx.author.mention}.", color=0xc283fe), mention_author=False)
        if view.value == 'No':
            await test.delete()
            em = discord.Embed(description="Canceled The Command", color=0xff0000)
            return await ctx.reply(embed=em, mention_author=False)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        
        webhook = discord.SyncWebhook.from_url(webhook_cmd_logs)
        try:
            emb = discord.Embed(title=f"Command runned in {ctx.guild.name}", description=f"Command name: `{ctx.command.qualified_name}`\nAuthor Name: {str(ctx.author)}\nGuild Id: {ctx.guild.id}\nCommand executed: `{ctx.message.content}`\nChannel name: {ctx.channel.name}\nChannel Id: {ctx.channel.id}\nJump Url: [Jump to]({ctx.message.jump_url})\nCommand runned without error: False", timestamp=ctx.message.created_at, color=0xc283fe)
        except:
            return
        emb.set_thumbnail(url=ctx.author.display_avatar.url)
        if isinstance(error, commands.BotMissingPermissions):
            permissions = ", ".join([f"{permission.capitalize()}" for permission in error.missing_permissions]).replace("_", " ")
            em = discord.Embed(description=f"<:cross:1156150663802265670>  Unfortunately I am missing **`{permissions}`** permissions to run the command `{ctx.command}`", color=0xff0000)
            try:
                await ctx.send(embed=em, delete_after=7)
            except:
                try:
                    await ctx.author.send(content=f'<:cross:1156150663802265670>  Unfortunately I am missing **`{permissions}`** permissions to run the command `{ctx.command}` in [{ctx.channel.name}]({ctx.channel.jump_url})')
                except:
                    pass
            emb.add_field(name="Error:", value=f"Bot Missing {permissions} permissions to run the command", inline=False)
            webhook.send(embed=emb, username=f"{str(self.bot.user)} | Error Command Logs", avatar_url=self.bot.user.avatar.url)
            return
        if isinstance(error, commands.MissingPermissions):
            permissions = ", ".join([f"{permission.capitalize()}" for permission in error.missing_permissions]).replace("_", " ")
            em = discord.Embed(description=f"<:cross:1156150663802265670>  You lack `{permissions}` permissions to run the command `{ctx.command}`.", color=0xff0000)
            await ctx.send(embed=em, delete_after=7)
            emb.add_field(name="Error:", value=f"User Missing {permissions} permissions to run the command", inline=False)
            webhook.send(embed=emb, username=f"{str(self.bot.user)} | Error Command Logs", avatar_url=self.bot.user.avatar.url)
            return
        if isinstance(error, commands.MissingRole):
            em = discord.Embed(description=f"<:cross:1156150663802265670>  You need `{error.missing_role}` role to use this command.", color=0xff0000)
            await ctx.send(embed=em, delete_after=5)
            emb.add_field(name="Error:", value=f"Missing role", inline=False)
            webhook.send(embed=emb, username=f"{str(self.bot.user)} | Error Command Logs", avatar_url=self.bot.user.avatar.url)
            return
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(description=f"<:cross:1156150663802265670>  This command is on cooldown. Please retry after `{round(error.retry_after, 1)} Seconds` .", color=0xff0000)
            await ctx.send(embed=em, delete_after=7)
            emb.add_field(name="Error:", value=f"Command On Cooldown", inline=False)
            webhook.send(embed=emb, username=f"{str(self.bot.user)} | Error Command Logs", avatar_url=self.bot.user.avatar.url)
            return
        if isinstance(error, commands.MissingRequiredArgument):
            em = discord.Embed(description=f"<:cross:1156150663802265670>  You missed the `{error.param.name}` argument.\nDo it like: `{ctx.prefix}{ctx.command.qualified_name} {ctx.command.signature}`", color=0xff0000)
            await ctx.send(embed=em, delete_after=7)
            emb.add_field(name="Error:", value=f"Argument missing", inline=False)
            webhook.send(embed=emb, username=f"{str(self.bot.user)} | Error Command Logs", avatar_url=self.bot.user.avatar.url)
            return
        if isinstance(error, commands.EmojiNotFound):
            em = discord.Embed(description=f"<:cross:1156150663802265670>  The Emoji Cannot be found", color=0xff0000)
            await ctx.send(embed=em, delete_after=3)
            emb.add_field(name="Error:", value=f"Emoji not found", inline=False)
            webhook.send(embed=emb, username=f"{str(self.bot.user)} | Error Command Logs", avatar_url=self.bot.user.avatar.url)
            return
        if isinstance(error, commands.RoleNotFound):
            em = discord.Embed(description=f"<:cross:1156150663802265670>  The Role Cannot be found", color=0xff0000)
            await ctx.send(embed=em, delete_after=3)
            emb.add_field(name="Error:", value=f"Role not found", inline=False)
            webhook.send(embed=emb, username=f"{str(self.bot.user)} | Error Command Logs", avatar_url=self.bot.user.avatar.url)
            return
        if isinstance(error, commands.GuildNotFound):
            em = discord.Embed(description=f"<:cross:1156150663802265670>  The Guild Cannot be found", color=0xff0000)
            await ctx.send(embed=em, delete_after=3)
            emb.add_field(name="Error:", value=f"Guild not found", inline=False)
            webhook.send(embed=emb, username=f"{str(self.bot.user)} | Error Command Logs", avatar_url=self.bot.user.avatar.url)
            return
        if isinstance(error, commands.UserNotFound):
            em = discord.Embed(description=f"<:cross:1156150663802265670>  The User Cannot be found", color=0xff0000)
            await ctx.send(embed=em, delete_after=3)
            emb.add_field(name="Error:", value=f"User not found", inline=False)
            webhook.send(embed=emb, username=f"{str(self.bot.user)} | Error Command Logs", avatar_url=self.bot.user.avatar.url)
            return
        if isinstance(error, commands.MemberNotFound):
            em = discord.Embed(description=f"<:cross:1156150663802265670>  The Member Cannot be found", color=0xff0000)
            await ctx.send(embed=em, delete_after=3)
            emb.add_field(name="Error:", value=f"Member not found", inline=False)
            webhook.send(embed=emb, username=f"{str(self.bot.user)} | Error Command Logs", avatar_url=self.bot.user.avatar.url)
            return
        if isinstance(error, commands.NSFWChannelRequired):
            em = discord.Embed(description=f"<:cross:1156150663802265670>  The Channel is required to be NSFW to execute this command", color=0xff0000)
            await ctx.send(embed=em, delete_after=8)
            emb.add_field(name="Error:", value=f"NSFW Channel disabled", inline=False)
            webhook.send(embed=emb, username=f"{str(self.bot.user)} | Error Command Logs", avatar_url=self.bot.user.avatar.url)
            return

    @commands.group(
        invoke_without_command=True, description="Shows the help page for scan commands"
    )
    async def scan(self, ctx):
        prefix = ctx.prefix
        if prefix == f"<@{self.bot.user.id}> ":
            prefix = f"@{str(self.bot.user)} "
        xd = discord.utils.get(self.bot.users, id=978930369392951366)
        anay = str(xd)
        pfp = xd.display_avatar.url
        listem = discord.Embed(colour=0xc283fe,
                                     description=f"<...> Duty | [...] Optional\n\n" 
                                                  f"`{prefix}scan`\n" 
                                                  f"This Command Will Show This Page\n\n" 
                                                  f"`{prefix}scan users`\n" 
                                                  f"Shows All users having Key Permissions\n\n"
                                                  f"`{prefix}scan bots`\n"
                                                  f"Shows All bots having Key Permissions\n\n"
                                                  f"`{prefix}scan roles`\n" 
                                                  f"Show All Roles having Key permissions\n\n" 
                                                  f"`{prefix}scan permissions`\n" 
                                                  f"Show Permissions of all roles.\n\n")
        listem.set_author(name=f"{str(ctx.author)}", icon_url=ctx.author.display_avatar.url)
        listem.set_footer(text=f"Made by stars.gg" ,  icon_url=pfp)
        await ctx.send(embed=listem)

    @scan.command(aliases=['user'], description="Shows All users having Key Permissions")
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def users(self, ctx):
        ls = []
        admin, ban, kick, mgn, mgnch, mgnro, mention = "", "", "", "", "", "", ""
        c1, c2, c3, c4, c5, c6, c7 = 1, 1, 1, 1, 1, 1, 1
        for member in ctx.guild.members:
          if not member.bot:
            if member.guild_permissions.administrator == True:
                admin += f"[{'0' + str(c1) if c1 < 10 else c1}] | {member.name} [{member.id}] - Joined At: <t:{round(member.joined_at.timestamp())}:R>\n"
                c1 += 1
            if member.guild_permissions.ban_members == True:
                ban += f"[{'0' + str(c2) if c2 < 10 else c2}] | {member.name} [{member.id}] - Joined At: <t:{round(member.joined_at.timestamp())}:R>\n"
                c2 += 1
            if member.guild_permissions.kick_members == True:
                kick += f"[{'0' + str(c3) if c3 < 10 else c3}] | {member.name} [{member.id}] - Joined At: <t:{round(member.joined_at.timestamp())}:R>\n"
                c3 += 1
            if member.guild_permissions.manage_guild == True:
                mgn += f"[{'0' + str(c4) if c4 < 10 else c4}] | {member.name} [{member.id}] - Joined At: <t:{round(member.joined_at.timestamp())}:R>\n"
                c4 += 1
            if member.guild_permissions.manage_channels == True:
                mgnch += f"[{'0' + str(c5) if c5 < 10 else c5}] | {member.name} [{member.id}] - Joined At: <t:{round(member.joined_at.timestamp())}:R>\n"
                c5 += 1
            if member.guild_permissions.manage_roles == True:
                mgnro += f"[{'0' + str(c6) if c6 < 10 else c6}] | {member.name} [{member.id}] - Joined At: <t:{round(member.joined_at.timestamp())}:R>\n"
                c6 += 1
            if member.guild_permissions.mention_everyone == True:
                mention += f"[{'0' + str(c7) if c7 < 10 else c7}] | {member.name} [{member.id}] - Joined At: <t:{round(member.joined_at.timestamp())}:R>\n"
                c7 += 1
        em1 = discord.Embed(title="Administrator Perms", description=admin, color=ctx.author.color)
        try:    
            em1.set_footer(text=f"Requested by: {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
        except:
            em1.set_footer(text=f"Requested by: {ctx.author.name}")
        em2 = discord.Embed(title="Kick Members", description=kick, color=ctx.author.color)
        try:    
            em2.set_footer(text=f"Requested by: {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
        except:
            em2.set_footer(text=f"Requested by: {ctx.author.name}")
        em3 = discord.Embed(title="Ban Members", description=ban, color=ctx.author.color)
        try:    
            em3.set_footer(text=f"Requested by: {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
        except:
            em3.set_footer(text=f"Requested by: {ctx.author.name}")
        em4 = discord.Embed(title="Manager server", description=mgn, color=ctx.author.color)
        try:    
            em4.set_footer(text=f"Requested by: {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
        except:
            em4.set_footer(text=f"Requested by: {ctx.author.name}")
        em5 = discord.Embed(title="Manager Channels", description=mgnch, color=ctx.author.color)
        try:    
            em5.set_footer(text=f"Requested by: {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
        except:
            em5.set_footer(text=f"Requested by: {ctx.author.name}")
        em6 = discord.Embed(title="Manager Roles", description=mgnro, color=ctx.author.color)
        try:    
            em6.set_footer(text=f"Requested by: {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
        except:
            em6.set_footer(text=f"Requested by: {ctx.author.name}")
        em7 = discord.Embed(title="Mention Everyone", description=mention, color=ctx.author.color)
        try:    
            em7.set_footer(text=f"Requested by: {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
        except:
            em7.set_footer(text=f"Requested by: {ctx.author.name}")
        ls.append(em1)
        ls.append(em2)
        ls.append(em3)
        ls.append(em4)
        ls.append(em5)
        ls.append(em6)
        ls.append(em7)
        page = PaginationView(embed_list=ls, ctx=ctx)
        await page.start(ctx)

    @scan.command(aliases=['bot'], description="Shows All bots having Key Permissions")
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def bots(self, ctx):
        ls = []
        admin, ban, kick, mgn, mgnch, mgnro, mention = "", "", "", "", "", "", ""
        c1, c2, c3, c4, c5, c6, c7 = 1, 1, 1, 1, 1, 1, 1
        for member in ctx.guild.members:
          if member.bot:
            if member.guild_permissions.administrator == True:
                admin += f"[{'0' + str(c1) if c1 < 10 else c1}] | {member.name} [{member.id}] - Joined At: <t:{round(member.joined_at.timestamp())}:R>\n"
                c1 += 1
            if member.guild_permissions.ban_members == True:
                ban += f"[{'0' + str(c2) if c2 < 10 else c2}] | {member.name} [{member.id}] - Joined At: <t:{round(member.joined_at.timestamp())}:R>\n"
                c2 += 1
            if member.guild_permissions.kick_members == True:
                kick += f"[{'0' + str(c3) if c3 < 10 else c3}] | {member.name} [{member.id}] - Joined At: <t:{round(member.joined_at.timestamp())}:R>\n"
                c3 += 1
            if member.guild_permissions.manage_guild == True:
                mgn += f"[{'0' + str(c4) if c4 < 10 else c4}] | {member.name} [{member.id}] - Joined At: <t:{round(member.joined_at.timestamp())}:R>\n"
                c4 += 1
            if member.guild_permissions.manage_channels == True:
                mgnch += f"[{'0' + str(c5) if c5 < 10 else c5}] | {member.name} [{member.id}] - Joined At: <t:{round(member.joined_at.timestamp())}:R>\n"
                c5 += 1
            if member.guild_permissions.manage_roles == True:
                mgnro += f"[{'0' + str(c6) if c6 < 10 else c6}] | {member.name} [{member.id}] - Joined At: <t:{round(member.joined_at.timestamp())}:R>\n"
                c6 += 1
            if member.guild_permissions.mention_everyone == True:
                mention += f"[{'0' + str(c7) if c7 < 10 else c7}] | {member.name} [{member.id}] - Joined At: <t:{round(member.joined_at.timestamp())}:R>\n"
                c7 += 1
        em1 = discord.Embed(title="Administrator Perms", description=admin, color=ctx.author.color)
        try:    
            em1.set_footer(text=f"Requested by: {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
        except:
            em1.set_footer(text=f"Requested by: {ctx.author.name}")
        em2 = discord.Embed(title="Kick Members", description=kick, color=ctx.author.color)
        try:    
            em2.set_footer(text=f"Requested by: {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
        except:
            em2.set_footer(text=f"Requested by: {ctx.author.name}")
        em3 = discord.Embed(title="Ban Members", description=ban, color=ctx.author.color)
        try:    
            em3.set_footer(text=f"Requested by: {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
        except:
            em3.set_footer(text=f"Requested by: {ctx.author.name}")
        em4 = discord.Embed(title="Manager server", description=mgn, color=ctx.author.color)
        try:    
            em4.set_footer(text=f"Requested by: {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
        except:
            em4.set_footer(text=f"Requested by: {ctx.author.name}")
        em5 = discord.Embed(title="Manager Channels", description=mgnch, color=ctx.author.color)
        try:    
            em5.set_footer(text=f"Requested by: {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
        except:
            em5.set_footer(text=f"Requested by: {ctx.author.name}")
        em6 = discord.Embed(title="Manager Roles", description=mgnro, color=ctx.author.color)
        try:    
            em6.set_footer(text=f"Requested by: {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
        except:
            em6.set_footer(text=f"Requested by: {ctx.author.name}")
        em7 = discord.Embed(title="Mention Everyone", description=mention, color=ctx.author.color)
        try:    
            em7.set_footer(text=f"Requested by: {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
        except:
            em7.set_footer(text=f"Requested by: {ctx.author.name}")
        ls.append(em1)
        ls.append(em2)
        ls.append(em3)
        ls.append(em4)
        ls.append(em5)
        ls.append(em6)
        ls.append(em7)
        page = PaginationView(embed_list=ls, ctx=ctx)
        await page.start(ctx)
    
    @scan.command(aliases=['role'], description="Show Permissions of all roles")
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def roles(self, ctx):
        ls = []
        admin, ban, kick, mgn, mgnch, mgnro, mention = "", "", "", "", "", "", ""
        c1, c2, c3, c4, c5, c6, c7 = 1, 1, 1, 1, 1, 1, 1
        view = night(ctx)
        hm = await ctx.reply(embed=discord.Embed(description="Which type of role you want to see", color=0xc283fe), mention_author=False, view=view)
        await view.wait()
        for role in list(reversed(ctx.guild.roles[:])):
         if view.value == 'both':
           
            if role.permissions.administrator:
                admin += f"[{'0' + str(c1) if c1 < 10 else c1}] | {role.name} [{role.id}] - Created At: <t:{round(role.created_at.timestamp())}:R>\n"
                c1 += 1
            if role.permissions.ban_members:
                ban += f"[{'0' + str(c2) if c2 < 10 else c2}] | {role.name} [{role.id}] - Created At: <t:{round(role.created_at.timestamp())}:R>\n"
                c2 += 1
            if role.permissions.kick_members:
                kick += f"[{'0' + str(c3) if c3 < 10 else c3}] | {role.name} [{role.id}] - Created At: <t:{round(role.created_at.timestamp())}:R>\n"
                c3 += 1
            if role.permissions.manage_guild:
                mgn += f"[{'0' + str(c4) if c4 < 10 else c4}] | {role.name} [{role.id}] - Created At: <t:{round(role.created_at.timestamp())}:R>\n"
                c4 += 1
            if role.permissions.manage_channels:
                mgnch += f"[{'0' + str(c5) if c5 < 10 else c5}] | {role.name} [{role.id}] - Created At: <t:{round(role.created_at.timestamp())}:R>\n"
                c5 += 1
            if role.permissions.manage_roles:
                mgnro += f"[{'0' + str(c6) if c6 < 10 else c6}] | {role.name} [{role.id}] - Created At: <t:{round(role.created_at.timestamp())}:R>\n"
                c6 += 1
            if role.permissions.mention_everyone:
                mention += f"[{'0' + str(c7) if c7 < 10 else c7}] | {role.name} [{role.id}] - Created At: <t:{round(role.created_at.timestamp())}:R>\n"
                c7 += 1
         elif view.value == 'simple':
          if role.is_bot_managed() is False:
            if role.permissions.administrator:
                admin += f"[{'0' + str(c1) if c1 < 10 else c1}] | {role.name} [{role.id}] - Created At: <t:{round(role.created_at.timestamp())}:R>\n"
                c1 += 1
            if role.permissions.ban_members:
                ban += f"[{'0' + str(c2) if c2 < 10 else c2}] | {role.name} [{role.id}] - Created At: <t:{round(role.created_at.timestamp())}:R>\n"
                c2 += 1
            if role.permissions.kick_members:
                kick += f"[{'0' + str(c3) if c3 < 10 else c3}] | {role.name} [{role.id}] - Created At: <t:{round(role.created_at.timestamp())}:R>\n"
                c3 += 1
            if role.permissions.manage_guild:
                mgn += f"[{'0' + str(c4) if c4 < 10 else c4}] | {role.name} [{role.id}] - Created At: <t:{round(role.created_at.timestamp())}:R>\n"
                c4 += 1
            if role.permissions.manage_channels:
                mgnch += f"[{'0' + str(c5) if c5 < 10 else c5}] | {role.name} [{role.id}] - Created At: <t:{round(role.created_at.timestamp())}:R>\n"
                c5 += 1
            if role.permissions.manage_roles:
                mgnro += f"[{'0' + str(c6) if c6 < 10 else c6}] | {role.name} [{role.id}] - Created At: <t:{round(role.created_at.timestamp())}:R>\n"
                c6 += 1
            if role.permissions.mention_everyone:
                mention += f"[{'0' + str(c7) if c7 < 10 else c7}] | {role.name} [{role.id}] - Created At: <t:{round(role.created_at.timestamp())}:R>\n"
                c7 += 1
         elif view.value == 'bot':
          if role.is_bot_managed() is True:
            if role.permissions.administrator:
                admin += f"[{'0' + str(c1) if c1 < 10 else c1}] | {role.name} [{role.id}] - Created At: <t:{round(role.created_at.timestamp())}:R>\n"
                c1 += 1
            if role.permissions.ban_members:
                ban += f"[{'0' + str(c2) if c2 < 10 else c2}] | {role.name} [{role.id}] - Created At: <t:{round(role.created_at.timestamp())}:R>\n"
                c2 += 1
            if role.permissions.kick_members:
                kick += f"[{'0' + str(c3) if c3 < 10 else c3}] | {role.name} [{role.id}] - Created At: <t:{round(role.created_at.timestamp())}:R>\n"
                c3 += 1
            if role.permissions.manage_guild:
                mgn += f"[{'0' + str(c4) if c4 < 10 else c4}] | {role.name} [{role.id}] - Created At: <t:{round(role.created_at.timestamp())}:R>\n"
                c4 += 1
            if role.permissions.manage_channels:
                mgnch += f"[{'0' + str(c5) if c5 < 10 else c5}] | {role.name} [{role.id}] - Created At: <t:{round(role.created_at.timestamp())}:R>\n"
                c5 += 1
            if role.permissions.manage_roles:
                mgnro += f"[{'0' + str(c6) if c6 < 10 else c6}] | {role.name} [{role.id}] - Created At: <t:{round(role.created_at.timestamp())}:R>\n"
                c6 += 1
            if role.permissions.mention_everyone:
                mention += f"[{'0' + str(c7) if c7 < 10 else c7}] | {role.name} [{role.id}] - Created At: <t:{round(role.created_at.timestamp())}:R>\n"
                c7 += 1
        no = ""
        if admin == no:
            admin = "No Roles"
        if kick == no:
            kick = "No Roles"
        if ban == no:
            ban = "No Roles"
        if mgn == no:
            mgn = "No Roles"
        if mgnch == no:
            mgnch = "No Roles"
        if mgnro == no:
            mgnro = "No Roles"
        if mention == no:
            mention = "No Roles"
        em1 = discord.Embed(title="Administrator Perms", description=admin, color=ctx.author.color)
        try:    
            em1.set_footer(text=f"Requested by: {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
        except:
            em1.set_footer(text=f"Requested by: {ctx.author.name}")
        em2 = discord.Embed(title="Kick Members", description=kick, color=ctx.author.color)
        try:    
            em2.set_footer(text=f"Requested by: {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
        except:
            em2.set_footer(text=f"Requested by: {ctx.author.name}")
        em3 = discord.Embed(title="Ban Members", description=ban, color=ctx.author.color)
        try:    
            em3.set_footer(text=f"Requested by: {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
        except:
            em3.set_footer(text=f"Requested by: {ctx.author.name}")
        em4 = discord.Embed(title="Manager server", description=mgn, color=ctx.author.color)
        try:    
            em4.set_footer(text=f"Requested by: {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
        except:
            em4.set_footer(text=f"Requested by: {ctx.author.name}")
        em5 = discord.Embed(title="Manager Channels", description=mgnch, color=ctx.author.color)
        try:    
            em5.set_footer(text=f"Requested by: {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
        except:
            em5.set_footer(text=f"Requested by: {ctx.author.name}")
        em6 = discord.Embed(title="Manager Roles", description=mgnro, color=ctx.author.color)
        try:    
            em6.set_footer(text=f"Requested by: {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
        except:
            em6.set_footer(text=f"Requested by: {ctx.author.name}")
        em7 = discord.Embed(title="Mention Everyone", description=mention, color=ctx.author.color)
        try:    
            em7.set_footer(text=f"Requested by: {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
        except:
            em7.set_footer(text=f"Requested by: {ctx.author.name}")
        ls.append(em1)
        ls.append(em2)
        ls.append(em3)
        ls.append(em4)
        ls.append(em5)
        ls.append(em6)
        ls.append(em7)
        await hm.delete()
        page = PaginationView(embed_list=ls, ctx=ctx)
        await page.start(ctx)

    @scan.command(aliases=["perms"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def permissions(self, ctx):
        ls = []
        count = 1
        for role in list(reversed(ctx.guild.roles[:])):
            if role.permissions.administrator:
                admin = "<:enabled:1152981697084797059>"
            else:
                admin = "<:disabled:1152981709663506492>"
            if role.permissions.kick_members:
                kick = "<:enabled:1152981697084797059>"
            else:
                kick = "<:disabled:1152981709663506492>"
            if role.permissions.ban_members:
                ban = "<:enabled:1152981697084797059>"
            else:
                ban = "<:disabled:1152981709663506492>"
            if role.permissions.manage_guild:
                server = "<:enabled:1152981697084797059>"
            else:
                server = "<:disabled:1152981709663506492>"
            if role.permissions.manage_channels:
                channel= "<:enabled:1152981697084797059>"
            else:
                channel= "<:disabled:1152981709663506492>"
            if role.permissions.manage_roles:
                roles= "<:enabled:1152981697084797059>"
            else:
                roles= "<:disabled:1152981709663506492>"
            if role.permissions.mention_everyone:
                everyone= "<:enabled:1152981697084797059>"
            else:
                everyone= "<:disabled:1152981709663506492>"
            em = discord.Embed(title=f"[{count}] - {role.name} [{role.id}]", color=ctx.author.color)
            em.add_field(name="Administrator", value=admin, inline=True)
            em.add_field(name="Kick Members", value=kick, inline=True)
            em.add_field(name="Ban Members", value=ban, inline=True)
            em.add_field(name="Manage Server", value=server, inline=True)
            em.add_field(name="Manage Channels", value=channel, inline=True)
            em.add_field(name="Manage Roles", value=roles, inline=True)
            em.add_field(name="Mention Everyone", value=everyone, inline=True)
            em.add_field(name=f"Total Members in {role.name}", value=f"{len(role.members)} Members", inline=True)
            count+=1
            ls.append(em)
        page = PaginationView(embed_list=ls, ctx=ctx)
        await page.start(ctx)

async def setup(bot):
    await bot.add_cog(moderation(bot))
