import discord
import datetime
from discord.ext import commands, tasks
from ast import literal_eval
import sqlite3
import io
from paginators import PaginationView, PaginatorView
from cogs.premium import check_upgraded

class enablemenu(discord.ui.Select):
    def __init__(self, ctx: commands.Context, role: discord.Role):
        options = []
        query = "SELECT * FROM  invc WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            log_db = cursor.fetchone()
        x = literal_eval(log_db['vc'])
        c = 0
        for i in x:
            if x[i] is None:
                xx = discord.utils.get(ctx.guild.channels, id=i)
                options.append(discord.SelectOption(label=f"{xx.name}", value=i))
                c = c+1
        super().__init__(placeholder="Select voice channels",
            min_values=1,
            max_values=c,
            options=options,
        )
        self.ctx = ctx
        self.role = role

    async def callback(self, interaction: discord.Interaction):
        ctx = self.ctx
        role = self.role
        query = "SELECT * FROM  invc WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            log_db = cursor.fetchone()
        x = literal_eval(log_db['vc'])
        des= ""
        for i in self.values:
            if x[int(i)] is None:
                x[int(i)] = role.id
                xx = discord.utils.get(ctx.guild.channels, id=int(i))
                des += f"{xx.mention}, "
        sql = (f"UPDATE invc SET 'vc' = ? WHERE guild_id = ?")
        val = (f"{x}", ctx.guild.id)
        cursor.execute(sql, val)
        db.commit()
        em = discord.Embed(description=f"{role.mention} is now invc role for {des[:-2]}", color=0xc283fe)
        await self.ctx.reply(embed=em)
        await interaction.message.delete()


class enableview(discord.ui.View):
    def __init__(self, ctx: commands.Context, role: discord.Role):
        super().__init__(timeout=60)
        self.add_item(enablemenu(ctx, role))
        self.ctx = ctx
        self.role = role
    
    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and interaction.user.id not in  [978930369392951366, 979353019235840000]:
            await interaction.response.send_message(f"Um, Looks like you are not the author of the command...", ephemeral=True)
            return False
        return True
    
    @discord.ui.button(label="All Voice Channels", style=discord.ButtonStyle.blurple)
    async def _enable(self, interaction, button):
        ctx = self.ctx
        role = self.role
        query = "SELECT * FROM  invc WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            log_db = cursor.fetchone()
        x = literal_eval(log_db['vc'])
        des= ""
        for i in x:
                x[i] = role.id
                xx = discord.utils.get(ctx.guild.channels, id=i)
                des += f"{xx.mention}, "
        sql = (f"UPDATE invc SET 'vc' = ? WHERE guild_id = ?")
        val = (f"{x}", ctx.guild.id)
        cursor.execute(sql, val)
        db.commit()
        em = discord.Embed(description=f"{role.mention} is now invc role for {des[:-2]}", color=0xc283fe)
        await self.ctx.reply(embed=em)
        await interaction.message.delete()

class disablemenu(discord.ui.Select):
    def __init__(self, ctx: commands.Context, role: discord.Role=None):
        options = []
        query = "SELECT * FROM  invc WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            log_db = cursor.fetchone()
        x = literal_eval(log_db['vc'])
        c = 0
        for i in x:
            if x[i] is not None:
                if role is None:
                    xx = discord.utils.get(ctx.guild.channels, id=i)
                    options.append(discord.SelectOption(label=f"{xx.name}", value=i))
                    c +=1
                else:
                    if x[i] == role.id:
                        xx = discord.utils.get(ctx.guild.channels, id=i)
                        options.append(discord.SelectOption(label=f"{xx.name}", value=i))
                        c +=1
        super().__init__(placeholder="Select voice channels",
            min_values=1,
            max_values=c,
            options=options,
        )
        self.ctx = ctx
        self.role = role

    async def callback(self, interaction: discord.Interaction):
        ctx = self.ctx
        role = self.role
        query = "SELECT * FROM  invc WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            log_db = cursor.fetchone()
        x = literal_eval(log_db['vc'])
        des= ""
        for i in self.values:
            if x[int(i)] is not None:
                if role is None:
                    x[int(i)] = None
                    xx = discord.utils.get(ctx.guild.channels, id=int(i))
                    des += f"{xx.mention}, "
                else:
                    if x[int(i)] == role.id:
                        x[int(i)] = None
                        xx = discord.utils.get(ctx.guild.channels, id=int(i))
                        des += f"{xx.mention}, "
        sql = (f"UPDATE invc SET 'vc' = ? WHERE guild_id = ?")
        val = (f"{x}", ctx.guild.id)
        cursor.execute(sql, val)
        db.commit()
        if role is not None:
            em = discord.Embed(description=f"{role.mention} is now removed from invc role for {des[:-2]}", color=0xc283fe)
        else:
            em = discord.Embed(description=f"All invc roles are now removed from {des[:-2]}", color=0xc283fe)
        await self.ctx.reply(embed=em)
        await interaction.message.delete()

class disableview(discord.ui.View):
    def __init__(self, ctx: commands.Context, role: discord.Role=None):
        super().__init__()
        self.add_item(disablemenu(ctx, role))
        self.ctx = ctx
        self.role = role

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and interaction.user.id not in  [978930369392951366, 979353019235840000]:
            await interaction.response.send_message(f"Um, Looks like you are not the author of the command...", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="All Voice Channels", style=discord.ButtonStyle.blurple)
    async def _disable(self, interaction, button):
        ctx = self.ctx
        role = self.role
        query = "SELECT * FROM  invc WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            log_db = cursor.fetchone()
        x = literal_eval(log_db['vc'])
        des= ""
        for i in x:
            if x[i] is not None:
                if role is None:
                    x[i] = None
                    xx = discord.utils.get(ctx.guild.channels, id=i)
                    des += f"{xx.mention}, "
                else:
                    if x[i] == role.id:
                        x[i] = None
                        xx = discord.utils.get(ctx.guild.channels, id=i)
                        des += f"{xx.mention}, "
        sql = (f"UPDATE invc SET 'vc' = ? WHERE guild_id = ?")
        val = (f"{x}", ctx.guild.id)
        cursor.execute(sql, val)
        db.commit()
        if role is not None:
            em = discord.Embed(description=f"{role.mention} is now removed from invc role for {des[:-2]}", color=0xc283fe)
        else:
            em = discord.Embed(description=f"All invc roles are now removed in the server", color=0xc283fe)
        await self.ctx.reply(embed=em)
        await interaction.message.delete()

class invc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(
        name="invc",
        invoke_without_command=True, description="Shows the invc's help menu"
    )
    async def invc(self, ctx):
        prefix = ctx.prefix
        if prefix == f"<@{self.bot.user.id}> ":
            prefix = f"@{str(self.bot.user)} "
        anay = discord.utils.get(self.bot.users, id=978930369392951366)
        ls = ["invc", "invc enable", "invc disable", "invc config"]
        des = ""
        for i in sorted(ls):
            cmd = self.bot.get_command(i)
            if cmd.description is None:
                cmd.description = "No Description"
            des += f"`{prefix}{i}`\n{cmd.description}\n\n"
        listem = discord.Embed(title=f"<:invc:1039145467331739661> Invc Role Commands", colour=0xc283fe,
                                     description=f"<...> Duty | [...] Optional\n\n{des}")
        listem.set_author(name=f"{str(ctx.author)}", icon_url=ctx.author.display_avatar.url)
        listem.set_footer(text=f"Made by stars.gg" ,  icon_url=anay.avatar.url)
        await ctx.send(embed=listem)
    
    @invc.command(name="config",description="Shows the current invc role settings")
    @commands.has_permissions(administrator=True)
    async def config(self, ctx):
        c = await check_upgraded(ctx.guild.id)
        if not c:
            em = discord.Embed(description=f"You just tried to execute a premium command but this guild is not upgarded\nYou can buy bot's premium from the link given below or by creating a ticket in the [Support Server](https://discord.gg/6Q9D7R8hYc)", color=0xc283fe).set_footer(text=f"{self.bot.user.name} Premium feature", icon_url=self.bot.user.avatar.url)
            v = discord.ui.View()
            v.add_item(discord.ui.Button(label="Patreon", url="https://www.patreon.com/gateway_bot"))
            v.add_item(discord.ui.Button(label="Support Server", url="https://discord.gg/6Q9D7R8hYc"))
            return await ctx.reply(embed=em, view=v)
        if ctx.author.id == ctx.guild.owner.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 979353019235840000]:
                em = discord.Embed(description=f"<:error:1153009680428318791>You must Have Higher Role than Bot To run This Command", color=0xff0000)
                return await ctx.send(embed=em)
        query = "SELECT * FROM  invc WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            log_db = cursor.fetchone()
        em = discord.Embed(title="Invc Role setting for the server", color=0xc283fe)
        x = literal_eval(log_db['vc'])
        c = 0
        for i in x:
            if x[i] is not None:
                cc = discord.utils.get(ctx.guild.channels, id=i)
                r = discord.utils.get(ctx.guild.roles, id=x[i])
                if r is None:
                    rr = "The role is deleted"
                else:
                    rr = r.mention
                em.add_field(name=f"{cc.name}:", value=f"{rr}", inline=True)
                c+=1
        if c==0:
            em.description = "No Invc Role is setup in this server"
        em.set_footer(text=f"Invc Role system", icon_url=self.bot.user.display_avatar.url)
        await ctx.reply(embed=em)

    @invc.command(name="enable", aliases=['on'], description="Enable the logs for the server")
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def enable(self, ctx, *, role: discord.Role):
        c = await check_upgraded(ctx.guild.id)
        if not c:
            em = discord.Embed(description=f"You just tried to execute a premium command but this guild is not upgarded\nYou can buy bot's premium from the link given below or by creating a ticket in the [Support Server](https://discord.gg/6Q9D7R8hYc)", color=0xc283fe).set_footer(text=f"{self.bot.user.name} Premium feature", icon_url=self.bot.user.avatar.url)
            v = discord.ui.View()
            v.add_item(discord.ui.Button(label="Patreon", url="https://www.patreon.com/gateway_bot"))
            v.add_item(discord.ui.Button(label="Support Server", url="https://discord.gg/6Q9D7R8hYc"))
            return await ctx.reply(embed=em, view=v)
        if role.is_bot_managed() or role.is_premium_subscriber():
            return await ctx.reply("It is a integrated role. Please provide a different role")
        if not role.is_assignable():
            return await ctx.reply("I cant assign this role to anyone so please check my permissions and position.")
        if role.permissions.administrator or role.permissions.manage_roles or role.permissions.ban_members or role.permissions.kick_members or role.permissions.manage_guild or role.permissions.manage_channels or role.permissions.mention_everyone or role.permissions.manage_webhooks:
            return await ctx.reply("The Role has dangerous permissions so it cant be used as a invc role.")
        if ctx.author.id == ctx.guild.owner.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 979353019235840000]:
                em = discord.Embed(description=f"<:error:1153009680428318791>You must Have Higher Role than Bot To run This Command", color=0xff0000)
                return await ctx.send(embed=em)
        query = "SELECT * FROM  invc WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            log_db = cursor.fetchone()
        ls = literal_eval(log_db['vc'])
        c = 0
        for i in ls:
            if ls[i] is None:
                c+=1
        if c == 0:
            return await ctx.reply(f"All Voice Channels have a invc role already enabled")
        view = enableview(ctx, role)
        em = discord.Embed(description=f"Which Voice channel should have {role.mention} as invc role?", color=0xc283fe)
        m = await ctx.reply(embed=em, view=view)
        await view.wait()
    
    @invc.command(name="disable", aliases=['off'], description="Disable the logs for the server")
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def disable(self, ctx, *, role: discord.Role=None):
        c = await check_upgraded(ctx.guild.id)
        if not c:
            em = discord.Embed(description=f"You just tried to execute a premium command but this guild is not upgarded\nYou can buy bot's premium from the link given below or by creating a ticket in the [Support Server](https://discord.gg/6Q9D7R8hYc)", color=0xc283fe).set_footer(text=f"{self.bot.user.name} Premium feature", icon_url=self.bot.user.avatar.url)
            v = discord.ui.View()
            v.add_item(discord.ui.Button(label="Patreon", url="https://www.patreon.com/gateway_bot"))
            v.add_item(discord.ui.Button(label="Support Server", url="https://discord.gg/6Q9D7R8hYc"))
            return await ctx.reply(embed=em, view=v)
        if role is not None:
            if role.is_bot_managed() or role.is_premium_subscriber():
                return await ctx.reply("It is a integrated role. Please provide a different role")
        if ctx.author.id == ctx.guild.owner.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [978930369392951366, 979353019235840000]:
                em = discord.Embed(description=f"<:error:1153009680428318791>You must Have Higher Role than Bot To run This Command", color=0xff0000)
                return await ctx.send(embed=em)
        query = "SELECT * FROM  invc WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            log_db = cursor.fetchone()
        ls = literal_eval(log_db['vc'])
        c = 0
        for i in ls:
            if ls[i] is not None:
                if role is not None:
                    if ls[i] == role.id:
                        c+=1
                else:
                    c+=1
        if c == 0:
            if role is not None:
                return await ctx.reply(embed=discord.Embed(description=f"{role.mention} is not invc role for any of the Voice Channel", color=0xc283fe))
            else:
                return await ctx.reply(f"Invc role system for All Voice Channels are already disabled")
        if role is not None:
            view = disableview(ctx, role)
        else:
            view = disableview(ctx)
        if role is not None:
            em = discord.Embed(description=f"Which Voice channel should not have {role.mention} as invc role?", color=0xc283fe)
        else:
            em = discord.Embed(description=f"Which Voice channel should not have any invc role?", color=0xc283fe)
        m = await ctx.reply(embed=em, view=view)
        await view.wait()
    

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel: discord.abc.GuildChannel) -> None:
        try:
            await self.bot.wait_until_ready()
            query = "SELECT * FROM  invc WHERE guild_id = ?"
            val = (channel.guild.id,)
            db = sqlite3.connect('./database.sqlite3') 
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            log_db = cursor.fetchone()
            ls = literal_eval(log_db['vc'])
            if isinstance(channel, discord.VoiceChannel):
                ls[channel.id] = None
            sql = (f"UPDATE invc SET 'vc' = ? WHERE guild_id = ?")
            val = (f"{ls}", channel.guild.id)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
        except:
            return

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel: discord.abc.GuildChannel) -> None:
        await self.bot.wait_until_ready()
        query = "SELECT * FROM  invc WHERE guild_id = ?"
        val = (channel.guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            log_db = cursor.fetchone()
        if log_db is None:
            return
        if log_db["vc"] is None:
            return
        ls = literal_eval(log_db['vc'])
        if isinstance(channel, discord.VoiceChannel):
            if channel.id in ls:
                del ls[channel.id]
        sql = (f"UPDATE invc SET 'vc' = ? WHERE guild_id = ?")
        val = (f"{ls}", channel.guild.id)
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role: discord.Role) -> None:
        await self.bot.wait_until_ready()
        query = "SELECT * FROM  invc WHERE guild_id = ?"
        val = (role.guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            log_db = cursor.fetchone()
        if log_db is None:
            return
        if log_db["vc"] is None:
            return
        ls = literal_eval(log_db['vc'])
        for i in ls:
            if ls[i] == role.id:
                ls[i] = None
        sql = (f"UPDATE invc SET 'vc' = ? WHERE guild_id = ?")
        val = (f"{ls}", role.guild.id)
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        await self.bot.wait_until_ready()
        c = await check_upgraded(member.guild.id)
        if not c:
            return
        guild = member.guild
        if not guild.me.guild_permissions.manage_roles:
          return
        query = "SELECT * FROM  invc WHERE guild_id = ?"
        val = (guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            log_db = cursor.fetchone()
        if log_db is None:
            return
        if log_db["vc"] is None:
            return
        ls = literal_eval(log_db['vc'])
        if before.channel:
            if before.channel.id in ls:
                r = discord.utils.get(guild.roles, id=ls[before.channel.id])
                if r is not None:
                  if r.position < guild.me.top_role.position:
                    await member.remove_roles(r, reason=f"{self.bot.user.name} | INVC ROLE")
        if after.channel:
            if after.channel.id in ls:
                r = discord.utils.get(guild.roles, id=ls[after.channel.id])
                if r is not None:
                  if r.position < guild.me.top_role.position:
                    await member.add_roles(r, reason=f"{self.bot.user.name} | INVC ROLE")
                

async def setup(bot):
	await bot.add_cog(invc(bot))
