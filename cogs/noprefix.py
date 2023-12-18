import discord
from discord.ext import commands
from discord import Webhook
from typing import Union, Optional
import re
import sqlite3
from ast import literal_eval
from botinfo import *
from paginators import PaginationView, PaginatorView

class noprefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = 0xc283fe

    @commands.command(aliases=['snp'])
    async def statusnopre(self, ctx, *, user: discord.User = None):
        ls = workowner
        if ctx.author.id not in ls and ctx.author.id not in self.bot.owner_ids:
            return
        if user is None:
            user = ctx.author
        query = "SELECT * FROM  noprefix WHERE user_id = ?"
        val = (user.id,)
        with sqlite3.connect('database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            np_db = cursor.fetchone()
        em = discord.Embed(title=f"No prefix status for {str(user)}", color=0xc283fe)
        if np_db is None:
            em.description = f"{str(user)} doesn't have any server's no prefix"
            return await ctx.send(embed=em)
        elif np_db['main'] == 0 and np_db['servers'] is None:
            em.description = f"{str(user)} doesn't have any server's no prefix"
            return await ctx.send(embed=em)
        elif np_db['main'] == 1:
            em.description = f"{str(user)} have all server's no prefix"
            return await ctx.send(embed=em)
        elif np_db['servers'] is not None:
            np = literal_eval(np_db['servers'])
            count = 1
            des, ls = [], []
            for i in np:
                g = discord.utils.get(self.bot.guilds, id=i)
                des.append(f"`[{'0' + str(count) if count < 10 else count}]` | {g.name} - [{g.id}]")
                count+=1
            for i in range(0, len(des), 10):
                ls.append(des[i: i + 10])
            em_list = []
            no = 1
            for k in ls:
                embed = discord.Embed(title=f"No prefix status for {str(user)}", color=0xc283fe)
                embed.description = "\n".join(k)
                embed.set_footer(text=f"{self.bot.user.name} • Page {no}/{len(ls)}", icon_url=self.bot.user.display_avatar.url)
                em_list.append(embed)
                no+=1
            page = PaginationView(embed_list=em_list, ctx=ctx)
            try:
                return await page.start(ctx)
            except:
                pass
        em.description = f"{str(user)} doesn't have any server's no prefix"
        return await ctx.send(embed=em)

    @commands.command(aliases=['anp'])
    async def addnopre(self, ctx, server: Union[discord.Guild, str] , *, user: discord.User):
        ls = workowner
        if ctx.author.id not in ls and ctx.author.id not in self.bot.owner_ids:
            return
        query = "SELECT * FROM  noprefix WHERE user_id = ?"
        val = (user.id,)
        with sqlite3.connect('database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            np_db = cursor.fetchone()
        if isinstance(server, str):
            if server.lower() == "all":
                pass
            elif server.lower() == "this":
                server = ctx.guild
            else:
                return await ctx.send("Please provide a valid guild id or 'all' for All servers or 'this' for this server")
        else:
            try:
                if np_db['servers'] is not None:
                    if server.id in literal_eval(np_db['servers']):
                        em = discord.Embed(description=f'{str(user)} already has no prefix for {server.name}', color=0xc283fe)
                        return await ctx.reply(embed=em, mention_author=False)
            except:
                pass
        if np_db is None:
            if isinstance(server, str):
                sql = (f"INSERT INTO noprefix(user_id, main) VALUES(?, ?)")
                val = (user.id, 1)
            else:
                sql = (f"INSERT INTO noprefix(user_id, servers) VALUES(?, ?)")
                val = (user.id, f'[{server.id}]')
        else:
            if isinstance(server, str):
                sql = (f"UPDATE noprefix SET main = ? WHERE user_id = ?")
                val = (1, user.id)
            else:
                if np_db['servers'] is None:
                    sql = (f"UPDATE noprefix SET servers = ? WHERE user_id = ?")
                    val = (f"[{server.id}]", user.id)
                else:
                    np = literal_eval(np_db['servers'])
                    np.append(server.id)
                    sql = (f"UPDATE noprefix SET servers = ? WHERE user_id = ?")
                    val = (f"{np}", user.id)
        cursor.execute(sql, val)
        em = discord.Embed(description=f"Added no prefix to {str(user)} for {server}", color=0xc283fe)
        await ctx.reply(embed=em, mention_author=False)
        db.commit()
        cursor.close()
        db.close()
        em = discord.Embed(description=f"No prefix for {server} server(s) were given to {user.mention} [{user.id}] by {ctx.author.mention} [{ctx.author.id}]")
        webhook = discord.SyncWebhook.from_url(webhook_np_logs)
        webhook.send(embed=em, username=f"{str(self.bot.user)} | No prefix Given Logs", avatar_url=self.bot.user.avatar.url)
        
    @commands.command(aliases=['rnp'])
    async def removenopre(self, ctx, server: Union[discord.Guild, str] , *, user: discord.User):
        ls = workowner
        if ctx.author.id not in ls and ctx.author.id not in self.bot.owner_ids:
            return
        query = "SELECT * FROM  noprefix WHERE user_id = ?"
        val = (user.id,)
        with sqlite3.connect('database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            np_db = cursor.fetchone()
        if isinstance(server, str):
            if server.lower() == "all":
                pass
            elif server.lower() == "this":
                server = ctx.guild
            else:
                return await ctx.send("Please provide a valid guild id or 'all' for All servers or 'this' for this server")
        else:
            if np_db['servers'] is not None:
                if server.id not in literal_eval(np_db['servers']):
                    em = discord.Embed(description=f"{str(user)} don't have no prefix for {server.name}", color=0xc283fe)
                    return await ctx.reply(embed=em, mention_author=False)
        if np_db is None:
            try:
                if server.lower() == "all":
                    server = "Any of the server"
            except:
                pass
            em = discord.Embed(description=f"{str(user)} don't have no prefix for {server}", color=0xc283fe)
            return await ctx.send(embed=em)
        else:
            if isinstance(server, str):
                sql = (f"UPDATE noprefix SET main = ? WHERE user_id = ?")
                val = (0, user.id,)
                cursor.execute(sql, val)
                sql = (f"UPDATE noprefix SET servers = ? WHERE user_id = ?")
                val = ("[]", user.id,)
                cursor.execute(sql, val)
            else:
                if np_db['servers'] is None:
                    em = discord.Embed(description=f"{str(user)} don't have no prefix for {server}", color=0xc283fe)
                    return await ctx.send(embed=em)
                else:
                    np = literal_eval(np_db['servers'])
                    np.remove(server.id)
                    sql = (f"UPDATE noprefix SET servers = ? WHERE user_id = ?")
                    val = (f"{np}", user.id)
                    cursor.execute(sql, val)
        em = discord.Embed(description=f"Removed no prefix from {str(user)} for {server}", color=0xc283fe)
        await ctx.reply(embed=em, mention_author=False)
        db.commit()
        cursor.close()
        db.close()
        em = discord.Embed(description=f"No prefix for {server} server(s) were removed from {user.mention} [{user.id}] by {ctx.author.mention} [{ctx.author.id}]")
        webhook = discord.SyncWebhook.from_url(webhook_np_logs)
        webhook.send(embed=em, username=f"{str(self.bot.user)} | No prefix Removed Logs", avatar_url=self.bot.user.avatar.url)

async def setup(bot):
    await bot.add_cog(noprefix(bot))
