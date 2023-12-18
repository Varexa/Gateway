import discord
from discord import app_commands
from discord.ext import commands
import sqlite3
import datetime
from paginators import PaginationView, PaginatorView
from hpag import HPaginationView
import random
from basic_help import dr, cogs
from typing import Optional, List

class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Get Help with the bot's commands or modules")
    @app_commands.describe(
        command="Choose the command or module you need help with"
    )
    async def help(self, interaction: discord.Interaction, command: Optional[str]):
        ctx = await self.bot.get_context(interaction, cls=commands.Context)
        if command is not None:
            cmd = self.bot.get_command(command)
            cog = command
            cog = self.bot.get_cog(cog.lower())
            if cog is not None:
                if cog.qualified_name.capitalize() in dr:
                    if cog.qualified_name == "nsfw":
                        if not ctx.channel.is_nsfw():
                            return
                    if cog.qualified_name == "extra":
                        return await self.extra(ctx=ctx)
                    command = cog.qualified_name
                    ls = []
                    for j in cog.walk_commands():
                        ls.append(j.qualified_name)
                    with sqlite3.connect('database.sqlite3') as db:
                        db.row_factory = sqlite3.Row
                        cursor = db.cursor()
                        cursor.execute(f"SELECT * FROM prefixes WHERE guild_id = {ctx.guild.id}")
                        res = cursor.fetchone()
                    prefix = "-"
                    xd = discord.utils.get(self.bot.users, id=978930369392951366)
                    anay = str(xd)
                    pfp = xd.display_avatar.url
                    ls1, hey = [], []
                    for i in sorted(ls):
                        cmd = self.bot.get_command(i)
                        if cmd is not None:
                            if cmd.description is None:
                                cmd.description = "No Description"
                        hey.append(f"`{prefix}{i}`\n{cmd.description}\n\n")
                    for i in range(0, len(hey), 10):
                        ls1.append(hey[i: i + 10])
                    em_list = []
                    no = 1
                    lss = dr[command.capitalize()]
                    for k in ls1:
                        listem = discord.Embed(title=f"{lss[0]} {command.capitalize()} Commands", colour=0xc283fe,
                                                description=f"<...> Duty | [...] Optional\n\n{''.join(k)}")
                        listem.set_author(name=f"{str(ctx.author)}", icon_url=ctx.author.display_avatar.url)
                        listem.set_footer(text=f"Made by stars.gg" ,  icon_url=pfp)
                        em_list.append(listem)
                        no+=1
                    page = PaginationView(embed_list=em_list, ctx=ctx)
                    await page.start(ctx)
                    return
            if isinstance(cmd, discord.ext.commands.core.Group):
                command = cmd.name
                ls = []
                for j in cmd.walk_commands():
                    ls.append(j.qualified_name)
                with sqlite3.connect('database.sqlite3') as db:
                    db.row_factory = sqlite3.Row
                    cursor = db.cursor()
                    cursor.execute(f"SELECT * FROM prefixes WHERE guild_id = {ctx.guild.id}")
                    res = cursor.fetchone()
                prefix = "-"
                xd = discord.utils.get(self.bot.users, id=978930369392951366)
                anay = str(xd)
                ls1, hey = [], []
                for i in sorted(ls):
                    cmd = self.bot.get_command(i)
                    if cmd is not None:
                        if cmd.description is None:
                            cmd.description = "No Description"
                    hey.append(f"`{prefix}{i}`\n{cmd.description}\n\n")
                for i in range(0, len(hey), 10):
                    ls1.append(hey[i: i + 10])
                em_list = []
                no = 1
                for k in ls1:
                    listem = discord.Embed(title=f"{command.capitalize()} Commands", colour=0xc283fe,
                                            description=f"<...> Duty | [...] Optional\n\n{''.join(k)}")
                    listem.set_author(name=f"{str(ctx.author)}")
                    listem.set_footer(text=f"Made by stars.gg")
                    em_list.append(listem)
                    no+=1
                page = PaginationView(embed_list=em_list, ctx=ctx)
                await page.start(ctx)
                return
            if cmd.cog_name == "nsfw":
                if not ctx.channel.is_nsfw():
                    return
            with sqlite3.connect('database.sqlite3') as db:
                db.row_factory = sqlite3.Row
                cursor = db.cursor()
                cursor.execute(f"SELECT * FROM prefixes WHERE guild_id = {ctx.guild.id}")
                res = cursor.fetchone()
            prefix = "-"
            em = discord.Embed(description="> ```[] is Optional argument```\n> ```<> is Required argument```", color=0xc283fe)
            if cmd.cog_name:
                filter_commands(self.bot.walk_commands(), sort=True)
            if needle in command.qualified_name
        ][:25]
        
    @commands.command(
        name="help", aliases=["h"]
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def _help(self, ctx, *, command: str=None):
        if command is not None:
            cmd = self.bot.get_command(command)
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
                "selfrole": "selfroles",
                "rr": "selfroles",
                "reactionrole": "selfroles"}
            cog = command
            for i in dc:
                if command.lower() == i:
                    cog = dc[i]
            cog = self.bot.get_cog(cog.lower())
            if cmd is None and cog is None:
                return await ctx.reply(embed=discord.Embed(description=f"No command or module found named `{command}`", color=0xff0000), mention_author=False)
            if cog is not None:
                if cog.qualified_name.capitalize() in dr:
                    if cog.qualified_name == "nsfw":
                        if not ctx.channel.is_nsfw():
                            return
                    if cog.qualified_name == "extra":
                        return await self.extra(ctx=ctx)
                    command = cog.qualified_name
                    ls = []
                    for j in cog.walk_commands():
                        ls.append(j.qualified_name)
                    prefix = ctx.prefix
                    if prefix == f"<@{self.bot.user.id}> ":
                        prefix = f"@{str(self.bot.user)} "
                    pfp = "https://cdn.discordapp.com/avatars/978930369392951366/0e55b0eed54d1ed038241f5106aa8999.png?size=1024"
                    ls1, hey = [], []
                    for i in sorted(ls):
                        cmd = self.bot.get_command(i)
                        if cmd is not None:
                            if cmd.description is None:
                                cmd.description = "No Description"
                        hey.append(f"`{prefix}{i}`\n{cmd.description}\n\n")
                    for i in range(0, len(hey), 10):
                        ls1.append(hey[i: i + 10])
                    em_list = []
                    no = 1
                    lss = dr[command.capitalize()]
                    for k in ls1:
                        listem = discord.Embed(title=f"{lss[0]} {command.capitalize()} Commands", colour=0xc283fe,
                                                description=f"<...> Duty | [...] Optional\n\n{''.join(k)}")
                        listem.set_author(name=f"{str(ctx.author)}")
                        listem.set_footer(text=f"Made by stars.gg" ,  icon_url="https://cdn.discordapp.com/avatars/978930369392951366/0e55b0eed54d1ed038241f5106aa8999.png?size=1024")
                        em_list.append(listem)
                        no+=1
                    page = PaginationView(embed_list=em_list, ctx=ctx)
                    await page.start(ctx)
                    return
            if isinstance(cmd, discord.ext.commands.core.Group):
                command = cmd.name
                ls = []
                for j in cmd.walk_commands():
                    ls.append(j.qualified_name)
                prefix = ctx.prefix
                if prefix == f"<@{self.bot.user.id}> ":
                    prefix = f"@{str(self.bot.user)} "
                ls1, hey = [], []
                for i in sorted(ls):
                    cmd = self.bot.get_command(i)
                    if cmd is not None:
                        if cmd.description is None:
                            cmd.description = "No Description"
                    hey.append(f"`{prefix}{i}`\n{cmd.description}\n\n")
                for i in range(0, len(hey), 10):
                    ls1.append(hey[i: i + 10])
                em_list = []
                no = 1
                for k in ls1:
                    listem = discord.Embed(title=f"{command.capitalize()} Commands", colour=0xc283fe,
                                            description=f"<...> Duty | [...] Optional\n\n{''.join(k)}")
                    listem.set_author(name=f"{str(ctx.author)}")
                    listem.set_footer(text=f"Made by stars.gg")
                    em_list.append(listem)
                    no+=1
                page = PaginationView(embed_list=em_list, ctx=ctx)
                await page.start(ctx)
                return
            if cmd.cog_name == "nsfw":
                if not ctx.channel.is_nsfw():
                    return
            em = discord.Embed(description="> ```[] is Optional argument```\n> ```<> is Required argument```", color=0xc283fe)
            if cmd.cog_name:
                em.set_author(name=cmd.cog_name.capitalize(), icon_url=self.bot.user.avatar.url)
            else:
                em.set_author(name=f"{self.bot.user.name}", icon_url=self.bot.user.avatar.url)
            if cmd.description:
                em.add_field(name="Description", value=cmd.description, inline=False)
            else:
                em.add_field(name="Description", value="No description provided", inline=False)
            if cmd.aliases: 
                em.add_field(name="Aliases", value=f'{" | ".join(cmd.aliases)}', inline=False)
            else:
                em.add_field(name="Aliases", value="No Aliases", inline=False)
            em.add_field(name="Usage", value=f"> {ctx.prefix}{cmd.qualified_name} {cmd.signature}", inline=False)
            return await ctx.reply(embed=em, mention_author=False)
        with sqlite3.connect('database.sqlite3') as db:
          db.row_factory = sqlite3.Row
          cursor = db.cursor()
          cursor.execute(f"SELECT * FROM prefixes WHERE guild_id = {ctx.guild.id}")
          res = cursor.fetchone()
          prefix = "-"
          v = ""
          c = ""
          s = ""
          index = round(len(list(cogs)) / 2)
          first_half = list(cogs)[:index]
          second_half = list(cogs)[index:]
          for i in cogs:
              ls = dr[i.capitalize()]
              v+=f"{ls[0]} {i.capitalize()}\n"
          for i in first_half:
              ls = dr[i.capitalize()]
              c+=f"> **[{ls[0]} {i.capitalize()}](https://gatewaybot.xyz)**\n"
          for i in second_half:
              ls = dr[i.capitalize()]
              s+=f"> **[{ls[0]} {i.capitalize()}](https://gatewaybot.xyz)**\n"
        help = discord.Embed(description=f"`{prefix}help [command/category]` - View specific command/category.\nClick on the dropdown for more information",
                                    colour=0xc283fe)
        help.set_author(name=f"{str(self.bot.user.name)} HelpDesk", icon_url=self.bot.user.display_avatar.url)
        help.add_field(name=f"<:8319folder:1154676193354862633> Categories", value=c, inline=True)
        help.add_field(name=f"** **", value=s, inline=True)
        help.add_field(name=f"<:link:1085613998973657118> Links", value=f'> **[Website](https://gatewaybot.xyz) | [Support Server](https://gatewaybot.xyz/discord) | [Invite Me](https://gatewaybot.xyz/invite) | [Documentation](https://docs.gatewaybot.xyz)**', inline=False)
        help.set_footer(text=f"Thanks for choosing Gateway • Made by stars.gg", icon_url=ctx.author.display_avatar.url)
        em_list = []
        em_list.append(help)
        
        for i in cogs:
                if i in cogs:
                    pass
                else:
                    continue
                x = self.bot.get_cog(i.lower())
                ls = []
                for j in x.walk_commands():
                    ls.append(j.qualified_name)
                ok = ""
                for k in sorted(ls):
                    ok+= f"`{k}`, "
                lss = dr[i.capitalize()]
                help_ = discord.Embed(title=f"{lss[0]} {i.capitalize()} Commands", colour=0xc283fe, description=ok[:-2])
                help.set_footer(text=f"Thanks for choosing Gateway • Made by stars.gg", icon_url=ctx.author.display_avatar.url)
                em_list.append(help_)

        x = round(random.random()*100000)
        with sqlite3.connect('database.sqlite3') as db:
           db.row_factory = sqlite3.Row
           cursor = db.cursor()
           sql = f"INSERT INTO help(main, 'no') VALUES(?, ?)"
           val = (x, 0)
           cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        count = 0
        for i in dr:
            count +=1
            dr[i].append(count)
        page = HPaginationView(embed_list=em_list, dr=dr, i=x, ctx=ctx)
        page.add_item(discord.ui.Button(label="Get Gateway", url=discord.utils.oauth_url(self.bot.user.id)))
        page.add_item(discord.ui.Button(label="Support Server", url="https://gatewaybot.xyz/discord"))
        page.add_item(discord.ui.Button(label="Vote", url="https://top.gg/bot/880765863953858601/vote"))
        await page.start(ctx)


    async def extra(self, ctx):
        prefix = ctx.prefix
        if prefix == f"<@{self.bot.user.id}> ":
            prefix = f"@{str(self.bot.user)} "
        anay = discord.utils.get(self.bot.users, id=978930369392951366)
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
        listem.set_author(name=f"{str(ctx.author)}")
        listem.set_footer(text=f"Made by stars.gg")
        listem1 = discord.Embed(colour=0xc283fe,
                                     description=f"<...> Duty | [...] Optional\n\n" 
                                                  f"`{prefix}nightmode`\n" 
                                                  f"Shows The help menu for nightmode\n\n" 
                                                  f"`{prefix}nightmode enable <perm>`\n" 
                                                  f"Take perms from every role that is below the bot\n\n"
                                                  f"`{prefix}nightmode disable`\n"
                                                  f"Give the role their permissions back\n\n")
        listem1.set_author(name=f"{str(ctx.author)}")
        listem1.set_footer(text=f"Made by stars.gg")
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
        setupem.set_author(name=f"{str(ctx.author)}")
        setupem.set_footer(text=f"Made by stars.gg")
        query = "SELECT * FROM  roles WHERE guild_id = ?"
        val = (ctx.guild.id,)
        with sqlite3.connect('./database.sqlite3') as db:
          db.row_factory = sqlite3.Row
          cursor = db.cursor()
          cursor.execute(query, val)
          setup_db = cursor.fetchone()
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
                        "invc": "https://docs.gatewaybot.xyz/features/#in-vc-roles",
              "extra": "https://docs.gatewaybot.xyz/features/#extra",
              "setup": "https://docs.gatewaybot.xyz/features/#extra",
              "team": "https://docs.gatewaybot.xyz/team/",
              "cmds": "https://docs.gatewaybot.xyz/commands/",
              "cmd": "https://docs.gatewaybot.xyz/commands/",
              "commands": "https://docs.gatewaybot.xyz/commands/",
              "command": "https://docs.gatewaybot.xyz/commands/",
              "faq": "https://docs.gatewaybot.xyz/faqs/"}
        des = ""
        if module is not None:
            if module.lower() not in ls:
                des = f"> [Click To read the doumentations of {self.bot.user.name}](https://docs.gatewaybot.xyz)\n"
            else:
                des = f"> [Click To read the doumentations of {module.capitalize()}]({ls[module.lower()]})\n"
        else:
            des = f"> [Click To read the doumentations of {self.bot.user.name}](https://docs.gatewaybot.xyz)\n"
        em = discord.Embed(description=des, color=0xc283fe)
        await ctx.reply(embed=em, mention_author=False)

async def setup(bot):
    await bot.add_cog(help(bot))
