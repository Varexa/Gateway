import discord
from discord.ext import commands
from discord import Webhook
from typing import Union
import re
import sqlite3
from collections import Counter
import datetime
from paginators import PaginationView, PaginatorView
from botinfo import *
import os
import io
from io import BytesIO
from ast import literal_eval

class owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #@commands.group(invoke_without_command=True)
    #@commands.is_owner()
    async def title(self, ctx):
        pass
            
    #@title.command(name="give", aliases=["a"], description="Gives the title to user")
    #@commands.is_owner()
    async def title_give(self, ctx, member: discord.User, *, title):
        db = sqlite3.connect('./database.sqlite3')
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM  titles WHERE user_id = {member.id}")
        result = cursor.fetchone()
        if result is None:
            sql = (f"INSERT INTO titles(user_id, title) VALUES(?, ?)")
            val = (member.id, title.upper())
            cursor.execute(sql, val)
        else:
            sql = (f"UPDATE titles SET title = ? WHERE user_id = ?")
            val = (title.upper(), member.id,)
            cursor.execute(sql, val)
        await ctx.send(f'Given **{title}** title to {str(member)}')
        db.commit()
        cursor.close()
        db.close()
        em = discord.Embed(description=f"{title} title was given to {member.mention} [{member.id}] by {ctx.author.mention} [{ctx.author.id}]")
        webhook = discord.SyncWebhook.from_url(webhook_badge_logs)
        webhook.send(embed=em, username=f"{str(self.bot.user)} | Title Given Logs", avatar_url=self.bot.user.avatar.url)
                          
    #@title.command(name="remove", aliases=["r"], description="Removes the title from user")
    #@commands.is_owner()

    async def title_remove(self, ctx, member: discord.User):
        ls = workowner
        if ctx.author.id not in ls and ctx.author.id not in self.bot.owner_ids:
            return
        db = sqlite3.connect('./database.sqlite3')
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM  titles WHERE user_id = {member.id}")
        result = cursor.fetchone()
        if result is not None:
            sql = (f"DELETE FROM titles WHERE user_id = ?")
            val = (member.id,)
            cursor.execute(sql, val)
        else:
            return await ctx.reply(f"{str(member)} don't have any title")
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        await ctx.reply(f"Removed Title from {str(member)}")
        em = discord.Embed(description=f"Title was removed from {member.mention} [{member.id}] by {ctx.author.mention} [{ctx.author.id}]")
        webhook = discord.SyncWebhook.from_url(webhook_badge_logs)
        webhook.send(embed=em, username=f"{str(self.bot.user)} | Title Removed Logs", avatar_url=self.bot.user.avatar.url)
        
    @commands.group(
        invoke_without_command=True, description="Shows the help menu for top"
    )
    async def top(self, ctx: commands.Context):
        if ctx.author.id not in workowner:
          return await ctx.send("Only Bot Dev Can Run This Command")
        ls = ["top", "top commands", "top users", "top guilds"]
        prefix = ctx.prefix
        if prefix == f"<@{self.bot.user.id}> ":
            prefix = f"@{str(self.bot.user)} "
        anay = discord.utils.get(self.bot.users, id=978930369392951366)
        des = ""
        for i in sorted(ls):
            cmd = self.bot.get_command(i)
            des += f"`{prefix}{i}`\n{cmd.description}\n\n"
        listem = discord.Embed(colour=0xc283fe,
                                     description=f"<...> Duty | [...] Optional\n\n{des}")
        listem.set_author(name=f"{str(ctx.author)}", icon_url=ctx.author.display_avatar.url)
        listem.set_footer(text=f"Made by stars.gg" ,  icon_url=anay.avatar.url)
        await ctx.send(embed=listem)
         
    @top.command(name="users", aliases=["user"], description="Shows the top users of the bot")
    async def _user(self, ctx: commands.Context):
        if ctx.author.id not in workowner:
          return await ctx.send("Only Bot Dev Can Run This Command")
        init = await ctx.reply(f"<:loading:1060851548869107782> Processing the command...", mention_author=False)
        query = "SELECT * FROM  count WHERE xd = ?"
        val = (1,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            count_db = cursor.fetchone()
        user = literal_eval(count_db['user_count'])
        #ls1 = {k: v for k, v in reversed(sorted(user.items(), key=lambda item: item[1]))}
        ls1 = user.copy()
        count = 0
        ls2 = []
        ls = []
        c = 0
        for i in ls1:
            c+=1
        cc = 0
        for i in ls1:
            cc+=ls1[i]
        for i in ls1:
            u = await self.bot.fetch_user(i)
            if u is None or u.id in workowner:
                pass
            else:
                count+=1
                ls2.append(f"`[{'0' + str(count) if count < 10 else count}]` | {str(u)} - {ls1[i]} Commands Runned")
                if count == 10:
                    break
        for i in range(0, len(ls2), 10):
           ls.append(ls2[i: i + 10])
        em_list = []
        no = 1
        for k in ls:
           embed =discord.Embed(color=0xc283fe)
           embed.title = f"Top {count} Users of the Bot"
           embed.description = "\n".join(k)
           embed.set_footer(text=f"{self.bot.user.name} • Page {no}/{len(ls)}", icon_url=self.bot.user.display_avatar.url)
           embed.set_author(name=f"Total users - {c} with {cc} commands runned", icon_url=ctx.author.display_avatar.url)
           em_list.append(embed)
           no+=1
        page = PaginationView(embed_list=em_list, ctx=ctx)
        await init.delete()
        await page.start(ctx)

    @top.command(name="guilds", aliases=["guild", "servers", "server"], description="Shows the top guilds of the bot")
    async def _guild(self, ctx: commands.Context):
        if ctx.author.id not in workowner:
          return await ctx.send("Only Bot Dev Can Run This Command")
        init = await ctx.reply(f"<:loading:1060851548869107782> Processing the command...", mention_author=False)
        query = "SELECT * FROM  count WHERE xd = ?"
        val = (1,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            count_db = cursor.fetchone()
        user = literal_eval(count_db['guild_count'])
        #ls1 = {k: v for k, v in reversed(sorted(user.items(), key=lambda item: item[1]))}
        ls1 = user.copy()
        count = 0
        ls2 = []
        ls = []
        for i in ls1:
            if i == 1036594185442177055:
                continue
            count+=1
            u = discord.utils.get(self.bot.guilds, id=i)
            if u is None:
                count-=1
                continue
            else:
                ls2.append(f"`[{'0' + str(count) if count < 10 else count}]` | {u.name} - {ls1[i]} Commands Runned")
                if count == 10:
                    break
        for i in range(0, len(ls2), 10):
           ls.append(ls2[i: i + 10])
        em_list = []
        no = 1
        for k in ls:
           embed =discord.Embed(color=0xc283fe)
           embed.title = f"Top {count} Guilds of the Bot"
           embed.description = "\n".join(k)
           embed.set_footer(text=f"{self.bot.user.name} • Page {no}/{len(ls)}", icon_url=self.bot.user.display_avatar.url)
           em_list.append(embed)
           no+=1
        page = PaginationView(embed_list=em_list, ctx=ctx)
        await init.delete()
        await page.start(ctx)

    @top.command(name="commands", aliases=["command", "cmd", "cmds"], description="Shows the top commands of the bot")
    async def _commands(self, ctx: commands.Context):
        if ctx.author.id not in workowner:
          return await ctx.send("Only Bot Dev Can Run This Command")
        init = await ctx.reply(f"<:loading:1060851548869107782> Processing the command...", mention_author=False)
        query = "SELECT * FROM  count WHERE xd = ?"
        val = (1,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            count_db = cursor.fetchone()
        user = literal_eval(count_db['cmd_count'])
        #ls1 = {k: v for k, v in reversed(sorted(user.items(), key=lambda item: item[1]))}
        ls1 = user.copy()
        count = 0
        ls2 = []
        ls = []
        c = 0
        for i in ls1:
            c+=ls1[i]
        for i in ls1:
            count+=1
            ls2.append(f"`[{'0' + str(count) if count < 10 else count}]` | {i} - {ls1[i]} Times Runned")
            if count == 10:
                break
        for i in range(0, len(ls2), 10):
           ls.append(ls2[i: i + 10])
        em_list = []
        no = 1
        for k in ls:
           embed =discord.Embed(color=0xc283fe)
           embed.title = f"Top {count} Commands of the Bot"
           embed.description = "\n".join(k)
           embed.set_footer(text=f"{self.bot.user.name} • Page {no}/{len(ls)}", icon_url=self.bot.user.display_avatar.url)
           embed.set_author(name=f"Total commands runned - {c}", icon_url=ctx.author.display_avatar.url)
           em_list.append(embed)
           no+=1
        page = PaginationView(embed_list=em_list, ctx=ctx)
        await init.delete()
        await page.start(ctx)
    
    @commands.command()
    @commands.is_owner()
    async def dailygrowth(self, ctx):
        no_em = discord.Embed(description=f"Till now there is no daily growth.", color=0xc283fe)
        query1 = "SELECT * FROM  daily WHERE id = ?"
        val1 = (self.bot.user.id,)
        with sqlite3.connect('./database.sqlite3') as db2:
            db2.row_factory = sqlite3.Row
            cursor2 = db2.cursor()
            try:
                cursor2.execute(query1, val1)
            except:
                return await ctx.reply(embed=no_em)
            d_db = cursor2.fetchone()
        if d_db is None:
            return await ctx.reply(embed=no_em)
        else:
            count = 0
            for g in self.bot.guilds:
                count += len(g.members)
            em = discord.Embed(description=f"Today's Growth in Guilds: {d_db['guild']} Guilds\nToday's Growth in Users: {d_db['user']} Users\nTotal Guilds: {len(self.bot.guilds)} Guilds\nTotal Users: {count} Users", color=0xc283fe)
            return await ctx.reply(embed=em)

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx: commands.Context, id):
        if not id.isdigit():
            if id.lower() != "all":
                await ctx.reply(f"Either pass a shard id or type 'all'")
            else:
                for iid, shard in self.bot.shards.items():
                    await ctx.reply(f"Reloding Shard {iid}")
                    await shard.reconnect()
        else:
            sh = self.bot.get_shard(int(id))
            if sh is None:
                await ctx.reply(f"Either pass a shard id or type 'all'")
            else:
                await ctx.reply(f"Reloding Shard {id}")
                await sh.reconnect()

    @commands.command()
    async def shards(self, ctx):
        if ctx.author.id not in workowner:
          return await ctx.send("Only Bot Dev Can Run This Command")
        ls = []
        for id, shard in self.bot.shards.items():
            c = 0
            cc = 0
            for guild in self.bot.guilds:
                if guild.shard_id == id:
                    if self.bot.wavelink.get_player(guild):
                        c += 1
                        if self.bot.wavelink.get_player(guild).is_playing():
                            cc += 1
            em = discord.Embed(color=0xc283fe)
            em.title = "Shards information"
            em.set_footer(text=str(self.bot.user), icon_url=self.bot.user.display_avatar.url)
            em.description = (f"Shard ID: {id}\nLatency: {round(shard.latency * 1000)} ms\nStatus: {not shard.is_closed()}\nGuilds: {sum(1 for guild in self.bot.guilds if guild.shard_id == id)}\nGuilds Unavailable: {sum(1 for guild in self.bot.guilds if guild.unavailable)}\nUsers: {sum(len(guild.members) for guild in self.bot.guilds if guild.shard_id == id)}\nPlayers: {cc}/{c}")
            ls.append(em)
        page = PaginationView(embed_list=ls, ctx=ctx)
        await page.start(ctx)
        
    @commands.group(invoke_without_command=True)
    @commands.is_owner()
    async def blacklist(self, ctx):
        pass

    @blacklist.command()
    @commands.is_owner()
    async def add(self, ctx, user:discord.User,*, reason=None):
            ls = self.bot.owner_ids
            if ctx.author.id not in ls:
                return
            if user.id in ls:
                if ctx.author.id == 978930369392951366:
                    pass
                else:
                    await ctx.send(f"{str(user)} is Your Daddy")
                    return
            query = "SELECT * FROM  bl WHERE main = 1"
            with sqlite3.connect('./database.sqlite3') as db:
              db.row_factory = sqlite3.Row
              cursor = db.cursor()
              cursor.execute(query)
              _db = cursor.fetchone()
            bl_db = literal_eval(_db["user_ids"])
            if user.id in bl_db:
                return await ctx.send(f"{str(user)} is already blacklisted")
            else:
                bl_db.append(user.id)
                sql = (f"UPDATE bl SET 'user_ids' = ? WHERE main = ?")
                val = (f"{bl_db}", 1,)
                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()
                if reason:
                    try:
                        await user.send(f"You are blacklisted from using {self.bot.user.name} for {reason}")
                    except:
                        pass
                    return await ctx.send(f"{str(user)} is added to blacklisted users for {reason}")
                else:
                    try:
                        await user.send(f"You are blacklisted from using {self.bot.user.name}")
                    except:
                        pass
                    return await ctx.send(f"{str(user)} is added to blacklisted users")

    @blacklist.command()
    @commands.is_owner()
    async def remove(self, ctx,*, user:discord.User):
            ls = self.bot.owner_ids
            if ctx.author.id not in ls:
                return
            query = "SELECT * FROM  bl WHERE main = 1"
            with sqlite3.connect('./database.sqlite3') as db:
              db.row_factory = sqlite3.Row
              cursor = db.cursor()
              cursor.execute(query)
              _db = cursor.fetchone()
            bl_db = literal_eval(_db["user_ids"])
            if user.id not in bl_db:
                return await ctx.send(f"{str(user)} is already whitelisted")
            else:
                bl_db.remove(user.id)
                sql = (f"UPDATE bl SET 'user_ids' = ? WHERE main = ?")
                val = (f"{bl_db}", 1,)
                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()
                try:
                    await user.send(f"You are allowed to use the bot now")
                except:
                    pass
                return await ctx.send(f"{str(user)} is removed from blacklisted users")
    
    @blacklist.command()
    async def show(self, ctx: commands.Context):
        if ctx.author.id not in workowner:
          return await ctx.send("Only Bot Dev Can Run This Command")
        query = "SELECT * FROM  bl  WHERE main = 1"
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query)
            _db = cursor.fetchone()
        mem, ls = [], []
        count = 0
        bl_db = literal_eval(_db["user_ids"])
        if len(bl_db) == 0:
            embed =discord.Embed(color=0xc283fe)
            embed.title = f"List of Blacklisted users - 0"
            embed.description = "No Blacklisted users"
            embed.set_footer(text=f"{self.bot.user.name}", icon_url=self.bot.user.display_avatar.url)
            await ctx.send(embed=embed)
            return
        for i in bl_db:
            u = discord.utils.get(self.bot.users, id=i)
            if u is None:
                continue
            count+=1
            mem.append(f"`[{'0' + str(count) if count < 10 else count}]` | {u.mention} `[{u.id}]`")
        for i in range(0, len(mem), 10):
           ls.append(mem[i: i + 10])
        em_list = []
        no = 1
        for k in ls:
            embed =discord.Embed(color=0xc283fe)
            embed.title = f"List of Blacklisted users - {count}"
            embed.description = "\n".join(k)
            embed.set_footer(text=f"{self.bot.user.name} • Page {no}/{len(ls)}", icon_url=self.bot.user.display_avatar.url)
            em_list.append(embed)
            no+=1
        page = PaginationView(embed_list=em_list, ctx=ctx)
        await page.start(ctx)
    
    @commands.command(description="To get the list of all running giveaways in all the server")
    @commands.is_owner()
    @commands.has_permissions(manage_guild=True)
    async def galist(self, ctx: commands.Context):
        query = "SELECT * FROM  gwmain"
        with sqlite3.connect('./database.sqlite3') as db:
                    db.row_factory = sqlite3.Row
                    cursor = db.cursor()
                    cursor.execute(query)
                    gw_db = cursor.fetchall()
        em_no = discord.Embed(description="No Giveaway is presently running in any of the server!", color=0xc283fe)
        em_no.set_footer(text=f"{self.bot.user.name} Giveaway", icon_url=self.bot.user.avatar.url)
        if gw_db is None:
            return await ctx.send(embed=em_no)
        xd = {}
        for i, j in gw_db:
            x = literal_eval(j)
            for f in x:
                xd[f] = x[f]
        xdd = xd.copy()
        for i in xd:
            if not xd[i]['status']:
                del xdd[i]
        if len(xdd) == 0:
            return await ctx.send(embed=em_no)
        xddd = {}
        for i in xdd:
            xddd[xdd[i]['end_time']] = xdd[i]
        ls, count=[],1
        des = []
        for j in sorted(xddd):
            try:
                channel = self.bot.get_channel(xddd[j]['channel_id'])
                g_msg = await channel.fetch_message(int(xddd[j]['g_id']))
            except:
                continue
            des.append(f"`[{'0' + str(count) if count < 10 else count}]` | {xddd[j]['prize']} - [[{xddd[j]['g_id']}]({g_msg.jump_url})] | Server name: `{channel.guild.name}` Ends at: <t:{round(j)}:R>")
            count+=1
        if len(des) == 0:
            return await ctx.send(embed=em_no)
        for i in range(0, len(des), 10):
           ls.append(des[i: i + 10])
        em_list = []
        no = 1
        for k in ls:
           embed =discord.Embed(color=0xc283fe)
           embed.title = f"Giveaways presently running in all the servers - {count-1}"
           embed.description = "\n".join(k)
           embed.set_footer(text=f"{self.bot.user.name} • Page {no}/{len(ls)}", icon_url=self.bot.user.display_avatar.url)
           em_list.append(embed)
           no+=1
        page = PaginationView(embed_list=em_list, ctx=ctx)
        await page.start(ctx)

    @commands.command()
    @commands.is_owner()
    async def guilds(self, ctx):
        xd = {}
        for ser in self.bot.guilds:
            xd[ser.id] = len(ser.members)
        ls = []
        server = []
        count = 1
        xd = {k: v for k, v in sorted(xd.items(), key=lambda item: item[1])}
        for ser in xd:
            s = discord.utils.get(self.bot.guilds, id=ser)
            server.append(f"[{count}] | {s.name} `[{s.id}]` - {len(s.members)} Members")
            count +=1
        for i in range(0, len(server), 10):
            ls.append(server[i: i + 10])
        em_list=[]
        for k in ls:
            em = discord.Embed(title=f"SERVERS OF {self.bot.user.name.upper()} - {count - 1}", description="\n".join(k),color=0xc283fe)
            em.set_footer(text=f"{self.bot.user.name.upper()}")
            em_list.append(em)
        page = PaginationView(embed_list=em_list, ctx=ctx)
        await page.start(ctx)
    
    @commands.command()
    async def listening(self, ctx, status, *, activity):
        if ctx.author.id not in workowner:
          return await ctx.send("Only Bot Dev Can Run This Command")
        xd = ['online', 'idle', 'dnd', 'invisible']
        if status.lower() not in xd:
            return await ctx.reply("Please send a valid status\nOptions are: Online, idle, dnd, invisible")
        if status.lower() == 'online':
            await self.bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name=f"{activity}"))
        if status.lower() == 'idle':
            await self.bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.listening, name=f"{activity}"))
        if status.lower() == 'dnd':
            await self.bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.listening, name=f"{activity}"))
        if status.lower() == 'invisible':
            await self.bot.change_presence(status=discord.Status.offline, activity=discord.Activity(type=discord.ActivityType.listening, name=f"{activity}"))
        await ctx.reply("Changed the bot's Status")
    
    @commands.command()
    @commands.is_owner()
    async def getinvite(self, ctx, *,guild_id: int):
        xd = discord.utils.get(self.bot.guilds, id=guild_id)
        if xd is None:
            return await ctx.reply(f"Not a valid guild id")
        for channel in xd.channels:
            try:
                inv = await channel.create_invite()
                return await ctx.reply(str(inv))
            except:
                pass
                                    
    @commands.command()
    @commands.is_owner()
    async def gleave(self, ctx, *,guild_id: int):
        if ctx.author.id not in botowner:
          return await ctx.send("Only Bot Dev Can Run This Command")
        xd = discord.utils.get(self.bot.guilds, id=guild_id)
        if xd is None:
            return await ctx.reply(f"Not a valid guild id")
        await xd.leave()
        await ctx.reply(f"I left {xd.name}")

    @commands.command()
    async def say(self, ctx, channel: discord.TextChannel = None, *,msg):
        if ctx.author.id not in workowner:
          return await ctx.send("Only Bot Dev Can Run This Command")
        if '@everyone' in msg:
            eme = discord.Embed(description=f"You can't Mention everyone", color=0x6509f5)
            return await ctx.send(embed=eme)
        if '@here' in msg:
            eme = discord.Embed(description=f"You can't Mention here", color=0x6509f5)
            return await ctx.send(embed=eme)
        if '<@&' in msg:
            eme = discord.Embed(description=f"You can't Mention role", color=0x6509f5)
            return await ctx.send(embed=eme)
        if '%' in msg:
            message = msg.replace('%','@')
            return await channel.send(message)
        await channel.send(msg)

    @commands.command()
    async def dm(self, ctx, user: discord.User, *, message: str):
        if ctx.author.id not in workowner:
          return await ctx.send("Only Bot Dev Can Run This Command")
        try:
            await user.send(message)
            await ctx.send(f"✉️ Sent a DM to **{user}**")
        except discord.Forbidden:
            await ctx.send("This user might be having DMs blocked or it's a bot account...")
        
    @commands.command()
    async def emsay(self, ctx, channel:discord.TextChannel=None, *,msg):
        if ctx.author.id not in workowner:
          return await ctx.send("Only Bot Dev Can Run This Command")
        await channel.send(embed=discord.Embed(description=msg, color=0x6509f5))

    @commands.command(aliases=['asi'])
    async def anyserverinfo(self, ctx, guild: discord.Guild):
        if ctx.author.id not in workowner:
          return await ctx.send("Only Bot Dev Can Run This Command")
        emote = ("<a:rightarrow:988109002443464804>")
        guild_roles = len(guild.roles)
        guild_members = len(guild.members)
        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        channels = text_channels + voice_channels
        pfp = ctx.author.display_avatar.url
        serverinfo = discord.Embed(colour=0xc283fe, title="Guild Information")
        serverinfo.add_field(name="General Information:",
                             value=f"Name: **{guild.name}**\n"
                                   f"ID: {guild.id}\n"
                                   f"Owner: {str(guild.owner)} ({guild.owner.mention})\n"
                                   f"Creation: <t:{round(guild.created_at.timestamp())}:R>\n"
                                   f"Total Member: {guild_members}\n"
                                   f"Roles: {guild_roles}\n"
                                   f"Channel: {channels}\n"
                                   f"Text Channel: {text_channels}\n"
                                   f"Voice Channel: {voice_channels}", inline=False)
        if guild.icon is not None:
            serverinfo.set_thumbnail(url=guild.icon.url)
            serverinfo.add_field(name="**SERVER ICON:**", value=f"[Icon]({guild.icon.url})", inline=False)
        if guild.banner is not None:
            serverinfo.set_image(url=guild.banner.url)
        serverinfo.set_footer(text=f"Requested by {ctx.author.name}" ,  icon_url=pfp)
        await ctx.send(embed=serverinfo)

    @commands.command(aliases=["ao"])
    @commands.is_owner()
    async def addowner(self, ctx, user: discord.Member):
        if ctx.author.id not in self.bot.owner_ids:
            return await ctx.send("Only Bot Dev Can Run This Command")
        if user.id in workowner:
            return await ctx.send(f"{str(user)} is already A Owner")
        workowner.append(user.id)
        await ctx.send(f"I added {user.mention} To Owner list")

    @commands.command(aliases=["ro"])
    @commands.is_owner()
    async def removeowner(self, ctx, user: discord.Member):
        if ctx.author.id not in self.bot.owner_ids:
            return await ctx.send("Only Bot Dev Can Run This Command")
        if user.id not in workowner:
            return await ctx.send(f"{str(user)} is Not A Owner")
        workowner.remove(user.id)
        await ctx.send(f"I removed {user.mention} From Owner list")

    @commands.command(description="List Of Bot's Owners",aliases=["lo",'ownerlist'])
    @commands.guild_only()
    @commands.is_owner()
    async def listowner(self, ctx):
        embed = discord.Embed(color=ctx.guild.me.color)
        st, count = "", 1
        for member in self.bot.owner_ids:
            ok = discord.utils.get(self.bot.users, id=member)
            st += f"[{'0' + str(count) if count < 10 else count}] | {str(ok)} [{ok.mention}]\n"
            test = count
            count += 1
        embed.title = f"Owners - {test}"
        embed.description = st
        await ctx.send(embed=embed)

    @commands.command(description="List Of Bot's Work Owners",aliases=["lwo",'workownerlist'])
    @commands.guild_only()
    @commands.is_owner()
    async def listworkowner(self, ctx):
        embed = discord.Embed(color=ctx.guild.me.color)
        st, count = "", 1
        for member in workowner:
            ok = discord.utils.get(self.bot.users, id=member)
            st += f"[{'0' + str(count) if count < 10 else count}] | {str(ok)} [{ok.mention}]\n"
            test = count
            count += 1
        embed.title = f"Work Owners - {test}"
        embed.description = st
        await ctx.send(embed=embed)

    @commands.command()
    async def backup(self, ctx: commands.Context):
        if ctx.author.id not in workowner:
          return await ctx.send("Only Bot Dev Can Run This Command")
        database = []
        for filename in os.listdir():
            if filename.endswith('.sqlite3'):
                database.append(filename)
        g = discord.utils.get(self.bot.guilds, id=1146104099369144340)
        x = discord.utils.get(g.categories, id=1155075084051026011)
        for i in database:
            c=discord.utils.get(g.channels, name=f"{i[:-8]}")
            if c is None:
                c=await g.create_text_channel(name=f"{i[:-8]}", category=x)
                webhook = await c.create_webhook(name=f"{i[:-8]}")
            else:
                webhook = await c.create_webhook(name=f"{i[:-8]}")
            with open(i, 'rb') as f:
                await webhook.send(f"Instant backup by {str(ctx.author)} - {ctx.author.id}\nTime for backup - {datetime.datetime.now()}", file=discord.File(BytesIO(f.read()), i), username=f"{str(self.bot.user)} | {i[:-8]} Backup", avatar_url=self.bot.user.avatar.url)
        await ctx.message.add_reaction("✅")

async def setup(bot):
    await bot.add_cog(owner(bot))
