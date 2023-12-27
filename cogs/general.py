import psutil
import discord
import platform
from discord.ext import commands
from discord import *
import os
import sqlite3
import urllib.parse
import aiohttp
import re
import datetime
import requests
from typing import Union
import os
import time
import wavelink
from paginators import PaginationView
from ast import literal_eval
from botinfo import *
from PIL import Image, ImageDraw, ImageTk, ImageFont
import requests
import numpy as np
from io import BytesIO
from wavelink.ext import spotify
import openai
import re

openai.api_key = "OPENAI_API_KEY"
google_key = "GOOGLE_API_KEY" 
cx = "GOOGLE_API_CX"
dr = {"Music": "<a:musical:1152999917724385421>",
      "General": "<:help:1152981730458878075>"}

def identify_code_language(code):
    # Define regular expressions for common programming languages
    languages = {
        'Python': r'\b(def|if|elif|else|while|for|print|import|from|as|with|try|except|raise|class|return)\b',
        'Java': r'\b(public|private|protected|abstract|class|void|int|double|float|boolean|char|String|static|final|extends|implements|new|if|else|while|for|switch|case|default|break|continue|return)\b',
        'C#': r'\b(public|private|protected|internal|abstract|sealed|class|void|int|double|float|bool|string|static|readonly|using|namespace|try|catch|finally|if|else|while|for|switch|case|default|break|continue|return)\b',
        'JavaScript': r'\b(function|var|let|const|if|else|while|for|switch|case|default|break|continue|return|import|export|class|extends|super|async|await|try|catch|finally)\b',
        'Go': r'\b(func|var|const|if|else|switch|case|default|for|range|import|package|type|struct|interface|defer|panic|recover)\b',
        'Ruby': r'\b(def|if|elsif|else|while|for|case|when|do|end|module|class|require|include|extend|public|private|protected|self|super|return)\b',
        'PHP': r'\b(function|if|else|while|for|switch|case|default|break|continue|return|require|include|class|public|private|protected|static|final|abstract|interface|namespace)\b',
        'Rust': r'\b(fn|let|mut|const|if|else|while|for|loop|match|return|use|mod|struct|enum|trait|impl|pub|priv|unsafe|as|dyn|super|self)\b',
        'Swift': r'\b(func|var|let|if|else|while|for|switch|case|default|break|continue|return|import|class|struct|enum|protocol|extension|guard|defer)\b',
        'Perl': r'\b(sub|if|elsif|else|while|for|foreach|last|next|redo|return|my|our|use|package|sub|require|import|do)\b',
        'Kotlin': r'\b(fun|var|val|if|else|while|for|when|in|is|as|return|import|class|interface|object|package|init)\b',
        'Lua': r'\b(function|local|if|then|elseif|else|while|for|in|do|end|return|require|module)\b',
        'PowerShell': r'\b(function|if|elseif|else|while|for|foreach|do|until|break|continue|return|param|begin|process|end|switch|case|default|try|catch|finally|throw|trap)\b',
    }
    for i in languages:
        if re.search(languages[i], code):
            return i.lower()
    return None


class BasicView(discord.ui.View):
    def __init__(self, ctx: commands.Context, timeout = 60):
        super().__init__(timeout=timeout)
        self.ctx = ctx

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and interaction.user.id not in  [978930369392951366]:
            await interaction.response.send_message(f"Um, Looks like you are not the author of the command...", ephemeral=True)
            return False
        return True

class OnOrOff(BasicView):
    def __init__(self, ctx: commands.Context):
        super().__init__(ctx, timeout=60)
        self.value = None

    @discord.ui.button(label="User Avatar", custom_id='Yes', style=discord.ButtonStyle.green)
    async def dare(self, interaction, button):
        self.value = 'Yes'
        self.stop()
    @discord.ui.button(label="Server Avatar", custom_id='No', style=discord.ButtonStyle.red)
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

class globalorlocal(BasicView):
    def __init__(self, ctx: commands.Context):
        super().__init__(ctx, timeout=120)
        self.value = None

    @discord.ui.button(label="All Servers (Mutuals)", custom_id='users', style=discord.ButtonStyle.secondary)
    async def users(self, interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        self.value = 'global'
        self.stop()

    @discord.ui.button(label="Only in this server (Current)", custom_id='bots', style=discord.ButtonStyle.secondary)
    async def bots(self, interaction, button):
        await interaction.response.defer(ephemeral=False, thinking=False)
        self.value = 'local'
        self.stop()

async def profile(bot: commands.Bot, ctx: commands.Context, user: discord.Member, b_db, u_db, p_ls, init, bot_bdg: list[discord.Emoji], user_bdg: list[discord.Emoji], total_cmd, user_rank):
    if u_db is None:
        totaltime = 0
        s_dic = {}
        f_dic = {}
        a_dic = {}
        t_dic = {}
    else:
        totaltime = u_db['totaltime']
        s_dic = literal_eval(u_db['server'])
        f_dic = literal_eval(u_db['friend'])
        a_dic = literal_eval(u_db['artist'])
        t_dic = literal_eval(u_db['track'])
    if b_db is None:
        bf_dic = {}
    else:
        bf_dic = literal_eval(b_db['user'])
    response = requests.get("https://cdn.discordapp.com/attachments/1155964405129953391/1156627795137544214/20230922_172728.png?ex=6515a913&is=65145793&hm=7d4277ceec1c84bd1a3d1161bd3db930098de7dea17aa05b2660dc229d07e958&")
    width = 1280
    height = 720

    # Create new image and ImageDraw object
    image = Image.open(BytesIO(response.content)).convert("RGBA")
    image = image.resize((width,height))
    draw = ImageDraw.Draw(image)
    pfp = user.display_avatar.url
    pfp = pfp.replace("gif", "png").replace("webp", "png").replace("jpeg", "png")
    logo_res = requests.get(pfp)
    AVATAR_SIZE = 128
    avatar_image = Image.open(BytesIO(logo_res.content)).convert("RGB")
    avatar_image = avatar_image.resize((AVATAR_SIZE, AVATAR_SIZE)) #
    circle_image = Image.new('L', (AVATAR_SIZE, AVATAR_SIZE))
    circle_draw = ImageDraw.Draw(circle_image)
    circle_draw.ellipse((0, 0, AVATAR_SIZE, AVATAR_SIZE), fill=255)
    image.paste(avatar_image, (150, 100), circle_image)
    font = ImageFont.truetype('Fonts/Quicksand-Bold.ttf', 28)
    draw.text( (295, 130), f"{str(user)}", fill=(255, 255, 255), font=font)
    px = 300
    for i in user_bdg:
        url = i.url
        url = url.replace("gif", "png").replace("webp", "png").replace("jpeg", "png")
        res = requests.get(url)
        size = 28
        avatar_image = Image.open(BytesIO(res.content)).convert("RGBA")
        avatar_image = avatar_image.resize((size, size))
        pixel_data = avatar_image.load()
        background_color = (0, 0, 0)  # specify the background color in RGB format
        for y in range(avatar_image.size[1]):
            for x in range(avatar_image.size[0]):
                if pixel_data[x, y] == background_color:
                    pixel_data[x, y] = (0, 0, 0, 0)
        #circle_image = Image.new('L', (spotify_size, spotify_size))
        #circle_draw = ImageDraw.Draw(circle_image)
        #circle_draw.ellipse((0, 0, spotify_size, spotify_size), fill=255)
        image.paste(avatar_image, (px, 170), avatar_image)
        px+=32
    sup_srvr = bot.get_guild(1068830296142782495)
    mm = sup_srvr.get_member(user.id)
    if mm is not None:
        for i in mm.roles:
            if i.hoist:
                title = i.name
        if title != "Community":
            draw.text( (285, 164), text=title.title(), font=ImageFont.truetype('Fonts/Quicksand-Bold.ttf', 28), fill="white")
    px = 300
    for i in bot_bdg:
        url = i.url
        url = url.replace("gif", "png").replace("webp", "png").replace("jpeg", "png")
        res = requests.get(url)
        size = 28
        avatar_image = Image.open(BytesIO(res.content)).convert("RGBA")
        avatar_image = avatar_image.resize((size, size))
        pixel_data = avatar_image.load()
        background_color = (0, 0, 0)  # specify the background color in RGB format
        for y in range(avatar_image.size[1]):
            for x in range(avatar_image.size[0]):
                if pixel_data[x, y] == background_color:
                    pixel_data[x, y] = (0, 0, 0, 0)
        #circle_image = Image.new('L', (spotify_size, spotify_size))
        #circle_draw = ImageDraw.Draw(circle_image)
        #circle_draw.ellipse((0, 0, spotify_size, spotify_size), fill=255)
        image.paste(avatar_image, (px, 200), avatar_image)
        px+=32
    #draw.rounded_rectangle((970, 0, 1180, 50), radius=3, fill=(255, 0, 0, 128))
    rect_x = 500
    rect_y = 0
    rect_width = 780-rect_x
    rect_height = 50-rect_y
    # start_color = "#2193b0"
    # end_color = "#6dd5ed"
    # for y in range(rect_x, rect_x+rect_width):
    #     # Interpolate the color between red and blue based on the current y-coordinate
    #     #color = (int(255 * (y - rect_y) / rect_height), 0, int(255 * (1 - (y - rect_y) / rect_height)), 128)
    #     r = int((int(end_color[1:3], 16) - int(start_color[1:3], 16)) * y / height + int(start_color[1:3], 16))
    #     g = int((int(end_color[3:5], 16) - int(start_color[3:5], 16)) * y / height + int(start_color[3:5], 16))
    #     b = int((int(end_color[5:7], 16) - int(start_color[5:7], 16)) * y / height + int(start_color[5:7], 16))
    #     draw.line((y, rect_y, y, rect_y+rect_height), fill=(r,g,b, 128))
    # draw.text( (640, 25), text="Gateway", font=ImageFont.truetype('Fonts/Quicksand-Medium.ttf', 28), fill=(0, 10, 36), anchor="mm")
    #draw.rounded_rectangle((100, 0, 310, 50), radius=3, fill=(255, 0, 0, 128))
    rect_x = 100
    rect_y = 0
    rect_width = 380-rect_x
    rect_height = 50-rect_y
    start_color = "#c40000"
    end_color = "#c40000"
    for y in range(rect_x, rect_x+rect_width):
        # Interpolate the color between red and blue based on the current y-coordinate
        #color = (int(255 * (y - rect_y) / rect_height), 0, int(255 * (1 - (y - rect_y) / rect_height)), 128)
        r = int((int(end_color[1:3], 16) - int(start_color[1:3], 16)) * y / height + int(start_color[1:3], 16))
        g = int((int(end_color[3:5], 16) - int(start_color[3:5], 16)) * y / height + int(start_color[3:5], 16))
        b = int((int(end_color[5:7], 16) - int(start_color[5:7], 16)) * y / height + int(start_color[5:7], 16))
        draw.line((y, rect_y, y, rect_y+rect_height), fill=(r,g,b, 128))
    draw.text( (240, 25), text=f"Rank #{user_rank}", font=ImageFont.truetype('Fonts/Quicksand-Medium.ttf', 28), fill="white", anchor="mm")
    rect_x = 900
    rect_y = 0
    rect_width = 1180-rect_x
    rect_height = 50-rect_y
    start_color = "#2193b0"
    end_color = "#6dd5ed"
    # for y in range(rect_x, rect_x+rect_width):
    #     # Interpolate the color between red and blue based on the current y-coordinate
    #     #color = (int(255 * (y - rect_y) / rect_height), 0, int(255 * (1 - (y - rect_y) / rect_height)), 128)
    #     r = int((int(end_color[1:3], 16) - int(start_color[1:3], 16)) * y / height + int(start_color[1:3], 16))
    #     g = int((int(end_color[3:5], 16) - int(start_color[3:5], 16)) * y / height + int(start_color[3:5], 16))
    #     b = int((int(end_color[5:7], 16) - int(start_color[5:7], 16)) * y / height + int(start_color[5:7], 16))
    #     draw.line((y, rect_y, y, rect_y+rect_height), fill=(r,g,b, 128))
    # count = 1
    # for i in bf_dic:
    #     if user.id == i:
    #         break
    #     count +=1
    # if user.id not in bf_dic:
    #     draw.text( (1040, 25), text="Music Rank Null", font=ImageFont.truetype('Fonts/Quicksand-Medium.ttf', 28), fill=(0, 10, 36), anchor="mm")
    # else:
    #     draw.text( (1040, 25), text=f"Music Rank #{count}", font=ImageFont.truetype('Fonts/Quicksand-Medium.ttf', 28), fill=(0, 10, 36), anchor="mm")
    rect_x = 860
    rect_y = 100
    rect_width = 1180-rect_x
    rect_height = 240-rect_y
    start_color = "#ff2508"
    end_color = "#c40000"
    # for y in range(rect_x, rect_x+rect_width):
    #     # Interpolate the color between red and blue based on the current y-coordinate
    #     #color = (int(255 * (y - rect_y) / rect_height), 0, int(255 * (1 - (y - rect_y) / rect_height)), 128)
    #     r = int((int(end_color[1:3], 16) - int(start_color[1:3], 16)) * y / height + int(start_color[1:3], 16))
    #     g = int((int(end_color[3:5], 16) - int(start_color[3:5], 16)) * y / height + int(start_color[3:5], 16))
    #     b = int((int(end_color[5:7], 16) - int(start_color[5:7], 16)) * y / height + int(start_color[5:7], 16))
    #     draw.line((y, rect_y, y, rect_y+rect_height), fill=(r,g,b, 128))
    tt = converttime(totaltime)
    if tt is None or tt == "":
        tt = "0m"
    draw.text((1024, 170), text=f"Total Commands Runned:\n{total_cmd}\nTotal Listening Time:\n{tt}", font=ImageFont.truetype('Fonts/Quicksand-SemiBold.ttf', 24), fill="#ffffff", anchor="mm")
    mask = Image.new('RGBA', image.size, (0, 0, 0, 0))
    m_draw = ImageDraw.Draw(mask)
    left = 0
    top = 0
    right = 530
    bottom = 110
    m_draw.rectangle((left, top, right, bottom), fill=(47, 49, 54, 196))
    image.paste(mask, (100, 250), mask)
    image.paste(mask, (650, 250), mask)
    image.paste(mask, (100, 380), mask)
    image.paste(mask, (650, 380), mask)
    left = 0
    top = 0
    right = 1080
    bottom = 110
    m_draw.rectangle((left, top, right, bottom), fill=(47, 49, 54, 196))
    image.paste(mask, (100, 510), mask)
    draw.text( (110, 260), text="Your Playlists", font=ImageFont.truetype('Fonts/Quicksand-SemiBold.ttf', 24), fill=(255, 255, 255), anchor="lt")
    p_pixel = 260
    count = 0
    for i, j, k in p_ls:
        if count >= 3:
            break
        count +=1
        p_pixel+=25
        k = converttime(k)
        draw.text( (110, p_pixel), text=f"{count}. {i} ({j} songs) - {k}", font=ImageFont.truetype('Fonts/Quicksand-Medium.ttf', 22), fill=(255, 255, 255), anchor="lt")
    if len(p_ls) == 0:
        draw.text( (110, 285), text=f"No Playlist Found", font=ImageFont.truetype('Fonts/Quicksand-Medium.ttf', 22), fill=(255, 255, 255), anchor="lt")

    draw.text( (660, 260), text="Top Servers", font=ImageFont.truetype('Fonts/Quicksand-SemiBold.ttf', 24), fill=(255, 255, 255), anchor="lt")
    p_pixel = 260
    count = 0
    for i in s_dic:
        if count >= 3:
            break
        count +=1
        p_pixel+=25
        k = converttime(s_dic[i])
        g = bot.get_guild(i)
        if g is None:
            n = "Unknown Server"
        else:
            n = g.name
        draw.text( (660, p_pixel), text=f"{count}. {k} - {n}", font=ImageFont.truetype('Fonts/Quicksand-Medium.ttf', 22), fill=(255, 255, 255), anchor="lt")
    if len(s_dic) == 0:
        draw.text( (660, 285), text="No Data", font=ImageFont.truetype('Fonts/Quicksand-Medium.ttf', 22), fill=(255, 255, 255), anchor="lt")

    draw.text( (110, 390), text="Top Friends", font=ImageFont.truetype('Fonts/Quicksand-SemiBold.ttf', 24), fill=(255, 255, 255), anchor="lt")
    p_pixel = 390
    count = 0
    for i in f_dic:
        if count >= 3:
            break
        count +=1
        p_pixel+=25
        k = converttime(f_dic[i])
        g = await bot.fetch_user(i)
        if g is None:
            n = "Unknown User"
        else:
            n = str(g)
        draw.text( (110, p_pixel), text=f"{count}. {k} - {n}", font=ImageFont.truetype('Fonts/Quicksand-Medium.ttf', 22), fill=(255, 255, 255), anchor="lt")
    if len(f_dic) == 0 :
        draw.text( (110, 415), text="No Data", font=ImageFont.truetype('Fonts/Quicksand-Medium.ttf', 22), fill=(255, 255, 255), anchor="lt")
    
    draw.text( (660, 390), text="Top Artists", font=ImageFont.truetype('Fonts/Quicksand-SemiBold.ttf', 24), fill=(255, 255, 255), anchor="lt")
    p_pixel = 390
    count = 0
    for i in a_dic:
        if count >= 3:
            break
        count +=1
        p_pixel+=25
        k = converttime(a_dic[i])
        draw.text( (660, p_pixel), text=f"{count}. {k} - {i}", font=ImageFont.truetype('Fonts/Quicksand-Medium.ttf', 22), fill=(255, 255, 255), anchor="lt")
    if len(a_dic) == 0:
        draw.text( (660, 415), text="No Data", font=ImageFont.truetype('Fonts/Quicksand-Medium.ttf', 22), fill=(255, 255, 255), anchor="lt")
    
    draw.text( (110, 520), text="Top Tracks", font=ImageFont.truetype('Fonts/Quicksand-SemiBold.ttf', 24), fill=(255, 255, 255), anchor="lt")
    p_pixel = 520
    count = 0
    for i in t_dic:
        if count >= 3:
            break
        count +=1
        p_pixel+=25
        k = converttime(t_dic[i])
        draw.text( (110, p_pixel), text=f"{count}. {k} - {i[:60]}", font=ImageFont.truetype('Fonts/Quicksand-Medium.ttf', 22), fill=(255, 255, 255), anchor="lt")
    if len(t_dic) == 0:
        draw.text( (110, 545), text="No Data", font=ImageFont.truetype('Fonts/Quicksand-Medium.ttf', 22), fill=(255, 255, 255), anchor="lt")

    with BytesIO() as image_binary:
        image.save(image_binary, 'PNG')
        image_binary.seek(0)
        await init.delete()
        await ctx.reply(file=discord.File(fp=image_binary, filename='profile.png'))
    
def converttime(seconds):
    time = int(seconds)
    month = time // (30 * 24 * 3600)
    time = time % (24 * 3600)
    day = time // (24 * 3600)
    time = time % (24 * 3600)
    hour = time // 3600
    time %= 3600
    minutes = time // 60
    time %= 60
    seconds = time
    ls = []
    if month != 0:
        ls.append(f"{month}mo")
    if day != 0:
        ls.append(f"{day}d")
    if hour != 0:
        ls.append(f"{hour}h")
    if minutes != 0:
        ls.append(f"{minutes}m")
    if seconds != 0:
        ls.append(f"{seconds}s")
    return ' '.join(ls)

class general(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def time_formatter(self, seconds: float):

        minutes, seconds = divmod(int(seconds), 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        tmp = ((str(days) + " days, ") if days else "") + \
            ((str(hours) + " hours, ") if hours else "") + \
            ((str(minutes) + " minutes, ") if minutes else "") + \
            ((str(seconds) + " seconds, ") if seconds else "")
        return tmp[:-2]

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        await self.bot.wait_until_ready()
        if not message.guild:
                        return
        if not message.guild.me.guild_permissions.read_messages:
            return
        if not message.guild.me.guild_permissions.read_message_history:
            return
        if not message.guild.me.guild_permissions.view_channel:
            return
        if not message.guild.me.guild_permissions.send_messages:
            return
        if message.mentions:
            for user_mention in message.mentions:
                query = "SELECT * FROM  afk WHERE user_id = ?"
                val = (user_mention.id,)
                with sqlite3.connect('./database.sqlite3') as db:
                    db.row_factory = sqlite3.Row
                    cursor = db.cursor()
                    cursor.execute(query, val)
                    auto_db = cursor.fetchone()
                    if auto_db is None:
                        continue
                try:
                    afk = literal_eval(auto_db['afkk'])
                except:
                    continue
                if message.guild.id in afk:
                  if afk[message.guild.id]['status'] == True:
                    if message.author.bot: 
                        continue
                    reason = afk[message.guild.id]['reason']
                    t = afk[message.guild.id]['time']
                    afk[message.guild.id]['mentions']+=1
                    sql = (f"UPDATE afk SET afkk = ? WHERE user_id = ?")
                    val = (f"{afk}", user_mention.id)
                    cursor.execute(sql, val)
                    try:
                        await message.channel.send(f'**{str(user_mention)}** went AFK <t:{t}:R>: {reason}')
                    except:
                        continue
                    db.commit()
                    cursor.close()
                    db.close()
        query = "SELECT * FROM  afk WHERE user_id = ?"
        val = (message.author.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            auto_db = cursor.fetchone()
            if auto_db is None:
                return
        try:
            afk = literal_eval(auto_db['afkk'])
            globally = auto_db['globally']
        except:
            return
        if message.guild.id in afk:
          if afk[message.guild.id]['status'] == True:
            meth = int(time.time()) - int(afk[message.guild.id]['time'])
            been_afk_for = await self.time_formatter(meth)
            if globally == 1:
                coun = 0
                for i in afk:
                    coun += afk[i]['mentions']
                for i in message.author.mutual_guilds:
                    m = i.get_member(message.author.id)
                    if m.display_name.startswith("[AFK]") and m.top_role.position < i.me.top_role.position:
                        try:
                            await m.edit(nick=f'{m.display_name[5:]}')
                        except:
                            pass
                try:
                    await message.channel.send(f"{message.author.mention} I removed your Afk, You were afk for {been_afk_for}, you were mentioned {afk[message.guild.id]['mentions']} times in this server and {coun-afk[message.guild.id]['mentions']} in other servers.", delete_after=60)
                except:
                    pass
                afk = {}
                globally = 0
            else:
                if message.author.display_name.startswith("[AFK]") and message.author.top_role.position < message.guild.me.top_role.position:
                    try:
                        await message.author.edit(nick=f'{message.author.display_name[5:]}')
                    except:
                        pass
                try:
                    await message.channel.send(f"{message.author.mention} I removed your Afk, You were afk for {been_afk_for}, you were mentioned {afk[message.guild.id]['mentions']} times in this server.", delete_after=60)
                except:
                    pass
                afk[message.guild.id]['status'] = False
                afk[message.guild.id]['reason'] = None
                afk[message.guild.id]['time'] = 0
                afk[message.guild.id]['mentions'] = 0
            sql = (f"UPDATE afk SET afkk = ? WHERE user_id = ?")
            val = (f"{afk}", message.author.id)
            cursor.execute(sql, val)
            sql = (f"UPDATE afk SET globally = ? WHERE user_id = ?")
            val = (globally, message.author.id)
            cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()

    @commands.command(name="uptime",
                    description="Shows you Bot's Uptime")
    async def uptime(self, ctx):
        bot = self.bot
        pfp = ctx.author.display_avatar.url
        uptime = datetime.datetime.utcnow() - starttime
        uptime = str(uptime).split('.')[0]
        embed = discord.Embed(title="Bot's Uptime", description=f"```{uptime}```",
                              color=0xc283fe)
        embed.set_footer(text=f"Requested by {ctx.author.name}" ,  icon_url=pfp)
        await ctx.send(embed=embed)

    #@commands.command(name="help", aliases=['h'], description="Shows the help command of the bot")
    async def help(self, ctx: commands.Context, *, command=None):
        if command is not None:
            cmd = self.bot.get_command(command)
            cog = command
            cog = self.bot.get_cog(cog.lower())
            if cmd is None and cog is None:
                return await ctx.reply(embed=discord.Embed(description=f"No command or module found named `{command}`", color=0xff0000), mention_author=False)
            if cog is not None:
                if cog.qualified_name.capitalize() in dr:
                    command = cog.qualified_name
                    ls = []
                    for j in cog.walk_commands():
                        ls.append(j.qualified_name)
                    prefix = ctx.prefix
                    if prefix == f"<@{self.bot.user.id}> ":
                        prefix = f"@{str(self.bot.user)} "
                    xd = discord.utils.get(self.bot.users, id=978930369392951366)
                    stars = str(xd)
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
                prefix = ctx.prefix
                if prefix == f"<@{self.bot.user.id}> ":
                    prefix = f"@{str(self.bot.user)} "
                xd = discord.utils.get(self.bot.users, id=978930369392951366)
                stars = str(xd)
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
                for k in ls1:
                    listem = discord.Embed(title=f"{command.capitalize()} Commands", colour=0xc283fe,
                                            description=f"<...> Duty | [...] Optional\n\n{''.join(k)}")
                    listem.set_author(name=f"{str(ctx.author)}", icon_url=ctx.author.display_avatar.url)
                    listem.set_footer(text=f"Made by stars.gg" ,  icon_url=pfp)
                    em_list.append(listem)
                    no+=1
                page = PaginationView(embed_list=em_list, ctx=ctx)
                await page.start(ctx)
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

    @commands.command(aliases=["bi", "stats"], description="Gets information of the bot")
    async def botinfo(self, ctx):
        bot = self.bot
        s_id = ctx.guild.shard_id
        sh = self.bot.get_shard(s_id)
        count = 0
        for g in self.bot.guilds:
          count += len(g.members)
        txt = 0
        vc = 0
        cat = 0
        join = 0
        play = 0
        for i in self.bot.guilds:
            for j in i.channels:
                if isinstance(j, discord.TextChannel):
                    txt+=1
                elif isinstance(j, discord.VoiceChannel):
                    vc+=1
                elif isinstance(j, discord.CategoryChannel):
                    cat+=1
        files = 0
        lines = 0
        for i in os.scandir():
            if i.is_file():
                if i.name.endswith(".py"):
                    with open(i.name, "r") as f:
                        try:
                            lines+=len(f.readlines())
                        except:
                            continue
                    files+=1
            else:
                for j in os.scandir(i):
                    if j.name.endswith(".py"):
                        with open(f"{i.name}/{j.name}", "r") as f:
                            try:
                                lines+=len(f.readlines())
                            except:
                                continue
                        files+=1
        embed = discord.Embed(colour=0xc283fe)
        stars = discord.utils.get(self.bot.users, id=978930369392951366)
        zeck = discord.utils.get(self.bot.users, id=933738517845118976)
        rexy = discord.utils.get(self.bot.users, id=966230921084796999)
        xeno = discord.utils.get(self.bot.users, id=1071843392268546068)

        embed.set_author(name=f"{self.bot.user.name} Statistics", icon_url=ctx.guild.me.display_avatar.url)
        embed.add_field(name="<:tools:1154448773695684639> General", value=f">>> **Developer:** [Stars](https://discord.com/users/{stars.id})\n**Total Guilds:** {len(self.bot.guilds)}\n**Total users:** {count}\n**Channels:**\n <:next:1154735525505269871> Total: {str(len(set(self.bot.get_all_channels())))}\n <:next:1154735525505269871> Text: {txt}\n <:next:1154735525505269871> Voice: {vc}\n <:next:1154735525505269871> Categories:  {cat}\n**Shards:** {ctx.guild.shard_id+1}/{len(self.bot.shards.items())}", inline=False) #\n**Team:** [ZecK](https://discord.com/users/{zeck.id}), [Xeno](https://discord.com/users/{xeno.id}), [RexY](https://discord.com/users/{rexy.id})\n
        embed.add_field(name="<:music:1154448634130219038> Player", value=f">>> **Total:** {join}\n**Playing:** {play}", inline=False)
        embed.add_field(name="<:8319folder:1154676193354862633> Miscellaneous", value=f">>> **Server Usage:**\n <:next:1154735525505269871> CPU Usage: {psutil.cpu_percent()}%\n <:next:1154735525505269871> Memory Usage: {psutil.virtual_memory().percent}%\n**Latency:** {round(sh.latency * 1000)}ms\n**Python Version:** {platform.python_version()}\n**Discord.py Version:** {discord.__version__}\n**Code Information:**\n <:next:1154735525505269871> Total Files: [{files} Files](https://discord.gg/wb4UCU3m5z)\n <:next:1154735525505269871> Total Lines: [{lines} Lines](https://discord.gg/wb4UCU3m5z)", inline=False)
        # embed.description = (
        #     f"**• Developer:** **[Stars](https://discord.com/users/{stars.id})**\n"
        #                      f"**• Bot Stats**\n**\u2192**Total Guilds: **{len(self.bot.guilds)} Guilds**\n**\u2192** Total users: **{count} Users**\n**\u2192** Channels:\n- Total: **{str(len(set(self.bot.get_all_channels())))} Channels**\n- Text: {txt} Channels\n- Voice: {vc} Channels\n- Categories:  {cat} Categories"
        #                      f"**• Players**\n**\u2192**Total: {join}\n**\u2192** Playing: {play}\n"
        #                      f"**• Server Usage**\n**\u2192** CPU Usage: {psutil.cpu_percent()}%\n**\u2192** Memory Usage: {psutil.virtual_memory().percent}%\n"
        #                      f"**• Latency:** {round(sh.latency * 1000)}ms\n"
        #                      f"**• Shards:** {ctx.guild.shard_id+1}/{len(self.bot.shards.items())}\n"
        #                      f"**• Python Version:** {platform.python_version()}\n"
        #                      f"**• Discord.py Version:** **{discord.__version__}**\n"
        #                      f"**• __Code Information__:**\n"
        #                      f"**\u2192** **Total no. of Files:** **[{files} Files](https://discord.gg/wb4UCU3m5z)**\n"
        #                      f"**\u2192** **Total no. of Lines:** **[{lines} Lines](https://discord.gg/wb4UCU3m5z)**")
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        embed.set_footer(text=f"Thanks for choosing Gateway • Requested By {str(ctx.author)}", icon_url=ctx.author.display_avatar.url)
        page = discord.ui.View()
        page.add_item(discord.ui.Button(label="Get Gateway", url=discord.utils.oauth_url(self.bot.user.id)))
        page.add_item(discord.ui.Button(label="Support Server", url="https://discord.gg/wb4UCU3m5z"))
        await ctx.reply(embed = embed, mention_author=False, view=page)

    @commands.command(name="teaminfo", aliases=['ti'], description="Shows the informatio of bot's team")
    async def teaminfo(self, ctx: commands.Context):
        stars = discord.utils.get(self.bot.users, id=978930369392951366)
        xeno = discord.utils.get(self.bot.users, id=602900188549611543)
        hemlock = discord.utils.get(self.bot.users, id=868569108361404436)
        byte = discord.utils.get(self.bot.users, id=1087248052793913345)
        harsh = discord.utils.get(self.bot.users, id=192383951191408640)
        priyanshu = discord.utils.get(self.bot.users, id=192383951191408640)
        cerar = discord.utils.get(self.bot.users, id=1066616611441750027)
        satyam = discord.utils.get(self.bot.users, id=972076172684967947)
        adi = discord.utils.get(self.bot.users, id=775333233335205918)
        positive = discord.utils.get(self.bot.users, id=1027270184798535711)
        hacker = discord.utils.get(self.bot.users, id=246469891761111051)
        drexy = discord.utils.get(self.bot.users, id=983787597627273267)
        sumit = discord.utils.get(self.bot.users, id=259176352748404736)
        anshit = discord.utils.get(self.bot.users, id=1009791206043160616)
        embed = discord.Embed(colour=0xc283fe)
        embed.set_author(name=f"| {self.bot.user.name}'s Team Information", icon_url=ctx.guild.me.display_avatar.url)
        embed.description = (f"**• Head Developer**\n> **[stars](https://discord.com/users/{stars.id})**\n"
                            #  f"**• Developer**\n> **[Xeno](https://discord.com/users/{xeno.id})**\n"
                            #  f"**• Owners**\n> **[Byte](https://discord.com/users/{byte.id}), [Hemlock](https://discord.com/users/{hemlock.id}), [Satyam](https://discord.com/users/{satyam.id})**\n"
                            #  f"**• Marketing Head**\n> **[Anshit](https://discord.com/users/{anshit.id}), [Cerar](https://discord.com/users/{cerar.id})**\n"
                            #  f"**• Team**\n> **[Harsh](https://discord.com/users/{harsh.id}), [Adi](https://discord.com/users/{adi.id}), [Positive](https://discord.com/users/{positive.id})**\n"
                            #  f"**• Contributor**\n> **[Priyanshu](https://discord.com/users/{priyanshu.id}), [Drexy](https://discord.com/users/{drexy.id}), [Hacker](https://discord.com/users/{hacker.id}), [Sumit](https://discord.com/users/{sumit.id})**\n\n"
                             f"**• Role Play**\n> **__Head Developer__** is responsible for the coding, both front end and back end of the bot.\n\n> **__Developers__** assist the head developer in coding of bot and provide ideas for some unique features.\n\n> **__Owners__** have the duty to keep a check on hosting and the database of the bot.\n\n> **__Marketing Head__** Leads the marketing team to showcase the features and benefits of our Discord bot to the world.\n\n> **__Team Members__** managers the support server, helps the owners in their duties and also act as community manager for the bot.\n\n> **__Contributers__** were always there to support us in each and every aspect related to coding, hosting etc.")
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.set_footer(text=f"Requested By {str(ctx.author)}", icon_url=ctx.author.display_avatar.url)
        page = discord.ui.View()
        page.add_item(discord.ui.Button(label="Invite me", url=discord.utils.oauth_url(self.bot.user.id)))
        page.add_item(discord.ui.Button(label="Support Server", url="https://discord.gg/wb4UCU3m5z"))
        await ctx.reply(embed = embed, mention_author=False, view=page)

    @commands.hybrid_command(name="chatgpt", aliases=['cgpt', 'gpt'], description="Given you results for your query from openai")
    async def chatgpt(self, ctx: commands.Context, *, prompt):
        c = prompt.count(' ') + 100
        completion = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=4097-c,
            temperature=0.8)

        text = completion.choices[0].text
        s = identify_code_language(text)
        if s is not None:
            text = f"```{s}\n{text}```"
        else:
            text = f"```{text}```"
        embed=discord.Embed(
            title=f'> {prompt.title()}',
            description=f'{text}',
            colour=0x2f3136
        ).set_author(name="| ChatGPT", icon_url=self.bot.user.avatar.url).set_footer(text=f"Requested by {str(ctx.author)}", icon_url = ctx.author.display_avatar.url).set_thumbnail(url=self.bot.user.avatar.url)
        await ctx.reply(embed=embed)
    
    @commands.command(name="afk", description="Changes the afk status of user")
    async def afk(self, ctx, *,reason=None):
        if reason is None:
            reason = "I'm Afk :))"
        if "@everyone" in reason or "@here" in reason:
            await ctx.reply("You cannot mention everyone or here in a afk reason")
            return
        if "<&" in reason:
            await ctx.reply("You cannot mention a role in a afk reason")
            return
        if "discord.gg" in reason:
            await ctx.reply("You cannot advertise a server in a afk reason")
            return
        em = discord.Embed(color=0xc283fe, description=f"Where do you want to set your afk?\nChoose your afk style from the buttons below.").set_author(name=f"{str(ctx.author.name)}", icon_url=ctx.author.display_avatar.url)
        v = globalorlocal(ctx)
        init =await ctx.reply(embed=em, view=v)
        await v.wait()
        if v.value is None:
            v.value = "local"
        query = "SELECT * FROM  afk WHERE user_id = ?"
        val = (ctx.author.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            auto_db = cursor.fetchone()
        if auto_db is None:
            if v.value == "global":
                g_ls = ctx.author.mutual_guilds
                globally = 0
            else:
                g_ls = [ctx.guild]
                globally = 1
            ds = {}
            for i in g_ls:
                ds[i.id] = {}
                ds[i.id]['status'] = True
                ds[i.id]['reason'] = reason
                ds[i.id]['time'] = int(time.time())
                ds[i.id]['mentions'] = 0
            sql = (f"INSERT OR IGNORE INTO 'afk'(user_id, afkk, globally) VALUES(?, ?, ?)")
            val = (ctx.author.id, f"{ds}", globally,)
            cursor.execute(sql, val)
        else:
            ds = literal_eval(auto_db['afkk'])
            if v.value == "global":
                g_ls = ctx.author.mutual_guilds
                globally = 1
            else:
                g_ls = [ctx.guild]
                globally = 0
            for i in g_ls:
                m = i.get_member(ctx.author.id)
                try:
                    await m.edit(nick=f'[AFK]{m.display_name}')
                except:
                    pass
                ds[i.id] = {}
                ds[i.id]['status'] = True
                ds[i.id]['reason'] = reason
                ds[i.id]['time'] = int(time.time())
                ds[i.id]['mentions'] = 0
            sql = (f"UPDATE afk SET afkk = ? WHERE user_id = ?")
            val = (f"{ds}", ctx.author.id)
            cursor.execute(sql, val)
            sql = (f"UPDATE afk SET globally = ? WHERE user_id = ?")
            val = (globally, ctx.author.id)
            cursor.execute(sql, val)
        await init.edit(content=f'{ctx.author.mention},', embed=discord.Embed(color=0xc283fe, description=f'[**{str(ctx.author.name)}**](https://discord.com/users/{str(ctx.author.id)}), Your AFK is now set to: {reason}').set_author(name=f"AFK", icon_url="https://cdn.discordapp.com/attachments/1155964405129953391/1155964438332063854/verified.png?ex=65192e06&is=6517dc86&hm=9f2f5b22bd965c6d9da87c213388f64eb6c1e5aab1c8e0b8348d01a7bcfd6e67&").set_footer(text=f"Requested by {ctx.author.name}" ,  icon_url=ctx.author.display_avatar.url), view=None)
        db.commit()
        cursor.close()
        db.close()
        return

    @commands.group(
        invoke_without_command=True, description="Shows the help menu for todo commands"
    )
    async def todo(self, ctx: commands.Context):
        ls = ["todo", "todo add", "todo remove", "todo list"]
        prefix = ctx.prefix
        if prefix == f"<@{self.bot.user.id}> ":
            prefix = f"@{str(self.bot.user)} "
        stars = discord.utils.get(self.bot.users, id=978930369392951366)
        des = ""
        for i in sorted(ls):
            cmd = self.bot.get_command(i)
            des += f"`{prefix}{i}`\n{cmd.description}\n\n"
        listem = discord.Embed(colour=0xc283fe,
                                     description=f"<...> Duty | [...] Optional\n\n{des}")
        listem.set_author(name=f"{str(ctx.author)}", icon_url=ctx.author.display_avatar.url)
        listem.set_footer(text=f"Made by stars.gg" ,  icon_url=stars.avatar.url)
        await ctx.send(embed=listem)

    @todo.command(name="add", description="Adds a todo for the user")
    async def _add(self, ctx: commands.Context, *, arguments):
        query = "SELECT * FROM  todo WHERE user_id = ?"
        val = (ctx.author.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            auto_db = cursor.fetchone()
        if auto_db is None:
            x = []
            x.append(arguments)
            sql = (f"INSERT INTO todo(user_id, todo) VALUES(?, ?)")
            val = (ctx.author.id, f"{x}")
            cursor.execute(sql, val)
        else:
            x = literal_eval(auto_db['todo'])
            x.append(arguments)
            sql = (f"UPDATE todo SET todo = ? WHERE user_id = ?")
            val = (f"{x}", ctx.author.id)
            cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        await ctx.reply(f"Successfully add `{arguments}` to your todo list")

    @todo.command(name="remove", description="Removes a todo from the user")
    async def _remove(self, ctx: commands.Context, *, number):
        if not number.isdigit():
            return await ctx.reply("Please provide a integer")
        number = abs(int(number))
        query = "SELECT * FROM  todo WHERE user_id = ?"
        val = (ctx.author.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            auto_db = cursor.fetchone()
        if auto_db is None:
            return await ctx.reply(f"You dont have any todo with number: {number}")
        x = literal_eval(auto_db['todo'])
        if len(x) < number:
            return await ctx.reply(f"You dont have any todo with number: {number}")
        else:
            x.pop(number-1)
            sql = (f"UPDATE todo SET todo = ? WHERE user_id = ?")
            val = (f"{x}", ctx.author.id)
            cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        await ctx.reply(f"Successfully removed todo number {number} from your todo list")

    @todo.command(name="list", description="Shows you your pending todo work")
    async def _list(self, ctx: commands.Context):
        init = await ctx.reply(f"<:loading:1060851548869107782> Processing the command...", mention_author=False)
        query = "SELECT * FROM  todo WHERE user_id = ?"
        val = (ctx.author.id,)
        with sqlite3.connect('./database.sqlite3') as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute(query, val)
            auto_db = cursor.fetchone()
        em = discord.Embed(title=f"Todo list for {str(ctx.author)}", color=0x2f3136).set_footer(text=f"{self.bot.user.name}", icon_url=self.bot.user.avatar.url)
        if auto_db is None:
            em.description = f"There is no todo work"
            return await ctx.reply(embed=em)
        x = literal_eval(auto_db["todo"])
        if len(x) == 0:
            em.description = f"There is no todo work"
            return await ctx.reply(embed=em)
        ls, todo = [], []
        count = 1
        for i in x:
            todo.append(f"`[{'0' + str(count) if count < 10 else count}]` | {i}")
            count += 1
        for i in range(0, len(todo), 5):
           ls.append(todo[i: i + 5])
        em_list = []
        no = 1
        for k in ls:
           embed =discord.Embed(color=0x2f3136)
           embed.title = f"Todo list for {str(ctx.author)}"
           embed.description = "\n".join(k)
           embed.set_footer(text=f"{self.bot.user.name} • Page {no}/{len(ls)}", icon_url=self.bot.user.display_avatar.url)
           em_list.append(embed)
           no+=1
        page = PaginationView(embed_list=em_list, ctx=ctx)
        await init.delete()
        await page.start(ctx)

    @commands.group(
        invoke_without_command=True, description="Shows the user's profile for bot",
        aliases=['badges', 'badge', 'pr', 'pf']
    )
    async def profile(self, ctx, member: discord.Member = None):
            member = member or ctx.author
            init = await ctx.reply(f"Building up the profile of {str(member)}...", mention_author=False)
            query = "SELECT * FROM  badges WHERE user_id = ?"
            val = (member.id,)
            with sqlite3.connect('./database.sqlite3') as db:
              db.row_factory = sqlite3.Row
              cursor = db.cursor()
              cursor.execute(query, val)
              user_columns = cursor.fetchone()
            des = []
            if user_columns is None:
                pass
            else:
                if user_columns['OWNER'] == 1:
                    bdg = "<:gt_owner:1156621155357180056>"
                    des.append(discord.PartialEmoji.from_str(bdg))
                if user_columns['DEVELOPER'] == 1:
                    bdg = "<:gt_developer:1156621161376006154>"
                    des.append(discord.PartialEmoji.from_str(bdg))
                if user_columns['STAFF'] == 1:
                    bdg = "<:gt_staff:1156623265721233438>"
                    des.append(discord.PartialEmoji.from_str(bdg))
                if user_columns['ADMIN'] == 1:
                    bdg = "<:gt_admin:1156623949006905516>"
                    des.append(discord.PartialEmoji.from_str(bdg))
                if user_columns['MOD'] == 1:
                    bdg = "<:mod:995145856686772265>"
                    des.append(discord.PartialEmoji.from_str(bdg))
                if user_columns['SPECIAL'] == 1:
                    bdg = "<:gt_specials:1156621164186177638>"
                    des.append(discord.PartialEmoji.from_str(bdg))
                if user_columns['SUPPORTER'] == 1:
                    bdg = "<:gt_supporter:1156614035253514281>"
                    des.append(discord.PartialEmoji.from_str(bdg))
                if user_columns['DONATOR'] == 1:
                    bdg = "<:gt_donator:1156621176098017330>"
                    des.append(discord.PartialEmoji.from_str(bdg))
                if user_columns['FRIEND'] == 1:
                    bdg = "<:gt_friends:1156621168678273035>"
                    des.append(discord.PartialEmoji.from_str(bdg))
                if user_columns['PREMIUM'] == 1:
                    bdg = "<:gt_donator:1156621176098017330>"
                    des.append(discord.PartialEmoji.from_str(bdg))
                if user_columns['BUG'] == 1:
                    bdg = "<:gt_bughunter:1156621178790752266>"
                    des.append(discord.PartialEmoji.from_str(bdg))
                if user_columns['VIP'] == 1:
                    bdg = "<:gt_vip:1156624995502522418>"
                    des.append(discord.PartialEmoji.from_str(bdg))
            balance = discord.PartialEmoji.from_str("<:balance:933685821092016158>")
            bravery = discord.PartialEmoji.from_str("<:bravery:933685857582448671>")
            brillance = discord.PartialEmoji.from_str("<:brillance:933685893024337980>")
            bug_1 = discord.PartialEmoji.from_str("<:bug_hunter_1:933685410738085899>")
            bug_2 = discord.PartialEmoji.from_str("<:bug_hunter_2:933685491486847036>")
            early = discord.PartialEmoji.from_str("<:early_sup:933685551012397107>")
            hype = discord.PartialEmoji.from_str("<a:hype:933685735905710080>")
            partner = discord.PartialEmoji.from_str("<:partner:933685923567251517>")
            staff = discord.PartialEmoji.from_str("<a:staff:933685961932558337>")
            system = discord.PartialEmoji.from_str("<:system:933686023995682848>")
            veri_bot = discord.PartialEmoji.from_str("<:verified_bot:933686190920564736>")
            veri_dev = discord.PartialEmoji.from_str("<:verified_dev:933685666477379647>")
            act_dev = discord.PartialEmoji.from_str("<:active_developer:1040478576581029928>")
            badge = []
            if member.public_flags.bug_hunter == True:
                badge.append(bug_1)
            if member.public_flags.bug_hunter_level_2 == True:
                badge.append(bug_2)
            if member.public_flags.hypesquad_bravery == True:
                badge.append(bravery)
            if member.public_flags.hypesquad_balance == True:
                badge.append(balance)
            if member.public_flags.hypesquad_brilliance == True:
                badge.append(brillance)
            if member.public_flags.hypesquad == True:
                badge.append(hype)
            if member.public_flags.early_supporter == True:
                badge.append(early)
            if member.public_flags.early_verified_bot_developer == True:
                badge.append(veri_dev)
            if member.public_flags.verified_bot == True:
                badge.append(veri_bot)
            if member.public_flags.staff == True:
                badge.append(staff)
            if member.public_flags.system == True:
                badge.append(system)
            if member.public_flags.partner == True:
                badge.append(partner)
            if member.public_flags.active_developer == True:
                badge.append(act_dev)
            query = "SELECT * FROM  count WHERE xd = ?"
            val = (1,)
            cursor.execute(query, val)
            count_db = cursor.fetchone()
            user = literal_eval(count_db['user_count'])
            if member.id in user:
                cmd_runned = f"{user[member.id]} Commands"
            else:
                cmd_runned = "0 Command"
            mem = member
            query = "SELECT * FROM bot WHERE bot_id = ?"
            val = (self.bot.user.id,)
            cursor.execute(query, val)
            b_db = cursor.fetchone()
            query = "SELECT * FROM user WHERE user_id = ?"
            val = (mem.id,)
            cursor.execute(query, val)
            u_db = cursor.fetchone()
            query = "SELECT * FROM  pl WHERE user_id = ?"
            val = (mem.id,)
            cursor.execute(query, val)
            p_db = cursor.fetchone()
            if p_db is None:
                p_ls = []
            else:
                xd = literal_eval(p_db['pl'])
                p_ls = []
                for i in xd:
                    tm = 0
                    for j in xd[i]:
                        if "youtube.com" in j:
                            song = await self.bot.wavelink.get_tracks(wavelink.YouTubeTrack, j)
                            tm += song[0].duration/1000
                        else:
                            track: spotify.SpotifyTrack = await spotify.SpotifyTrack.search(query=j)
                            tm += track.duration/1000
                    p_ls.append((i, len(xd[i]), tm))
            query = "SELECT * FROM  count WHERE xd = ?"
            val = (1,)
            cursor.execute(query, val)
            count_db = cursor.fetchone()
            user = literal_eval(count_db['user_count'])
            cursor.close()
            db.close()
            u_count = 1
            for i in user:
                if i == mem.id:
                    break
                u_count+=1
            await profile(self.bot, ctx, mem, b_db, u_db, p_ls, init, des, badge, cmd_runned, u_count)

    @profile.command(name="add", aliases=["a"], description="Gives the badge to user")
    async def badge_add(self, ctx, member: discord.User, *, badge):
        ls = workowner
        if ctx.author.id not in ls and ctx.author.id not in self.bot.owner_ids:
            return
        if not badge:
            await ctx.reply("Mention a badge to Assign")
        badge = badge.upper()
        valid = ["ALL", "OWNER", "DEVELOPER", "SPECIAL", "SUPPORTER", "FRIEND", "DONATOR", "BUG"]
        if badge not in valid:
            return await ctx.send("Please send A valid Badge\nASSIGNABLE BADGES ARE: All, Owner, Developer, Special, Supporter, Friend, Donator, Bug")
        db = sqlite3.connect('./database.sqlite3')
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM  badges WHERE user_id = {member.id}")
        result = cursor.fetchone()
        if result is None:
            sql = (f"INSERT INTO badges(user_id) VALUES(?)")
            val = (member.id,)
            cursor.execute(sql, val)
        if badge == "ALL":
            for i in valid[1:]:
                sql = (f"UPDATE badges SET {i} = ? WHERE user_id = ?")
                val = (1, member.id,)
                cursor.execute(sql, val)
            await ctx.send(f'Given **All** badges to {str(member)}')
        else:
            sql = (f"UPDATE badges SET {badge} = ? WHERE user_id = ?")
            val = (1, member.id,)
            await ctx.send(f'Given **{badge}** to {str(member)}')
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        em = discord.Embed(description=f"{badge} badge(s) were given to {member.mention} [{member.id}] by {ctx.author.mention} [{ctx.author.id}]")
        webhook = discord.SyncWebhook.from_url(webhook_badge_logs)
        webhook.send(embed=em, username=f"{str(self.bot.user)} | Badge Given Logs", avatar_url=self.bot.user.avatar.url)

    @profile.command(name="remove", aliases=["r"], description="Removes the badge from user")
    async def badge_remove(self, ctx, member: discord.User, *, badge):
        ls = workowner
        if ctx.author.id not in ls and ctx.author.id not in self.bot.owner_ids:
            return
        if not badge:
            await ctx.reply("Mention a badge to Remove")
        badge = badge.upper()
        valid = ["ALL", "OWNER", "DEVELOPER", "SPECIAL", "SUPPORTER", "FRIEND", "DONATOR", "BUG"]
        if badge not in valid:
            return await ctx.send("Please send A valid Badge\nASSIGNABLE BADGES ARE: All, Owner, Developer, Special, Supporter, Friend, Donator, Bug")
        db = sqlite3.connect('./database.sqlite3')
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM  badges WHERE user_id = {member.id}")
        result = cursor.fetchone()
        if result is None:
            sql = (f"INSERT INTO badges(user_id) VALUES(?)")
            val = (member.id,)
            cursor.execute(sql, val)
        if badge == "ALL":
            for i in valid[1:]:
                sql = (f"UPDATE badges SET {i} = ? WHERE user_id = ?")
                val = (0, member.id,)
                cursor.execute(sql, val)
            await ctx.send(f'Removed **All** badges from {str(member)}')
        else:
            sql = (f"UPDATE badges SET {badge} = ? WHERE user_id = ?")
            val = (0, member.id,)
            await ctx.send(f'Removed **{badge}** from {str(member)}')
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()
        em = discord.Embed(description=f"{badge} badge(s) were removed from {member.mention} [{member.id}] by {ctx.author.mention} [{ctx.author.id}]")
        webhook = discord.SyncWebhook.from_url(webhook_badge_logs)
        webhook.send(embed=em, username=f"{str(self.bot.user)} | Badge Removed Logs", avatar_url=self.bot.user.avatar.url)

    @commands.group(
        invoke_without_command=True, description="Shows the help menu for list commands"
    )
    async def list(self, ctx):
        ls = ["list", "list joinpos", "list bans", "list mods", "list admins", "list boosters", "list bots", "list inrole", "list roles", "list botemojis", "list emojis", "list early", "list createpos"]
        prefix = ctx.prefix
        if prefix == f"<@{self.bot.user.id}> ":
            prefix = f"@{str(self.bot.user)} "
        stars = discord.utils.get(self.bot.users, id=978930369392951366)
        des = ""
        for i in sorted(ls):
            cmd = self.bot.get_command(i)
            des += f"`{prefix}{i}`\n{cmd.description}\n\n"
        listem = discord.Embed(colour=0xc283fe,
                                     description=f"<...> Duty | [...] Optional\n\n{des}")
        listem.set_author(name=f"{str(ctx.author)}", icon_url=ctx.author.display_avatar.url)
        listem.set_footer(text=f"Made by stars.gg" ,  icon_url=stars.avatar.url)
        await ctx.send(embed=listem)

    @list.command(name="roles", description="Shows all the roles in the server")
    async def list_roles(self, ctx):
        init = await ctx.reply(f"<:loading:1060851548869107782> Processing the command...", mention_author=False)
        ls, roles = [], []
        count = 1
        for role in list(reversed(ctx.guild.roles[1:])):
            roles.append(f"`[{'0' + str(count) if count < 10 else count}]` | {role.mention} `[{role.id}]` - {len(role.members)} Members")
            count += 1
        for i in range(0, len(roles), 10):
           ls.append(roles[i: i + 10])
        em_list = []
        no = 1
        for k in ls:
           embed =discord.Embed(color=0xc283fe)
           embed.title = f"List of Roles in {ctx.guild.name} - {count-1}"
           embed.description = "\n".join(k)
           embed.set_footer(text=f"{self.bot.user.name} • Page {no}/{len(ls)}", icon_url=self.bot.user.display_avatar.url)
           em_list.append(embed)
           no+=1
        page = PaginationView(embed_list=em_list, ctx=ctx)
        await init.delete()
        await page.start(ctx)

    @list.command(name="bots", description="Shows a list of all bots in server")
    async def list_bots(self, ctx):
        init = await ctx.reply(f"<:loading:1060851548869107782> Processing the command...", mention_author=False)
        ls, bots = [], []
        count = 1
        for member in ctx.guild.members:
            if member.bot:
                bots.append(f"`[{'0' + str(count) if count < 10 else count}]` | {member} [{member.mention}]")
                count += 1
        for i in range(0, len(bots), 10):
            ls.append(bots[i: i + 10])
        em_list = []
        no = 1
        for k in ls:
            embed =discord.Embed(color=0xc283fe)
            embed.title = f"Bots in {ctx.guild.name} - {count-1}"
            embed.description = "\n".join(k)
            embed.set_footer(text=f"{self.bot.user.name} • Page {no}/{len(ls)}", icon_url=self.bot.user.display_avatar.url)
            em_list.append(embed)
            no+=1
        page = PaginationView(embed_list=em_list, ctx=ctx)
        await init.delete()
        await page.start(ctx)
    
    @list.command(name="botemojis", description="Shows a list of all emojis the bot can see")
    async def list_botemojis(self, ctx):
        init = await ctx.reply(f"<:loading:1060851548869107782> Processing the command...", mention_author=False)
        ls, emo = [], []
        count = 1
        for emoji in self.bot.emojis:
            emo.append(f"`[{'0' + str(count) if count < 10 else count}]` | {emoji} - \{emoji}")
            count += 1
        for i in range(0, len(emo), 10):
           ls.append(emo[i: i + 10])
        em_list = []
        no = 1
        for k in ls:
           embed =discord.Embed(color=0xc283fe)
           embed.title = f"Emojis the bot can see - {count-1}"
           embed.description = "\n".join(k)
           embed.set_footer(text=f"{self.bot.user.name} • Page {no}/{len(ls)}", icon_url=self.bot.user.display_avatar.url)
           em_list.append(embed)
           no+=1
        page = PaginationView(embed_list=em_list, ctx=ctx)
        await init.delete()
        await page.start(ctx)

    @list.command(name="emojis", description="Shows a list of all emojis in the server")
    async def list_emojis(self, ctx):
        init = await ctx.reply(f"<:loading:1060851548869107782> Processing the command...", mention_author=False)
        ls, emo = [], []
        count = 1
        if not ctx.guild.emojis:
            await init.delete()
            return await ctx.reply("No emojis in the server", mention_author=False)
        for emoji in ctx.guild.emojis:
            emo.append(f"`[{'0' + str(count) if count < 10 else count}]` | {emoji} - \{emoji}")
            count += 1
        for i in range(0, len(emo), 10):
           ls.append(emo[i: i + 10])
        em_list = []
        no = 1
        for k in ls:
           embed =discord.Embed(color=0xc283fe)
           embed.title = f"Emojis in {ctx.guild.name} - {count-1}"
           embed.description = "\n".join(k)
           embed.set_footer(text=f"{self.bot.user.name} • Page {no}/{len(ls)}", icon_url=self.bot.user.display_avatar.url)
           em_list.append(embed)
           no+=1
        page = PaginationView(embed_list=em_list, ctx=ctx)
        await init.delete()
        await page.start(ctx)
        
    @list.command(name="admins", description="Shows a list of all admins in the server")
    async def list_admins(self, ctx):
        init = await ctx.reply(f"<:loading:1060851548869107782> Processing the command...", mention_author=False)
        ls, admins = [], []
        count = 1
        for member in ctx.guild.members:
            if member.guild_permissions.administrator == True:
                if not member.bot:
                    admins.append(f"`[{'0' + str(count) if count < 10 else count}]` | {member} [{member.mention}]")
                    count += 1
        for i in range(0, len(admins), 10):
           ls.append(admins[i: i + 10])
        em_list = []
        no = 1
        for k in ls:
           embed =discord.Embed(color=0xc283fe)
           embed.title = f"Admins in {ctx.guild.name} - {count-1}"
           embed.description = "\n".join(k)
           embed.set_footer(text=f"{self.bot.user.name} • Page {no}/{len(ls)}", icon_url=self.bot.user.display_avatar.url)
           em_list.append(embed)
           no+=1
        page = PaginationView(embed_list=em_list, ctx=ctx)
        await init.delete()
        await page.start(ctx)

    @list.command(name="mods", description="Shows the list of all mods in the server")
    async def list_mods(self, ctx):
        init = await ctx.reply(f"<:loading:1060851548869107782> Processing the command...", mention_author=False)
        ls, mods = [], []
        count = 1
        for member in ctx.guild.members:
            if member.guild_permissions.manage_emojis == True:
                if not member.bot:
                    mods.append(f"`[{'0' + str(count) if count < 10 else count}]` | {member} [{member.mention}]")
                    count += 1
        for i in range(0, len(mods), 10):
           ls.append(mods[i: i + 10])
        em_list = []
        no = 1
        for k in ls:
           embed =discord.Embed(color=0xc283fe)
           embed.title = f"Mods in {ctx.guild.name} - {count-1}"
           embed.description = "\n".join(k)
           embed.set_footer(text=f"{self.bot.user.name} • Page {no}/{len(ls)}", icon_url=self.bot.user.display_avatar.url)
           em_list.append(embed)
           no+=1
        page = PaginationView(embed_list=em_list, ctx=ctx)
        await init.delete()
        await page.start(ctx)
        
    @list.command(name="bans", description="Shows the list of banned members in the server")
    async def list_bans(self, ctx):
        init = await ctx.reply(f"<:loading:1060851548869107782> Processing the command...", mention_author=False)
        ls, bans = [], []
        count = 1
        xd = [member async for member in ctx.guild.bans()]
        if len(xd) == 0:
            await init.delete()
            return await ctx.reply("There aren't any banned users.", mention_author=False)
        async for member in ctx.guild.bans():
            bans.append(f"`[{'0' + str(count) if count < 10 else count}]` | {member.user} `[{member.user.id}]`")
            count += 1
        for i in range(0, len(bans), 10):
           ls.append(bans[i: i + 10])
        em_list = []
        no = 1
        for k in ls:
           embed =discord.Embed(color=0xc283fe)
           embed.title = f"Banned Users in {ctx.guild.name} - {count-1}"
           embed.description = "\n".join(k)
           embed.set_footer(text=f"{self.bot.user.name} • Page {no}/{len(ls)}", icon_url=self.bot.user.display_avatar.url)
           em_list.append(embed)
           no+=1
        page = PaginationView(embed_list=em_list, ctx=ctx)
        init = await ctx.reply(f"<:loading:1060851548869107782> Processing the command...", mention_author=False)
        await page.start(ctx)
        
    @list.command(name="inrole", description="Shows the list of members in a role")
    async def list_inrole(self, ctx, *,role: discord.Role):
        init = await ctx.reply(f"<:loading:1060851548869107782> Processing the command...", mention_author=False)
        ls, inrole = [], []
        count = 1
        xd = [member for member in role.members]
        if len(xd) == 0:
            await init.delete()
            return await ctx.reply("There aren't any users in this role.", mention_author=False)
        for member in role.members:
            inrole.append(f"`[{'0' + str(count) if count < 10 else count}]` | {member} [{member.mention}] - [{member.id}]")
            count += 1
        for i in range(0, len(inrole), 10):
           ls.append(inrole[i: i + 10])
        em_list = []
        no = 1
        for k in ls:
           embed =discord.Embed(color=0xc283fe)
           embed.title = f"Members in Role {role.name} - {count-1}"
           embed.description = "\n".join(k)
           embed.set_footer(text=f"{self.bot.user.name} • Page {no}/{len(ls)}", icon_url=self.bot.user.display_avatar.url)
           em_list.append(embed)
           no+=1
        page = PaginationView(embed_list=em_list, ctx=ctx)
        await init.delete()
        await page.start(ctx)

    @list.command(name="boosters", description="Shows the list of boosters of the server")
    async def list_boosters(self, ctx):
        init = await ctx.reply(f"<:loading:1060851548869107782> Processing the command...", mention_author=False)
        ls, boosters = [], []
        count = 1
        xd = [member for member in ctx.guild.premium_subscribers]
        if len(xd) == 0:
            await init.delete()
            return await ctx.reply("There aren't any boosters in this server.", mention_author=False)
        for member in ctx.guild.premium_subscribers:
            boosters.append(f"`[{'0' + str(count) if count < 10 else count}]` | {member} [{member.mention}] - <t:{int(member.premium_since.timestamp())}:R>")
            count += 1
        for i in range(0, len(boosters), 10):
           ls.append(boosters[i: i + 10])
        em_list = []
        no = 1
        for k in ls:
           embed =discord.Embed(color=0xc283fe)
           embed.title = f"Boosters in {ctx.guild.name} - {count-1}"
           embed.description = "\n".join(k)
           embed.set_footer(text=f"{self.bot.user.name} • Page {no}/{len(ls)}", icon_url=self.bot.user.display_avatar.url)
           em_list.append(embed)
           no+=1
        page = PaginationView(embed_list=em_list, ctx=ctx)
        await init.delete()
        await page.start(ctx)

    @list.command(name='early', description="Shows the list of early supporter ids in the server")
    async def list_early(self, ctx):
        init = await ctx.reply(f"<:loading:1060851548869107782> Processing the command...", mention_author=False)
        mem = {}
        for member in ctx.guild.members:
            if member.public_flags.early_supporter == True:
                mem[member.created_at.timestamp()] = member
        if mem == "{}":
            await init.delete()
            return await ctx.reply("No early ids in the server", mention_author=False)
        ls, early = [], []
        count = 1
        for m in sorted(mem):
                early.append(f"`[{'0' + str(count) if count < 10 else count}]` | {mem[m]} [{mem[m].mention}] - <t:{round(mem[m].created_at.timestamp())}:R>")
                count += 1
        if count == 1:
            return await ctx.reply("No early ids in the server", mention_author=False)
        for i in range(0, len(early), 10):
            ls.append(early[i: i + 10])
        em_list = []
        no = 1
        for k in ls:
            embed =discord.Embed(color=0xc283fe)
            embed.title = f"Early Id's in {ctx.guild.name} - {count-1}"
            embed.description = "\n".join(k)
            embed.set_footer(text=f"{self.bot.user.name} • Page {no}/{len(ls)}", icon_url=self.bot.user.display_avatar.url)
            em_list.append(embed)
            no+=1
        page = PaginationView(embed_list=em_list, ctx=ctx)
        await init.delete()
        await page.start(ctx)

    @list.command(name="joinpos", description="Shows the join position of every user in the server")
    async def list_joinpos(self, ctx):
        init = await ctx.reply(f"<:loading:1060851548869107782> Processing the command...", mention_author=False)
        mem = {}
        for member in ctx.guild.members:
            mem[member.joined_at.timestamp()] = member
        ls, count = [], 1
        joinpos = []
        for _t in sorted(mem):
            joinpos.append(f"`[{'0' + str(count) if count < 10 else count}]` | {mem[_t]} - Joined: <t:{round(mem[_t].joined_at.timestamp())}:R>")
            count += 1
        for i in range(0, len(joinpos), 10):
           ls.append(joinpos[i: i + 10])
        em_list = []
        no = 1
        for k in ls:
           embed =discord.Embed(color=0xc283fe)
           embed.title = f"Join Position of every user in {ctx.guild.name} - {count-1}"
           embed.description = "\n".join(k)
           embed.set_footer(text=f"{self.bot.user.name} • Page {no}/{len(ls)}", icon_url=self.bot.user.display_avatar.url)
           em_list.append(embed)
           no+=1
        page = PaginationView(embed_list=em_list, ctx=ctx)
        await init.delete()
        await page.start(ctx)
        
    @list.command(name="createpos", description="Shows the position of creation of all id in the server")
    async def list_createpos(self, ctx):
        init = await ctx.reply(f"<:loading:1060851548869107782> Processing the command...", mention_author=False)
        mem = {}
        view = create(ctx)
        em = discord.Embed(description="Which type of Members you want to see?", color=0xc283fe)
        ok = await ctx.reply(embed=em, view=view, mention_author=False)
        await view.wait()
        if not view.value:
            await ctx.send("Timed Out")
        if view.value == 'users':
            for member in ctx.guild.members:
              if not member.bot:
                mem[member.created_at.timestamp()] = member
        if view.value == 'bots':
            for member in ctx.guild.members:
              if member.bot:
                mem[member.created_at.timestamp()] = member
        if view.value == 'both':
            for member in ctx.guild.members:
                mem[member.created_at.timestamp()] = member
        await ok.delete()
        ls, count = [], 1
        joinpos = []
        for _t in sorted(mem):
            joinpos.append(f"`[{'0' + str(count) if count < 10 else count}]` | {mem[_t]} - Created at: <t:{round(mem[_t].created_at.timestamp())}:R>")
            count += 1
        for i in range(0, len(joinpos), 10):
           ls.append(joinpos[i: i + 10])
        em_list = []
        no = 1
        for k in ls:
           embed =discord.Embed(color=0xc283fe)
           embed.title = f"Creation every id in {ctx.guild.name} - {count-1}"
           embed.description = "\n".join(k)
           embed.set_footer(text=f"{self.bot.user.name} • Page {no}/{len(ls)}", icon_url=self.bot.user.display_avatar.url)
           em_list.append(embed)
           no+=1
        page = PaginationView(embed_list=em_list, ctx=ctx)
        await init.delete()
        await page.start(ctx)
        
    @commands.command(aliases=["ms"], description="Show's the Ping of bot")
    @commands.guild_only()
    async def ping(self, ctx: commands.Context):
      pfp = ctx.author.display_avatar.url
      s_id = ctx.guild.shard_id
      sh = self.bot.get_shard(s_id)
      embed = discord.Embed(description=f"**Message ping:** {round(sh.latency * 1000)} ms ", colour=0xc283fe)
      embed.set_author(name=f"| Bot latency", icon_url=pfp)
      embed.timestamp = datetime.datetime.utcnow()
      await ctx.reply(embed=embed, mention_author = False)

    @commands.command(aliases=["si"], description="Shows information about this server")
    async def serverinfo(self, ctx):
        humans = [member for member in ctx.guild.members if not member.bot]
        bots = [member for member in ctx.guild.members if member.bot]
        text_channels = len(ctx.guild.text_channels)
        voice_channels = len(ctx.guild.voice_channels)
        cats = len(ctx.guild.categories)
        chs = len(ctx.guild.channels)
        channels = cats + text_channels + voice_channels
        emotes = len(ctx.guild.emojis)
        emoslots = ctx.guild.emoji_limit
        regular = [emoji for emoji in ctx.guild.emojis if not emoji.animated]
        animated = [emoji for emoji in ctx.guild.emojis if emoji.animated]
        #
        general = [
            f'Name: {ctx.guild.name} ( ID: {ctx.guild.id} )',
            f'Owner: {ctx.guild.owner.mention} ( ID: {str(ctx.guild.owner.id)} )',
            f'Created: <t:{round(ctx.guild.created_at.timestamp())}> ( <t:{round(ctx.guild.created_at.timestamp())}:R> )',
            f'Members: {len(ctx.guild.members)} ( <:person:1158085258961490005> {len(humans)} | <:bot:1158073835439018015> {len(bots)} )',
            f'Roles: {len(ctx.guild.roles)}'
        ]
        if ctx.guild.vanity_url_code is not None:
            general.append(f'Vanity: [{ctx.guild.vanity_url_code}]({ctx.guild.vanity_url})')
        #
        channels = [
            f'<:category:1158316329540001823> Category: {cats}',
            f'<:text:1158316318488010935> Text: {text_channels}',
            f'<:voice:1158316323529564190> Voice: {voice_channels}'
        ]
        if ctx.guild.rules_channel is not None:
            channels.append(f'<:rules:1158316316382482432> Rules: {ctx.guild.rules_channel.mention}')
        
        emojis = [
            f'Regular: {len(regular)} / {emoslots}',
            f'Animated: {len(animated)} / {emoslots}'
        ]
        boosts = [
            f'Level: {ctx.guild.premium_tier}',
            f'Count: {ctx.guild.premium_subscription_count}'
        ]
        if ctx.guild.premium_subscriber_role is not None:
            boosts.append(f'Role: {ctx.guild.premium_subscriber_role.mention}')
        #
        nums = [ "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine" ]
        features = []
        if len(ctx.guild.features) > 0:
            for i in ctx.guild.features:
                c = i.split("_")
                v = []
                for j in c:
                    if j.lower() in nums:
                        v.append(str(nums.index(j.lower())))
                    else:
                        v.append(j.title())
                features.append("<:tick_gandway:1156895119853752410> " + " ".join(v))

        icon_url = ""
        if ctx.guild.icon is not None:
            icon_url = ctx.guild.icon.url
        elif ctx.author.avatar is not None:
            icon_url = ctx.author.display_avatar.url
        else:
            icon_url = self.bot.user.display_avatar.url
        #
        pfp = ctx.author.display_avatar.url
        
        serverinfo = discord.Embed(colour=0xc283fe)
        if ctx.guild.banner is not None:
            serverinfo.set_image(url=ctx.guild.banner.url)
        
        serverinfo.set_thumbnail(url=icon_url)
        serverinfo.set_author(name=f"{ctx.guild.name}'s Information", icon_url=icon_url)
        serverinfo.add_field(name="General", value="\n".join(general), inline=False)
        serverinfo.add_field(name=f"Channels [{chs}]", value="\n".join(channels), inline=False)
        if emotes > 0:
            serverinfo.add_field(name=f"Emojis [{emotes}]", value="\n".join(emojis), inline=False)
        if ctx.guild.premium_tier > 0:
            serverinfo.add_field(name=f"Boosts", value="\n".join(boosts), inline=False)
        if(len(features) > 0):
            serverinfo.add_field(name=f"Perks", value="\n".join(features[:17]), inline=False)
        #
        serverinfo.set_footer(text=f"Requested by {ctx.author.name}" ,  icon_url=pfp)
        
        if ctx.guild.description is not None:
            serverinfo.description = ctx.guild.description
        #
        await ctx.send(embed=serverinfo)

    @commands.command(aliases=["ri"], description="Shows information about the Role")
    async def roleinfo(self, ctx, role: discord.Role):
        roleinfo = discord.Embed(colour=0xc283fe, title=f"{role.name}'s Information")
        roleinfo.add_field(name="Role Information:",
                                 value=f"**Role Name:** {role.name}\n"
                                       f"**Role ID:** {role.id}\n"
                                       f"**Role Position:** {role.position}\n"
                                       f"**Hex code:** {str(role.color)}\n"
                                       f"**Created At:** <t:{round(role.created_at.timestamp())}:R>\n"
                                       f"**Mentionability:** {role.mentionable}\n"
                                       f"**Separated:** {role.hoist}\n"
                                       f"**Integration:** {role.is_bot_managed()}\n", inline=False)
        role_perm = ', '.join([str(p[0]).replace("_", " ").title() for p in role.permissions if p[1]])
        if role_perm is None:
            role_perm = "No permissions"
        roleinfo.add_field(name="Allowed Permissions:",
                                 value=role_perm, inline=False)
        if len(role.members) != 0:
            role_memb = [m.mention for m in role.members]
            role_mem = ""
            if len(role.members) > 15:
                role_mem = "Too many Members to show here"
            else:
                role_mem = str(role_memb).replace("'", "").replace("[", "").replace("]", "")
            roleinfo.add_field(name=f"Role Members [{len(role.members)}]:",
                                     value=role_mem, inline=False)
        await ctx.send(embed=roleinfo)

    #@commands.command(description="Shows status information about the user")
    async def status(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        pfp = ctx.author.display_avatar.url
        dnd = ("<:dnd:1060577788949713016>")
        on = ("<:online:1060577713871663135>")
        idlee = ("<:idle:1060577756141846598>")
        off = ("<:offline:1060577845862203433>")
        mobile = ("<:mobile:1060590518834319511>")
        desktop = ("<:desktop:1060589563078254592>")
        web = ("<:browser:1060589628849127484>")
        activity = ("<:activity:1060590224444489870>")
        if member.status == discord.Status.online:
            st = f"{on} Online"
        elif member.status == discord.Status.idle:
            st = f"{idlee} Idle"
        elif member.status == discord.Status.dnd:
            st = f"{dnd} Do Not Disturb"
        else:
            st = f"{off} Invisible"
        d = []
        if member.status == discord.Status.offline:
            d.append("None")
        elif member.mobile_status == member.status:
            d.append(f"{mobile} Mobile")
        elif member.desktop_status == member.status:
            d.append(f"{desktop} Desktop")
        elif member.web_status == member.status:
            d.append(f"{web} Browser")
        dd = "\n".join(d)
        em = discord.Embed(title=f"Status information of {str(member)}", color=0xc283fe)
        em.add_field(name="Status", value=st, inline=False)
        em.add_field(name="Device", value=dd, inline=False)
        em.add_field(name="Activity", value=str(member.activity), inline=False)
        if ctx.author.avatar:
            i = ctx.author.display_avatar.url
        else:
            i = None
        em.set_footer(text=f"Requested by {str(ctx.author)}", icon_url=i)
        await ctx.reply(embed=em, mention_author=False)

    @commands.command(aliases=["ui", "whois"], description="Shows information about the user")
    async def userinfo(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        pfp = ctx.author.display_avatar.url
        dnd = ("<:dnd:1060577788949713016>")
        on = ("<:online:1060577713871663135>")
        idlee = ("<:idle:1060577756141846598>")
        off = ("<:offline:1060577845862203433>")
        mobile = ("<:mobile:1060590518834319511>")
        desktop = ("<:desktop:1060589563078254592>")
        web = ("<:browser:1060589628849127484>")
        activity = ("<:activity:1060590224444489870>")
        if member in ctx.guild.members:
            order = sorted(ctx.guild.members, key=lambda member: member.joined_at or discord.utils.utcnow()).index(member) + 1
        nitro = ("<:BadgeNitro:935510739886694410> ")
        boost = ("<a:booster:935500316495978536> ")
        balance = ("<:balance:933685821092016158> ")
        bravery = ("<:bravery:933685857582448671> ")
        brillance = ("<:brillance:933685893024337980> ")
        bug_1 = ("<:bug_hunter_1:933685410738085899> ")
        bug_2 = ("<:bug_hunter_2:933685491486847036> ")
        early = ("<:early_sup:933685551012397107> ")
        hype = ("<a:hype:933685735905710080> ")
        partner = ("<:partner:933685923567251517> ")
        staff = ("<a:staff:933685961932558337> ")
        system = ("<:system:933686023995682848> ")
        veri_bot = ("<:verified_bot:933686190920564736> ")
        veri_dev = ("<:verified_dev:933685666477379647> ")
        act_dev = ("<:active_developer:1040478576581029928> ")
        badge = ""
        if member.public_flags.bug_hunter == True:
            badge += bug_1
        if member.public_flags.bug_hunter_level_2 == True:
            badge += bug_2
        if member.public_flags.hypesquad_bravery == True:
            badge += bravery
        if member.public_flags.hypesquad_balance == True:
            badge += balance
        if member.public_flags.hypesquad_brilliance == True:
            badge += brillance
        if member.public_flags.hypesquad == True:
            badge += hype
        if member.public_flags.early_supporter == True:
            badge += early
        if member.public_flags.early_verified_bot_developer == True:
            badge += veri_dev
        if member.public_flags.verified_bot == True:
            badge += veri_bot
        if member.public_flags.staff == True:
            badge += staff
        if member.public_flags.system == True:
            badge += system
        if member.public_flags.partner == True:
            badge += partner
        if member.public_flags.active_developer == True:
            badge += act_dev
        if not badge:
            badge = "None"
        achive = ""
        emote = ("<a:rightarrow:988109002443464804>")
        query = "SELECT * FROM  titles WHERE user_id = ?"
        val = (member.id,)
        with sqlite3.connect('./database.sqlite3') as db:
          db.row_factory = sqlite3.Row
          cursor = db.cursor()
          cursor.execute(query, val)
          user_columns = cursor.fetchone()
        des = ""
        if user_columns is None:
          des = None
        else:
            des = user_columns['title']
        member = ctx.author if not member else member
        if member in ctx.guild.members:
            member_roles = len(member.roles)
            if member_roles < 20:
                role_string = ' • '.join([r.mention for r in reversed(member.roles)][:-1])
                member_roles = role_string
            else:
                member_roles = "Too many roles to show here."
        userinfo = discord.Embed(colour=0xc283fe, title=f"{member.name}'s profile")
        userinfo.add_field(name="<:tick_gandway:1156895119853752410>General Information:",
                                 value=f"**Name:** {member}\n"
                                       f"**ID:** {member.id}\n"
                                       f"**Nick:** {member.nick}\n"
                                       f"**Join Pos**: {order}/{len(ctx.guild.members)}\n"
                                       f"**Badge**: {badge}\n"
                                       f"**Account Creation:** <t:{round(member.created_at.timestamp())}:R>\n"
                                       f"**Server Joined:** <t:{round(member.joined_at.timestamp())}:R>\n", inline=False)
        userinfo.add_field(name="<:rules:1158316316382482432>Role Info:",
                                value=f"**Top Role:** {member.top_role.mention}\n"
                                    f"**Roles [{(len(member.roles)-1)}]:** {member_roles}\n"
                                    f"**Color:** {str(member.color)}", inline=False)
        if member in ctx.guild.members:
            perm_string = ""
            if member.guild_permissions.administrator == True:
                admin = "Administrator, "
                perm_string +=admin
            if member.guild_permissions.kick_members == True:
                kick = "Kick Members, "
                perm_string +=kick
            if member.guild_permissions.ban_members == True:
                ban = "Ban Members, "
                perm_string +=ban
            if member.guild_permissions.manage_channels == True:
                mc = "Manage Channels, "
                perm_string +=mc
            if member.guild_permissions.manage_guild == True:
                ms = "Manage Server, "
                perm_string +=ms
            if member.guild_permissions.manage_messages == True:
                mm = "Manage Messages, "
                perm_string +=mm
            if member.guild_permissions.mention_everyone == True:
                me = "Mention Everyone, "
                perm_string +=me
            if member.guild_permissions.manage_nicknames == True:
                mn = "Manage Nicknames, "
                perm_string +=mn
            if member.guild_permissions.manage_roles == True:
                mr = "Manage Roles, "
                perm_string +=mr
            if member.guild_permissions.manage_webhooks == True:
                mw = "Manage Webhooks, "
                perm_string +=mw
            if member.guild_permissions.manage_emojis == True:
                me = "Manage Emojis, "
                perm_string +=me
            if perm_string != "":
                userinfo.add_field(name="<:Untitled1:1155962780298530856>Key permissions:", value=perm_string[:-2], inline=False)
            else:
                pass
            if ctx.guild.owner.id == member.id:
                so = "**SERVER OWNER**"
                achive = so
            else:
                if member.guild_permissions.administrator == True:
                    sa = "**SERVER ADMIN**"
                    achive = sa
                elif member.guild_permissions.manage_guild == True:
                        sm = "**SERVER MANAGER**"
                        achive = sm
                else:
                    if member.guild_permissions.manage_messages == True:
                        sms = "**SERVER MODERATOR**"
                        achive = sms
            if achive != "":
                userinfo.add_field(name="<:Untitled3:1155962794244575353> Acknowledgements:", value=achive.title(), inline=False)
            else:
                pass
        if des is not None:
            userinfo.add_field(name="Bot Title:", value=f"**{des.title()}**", inline=False)
        usr = await self.bot.fetch_user(member.id)
        if usr.banner:
            banner = usr.banner.url
            userinfo.set_image(url=banner)
        userinfo.set_footer(text=f"Requested by {ctx.author.name}" ,  icon_url=pfp)
        if member.avatar is not None:
           userinfo.set_thumbnail(url=member.display_avatar.url)
        await ctx.send(embed=userinfo)
        
    @commands.command(description="Shows the server icon")
    async def servericon(self, ctx):
         pfp = ctx.author.display_avatar.url
         em=discord.Embed(title="SERVER ICON", color=0xc283fe)
         em.set_image(url=ctx.guild.icon.url)
         em.set_footer(text=f"Requested by {ctx.author.name}" ,  icon_url=pfp)
         await ctx.send(embed=em)

    @commands.command(aliases=["av"], brief="Avatar", description="Shows the avatar of user")
    @commands.guild_only()
    async def avatar(self, ctx, member: Union[discord.Member, discord.User] = None):
        member = (
            member or ctx.author
        )
        if isinstance(member, discord.User):
            if member in ctx.guild.members:
                member = discord.utils.get(ctx.guild.members, id=member.id)
            else:
                member = member
        if not member.avatar:
            await ctx.reply(f"There is no avatar for {str(member)}")
            return
        if member.avatar.url != member.display_avatar.url:
            em = discord.Embed(description="Which avatar would you like to see?", color=0xc283fe)
            view = OnOrOff(ctx)
            hm = await ctx.reply(embed = em, view=view, mention_author=False)
            await view.wait()
            if view.value == 'Yes':
                await hm.delete()
                pfp=member.avatar.url
                if "gif" in pfp:
                    des = f'[PNG]({pfp.replace("gif", "png").replace("webp", "png").replace("jpeg", "png")}) | [GIF]({pfp})'
                else:
                  if "png" or "jpeg" or "webp" in pfp:
                    des = f'[PNG]({pfp.replace("webp", "png").replace("jpeg", "png")})'
                embed = discord.Embed(title=str(member), description=des, color=0xc283fe)
                embed.set_image(url=pfp)
                embed.set_footer(text=f"Requested by {ctx.author.name}" ,  icon_url=pfp)
                return await ctx.send(embed=embed)
            if view.value == 'No':
                await hm.delete()
                pfp=member.display_avatar.url
                

                if "gif" in pfp:
                    des = f'[PNG]({pfp.replace("gif", "png").replace("webp", "png").replace("jpeg", "png")}) | [GIF]({pfp})'
                else:
                  if "png" or "jpeg" or "webp" in pfp:
                    des = f'[PNG]({pfp.replace("webp", "png").replace("jpeg", "png")})'
                embed = discord.Embed(title=str(member), description=des, color=0xc283fe)
                embed.set_image(url=pfp)
                embed.set_footer(text=f"Requested by {ctx.author.name}" ,  icon_url=ctx.author.display_avatar.url)
                return await ctx.send(embed=embed)
        else:
            pfp=member.avatar.url
            if "gif" in pfp:
                    des = f'[PNG]({pfp.replace("gif", "png").replace("webp", "png").replace("jpeg", "png")}) | [GIF]({pfp})'
            else:
                if "png" or "jpeg" or "webp" in pfp:
                    des = f'[PNG]({pfp.replace("webp", "png").replace("jpeg", "png")})'
            embed = discord.Embed(title=str(member), description=des, color=0xc283fe)
            embed.set_image(url=pfp)
            embed.set_footer(text=f"Requested by {ctx.author.name}" ,  icon_url=ctx.author.display_avatar.url)
            return await ctx.send(embed=embed)
    
    @commands.group(name="banner",invoke_without_command=True, description="Shows the banner's help menu")
    async def banner(self, ctx):
        prefix = ctx.prefix
        if prefix == f"<@{self.bot.user.id}> ":
            prefix = f"@{str(self.bot.user)} "
        stars = discord.utils.get(self.bot.users, id=978930369392951366)
        ls = ["banner", "banner user", "banner server"]
        des = ""
        for i in sorted(ls):
            cmd = self.bot.get_command(i)
            if cmd.description is None:
                cmd.description = "No Description"
            des += f"`{prefix}{i}`\n{cmd.description}\n\n"
        listem = discord.Embed(title=f"Banner Commands", colour=0xc283fe,
                                     description=f"<...> Duty | [...] Optional\n\n{des}")
        listem.set_author(name=f"{str(ctx.author)}", icon_url=ctx.author.display_avatar.url)
        listem.set_footer(text=f"Made by stars.gg" ,  icon_url=stars.avatar.url)
        await ctx.send(embed=listem)

    @banner.command(name="user", description="Shows the user's banner")
    async def user_banner(self, ctx, *, member: discord.Member = None):
        member = member or ctx.author
        member = await self.bot.fetch_user(member.id)
        em = discord.Embed(color=0xc283fe)
        em.set_author(name=str(member), icon_url=member.display_avatar.url)
        em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
        if member.banner is None:
            em.description = f"`{str(member)}` doesn't have any banner"
            return await ctx.reply(embed=em)
        else:
            pfp=member.banner.url
            if "gif" in pfp:
                des = f'[PNG]({pfp.replace("gif", "png").replace("webp", "png").replace("jpeg", "png")}) | [GIF]({pfp})'
            else:
                if "png" or "jpeg" or "webp" in pfp:
                    des = f'[PNG]({pfp.replace("webp", "png").replace("jpeg", "png")})'
            em.description = des
            em.set_image(url=pfp)
            await ctx.reply(embed=em)

    @banner.command(name="server", description="Shows the server's banner")
    async def server_banner(self, ctx):
        em = discord.Embed(color=0xc283fe)
        em.set_author(name=str(ctx.guild.name))
        em.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
        if ctx.guild.banner is None:
            em.description = f"The server doesn't have any banner"
            return await ctx.reply(embed=em)
        else:
            pfp=ctx.guild.banner.url
            if "gif" in pfp:
                des = f'[PNG]({pfp.replace("gif", "png").replace("webp", "png").replace("jpeg", "png")}) | [GIF]({pfp})'
            else:
                if "png" or "jpeg" or "webp" in pfp:
                    des = f'[PNG]({pfp.replace("webp", "png").replace("jpeg", "png")})'
            em.description = des
            em.set_image(url=pfp)
            await ctx.reply(embed=em)

    #@commands.command(name='first-message', aliases=['firstmsg', 'fm', 'firstmessage'], description="Shows the first message of the channel")
    async def _first_message(self, ctx, channel: discord.TextChannel = None):
        pfp = ctx.author.display_avatar.url
        if channel is None:
            channel = ctx.channel
        first_message = (await channel.history(limit=1, oldest_first=True).flatten())[0]
        embed = discord.Embed(description=f"> {first_message.content}", color=0xc283fe)
        embed.add_field(name="First Message", value=f"[Jump]({first_message.jump_url})")
        embed.set_footer(text=f"Requested by {ctx.author.name}" ,  icon_url=pfp)
        await ctx.send(embed=embed)
        
    @commands.command(aliases=["mc"], description="Returns the members count for the server")
    async def membercount(self, ctx):
        humans = [member for member in ctx.guild.members if not member.bot]
        bots = [member for member in ctx.guild.members if member.bot]
        embed = discord.Embed(title=f"Member Count", color=0x2f3236)
        embed.add_field(name=f"**Total Members:**", value=f"{len(ctx.guild.members)} Members")
        embed.add_field(name=f"**Total Humans:**", value=f"{len(humans)} Members")
        embed.add_field(name=f"**Total Bots:**", value=f"{len(bots)} Members")
        await ctx.reply(embed=embed)
        
    #@commands.command(aliases=["smc"], description="Returns the status members count for the server")
    async def statusmembercount(self, ctx):
        on = [member for member in ctx.guild.members if member.status == discord.Status.online]
        dnd = [member for member in ctx.guild.members if member.status == discord.Status.dnd]
        off = [member for member in ctx.guild.members if member.status == discord.Status.offline]
        idle = [member for member in ctx.guild.members if member.status == discord.Status.idle]
        embed = discord.Embed(title=f"Member Count", color=0x2f3236)
        embed.add_field(name=f"**<:online:1060577713871663135> Online:**", value=f"{len(on)} Members")
        embed.add_field(name=f"**<:idle:1060577756141846598> Idle:**", value=f"{len(idle)} Members")
        embed.add_field(name=f"**<:dnd:1060577788949713016> Dnd:**", value=f"{len(dnd)} Members")
        embed.add_field(name=f"**<:offline:1060577845862203433>Offline:**", value=f"{len(off)} Members")
        if ctx.guild.icon:
            i = ctx.guild.icon.url
        else:
            i = self.bot.user.avatar.url
        embed.set_footer(text=f"{len(ctx.guild.members)} Total Members", icon_url=i)
        await ctx.reply(embed=embed)

    @commands.command(name="google", aliases=["googlesearch"], description="Search google for your query and returns the top 10 results")
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def google(self, ctx, *, search: str):
        """Simple google search Engine"""
        search = urllib.parse.quote(search)

        url = f"https://www.googleapis.com/customsearch/v1?key={google_key}&cx={cx}&q={search}"
        async with requests.Session() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    json_ = await response.json()
                else:
                    return await ctx.reply(
                        f"{ctx.author.mention} No results found.```\n{search}```"
                    )

        pages = []
        count = 1

        for item in json_["items"]:
            title = item["title"]
            link = item["link"]
            displaylink = item["displayLink"]
            snippet = item.get("snippet")
            try:
                img = item["pagemap"]["cse_thumbnail"][0]["src"]
            except KeyError:
                img = None
            em = discord.Embed(
                title=f"{title}",
                description=f"{snippet}",
                timestamp=datetime.datetime.utcnow(),
                url=f"{link}",
            )
            em.set_author(name=str(self.bot.user), icon_url=self.bot.user.display_avatar.url)
            em.set_footer(text=f"{str(ctx.author)} • Page {count}/10 ", icon_url=ctx.author.display_avatar.url)
            count +=1
            if not img:
                pass
            else:
                em.set_thumbnail(url=img)
            pages.append(em)

        page = PaginationView(embed_list=pages, ctx=ctx)
        await page.start(ctx)
        
async def setup(bot):
    await bot.add_cog(general(bot))
