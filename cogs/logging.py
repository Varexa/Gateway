import discord
import datetime
from discord.ext import commands, tasks
from ast import literal_eval
import sqlite3
import io
from paginators import PaginationView, PaginatorView

import io

class enablemenu(discord.ui.Select):
    def __init__(self, ctx: commands.Context, channel: discord.TextChannel):
        options = []
        ls = ["mod", "role", "message", "member", "channel", "server"]
        query = "SELECT * FROM  'logs' WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            log_db = cursor.fetchone()
        db.commit()
        cursor.close()
        db.close()
        c = 0
        for i in sorted(ls):
            if log_db[i] is None:
                options.append(discord.SelectOption(label=f"{i.capitalize()} Logs", value=i))
                c = c+1
        super().__init__(placeholder="Select specific types of loggings",
            min_values=1,
            max_values=c,
            options=options,
        )
        self.ctx = ctx
        self.channel = channel

    async def callback(self, interaction: discord.Interaction):
        ctx = self.ctx
        channel = self.channel
        query = "SELECT * FROM  logs WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            log_db = cursor.fetchone()
        des= ""
        for i in self.values:
                if log_db[i] is None:
                    sql = (f"UPDATE logs SET '{i}' = ? WHERE guild_id = ?")
                    val = (channel.id, ctx.guild.id)
                    cursor.execute(sql, val)
                    des += f"{i.capitalize()} Logs, "
                    pass
                else:
                    sql = (f"UPDATE logs SET '{i}' = ? WHERE guild_id = ?")
                    val = (channel.id, ctx.guild.id)
                    cursor.execute(sql, val)
                    des += f"{i.capitalize()} Logs, "
                    pass
        db.commit()
        cursor.close()
        db.close()
        em = discord.Embed(description=f"{channel.mention} is now set for {des[:-2]}", color=0xc283fe)
        await self.ctx.reply(embed=em)
        await interaction.message.delete()

class enableview(discord.ui.View):
    def __init__(self, ctx: commands.Context, channel: discord.TextChannel):
        super().__init__(timeout=60)
        self.add_item(enablemenu(ctx, channel))
        self.ctx = ctx
        self.channel = channel

    @discord.ui.button(label="All Loggings", style=discord.ButtonStyle.blurple)
    async def _enable(self, interaction, button):
        ctx = self.ctx
        channel = self.channel
        query = "SELECT * FROM  logs WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            log_db = cursor.fetchone()
        des= ""
        ls = ["mod", "role", "message", "member", "channel", "server"]
        for i in sorted(ls):
                if log_db[i] is None:
                    sql = (f"UPDATE logs SET '{i}' = ? WHERE guild_id = ?")
                    val = (channel.id, ctx.guild.id)
                    cursor.execute(sql, val)
                    des += f"{i.capitalize()} Logs, "
                    pass
                else:
                    sql = (f"UPDATE logs SET '{i}' = ? WHERE guild_id = ?")
                    val = (channel.id, ctx.guild.id)
                    cursor.execute(sql, val)
                    des += f"{i.capitalize()} Logs, "
                    pass
        db.commit()
        cursor.close()
        db.close()
        em = discord.Embed(description=f"{channel.mention} is now set for {des[:-2]}", color=0xc283fe)
        await self.ctx.reply(embed=em)
        await interaction.message.delete()

class disablemenu(discord.ui.Select):
    def __init__(self, ctx: commands.Context, channel: discord.TextChannel=None):
        options = []
        ls = ["mod", "role", "message", "member", "channel", "server"]
        query = "SELECT * FROM  'logs' WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            log_db = cursor.fetchone()
        db.commit()
        cursor.close()
        db.close()
        c = 0
        for i in sorted(ls):
            if log_db[i] is not None:
                if channel is not None:
                    if log_db[i] == channel.id:
                        options.append(discord.SelectOption(label=f"{i.capitalize()} Logs", value=i))
                        c = c+1
                else:
                    options.append(discord.SelectOption(label=f"{i.capitalize()} Logs", value=i))
                    c = c+1
        super().__init__(placeholder="Select specific types of loggings to be removed",
            min_values=1,
            max_values=c,
            options=options,
        )
        self.ctx = ctx
        self.channel = channel

    async def callback(self, interaction: discord.Interaction):
        ctx = self.ctx
        channel = self.channel
        query = "SELECT * FROM  logs WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            log_db = cursor.fetchone()
        des= ""
        for i in self.values:
                if log_db[i] is None:
                    sql = (f"UPDATE logs SET '{i}' = ? WHERE guild_id = ?")
                    val = (None, ctx.guild.id)
                    cursor.execute(sql, val)
                    des += f"{i.capitalize()} Logs, "
                    pass
                else:
                    sql = (f"UPDATE logs SET '{i}' = ? WHERE guild_id = ?")
                    val = (None, ctx.guild.id)
                    cursor.execute(sql, val)
                    des += f"{i.capitalize()} Logs, "
                    pass
        db.commit()
        cursor.close()
        db.close()
        if channel is not None:
            em = discord.Embed(description=f"Removed {des[:-2]} from being logged in {channel.mention}", color=0xc283fe)
        else:
            em = discord.Embed(description=f"Removed {des[:-2]} from being logged in the server", color=0xc283fe)
        await self.ctx.reply(embed=em)
        await interaction.message.delete()
        self.stop()

class disableview(discord.ui.View):
    def __init__(self, ctx: commands.Context, channel: discord.TextChannel=None):
        super().__init__(timeout=60)
        self.add_item(disablemenu(ctx, channel))
        self.ctx = ctx
        self.channel = channel

    

    @discord.ui.button(label="All Loggings", style=discord.ButtonStyle.blurple)
    async def _disable(self, interaction, button):
        ctx = self.ctx
        channel = self.channel
        query = "SELECT * FROM  logs WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            log_db = cursor.fetchone()
        db.commit()
        cursor.close()
        db.close()
        des= ""
        ls = ["mod", "role", "message", "member", "channel", "server"]
        ls1 = []
        if channel is not None:
            for i in ls:
                if log_db[i] == channel.id:
                    ls1.append(i)
            for i in sorted(ls1):
                        sql = (f"UPDATE logs SET '{i}' = ? WHERE guild_id = ?")
                        val = (None, ctx.guild.id)
                        cursor.execute(sql, val)
                        des += f"{i.capitalize()} Logs, "
                        pass
            db.commit()
            em = discord.Embed(description=f"Removed all loggings from {channel.mention}", color=0xc283fe)
        else:
            for i in sorted(ls):
                        sql = (f"UPDATE logs SET '{i}' = ? WHERE guild_id = ?")
                        val = (None, ctx.guild.id)
                        cursor.execute(sql, val)
                        des += f"{i.capitalize()} Logs, "
                        pass
            db.commit()
            em = discord.Embed(description=f"Removed all loggings from the server", color=0xc283fe)
        await self.ctx.reply(embed=em)
        await interaction.message.delete()
        self.stop()

class logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.group(
        name="logging",
        invoke_without_command=True, description="Shows the logging's help menu"
    )
    async def logging(self, ctx):
        prefix = ctx.prefix
        if prefix == f"<@{self.bot.user.id}> ":
            prefix = f"@{str(self.bot.user)} "
        anay = discord.utils.get(self.bot.users, id=978930369392951366)
        ls = ["logging", "logging enable", "logging disable", "logging config"]
        des = ""
        for i in sorted(ls):
            cmd = self.bot.get_command(i)
            if cmd.description is None:
                cmd.description = "No Description"
            des += f"`{prefix}{i}`\n{cmd.description}\n\n"
        listem = discord.Embed(title=f"<:logging:1036689057654263898> Logging Commands", colour=0xc283fe,
                                     description=f"<...> Duty | [...] Optional\n\n{des}")
        listem.set_author(name=f"{str(ctx.author)}", icon_url=ctx.author.display_avatar.url)
        listem.set_footer(text=f"Made by stars.gg" ,  icon_url=anay.avatar.url)
        await ctx.send(embed=listem)
    
    @logging.command(name="config",description="Shows the current Logging settings")
    @commands.has_permissions(administrator=True)
    async def config(self, ctx):
        if ctx.author.id == ctx.guild.owner.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 979353019235840000]:
                em = discord.Embed(description=f"<:error:1153009680428318791>You must Have Higher Role than Bot To run This Command", color=0xff0000)
                return await ctx.send(embed=em)
        query = "SELECT * FROM  logs WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            log_db = cursor.fetchone()
        db.commit()
        cursor.close()
        db.close()
        ls = ["mod", "role", "message", "member", "channel", "server"]
        em = discord.Embed(title="Logs setting for the server", color=0xc283fe)
        for i in sorted(ls):
            if log_db[i] is not None:
                c = discord.utils.get(ctx.guild.channels, id=log_db[i])
                if c is None:
                    em.add_field(name=f"{i.capitalize()} Logs:", value="The channel is deleted", inline=True)
                else:
                    em.add_field(name=f"{i.capitalize()} Logs:", value=c.mention, inline=True)
            else:
                em.add_field(name=f"{i.capitalize()} Logs:", value="Disabled")
        em.set_footer(text=f"Logging system", icon_url=self.bot.user.display_avatar.url)
        await ctx.reply(embed=em)

    @logging.command(name="enable", aliases=['on'], description="Enable the logs for the server")
    @commands.has_permissions(administrator=True)
    async def enable(self, ctx, *, channel: discord.TextChannel):
        if ctx.author.id == ctx.guild.owner.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 979353019235840000]:
                em = discord.Embed(description=f"<:error:1153009680428318791>You must Have Higher Role than Bot To run This Command", color=0xff0000)
                return await ctx.send(embed=em)
        query = "SELECT * FROM  logs WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            log_db = cursor.fetchone()
        db.commit()
        cursor.close()
        db.close()
        ls = ["mod", "role", "message", "member", "channel", "server"]
        c = 0
        for i in ls:
            if log_db[i] is None:
                c+=1
        if c == 0:
            return await ctx.reply(f"All types of loggings are already enabled")
        view = enableview(ctx, channel)
        em = discord.Embed(description=f"Which types of loggings should be logged in {channel.mention}?", color=0xc283fe)
        m = await ctx.reply(embed=em, view=view)
        await view.wait()
    
    @logging.command(name="disable", aliases=['off'], description="Disable the logs for the server")
    @commands.has_permissions(administrator=True)
    async def disable(self, ctx, *, channel: discord.TextChannel=None):
        if ctx.author.id == ctx.guild.owner.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 979353019235840000]:
                em = discord.Embed(description=f"<:error:1153009680428318791>You must Have Higher Role than Bot To run This Command", color=0xff0000)
                return await ctx.send(embed=em)
        query = "SELECT * FROM  logs WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            log_db = cursor.fetchone()
        db.commit()
        cursor.close()
        db.close()
        ls = ["mod", "role", "message", "member", "channel", "server"]
        c = 0
        for i in ls:
            if log_db[i] is not None:
                if channel is not None:
                    if log_db[i] == channel.id:
                        c+=1
                else:
                    c+=1
        if c == 0:
            if channel is not None:
                return await ctx.reply(f"All types of loggings are already disabled in {channel.mention}")
            else:
                return await ctx.reply(f"All types of loggings are already disabled")
        if channel is not None:
            view = disableview(ctx, channel)
        else:
            view = disableview(ctx)
        if channel is not None:
            em = discord.Embed(description=f"Which types of loggings should be removed from being logged in {channel.mention}?", color=0xc283fe)
        else:
            em = discord.Embed(description=f"Which types of loggings should be removed from being logged?", color=0xc283fe)
        m = await ctx.reply(embed=em, view=view)
        await view.wait()
    
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        await self.bot.wait_until_ready()
        if not member.guild:
            return
        if not member.guild.me:
            return
        if not member.guild.me.guild_permissions.view_audit_log:
            return
        query = "SELECT * FROM  logs WHERE guild_id = ?"
        val = (member.guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            log_db = cursor.fetchone()
        db.commit()
        cursor.close()
        db.close()
        if log_db is None:
            return
        if log_db['member'] is not None:
            c = discord.utils.get(member.guild.channels, id=log_db['member'])
            if c is None:
                return
            em = discord.Embed(title="A member joined the server", description=f"Username: {str(member)}\nUser id: {member.id}\nAccount created at: <t:{round(member.created_at.timestamp())}:R>", color=0xc283fe)
            if member.bot:
                async for entry in member.guild.audit_logs(limit=1,after=datetime.datetime.now() - datetime.timedelta(minutes=2),action=discord.AuditLogAction.bot_add):
                    em.title = "A bot added to the server"
                    m = entry.user
                    em.add_field(name="Bot added by:", value=f"{str(m)} - [{m.id}] {m.mention}")
            em.set_author(name=f"{str(member)}", icon_url=member.display_avatar.url)
            em.set_footer(text="Joined", icon_url=member.guild.me.display_avatar.url)
            em.timestamp = datetime.datetime.utcnow()
            em.set_thumbnail(url=member.display_avatar.url)
            await c.send(embed=em)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        await self.bot.wait_until_ready()
        if not member.guild:
            return
        if not member.guild.me:
            return
        if not member.guild.me.guild_permissions.view_audit_log:
            return
        query = "SELECT * FROM  logs WHERE guild_id = ?"
        val = (member.guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            log_db = cursor.fetchone()
        db.commit()
        cursor.close()
        db.close()
        if log_db is None:
            return
        if log_db['member'] is None and log_db['mod'] is None:
            return
        kick = False
        if member.guild.me.guild_permissions.view_audit_log:
            async for entry in member.guild.audit_logs(
                limit=1,
                after=datetime.datetime.now() - datetime.timedelta(seconds=3),
                action=discord.AuditLogAction.kick):
                x = datetime.datetime.now() - datetime.timedelta(seconds=10)
                if entry.target.id == member.id and x.timestamp() <= entry.created_at.timestamp():
                    kick = True
                    m = entry.user
                    if not m.guild:
                      return
                    if entry.reason:
                        r = entry.reason
        if log_db['member'] is not None:
            c = discord.utils.get(member.guild.channels, id=log_db['member'])
            if c is None:
                return
            em = discord.Embed(title="A member left the server", description=f"Username: {str(member)}\nUser id: {member.id}\nAccount created at: <t:{round(member.created_at.timestamp())}:R>", color=0xc283fe)
            em.set_author(name=f"{str(member)}", icon_url=member.display_avatar.url)
            em.set_footer(text="Left", icon_url=member.guild.me.display_avatar.url)
            em.timestamp = datetime.datetime.utcnow()
            em.set_thumbnail(url=member.display_avatar.url)
            await c.send(embed=em)
        if kick:
            if log_db['mod'] is not None:
                c = discord.utils.get(member.guild.channels, id=log_db['mod'])
                if c is None:
                    return
                em = discord.Embed(title="A member got kicked from the server", description=f"Username: {str(member)}\nUser id: {member.id}\nAccount created at: <t:{round(member.created_at.timestamp())}:R>", color=0xc283fe)
                em.add_field(name="Kicked by:", value=f"{str(m)} - [{m.id}] {m.mention}")
                if r:
                    em.add_field(name="Reason:", value=r)
                em.set_author(name=f"{str(member)}", icon_url=member.display_avatar.url)
                em.set_footer(text="Kicked", icon_url=member.guild.me.display_avatar.url)
                em.timestamp = datetime.datetime.utcnow()
                em.set_thumbnail(url=member.display_avatar.url)
                await c.send(embed=em)
    
    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member,
                               after: discord.Member) -> None:
        await self.bot.wait_until_ready()
        if not after.guild:
            return
        if not after.guild.me.guild_permissions.view_audit_log:
            return
        query = "SELECT * FROM  logs WHERE guild_id = ?"
        val = (after.guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            log_db = cursor.fetchone()
        db.commit()
        cursor.close()
        db.close()
        if log_db is None:
            return
        if log_db['member'] is None:
            return
        async for entry in after.guild.audit_logs(
                limit=1,
                after=datetime.datetime.now() - datetime.timedelta(seconds=3),
                action=discord.AuditLogAction.member_update):
                if log_db['member'] is not None:
                    c = discord.utils.get(after.guild.channels, id=log_db['member'])
                    if c is None:
                        return
                    member = entry.target
                    if not member.guild:
                      return
                    em = discord.Embed(title="A member updated", color=0xc283fe)
                    em.set_author(name=f"{str(member)}", icon_url=member.display_avatar.url)
                    em.set_footer(text="UPDATED", icon_url=member.guild.me.display_avatar.url)
                    em.timestamp = datetime.datetime.utcnow()
                    em.set_thumbnail(url=member.display_avatar.url)
                    if after.nick != before.nick:
                        em.description=f"Nickname changed:\n`{before.nick}` to `{after.nick}`"
                        em.add_field(name="Nick changed by:", value=f"{str(entry.user)} - [{entry.user.id}] {entry.user.mention}")
                        em.title = "A member's nickname changed"
                        await c.send(embed=em)
                    if len(after.roles) != len(before.roles):
                        async for ent in after.guild.audit_logs(
                                        limit=1,
                                        after=datetime.datetime.now() - datetime.timedelta(seconds=3),
                                        action=discord.AuditLogAction.member_role_update):
                            check = False
                            if len(after.roles) > len(before.roles):
                                for r in after.roles:
                                    if r.id == after.guild.premium_subscriber_role.id:
                                        continue
                                    if r not in before.roles:
                                        em.add_field(name="Role Added:", value=f"{r.mention} - [{r.id}]")
                                        em.add_field(name="Role Added by:", value=f"{str(ent.user)} - [{ent.user.id}] {ent.user.mention}")
                                        x = "No"
                                        if after.top_role != before.top_role:
                                            x = "Yes"
                                        em.add_field(name="Top role changed?", value=x)
                                        em.title = "A member's role changed"
                                        check = True
                            else:
                                for r in before.roles:
                                    if r.id == after.guild.premium_subscriber_role.id:
                                        continue
                                    if r not in after.roles:
                                        em.add_field(name="Role Removed:", value=f"{r.mention} - [{r.id}]")
                                        em.add_field(name="Role Removed by:", value=f"{str(ent.user)} - [{ent.user.id}] {ent.user.mention}")
                                        x = "No"
                                        if after.top_role != before.top_role:
                                            x = "Yes"
                                        em.add_field(name="Top role changed?", value=x)
                                        em.title = "A member's role changed"
                                        check = True
                            if ent.reason:
                                em.add_field(name="Reason", value=ent.reason)
                            em.set_author(name=f"{str(ent.target)}", icon_url=ent.target.display_avatar.url)
                            em.set_footer(text="UPDATED", icon_url=ent.target.guild.me.display_avatar.url)
                            em.timestamp = datetime.datetime.utcnow()
                            em.set_thumbnail(url=ent.target.display_avatar.url)
                            if check:
                                return await c.send(embed=em)
                            

    @commands.Cog.listener()
    async def on_member_ban(self, guild: discord.Guild, member: discord.Member):
        await self.bot.wait_until_ready()
        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        query = "SELECT * FROM  logs WHERE guild_id = ?"
        val = (guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            log_db = cursor.fetchone()
        db.commit()
        cursor.close()
        db.close()
        if log_db is None:
            return
        if log_db['mod'] is None:
            return
        async for entry in guild.audit_logs(limit=1,
                                            after=datetime.datetime.utcnow() -
                                            datetime.timedelta(minutes=2),
                                            action=discord.AuditLogAction.ban):
            if log_db['mod'] is not None:
                m = entry.user
                if not m.guild:
                    return
                c = discord.utils.get(member.guild.channels, id=log_db['mod'])
                
                if c is None:
                    return
                em = discord.Embed(title="A member got banned from the server", description=f"Username: {str(member)}\nUser id: {member.id}\nAccount created at: <t:{round(member.created_at.timestamp())}:R>", color=0xc283fe)
                em.add_field(name="Banned by:", value=f"{str(m)} - [{m.id}] {m.mention}")
                if entry.reason:
                    em.add_field(name="Reason:", value=entry.reason)
                em.set_author(name=f"{str(member)}", icon_url=member.display_avatar.url)
                em.set_footer(text="Banned", icon_url=member.guild.me.display_avatar.url)
                em.timestamp = datetime.datetime.utcnow()
                em.set_thumbnail(url=member.display_avatar.url)
                await c.send(embed=em)

    @commands.Cog.listener()
    async def on_member_unban(self, guild: discord.Guild, member: discord.Member):
        await self.bot.wait_until_ready()
        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        query = "SELECT * FROM  logs WHERE guild_id = ?"
        val = (guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            log_db = cursor.fetchone()
        db.commit()
        cursor.close()
        db.close()
        if log_db is None:
            return
        if log_db['mod'] is None:
            return
        async for entry in guild.audit_logs(limit=1,
                                            after=datetime.datetime.now() -
                                            datetime.timedelta(minutes=2),
                                            action=discord.AuditLogAction.unban):
            if log_db['mod'] is not None:
                m = entry.user
                if not m.guild:
                    return
                c = discord.utils.get(guild.channels, id=log_db['mod'])
                
                if c is None:
                    return
                em = discord.Embed(title="A member got unbanned from the server", description=f"Username: {str(member)}\nUser id: {member.id}\nAccount created at: <t:{round(member.created_at.timestamp())}:R>", color=0xc283fe)
                em.add_field(name="Unbanned by:", value=f"{str(m)} - [{m.id}] {m.mention}")
                if entry.reason:
                    em.add_field(name="Reason:", value=entry.reason)
                em.set_author(name=f"{str(member)}", icon_url=member.display_avatar.url)
                em.set_footer(text="Unbanned", icon_url=guild.me.display_avatar.url)
                em.timestamp = datetime.datetime.utcnow()
                em.set_thumbnail(url=member.display_avatar.url)
                await c.send(embed=em)

    @commands.Cog.listener()
    async def on_guild_role_create(self, role: discord.Role) -> None:
        await self.bot.wait_until_ready()
        guild = role.guild
        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        query = "SELECT * FROM  logs WHERE guild_id = ?"
        val = (guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            log_db = cursor.fetchone()
        db.commit()
        cursor.close()
        db.close()
        if log_db is None:
            return
        if log_db['role'] is None:
            return
        async for entry in guild.audit_logs(limit=1,
                                            after=datetime.datetime.now() -
                                            datetime.timedelta(minutes=2),
                                            action=discord.AuditLogAction.role_create):
            if log_db['role'] is not None:
                m = entry.user
                if not m.guild:
                    return
                c = discord.utils.get(guild.channels, id=log_db['role'])
                
                if c is None:
                    return
                em = discord.Embed(title="Role Created", description=f"Role {role.mention} Created by {entry.user.mention}", color=0xc283fe)
                em.add_field(name="Name", value=f"{role.name}")
                em.add_field(name="Colour", value=f"{role.color}")
                em.add_field(name="Mentionable", value=role.mentionable)
                em.add_field(name="Hoist", value=role.hoist)
                em.add_field(name="Position", value=role.position + 1)
                role_perm = ', '.join([str(p[0]).replace("_", " ").title() for p in role.permissions if p[1]])
                if role_perm is None:
                    role_perm = "No Permissions"
                em.add_field(name="Permissions", value=role_perm)
                if entry.reason:
                    em.add_field(name="Reason:", value=entry.reason)
                em.set_author(name=f"{str(entry.user)}", icon_url=entry.user.display_avatar.url)
                em.set_footer(text="Created", icon_url=guild.me.display_avatar.url)
                em.timestamp = datetime.datetime.utcnow()
                em.set_thumbnail(url=entry.user.display_avatar.url)
                if len(em.fields) > 0:
                    await c.send(embed=em)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role: discord.Role) -> None:
        await self.bot.wait_until_ready()
        guild = role.guild
        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        query = "SELECT * FROM  logs WHERE guild_id = ?"
        val = (guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            log_db = cursor.fetchone()
        db.commit()
        cursor.close()
        db.close()
        if log_db is None:
            return
        if log_db['role'] is None:
            return
        async for entry in guild.audit_logs(limit=1,
                                            after=datetime.datetime.now() -
                                            datetime.timedelta(minutes=2),
                                            action=discord.AuditLogAction.role_delete):
            if log_db['role'] is not None:
                m = entry.user
                if not m.guild:
                    return
                c = discord.utils.get(guild.channels, id=log_db['role'])
                
                if c is None:
                    return
                em = discord.Embed(title="Role Deleted", description=f"Role `{role.name}` Deleted by {entry.user.mention}", color=0xc283fe)
                em.add_field(name="Name", value=f"{role.name}")
                em.add_field(name="Colour", value=f"{role.color}")
                em.add_field(name="Mentionable", value=role.mentionable)
                em.add_field(name="Hoist", value=role.hoist)
                em.add_field(name="Members", value=len(role.members))
                role_perm = ', '.join([str(p[0]).replace("_", " ").title() for p in role.permissions if p[1]])
                if role_perm is None:
                    role_perm = "No Permissions"
                em.add_field(name="Permissions", value=role_perm)
                if entry.reason:
                    em.add_field(name="Reason:", value=entry.reason)
                em.set_author(name=f"{str(entry.user)}", icon_url=entry.user.display_avatar.url)
                em.set_footer(text="Deleted", icon_url=guild.me.display_avatar.url)
                em.timestamp = datetime.datetime.utcnow()
                em.set_thumbnail(url=entry.user.display_avatar.url)
                if len(em.fields) > 0:
                    await c.send(embed=em)

    @commands.Cog.listener()
    async def on_guild_role_update(self, before: discord.Role,
                                   after: discord.Role) -> None:
        await self.bot.wait_until_ready()
        guild = after.guild
        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        query = "SELECT * FROM  logs WHERE guild_id = ?"
        val = (guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            log_db = cursor.fetchone()
        db.commit()
        cursor.close()
        db.close()
        if log_db is None:
            return
        if log_db['role'] is None:
            return
        async for entry in guild.audit_logs(limit=1,
                                            after=datetime.datetime.now() -
                                            datetime.timedelta(minutes=2),
                                            action=discord.AuditLogAction.role_update):
            if log_db['role'] is not None:
                m = entry.user
                if not m.guild:
                    return
                c = discord.utils.get(guild.channels, id=log_db['role'])
                
                if c is None:
                    return
                em = discord.Embed(title="Role Updated", description=f"Role {after.mention} Updated by {entry.user.mention}", color=0xc283fe)
                if before.name != after.name:
                    em.add_field(name="Name changed", value=f"`{before.name}` to `{after.name}`")
                if before.color != after.color:
                    em.add_field(name="Color changed", value=f"{before.color} to {after.color}")
                if before.hoist != after.hoist:
                    em.add_field(name="Hoist changed", value=f'{"False" if after.hoist == True else "True"} to {after.hoist}')
                if before.mentionable != after.mentionable:
                    em.add_field(name="Mentionable changed", value=f'{"False" if after.mentionable == True else "True"} to {after.mentionable}')
                if before.permissions.value != after.permissions.value:
                    all_perm = []
                    b_perm = {}
                    a_perm = {}
                    given_perm = []
                    removed_perm = []
                    for i in before.permissions:
                        b_perm[i[0]] = i[1]
                        all_perm.append(i[0])
                    for i in after.permissions:
                        a_perm[i[0]] = i[1]
                    for i in all_perm:
                        if a_perm[i] != b_perm[i]:
                            if a_perm[i] == True:
                                given_perm.append(i)
                            else:
                                removed_perm.append(i)
                    if len(given_perm) > 0:
                        des = ', '.join([str(p).replace("_", " ").title() for p in given_perm])
                        em.add_field(name="Permissions given", value=des)
                    if len(removed_perm) > 0:
                        des1 = ', '.join([str(p).replace("_", " ").title() for p in removed_perm])
                        em.add_field(name="Permissions removed", value=des1)
                if before.icon != after.icon:
                    if before.icon is None:
                      d = f"None to [New Icon]({after.icon.url})"
                    elif after.icon is None:
                      d = f"[Old Icon]({before.icon.url}) to None"
                    else:
                      d = f"[Old Icon]({before.icon.url}) to [New Icon]({after.icon.url})"
                    em.add_field(name="Role icon changed", value=d)
                if entry.reason:
                    em.add_field(name="Reason:", value=entry.reason)
                em.set_author(name=f"{str(entry.user)}", icon_url=entry.user.display_avatar.url)
                em.set_footer(text="Updated", icon_url=guild.me.display_avatar.url)
                em.timestamp = datetime.datetime.utcnow()
                em.set_thumbnail(url=entry.user.display_avatar.url)
                if len(em.fields) > 0:
                    await c.send(embed=em)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel: discord.abc.GuildChannel) -> None:
        await self.bot.wait_until_ready()
        guild = channel.guild
        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        query = "SELECT * FROM  logs WHERE guild_id = ?"
        val = (guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            log_db = cursor.fetchone()
        db.commit()
        cursor.close()
        db.close()
        if log_db is None:
            return
        if log_db['channel'] is None:
            return
        async for entry in guild.audit_logs(limit=1,
                                            after=datetime.datetime.now() -
                                            datetime.timedelta(minutes=2),
                                            action=discord.AuditLogAction.channel_create):
            if log_db['channel'] is not None:
                m = entry.user
                if not m.guild:
                    return
                c = discord.utils.get(guild.channels, id=log_db['channel'])
                
                if c is None:
                    return
                if isinstance(channel, discord.TextChannel):
                    em = discord.Embed(title="Text Channel Created", description=f"Text Channel {channel.mention} Created by {entry.user.mention}", color=0xc283fe)
                if isinstance(channel, discord.VoiceChannel):
                    em = discord.Embed(title="Voice Channel Created", description=f"Voice Channel {channel.mention} Created by {entry.user.mention}", color=0xc283fe)
                if isinstance(channel, discord.CategoryChannel):
                    em = discord.Embed(title="Category Created", description=f"Category Channel {channel.mention} Created by {entry.user.mention}", color=0xc283fe)
                if isinstance(channel, discord.StageChannel):
                    em = discord.Embed(title="Stage Channel Created", description=f"Stage Channel {channel.mention} Created by {entry.user.mention}", color=0xc283fe)
                em.add_field(name="Name", value=f"{channel.name}")
                em.add_field(name="Position", value=channel.position + 1)
                overwrite = channel.overwrites_for(guild.default_role)
                em.add_field(name="Private?", value=f'{"Yes" if not overwrite.view_channel else "No"}')
                em.add_field(name="Permissions synced?", value=f'{"Yes" if channel.permissions_synced else "No"}')
                if isinstance(channel, discord.VoiceChannel) or isinstance(channel, discord.StageChannel):
                    em.add_field(name="Bitrate", value=channel.bitrate/1000)
                if channel.category:
                    em.add_field(name="Category", value=f"{channel.category.name} - [{channel.category_id}")
                if entry.reason:
                    em.add_field(name="Reason:", value=entry.reason)
                em.set_author(name=f"{str(entry.user)}", icon_url=entry.user.display_avatar.url)
                em.set_footer(text="Created", icon_url=guild.me.display_avatar.url)
                em.timestamp = datetime.datetime.utcnow()
                em.set_thumbnail(url=entry.user.display_avatar.url)
                if len(em.fields) > 0:
                    await c.send(embed=em)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel: discord.abc.GuildChannel) -> None:
        await self.bot.wait_until_ready()
        guild = channel.guild
        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        query = "SELECT * FROM  logs WHERE guild_id = ?"
        val = (guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            log_db = cursor.fetchone()
        db.commit()
        cursor.close()
        db.close()
        if log_db is None:
            return
        if log_db['channel'] is None:
            return
        async for entry in guild.audit_logs(limit=1,
                                            after=datetime.datetime.now() -
                                            datetime.timedelta(minutes=2),
                                            action=discord.AuditLogAction.channel_delete):
            if log_db['channel'] is not None:
                m = entry.user
                if not m.guild:
                    return
                c = discord.utils.get(guild.channels, id=log_db['channel'])
                if c is None:
                    return
                if isinstance(channel, discord.TextChannel):
                    em = discord.Embed(title="Text Channel Deleted", description=f"Text Channel {channel.mention} Deleted by {entry.user.mention}", color=0xc283fe)
                if isinstance(channel, discord.VoiceChannel):
                    em = discord.Embed(title="Voice Channel Deleted", description=f"Voice Channel {channel.mention} Deleted by {entry.user.mention}", color=0xc283fe)
                if isinstance(channel, discord.CategoryChannel):
                    em = discord.Embed(title="Category Deleted", description=f"Category Channel {channel.mention} Deleted by {entry.user.mention}", color=0xc283fe)
                if isinstance(channel, discord.StageChannel):
                    em = discord.Embed(title="Stage Channel Deleted", description=f"Stage Channel {channel.mention} Deleted by {entry.user.mention}", color=0xc283fe)
                em.add_field(name="Name", value=f"{channel.name}")
                em.add_field(name="Position", value=channel.position + 1)
                overwrite = channel.overwrites_for(guild.default_role)
                em.add_field(name="Permissions synced?", value=f'{"Yes" if channel.permissions_synced else "No"}')
                if isinstance(channel, discord.VoiceChannel) or isinstance(channel, discord.StageChannel):
                    em.add_field(name="Bitrate", value=f"{channel.bitrate/1000} kbps")
                if channel.category:
                    em.add_field(name="Category", value=f"{channel.category.name} - [{channel.category_id}")
                if entry.reason:
                    em.add_field(name="Reason:", value=entry.reason)
                em.set_author(name=f"{str(entry.user)}", icon_url=entry.user.display_avatar.url)
                em.set_footer(text="Deleted", icon_url=guild.me.display_avatar.url)
                em.timestamp = datetime.datetime.utcnow()
                em.set_thumbnail(url=entry.user.display_avatar.url)
                if len(em.fields) > 0:
                    await c.send(embed=em)
    
    @commands.Cog.listener()
    async def on_guild_channel_update(self, before: discord.abc.GuildChannel,
                                   after: discord.abc.GuildChannel) -> None:
        await self.bot.wait_until_ready()
        guild = after.guild
        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        query = "SELECT * FROM  logs WHERE guild_id = ?"
        val = (guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            log_db = cursor.fetchone()
        db.commit()
        cursor.close()
        db.close()
        if log_db is None:
            return
        if log_db['channel'] is None:
            return
        async for entry in guild.audit_logs(limit=1,
                                            after=datetime.datetime.now() -
                                            datetime.timedelta(minutes=2),
                                            action=discord.AuditLogAction.channel_update):
            if log_db['channel'] is not None:
                m = entry.user
                if not m.guild:
                    return
                c = discord.utils.get(guild.channels, id=log_db['channel'])
                if c is None:
                    return
                if isinstance(after, discord.TextChannel):
                    em = discord.Embed(title="Text Channel Updated", description=f"Text Channel {after.mention} Updated by {entry.user.mention}", color=0xc283fe)
                if isinstance(after, discord.VoiceChannel):
                    em = discord.Embed(title="Voice Channel Updated", description=f"Voice Channel {after.mention} Updated by {entry.user.mention}", color=0xc283fe)
                if isinstance(after, discord.CategoryChannel):
                    em = discord.Embed(title="Category Updated", description=f"Category Channel {after.mention} Updated by {entry.user.mention}", color=0xc283fe)
                if isinstance(after, discord.StageChannel):
                    em = discord.Embed(title="Stage Channel Updated", description=f"Stage Channel {after.mention} Updated by {entry.user.mention}", color=0xc283fe)
                if before.name != after.name:
                    em.add_field(name="Name changed", value=f"`{before.name}` to `{after.name}`")
                if isinstance(after, discord.TextChannel) and isinstance(before, discord.TextChannel):
                    if before.topic != after.topic:
                        em.add_field(name="Channel's topic updated", value=f"`{before.topic}` to `{after.topic}`")
                    if before.slowmode_delay != after.slowmode_delay:
                        em.add_field(name="Slowmode delay updated", value=f"`{before.slowmode_delay} Seconds` to `{after.slowmode_delay} Seconds`")
                    if before.nsfw != after.nsfw:
                        em.add_field(name="NSFW State updated", value=f'{"Yes to No" if before.nsfw else "No to Yes"}')
                if isinstance(after, discord.VoiceChannel) and isinstance(before, discord.VoiceChannel):
                    if before.slowmode_delay != after.slowmode_delay:
                        em.add_field(name="Bitrate updated", value=f"`{before.bitrate/1000} kbps` to `{after.bitrate/1000} kbps`")
                    if before.user_limit != after.user_limit:
                        em.add_field(name="User Limit updated", value=f"`{before.user_limit} users` to `{after.user_limit} users`")
                if entry.reason:
                    em.add_field(name="Reason:", value=entry.reason)
                em.set_author(name=f"{str(entry.user)}", icon_url=entry.user.display_avatar.url)
                em.set_footer(text="Updated", icon_url=guild.me.display_avatar.url)
                em.timestamp = datetime.datetime.utcnow()
                em.set_thumbnail(url=entry.user.display_avatar.url)
                if len(em.fields) > 0:
                    await c.send(embed=em)

    @commands.Cog.listener()
    async def on_guild_update(self, before: discord.Guild,
                              after: discord.Guild) -> None:
        await self.bot.wait_until_ready()
        guild = after
        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        query = "SELECT * FROM  logs WHERE guild_id = ?"
        val = (guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            log_db = cursor.fetchone()
        db.commit()
        cursor.close()
        db.close()
        if log_db is None:
            return
        async for entry in after.audit_logs(
                limit=1,
                after=datetime.datetime.now() - datetime.timedelta(minutes=2),
                action=discord.AuditLogAction.guild_update):
            if log_db['server'] is not None:
                m = entry.user
                if not m.guild:
                    return
                c = discord.utils.get(guild.channels, id=log_db['server'])
                if c is None:
                    return
                em = discord.Embed(title="Server Updated", description=f"Server Updated by {entry.user.mention}", color=0xc283fe)
                if before.name != after.name:
                    em.add_field(name="Server Name changed", value=f"`{before.name}` to `{after.name}`")
                if before.icon != after.icon:
                    if before.icon is None:
                      d = f"None to [New Icon]({after.icon.url})"
                    elif after.icon is None:
                      d = f"[Old Icon]({before.icon.url}) to None"
                    else:
                      d = f"[Old Icon]({before.icon.url}) to [New Icon]({after.icon.url})"
                    em.add_field(name="Guild icon changed", value=d)
                if before.banner != after.banner:
                    if before.banner is None:
                      d = f"None to [New Banner]({after.banner.url})"
                    elif after.icon is None:
                      d = f"[Old Banner]({before.banner.url}) to None"
                    else:
                      d = f"[Old Banner]({before.banner.url}) to [New Banner]({after.banner.url})"
                    em.add_field(name="Guild Banner changed", value=d)
                if before.owner_id != after.owner_id:
                    em.add_field(name="Ownership Transfered", value=f"From: {before.owner.mention} - [{before.owner_id}\nTo: {after.owner.mention} - [{after.owner_id}]")
                if 'VANITY_URL' in before.features and 'VANITY_URL' in after.verification_level:
                    bvanity = await before.vanity_invite()
                    avanity = await after.vanity_invite()
                    bvanity = str(bvanity).replace("https://discord.gg/", "")
                    avanity = str(avanity).replace("https://discord.gg/", "")
                    if bvanity != avanity:
                        em.add_field(name="Server Vanity Changed", value=f"`{bvanity}` to `{avanity}`")
                if before.description != after.description:
                    em.add_field(name="Server's Description Updated", value=f"`{str(before.description)}` to `{str(after.description)}`")
                if before.verification_level != after.verification_level:
                    em.add_field(name="Server Verification Updated", value=f"`{str(before.verification_level)}` to `{str(after.verification_level)}`")
                if before.features != after.features:
                    afeat = ['VIP_REGIONS','VANITY_URL','INVITE_SPLASH','VERIFIED','PARTNERED','MORE_EMOJI','DISCOVERABLE','FEATURABLE','COMMUNITY','COMMERCE','PUBLIC','NEWS','BANNER','ANIMATED_ICON','PUBLIC_DISABLED','WELCOME_SCREEN_ENABLED','MEMBER_VERIFICATION_GATE_ENABLED','PREVIEW_ENABLED']
                    fadd = ""
                    fremoved = ""
                    for i in afeat:
                        if i in before.features and i not in after.features:
                            fremoved += f"{i.capitalize()}, "
                        if i not in before.features and i in after.features:
                            fadd += f"{i.capitalize()}, "
                    if len(fadd) > 0:
                        em.add_field(name="Features Added", value=fadd[:-2])
                    if len(fremoved) > 0:
                        em.add_field(name="Features Removed", value=fremoved[:-2])
                if before.system_channel != after.system_channel:
                    if before.system_channel is None:
                        bmen = "None"
                    else:
                        bmen = before.system_channel.mention
                    if after.system_channel is None:
                        amen = "None"
                    else:
                        amen = after.system_channel.mention                    
                    em.add_field(name="Server's System Channel Updated", value=f"{bmen} to {amen}")
                if before.rules_channel != after.rules_channel:
                    if before.rules_channel is None:
                        bmen = "None"
                    else:
                        bmen = before.rules_channel.mention
                    if after.rules_channel is None:
                        amen = "None"
                    else:
                        amen = after.rules_channel.mention       
                    em.add_field(name="Server's Rules Channel Updated", value=f"{bmen} to {amen}")
                if before.afk_channel != after.afk_channel:
                    if before.afk_channel is None:
                        bmen = "None"
                    else:
                        bmen = before.afk_channel.mention
                    if after.afk_channel is None:
                        amen = "None"
                    else:
                        amen = after.afk_channel.mention       
                    em.add_field(name="Afk Channel Updated", value=f"{bmen} to {amen}")
                if before.afk_timeout != after.afk_timeout:
                    em.add_field(name="Afk Timeout Updated", value=f"`{int(before.afk_timeout)} Minutes` to `{int(after.afk_timeout)} Minutes`")
                if entry.reason:
                    em.add_field(name="Reason:", value=entry.reason)
                em.set_author(name=f"{str(entry.user)}", icon_url=entry.user.display_avatar.url)
                em.set_footer(text="Updated", icon_url=guild.me.display_avatar.url)
                em.timestamp = datetime.datetime.utcnow()
                em.set_thumbnail(url=entry.user.display_avatar.url)
                if len(em.fields) > 0:
                    await c.send(embed=em)

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after:discord.Message):
        await self.bot.wait_until_ready()
        if before.author.bot:
            return
        guild = after.guild
        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        query = "SELECT * FROM  logs WHERE guild_id = ?"
        val = (guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            log_db = cursor.fetchone()
        db.commit()
        cursor.close()
        db.close()
        if log_db is None:
            return
        if before.content == after.content:
            return
        if log_db['message'] is not None:
            c = discord.utils.get(guild.channels, id=log_db['message'])
            if c is None:
                return
            em = discord.Embed(description=f":scroll: Message sent by {after.author.mention} edited in {after.channel.mention} [Jump to message]({after.jump_url})", color=0xc283fe)
            em.add_field(name="Before", value=f"```{before.content}```", inline=False)
            em.add_field(name="After", value=f"```{after.content}```", inline=False)
            em.set_author(name=f"{str(after.author)}", icon_url=after.author.display_avatar.url)
            em.set_footer(text="Edited", icon_url=guild.me.display_avatar.url)
            em.timestamp = datetime.datetime.utcnow()
            if len(em.fields) > 0:
                await c.send(embed=em)

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        await self.bot.wait_until_ready()
        guild = message.guild
        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        query = "SELECT * FROM  logs WHERE guild_id = ?"
        val = (guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            log_db = cursor.fetchone()
        db.commit()
        cursor.close()
        db.close()
        if log_db is None:
            return
        if log_db['message'] is None:
            return
        if message.author.bot:
            return
        async for entry in message.guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 1), action=discord.AuditLogAction.message_delete):
            if log_db['message'] is not None:
                c = discord.utils.get(guild.channels, id=log_db['message'])
                
                if c is None:
                    return
                em = discord.Embed(description=f":put_litter_in_its_place: Message sent by {message.author.mention} deleted in {message.channel.mention}", color=0xc283fe)
                url = None
                for x in message.attachments:
                    url = x.url
                if message.content == "":
                    content = "***Content Unavailable***"
                else:
                    content = message.content
                em.add_field(name="__Content__:",
                                  value=f"{content}",
                                  inline=False)
                x = datetime.datetime.now() - datetime.timedelta(seconds=5)
                if entry.user is not None and entry.target.id == message.author.id and x.timestamp() <= entry.created_at.timestamp():
                    em.add_field(name="**Deleted By:**",
                                    value=f"{entry.user.mention} (ID: {entry.user.id})")
                if url is not None:
                    if url.startswith("http") or url.startswith("http"):
                        em.set_image(url=url)
                em.set_author(name=f"{str(message.author)}", icon_url=message.author.display_avatar.url)
                em.set_footer(text="Deleted", icon_url=guild.me.display_avatar.url)
                em.timestamp = datetime.datetime.utcnow()
                if len(em.fields) > 0:
                    await c.send(embed=em)

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages: discord.Message):
        await self.bot.wait_until_ready()
        guild = messages[0].guild
        if not guild:
            return
        if not guild.me.guild_permissions.view_audit_log:
            return
        query = "SELECT * FROM  logs WHERE guild_id = ?"
        val = (guild.id,)
        db = sqlite3.connect('./database.sqlite3')
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        cursor.execute(query, val)
        log_db = cursor.fetchone()
        db.commit()
        cursor.close()
        db.close()
        if log_db is None:
            return
        if log_db['message'] is None:
            return
        async for entry in guild.audit_logs(limit=1, after=datetime.datetime.now() - datetime.timedelta(minutes = 1), action=discord.AuditLogAction.message_bulk_delete):
            if log_db is not None and log_db['message'] is not None:
                c = discord.utils.get(guild.channels, id=log_db['message'])
                if c is None:
                    return
                em = discord.Embed(description=f":put_litter_in_its_place: {len(messages)} Messages were deleted in {messages[0].channel.mention}", color=0xc283fe)
                x = datetime.datetime.now() - datetime.timedelta(seconds=5)
                em.add_field(name="**Deleted By:**",
                                    value=f"{entry.user.mention} (ID: {entry.user.id})")
                em.set_author(name=f"{str(self.bot.user)}", icon_url=self.bot.user.display_avatar.url)
                em.set_footer(text="Deleted", icon_url=guild.me.display_avatar.url)
                em.timestamp = datetime.datetime.utcnow()
                transcript = None
                #transcript = await chat_exporter.raw_export(messages[0].channel, messages=messages)
                if transcript is None:
                    file = None
                else:
                    file = discord.File(
                        io.BytesIO(transcript.encode()),
                        filename=f"transcript-{messages[0].channel.id}.html",
                    )
                #if len(em.fields) > 0:
                 #   msg = await c.send(embed=em, file=file)
                  #  if transcript is not None:
                   #     link = await chat_exporter.link(msg)
                    #    em.add_field(name="Direct Link to transcript:", value=f"[Transcript]({link})")
                     #   await msg.edit(embed=em)

async def setup(bot):
	await bot.add_cog(logging(bot))
