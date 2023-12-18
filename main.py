import discord
from discord.ext import commands
import os
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
import wavelink
import sqlite3
import datetime
import asyncpg
import re
from ast import literal_eval
import botinfo
from cogs.premium import check_upgraded
import topgg
from wavelink.ext import spotify
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import asyncio
import aiohttp
import logging
from database import *
# logging.basicConfig(level=logging.DEBUG)
# log = logging.getLogger(__name__)

# async def on_request_end(
#     session: aiohttp.ClientSession,
#     trace_config_ctx,
#     params: aiohttp.TraceRequestEndParams,
# ) -> None:
#     if params.response.status >= 400:
#         log.warning(
#             'Request to %s failed with status code %s with method %s',
#             params.url,
#             params.response.status,
#             params.method,
#         )

# trace = aiohttp.TraceConfig()
# trace.on_request_end.append(on_request_end)

botinfo.starttime = datetime.datetime.utcnow()
check = False

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

async def add_count(ctx, user, guild, cmd_name):
    query = "SELECT * FROM  count WHERE xd = ?"
    val = (1,)
    with sqlite3.connect('./database.sqlite3') as db:
      db.row_factory = sqlite3.Row
      cursor = db.cursor()
      cursor.execute(query, val)
      user_columns = cursor.fetchone()
    if user_columns is None:
        c = {}
        c[user.id] = 1
        cc = {}
        cc[guild.id] = 1
        ccc = {}
        ccc[cmd_name] = 1
        sql = (f"INSERT INTO count(xd, 'user_count', 'guild_count', 'cmd_count') VALUES(?, ?, ?, ?)")
        val = (1, f"{c}", f"{cc}", f"{ccc}",)
        cursor.execute(sql, val)
    else:
        c = literal_eval(user_columns['user_count'])
        if user.id in c:
            c[user.id] = c[user.id] + 1
        else:
            c[user.id] = 1
        c = {k: v for k, v in reversed(sorted(c.items(), key=lambda item: item[1]))}
        sql = "UPDATE count SET 'user_count' = ? WHERE xd = ?"
        val = (f"{c}", 1,)
        cursor.execute(sql, val)
        cc = literal_eval(user_columns['guild_count'])
        if guild.id in cc:
            cc[guild.id] = cc[guild.id] + 1
        else:
            cc[guild.id] = 1
        cc = {k: v for k, v in reversed(sorted(cc.items(), key=lambda item: item[1]))}
        sql = "UPDATE count SET 'guild_count' = ? WHERE xd = ?"
        val = (f"{cc}", 1,)
        cursor.execute(sql, val)
        ccc = literal_eval(user_columns['cmd_count'])
        if cmd_name in ccc:
            ccc[cmd_name] = ccc[cmd_name] + 1
        else:
            ccc[cmd_name] = 1
        ccc = {k: v for k, v in reversed(sorted(ccc.items(), key=lambda item: item[1]))}
        sql = "UPDATE count SET 'cmd_count' = ? WHERE xd = ?"
        val = (f"{ccc}", 1,)
        cursor.execute(sql, val)
    db.commit()
    cursor.close()
    db.close()

async def get_prefix(message: discord.Message):
    with sqlite3.connect('database.sqlite3') as db:
      db.row_factory = sqlite3.Row
      cursor = db.cursor()
      cursor.execute(f'SELECT prefix FROM prefixes WHERE guild_id = {message.guild.id}')
      res = cursor.fetchone()
    if res:
      prefix = str(res[0])
    if not res:
      prefix = '?'
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

async def get_pre(bot, ctx):
    if ctx.guild is None:
        return commands.when_mentioned_or(f"-")(bot, ctx)
    with sqlite3.connect('database.sqlite3') as db:
      db.row_factory = sqlite3.Row
      cursor = db.cursor()
      cursor.execute(f'SELECT prefix FROM prefixes WHERE guild_id = {ctx.guild.id}')
      res = cursor.fetchone()
    if res:
      prefix = str(res[0])
    if not res:
      prefix = '-'
    try:
        cursor.execute(f'SELECT * FROM noprefix WHERE user_id = {ctx.author.id}')
        res1 = cursor.fetchone()
        if res1 is not None:
            if res1['servers'] is not None:
                no_prefix = literal_eval(res1['servers'])
                if ctx.guild.id in no_prefix:
                    return commands.when_mentioned_or(f"{prefix}", "")(bot, ctx)
            if res1['main'] is not None:
                if res1['main'] == 1:
                    return commands.when_mentioned_or(f"{prefix}", "")(bot, ctx)
    except:
        pass
    db.commit()
    cursor.close()
    db.close()
    return commands.when_mentioned_or(prefix)(bot,ctx)

async def node_connect():
    await bot.wait_until_ready()
    bot.wavelink = await wavelink.NodePool.create_node(bot=bot,host="54.38.198.24", port=88, password="stonemusicgay")

shard_count = 3
intents = discord.Intents.all()
intents.presences = False
class Bot(commands.AutoShardedBot):
  def __init__(self, get_pre, intents) -> None:
     super().__init__(command_prefix = get_pre, case_insensitive=True, intents=intents, shard_count=shard_count)


  async def setup_hook(self) -> None:
    #node: wavelink.Node = wavelink.Node(id="Node-01", uri="54.38.198.24:88", password="stonemusicgay")
    #self.wavelink = node
    #client_id ='9d340e339c10432e9c478742931d64e9'
    #client_secret = '2e23b2ab872046eca5fdf3379006f7de'
    #sc: spotify.SpotifyClient = spotify.SpotifyClient(
    #    client_id=client_id,
    #    client_secret=client_secret
    #)
    #client_credentials_manager = SpotifyClientCredentials(client_id = client_id, client_secret =client_secret)

    #self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    #self.spotify = sc
    self.conn = await asyncpg.connect('postgres://mfsjswgw:yz-JpViH_pE4AlcwS6ceyrbATnDRzMyL@ruby.db.elephantsql.com/mfsjswgw')
    await create_table(self.conn)

    #await wavelink.NodePool.connect(client=self, nodes=[node], spotify=sc)
    initial_extensions = ['jishaku']

    for filename in os.listdir('./cogs'):
      if filename.endswith('.py'):
        initial_extensions.append("cogs." + filename[:-3])

    for extension in initial_extensions:
        await self.load_extension(extension)
    await self.tree.sync()


bot = Bot(get_pre, intents)
ownerids = botinfo.botowner
bot.owner_ids = ownerids
bot.remove_command("help")


@bot.event
async def on_ready():
    check = True
    #bot.loop.create_task(node_connect())
    bot.topggpy = topgg.client.DBLClient(bot=bot, token=botinfo.dbltoken, autopost=True, post_shard_count=False, autopost_interval=900)

@bot.event
async def on_autopost_success():
    try:
        print(f"Posted server count ({bot.topggpy.guild_count})")
    except:
        pass
    
@bot.event
async def process_commands(message: discord.Message) -> None:
    if message.author.bot:
        return
    if not message.guild.me.guild_permissions.read_messages:
        return
    if not message.guild.me.guild_permissions.read_message_history:
        return
    if not message.guild.me.guild_permissions.view_channel:
        return
    if not message.guild.me.guild_permissions.send_messages:
        return
    s_id = message.guild.shard_id
    sh = bot.get_shard(s_id)
    if sh.is_ws_ratelimited() and check:
            webhook = discord.SyncWebhook.from_url(botinfo.webhook_ratelimit_logs)
            webhook.send("The bot is being ratelimited", username=f"{str(bot.user)} | Ratelimit Logs", avatar_url=bot.user.avatar.url)
    ctx = await bot.get_context(message)
    query = "SELECT * FROM  ignore WHERE guild_id = ?"
    val = (message.guild.id,)
    with sqlite3.connect('database.sqlite3') as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        cursor.execute(query, val)
        ig_db = cursor.fetchone()
    if ig_db is None:
      if ctx.command:
        if not ctx.command.qualified_name.startswith("jishaku"):
            await add_count(ctx, ctx.author, ctx.guild, cmd_name=ctx.command.qualified_name)
        await bot.invoke(ctx)
    else:
        xd = literal_eval(ig_db['cmd'])
        xdd = literal_eval(ig_db['module'])
        if ctx.command:
            c_cmd = await by_cmd(ctx, message.author, ctx.command.qualified_name)
            c_module = await by_module(ctx, message.author, str(ctx.command.cog_name.lower()))
            if ctx.command.qualified_name in xd and not c_cmd:
                s = str(ctx.command.qualified_name.capitalize())
                em = discord.Embed(description=f"{s} command is disabled for this server", color=0xc283fe).set_footer(text=bot.user.name, icon_url=bot.user.avatar.url)
                return await ctx.reply(embed=em, delete_after=30)
            elif str(ctx.command.cog_name.lower()) in xdd and not c_module:
                s = str(ctx.command.cog_name.capitalize())
                em = discord.Embed(description=f"{s} module is disabled for this server", color=0xc283fe).set_footer(text=bot.user.name, icon_url=bot.user.avatar.url)
                return await ctx.reply(embed=em, delete_after=30)
            else:
              if not ctx.command.qualified_name.startswith("jishaku"):
                await add_count(ctx, ctx.author, ctx.guild, cmd_name=ctx.command.qualified_name)
              await bot.invoke(ctx)

@bot.event
async def on_message(message: discord.Message) -> None:
    await bot.wait_until_ready()
    if isinstance(message.channel, discord.DMChannel):
        if message.author.id != bot.user.id:
            webhook = discord.SyncWebhook.from_url(botinfo.webhook_dm_logs)
            if message.author.avatar:
                webhook.send(f"{message.content}", username=f"{str(message.author)} | Dm Logs", avatar_url=message.author.avatar.url)
            else:
                webhook.send(f"{message.content}", username=f"{str(message.author)} | Dm Logs")
        return
    if not message.guild.me.guild_permissions.read_messages:
        return
    if not message.guild.me.guild_permissions.read_message_history:
        return
    if not message.guild.me.guild_permissions.view_channel:
        return
    if not message.guild.me.guild_permissions.send_messages:
        return
    ctx = await bot.get_context(message)
    if re.fullmatch(rf"<@!?{bot.user.id}>", message.content) and not ctx.author.bot:
        with sqlite3.connect('database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(f"SELECT * FROM prefixes WHERE guild_id = {message.guild.id}")
            res = cursor.fetchone()
        
        prefix = ""
        if(res and res["prefix"]):
            prefix = res["prefix"]
        else:
            prefix = botinfo.prefix
        emb = discord.Embed(description=f"Hey {message.author.mention} My prefix for this guild is `{prefix}`\nTo view all my modules and commands use `{prefix}help` or </help:1063005466914979900>.\nFor specific module related help use `{prefix}help <module name>` or </help:1063005466914979900> `<module name>`", color=0xc283fe)
        page = discord.ui.View()
        page.add_item(discord.ui.Button(label="Invite me", url=discord.utils.oauth_url(bot.user.id)))
        page.add_item(discord.ui.Button(label="Support Server", url="https://discord.gg/wb4UCU3m5z"))
        page.add_item(discord.ui.Button(label="Vote", url="https://top.gg/bot/880765863953858601/vote"))
        page.add_item(discord.ui.Button(label="Website", url="https://gatewaybot.xyz/"))
        await ctx.reply(embed=emb, mention_author=False, view=page)
    query = "SELECT * FROM  bl  WHERE main = 1"
    with sqlite3.connect('./database.sqlite3') as dbb:
        dbb.row_factory = sqlite3.Row
        cursorb = dbb.cursor()
        cursorb.execute(query)
        bl_db = cursorb.fetchone()
    if bl_db is not None:
        bl_db = literal_eval(bl_db["user_ids"])
        if ctx.author.id in bl_db:
            return
    query = "SELECT * FROM  ignore WHERE guild_id = ?"
    val = (message.guild.id,)
    with sqlite3.connect('database.sqlite3') as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        cursor.execute(query, val)
        ig_db = cursor.fetchone()
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
    if message.author.id == bot.user.id:
        return
    try:
        if bot.mesaagecreate:
            return await bot.process_commands(message)
    except:
        pass
    query = "SELECT * FROM setup WHERE guild_id = ?"
    val = (message.guild.id,)
    with sqlite3.connect('./database.sqlite3') as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        cursor.execute(query, val)
        s_db = cursor.fetchone()
    db.commit()
    cursor.close()
    db.close()
    if s_db is None:
        return await bot.process_commands(message)
    elif message.channel.id != s_db['channel_id']:
        return await bot.process_commands(message)
    else:
            pre = await get_prefix(message)
            check = False
            content = message.content
            prefix = None
            for k in pre:
                if content.startswith(k):
                    content = content.replace(k, "").strip()
                    check = True
                    prefix = k
            s = ""
            for i in content:
                if i == " ":
                    break
                s+=i
            cmd = bot.get_command(s)
            if cmd is None:
                if check and prefix != "":
                    message.content = f"<@{message.guild.me.id}> {content}"
                else:
                    message.content = f"<@{message.guild.me.id}> play {message.content}"
            else:
                if cmd.cog_name != "music":
                    return await ctx.send(f"{message.author.mention} You can only runs command from music module, no other command can be runned in this channel.", delete_after=15)
                if check:
                    message.content = prefix + content
                else:
                    message.content = f"<@{message.guild.me.id}> {message.content}"
            await bot.process_commands(message)
            try:
                await message.delete()
            except:
                pass
            await asyncio.sleep(60)
            async for msg in message.channel.history(limit=100):
                if msg.id == s_db['msg_id']:
                    pass
                else:
                    try:
                        await msg.delete()
                    except:
                        pass

@bot.event
async def on_message_edit(before: discord.Message, after: discord.Message):
    await bot.wait_until_ready()
    if after.content == before.content:
        return
    message = after
    ctx = await bot.get_context(message)
    query = "SELECT * FROM  bl  WHERE main = 1"
    with sqlite3.connect('./database.sqlite3') as dbb:
        dbb.row_factory = sqlite3.Row
        cursorb = dbb.cursor()
        cursorb.execute(query)
        bl_db = cursorb.fetchone()
    if bl_db is not None:
        bl_db = literal_eval(bl_db["user_ids"])
        if ctx.author.id in bl_db:
            return
    query = "SELECT * FROM  ignore WHERE guild_id = ?"
    val = (message.guild.id,)
    with sqlite3.connect('database.sqlite3') as db:
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        cursor.execute(query, val)
        ig_db = cursor.fetchone()
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
    await bot.process_commands(after)


#mai toh papa hu iss duniya ka papa geek nova toh papa coder hai Anay Hijda lode pe 

bot.run('')
