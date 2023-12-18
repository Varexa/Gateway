import discord
import json
import asyncio
import datetime
import time as timeee
import random
import sqlite3
from ast import literal_eval
from paginators import PaginationView

from discord.ext import commands, tasks        

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
        return val * time_dic[unit]
    else:
        return val * time_dic[unit]

async def stop_giveaway(self, g_id, data, guild_id, reroll = None):
    if reroll is None:
      if data["status"] is False:
        return
    else:
      pass
    query = "SELECT * FROM  gwmain WHERE guild_id = ?"
    val = (guild_id,)
    with sqlite3.connect('./database.sqlite3') as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        cursor.execute(query, val)
        gw_db = cursor.fetchone()
    xd = literal_eval(gw_db["gw"])
    try:
      channel = self.bot.get_channel(data["channel_id"])
      giveaway_message = await channel.fetch_message(int(g_id))
    except:
      if g_id in xd:
        del xd[g_id]
        sql = (f"UPDATE gwmain SET gw = ? WHERE guild_id = ?")
        val = (f"{xd}", guild_id)
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
    data['status'] = False
    xd[giveaway_message.id] = data
    sql = (f"UPDATE gwmain SET gw = ? WHERE guild_id = ?")
    val = (f"{xd}", channel.guild.id)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()
    await giveaway_message.edit(view=xddd())
    users = data["users"]
    if len(users) < data["winners"]:
        winners_number = len(users)
    else:
        winners_number = data["winners"]
    winners = random.sample(users, winners_number)
    users_mention = []
    for user in winners:
        u = await self.bot.fetch_user(user)
        users_mention.append(u.mention)
    if len(users_mention) == 0:
        x = discord.utils.get(self.bot.users, id=data['host'])
        result_embed = discord.Embed(
            title=f" {data['prize']} ",
            color=0xc283fe,
            description=f"Ended <t:{round(datetime.datetime.now().timestamp())}:R> <t:{round(datetime.datetime.now().timestamp())}:f>\nWinners: No one Entered the giveaway\nHosted by {x.mention}")
        result_embed.set_footer(icon_url=self.bot.user.avatar.url, text="Giveaway Ended")
        result_embed.timestamp = datetime.datetime.now()
        await giveaway_message.edit(embed=result_embed)
        v = discord.ui.View()
        v.add_item(discord.ui.Button(label=f"Jump to Giveaway", url=giveaway_message.jump_url))
        await channel.send(f"No one entered the giveaway with the prize `{data['prize']}`", view=v)
    else:
        x = discord.utils.get(self.bot.users, id=data['host'])
        result_embed = discord.Embed(
            title=f" {data['prize']} ",
            color=0xc283fe,
            description=f"Ended <t:{round(datetime.datetime.now().timestamp())}:R> <t:{round(datetime.datetime.now().timestamp())}:f>\nWinners: {', '.join(users_mention)}\nHosted by {x.mention}\nEntries recieved: **{len(data['users'])}**")
        result_embed.set_footer(icon_url=self.bot.user.avatar.url, text="Giveaway Ended")
        await giveaway_message.edit(embed=result_embed)
        em = discord.Embed(description=f"You won the prize `{data['prize']}`.\nContact the giveaway host {x.mention} to claim your reward.", color=0xc283fe)
        em.set_footer(icon_url=self.bot.user.avatar.url, text="Giveaway Ended")
        em.timestamp = datetime.datetime.now()
        v = discord.ui.View()
        v.add_item(discord.ui.Button(label=f"Jump to Giveaway", url=giveaway_message.jump_url))
        await channel.send(f'{", ".join(users_mention)}', embed=em, view=v)

class xddd(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
        self.value = None

    @discord.ui.button(emoji="🎉", custom_id='gw', disabled=True, style=discord.ButtonStyle.grey)
    async def _b(self, interaction, button):
        self.value = 'ban'
        self.stop()

class GWBUTTON(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None
    
    @discord.ui.button(emoji="🎉", custom_id='gw', style=discord.ButtonStyle.grey)
    async def png(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        query = "SELECT * FROM  gwmain WHERE guild_id = ?"
        val = (interaction.guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            gw_db = cursor.fetchone()
        if gw_db is None:
            pass
        else:
            xd = literal_eval(gw_db["gw"])
            if interaction.message.id in xd:
                ls = xd[interaction.message.id]["users"]
                if interaction.user.id not in ls:
                    c = True
                    ls.append(interaction.user.id)
                else:
                    c = False
                    ls.remove(interaction.user.id)
                xd[interaction.message.id]["users"] = ls
                host = await interaction.client.fetch_user(xd[interaction.message.id]["host"])
                em = interaction.message.embeds[0]
                em.description = f"Ends <t:{round(xd[interaction.message.id]['end_time'])}:R> <t:{round(xd[interaction.message.id]['end_time'])}:f>\nHosted by {host.mention}\n{'Winners' if xd[interaction.message.id]['winners'] > 1 else 'Winner'}: **{xd[interaction.message.id]['winners']}**\nEntries: **{len(ls)}**"
                await interaction.message.edit(embed=em, view=self)
                sql = (f"UPDATE gwmain SET gw = ? WHERE guild_id = ?")
                val = (f"{xd}", interaction.guild.id)
                cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        em = discord.Embed(color=0xc283fe).set_author(name=str(interaction.user), icon_url=interaction.user.display_avatar.url).set_footer(text=str(interaction.client.user), icon_url=interaction.client.user.avatar.url)
        em.timestamp = datetime.datetime.now()
        if c:
            em.description = f"Your entry for [{str(xd[interaction.message.id]['prize']).upper()}]({interaction.message.jump_url}) Giveaway has been confirmed\n\n"
        else:
            em.description = f"> You successfully left Giveaway [{str(xd[interaction.message.id]['prize']).upper()}]({interaction.message.jump_url})"
        v = discord.ui.View()
        v.add_item(discord.ui.Button(label="Invite me", url=discord.utils.oauth_url(interaction.client.user.id)))
        try:
            await interaction.user.send(embed=em, view=v)
        except:
            pass

class giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.giveaway_task.start()

    def cog_unload(self):
        self.giveaway_task.cancel()

    @tasks.loop(seconds=45)
    async def giveaway_task(self):
        await self.bot.wait_until_ready()
        query = "SELECT * FROM  gwmain"
        with sqlite3.connect('./database.sqlite3') as db:
                    db.row_factory = sqlite3.Row
                    cursor = db.cursor()
                    cursor.execute(query)
                    gw_db = cursor.fetchall()
        for i, j in gw_db:
                x = literal_eval(j)
                for f in x:
                    if int(timeee.time()) > x[f]['end_time']:
                        if x[f]['status']:
                            try:
                                await stop_giveaway(self, f, x[f], guild_id=i)
                            except:
                                continue
    
    @commands.command(aliases=['gcreate'], description="To start a giveaway")
    @commands.has_permissions(manage_guild=True)
    async def gstart(self, ctx: commands.Context):
        x = discord.Embed(
            title="🎉 New Giveaway!! 🎉",
            description="Please answer the following questions",
            color=0xc283fe)
        x.set_footer(icon_url=self.bot.user.avatar.url, text=self.bot.user.name)
        init = await ctx.send(embed=x)

        questions = [
            "What would be the prize of the giveaway?",
            "What would the giveaway channel be like? (Please mention the giveaway channel)",
            "What would be the duration of the giveaway?",
            "How many winners do you want for this Giveaway?"
        ]

        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel

        index = 1
        answers = []
        question_message = None
        for question in questions:
            embed = discord.Embed(
                title="Giveaway 🎉",
                description=question,
                color=0xc283fe
            ).set_footer(icon_url=self.bot.user.avatar.url, text="Giveaway !")
            if index == 1:
                question_message = await ctx.send(embed=embed)
            else:
                await question_message.edit(embed=embed)

            try:
                user_response = await self.bot.wait_for("message", timeout=120, check=check)
                await user_response.delete()
            except asyncio.TimeoutError:
                await ctx.send(embed=discord.Embed(
                    title="Error",
                    color=0xc283fe,
                    description="You took too long to answer this question"
                ))
                await init.delete()
                await question_message.delete()
                return
            else:
                answers.append(user_response.content)
                index += 1
        try:
            channel_id = int(answers[1][2:-1])
        except ValueError:
            await ctx.send(f"You didn't mention the channel correctly, do it like {ctx.channel.mention}.")
            await init.delete()
            await question_message.delete()
            return

        try:
            winners = abs(int(answers[3]))
            if winners == 0:
                await ctx.send("You did not enter an postive number.")
                return
        except ValueError:
            await ctx.send("You did not enter an integer.")
            await init.delete()
            await question_message.delete()
            return
        prize = answers[0].title()
        channel = self.bot.get_channel(channel_id)
        converted_time = convert(answers[2])
        if converted_time == -1:
            await ctx.send("You did not enter the correct unit of time (s|m|h|d)")
        elif converted_time == -2:
            await ctx.send("Your time value should be an integer.")
            return
        await init.delete()
        if converted_time < 60:
          return await ctx.reply(f"The time of giveaway must be more than 1 minute")
        await question_message.delete()
        stamp = datetime.datetime.now() + datetime.timedelta(seconds=converted_time)
        giveaway_embed = discord.Embed(
            title=f" {prize} ",
            color=0xc283fe,
            description=f'Ends at: <t:{round(stamp.timestamp())}:R> <t:{round(stamp.timestamp())}:f>\n'
                        f'Hosted by {ctx.author.mention}\n'
                        f"{'Winners' if winners > 1 else 'Winner'}: **{winners}**\n"
                        f'Entries: **0**')
        giveaway_embed.set_footer(icon_url=self.bot.user.avatar.url, text=f"Ends at ")
        giveaway_embed.timestamp = datetime.datetime.utcnow() + datetime.timedelta(seconds=converted_time)
        giveaway_message = await channel.send("🎉**New Giveaway**🎉", embed=giveaway_embed)
        v = GWBUTTON()
        await giveaway_message.edit(view=v)
        self.bot.add_view(v)
        now = int(timeee.time())
        data = {
            "prize": prize,
            "host": ctx.author.id,
            "winners": winners,
            "end_time": now + converted_time,
            "channel_id": channel.id,
            "g_id": giveaway_message.id,
            "users": [],
            "status": True
        }
        query = "SELECT * FROM  gwmain WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            gw_db = cursor.fetchone()
        if gw_db is None:
            xd = {}
            xd[giveaway_message.id] = data
            sql = (f"INSERT INTO gwmain(guild_id, gw) VALUES(?, ?)")
            val = (ctx.guild.id, f"{xd}")
            cursor.execute(sql, val)
        else:
            xd = literal_eval(gw_db["gw"])
            xd[giveaway_message.id] = data
            sql = (f"UPDATE gwmain SET gw = ? WHERE guild_id = ?")
            val = (f"{xd}", ctx.guild.id)
            cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        await ctx.reply(f"Giveaway started in {channel.mention}")

    @commands.command(description="To quickly start a giveaway")
    @commands.has_permissions(manage_guild=True)
    async def gquick(self, ctx: commands.Context, time, winner, *, prize):
        await ctx.message.delete()
        winner = int(winner)
        converted_time = convert(time)
        channel = ctx.channel
        prize = prize.title()
        if converted_time == -1 or converted_time == -2:
            em = discord.Embed(description=f"<:error:1153009680428318791>Provide specific time!", color=0xff0000)
            return await ctx.send(embed=em)
        if converted_time < 60:
          return await ctx.reply(f"The time of giveaway must be more than 1 minute")
        stamp = datetime.datetime.now() + datetime.timedelta(seconds=converted_time)
        giveaway_embed = discord.Embed(
            title=f" {prize} ",
            color=0xc283fe,
            description=f'Ends at: <t:{round(stamp.timestamp())}:R> <t:{round(stamp.timestamp())}:f>\n'
                        f'Hosted by {ctx.author.mention}\n'
                        f"{'Winners' if winner > 1 else 'Winner'}: **{winner}**\n"
                        f'Entries: **0**')
        giveaway_embed.set_footer(icon_url=self.bot.user.avatar.url, text=f"Ends at ")
        giveaway_embed.timestamp = datetime.datetime.utcnow() + datetime.timedelta(seconds=converted_time)
        giveaway_message = await ctx.send("🎉**New Giveaway**🎉", embed=giveaway_embed)
        v = GWBUTTON()
        await giveaway_message.edit(view=v)
        self.bot.add_view(v)
        now = int(timeee.time())
        data = {
            "prize": prize,
            "host": ctx.author.id,
            "winners": winner,
            "end_time": now + converted_time,
            "channel_id": channel.id,
            "g_id": giveaway_message.id,
            "users": [],
            "status": True
        }
        query = "SELECT * FROM  gwmain WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            gw_db = cursor.fetchone()
        if gw_db is None:
            xd = {}
            xd[giveaway_message.id] = data
            sql = (f"INSERT INTO gwmain(guild_id, gw) VALUES(?, ?)")
            val = (ctx.guild.id, f"{xd}")
            cursor.execute(sql, val)
        else:
            xd = literal_eval(gw_db["gw"])
            xd[giveaway_message.id] = data
            sql = (f"UPDATE gwmain SET gw = ? WHERE guild_id = ?")
            val = (f"{xd}", ctx.guild.id)
            cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
    
    @commands.command(description="To get the list of all running giveaways in the server")
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(manage_guild=True)
    async def glist(self, ctx: commands.Context):
        query = "SELECT * FROM  gwmain WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
                    db.row_factory = sqlite3.Row
                    cursor = db.cursor()
                    cursor.execute(query, val)
                    gw_db = cursor.fetchone()
        em_no = discord.Embed(description="No Giveaway is presently running in this server!", color=0xc283fe)
        em_no.set_footer(text=f"{self.bot.user.name} Giveaway", icon_url=self.bot.user.avatar.url)
        if gw_db is None:
            return await ctx.send(embed=em_no)
        xd = literal_eval(gw_db["gw"])
        if len(xd) == 0:
            return await ctx.send(embed=em_no)
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
            des.append(f"`[{'0' + str(count) if count < 10 else count}]` | {xddd[j]['prize']} - [[{xddd[j]['g_id']}]({g_msg.jump_url})] Ends at: <t:{round(j)}:R>")
            count+=1
        if len(des) == 0:
            return await ctx.send(embed=em_no)
        for i in range(0, len(des), 10):
           ls.append(des[i: i + 10])
        em_list = []
        no = 1
        for k in ls:
           embed =discord.Embed(color=0xc283fe)
           embed.title = f"Giveaways presently running in the server - {count-1}"
           embed.description = "\n".join(k)
           embed.set_footer(text=f"{self.bot.user.name} • Page {no}/{len(ls)}", icon_url=self.bot.user.display_avatar.url)
           em_list.append(embed)
           no+=1
        page = PaginationView(embed_list=em_list, ctx=ctx)
        await page.start(ctx)

    @commands.command(aliases=['gstop'], description="To end a giveaway")
    @commands.has_permissions(manage_guild=True)
    async def gend(self, ctx: commands.Context, message_id):
        await ctx.message.delete()
        query = "SELECT * FROM  gwmain WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
                    db.row_factory = sqlite3.Row
                    cursor = db.cursor()
                    cursor.execute(query, val)
                    gw_db = cursor.fetchone()
        if gw_db is None:
            return await ctx.send(f"Invalid Giveaway id")
        xd = literal_eval(gw_db["gw"])
        if int(message_id) not in xd:
            return await ctx.send(f"Invalid Giveaway id")
        if xd[int(message_id)]['status']:
                await stop_giveaway(self, message_id, xd[int(message_id)])
        else:
            return await ctx.send("Giveaway is already ended")

    @commands.command(description="To reroll the winner for giveaway")
    @commands.has_permissions(manage_guild=True)
    async def greroll(self, ctx: commands.Context, message_id):
        await ctx.message.delete()
        query = "SELECT * FROM  gwmain WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
                    db.row_factory = sqlite3.Row
                    cursor = db.cursor()
                    cursor.execute(query, val)
                    gw_db = cursor.fetchone()
        if gw_db is None:
            return await ctx.send(f"Invalid Giveaway id")
        xd = literal_eval(gw_db["gw"])
        if int(message_id) not in xd:
            return await ctx.send(f"Invalid Giveaway id")
        if not xd[int(message_id)]['status']:
                await stop_giveaway(self, message_id, xd[int(message_id)], ctx.guild.id, True)
        else:
            return await ctx.send(f"Giveaway is not yet ended")
    
    @commands.command(description="To cancel a giveaway")
    @commands.has_permissions(manage_guild=True)
    async def gcancel(self, ctx: commands.Context, message_id):
        query = "SELECT * FROM  gwmain WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
                    db.row_factory = sqlite3.Row
                    cursor = db.cursor()
                    cursor.execute(query, val)
                    gw_db = cursor.fetchone()
        if gw_db is None:
            return await ctx.send(f"Invalid Giveaway id")
        xd = literal_eval(gw_db["gw"])
        if int(message_id) not in xd:
            return await ctx.send(f"Invalid Giveaway id")
        if not xd[int(message_id)]['status']:
            return await ctx.send("Giveaway is already ended")
        else:
            xd[int(message_id)]['status'] = False
        sql = (f"UPDATE gwmain SET gw = ? WHERE guild_id = ?")
        val = (f"{xd}", ctx.guild.id)
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        await ctx.reply(f"Cancelled the giveaway with prize: `{xd[int(message_id)]['prize']}`")

async def setup(bot):
    await bot.add_cog(giveaway(bot))
