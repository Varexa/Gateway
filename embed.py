from ast import literal_eval
import discord
from discord.ext import commands
import asyncio
import requests
import matplotlib
from dump.converter import *

xdd = {}

memc = {}

async def memcount(guild, id, dic: dict):
    if id not in memc:
        memc[id] = {}
        ls = {}
    else:
        ls = memc[id]["new"]
    memc[id]["old"] = dic.copy()
    ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])
    for i in dic:
        if "$membercount" in str(dic[i]) or "$membercount_ordinal" in str(dic[i]):
            ls[i] = str(dic[i]).replace("$membercount_ordinal", ordinal(len(guild.members))).replace("$membercount", str(len(guild.members)))
            dic[i] = ls[i]
    for i in dic:
        try:
            if i == 'author' or i == 'footer' or i == 'thumbnail' or i == 'fields' or i == 'image':
                dic[i] = literal_eval(dic[i])
        except:
            pass
    memc[id]["new"] = ls
    return dic

async def umemccount(id, dic):
    if id not in memc:
        memc[id] = {}
        memc[id]["new"] = {}
        memc[id]["old"] = dic
    else:
        dc = memc[id]["new"]
        dcc = memc[id]["old"]
        for i in dic:
            if i in dc:
                if str(dic[i]) == str(dc[i]):
                    dic[i] = dcc[i]
                else:
                    pass
        for i in dic:
            try:
                if i == 'author' or i == 'footer' or i == 'thumbnail' or i == 'fields' or i == 'image':
                    dic[i] = literal_eval(dic[i])
            except:
                pass
    return dic

async def getembed(guild, member, id, b: bool=None):
    if id not in xdd:
        return 0
    else:
        x = await convert_sample_embed(guild, member, xdd[id])
        #if b is None:
            #x = await memcount(guild, id, x)
        return x

async def updateembed(id, emb: dict):
    #emb = await umemccount(id, emb)
    xdd[id] = emb
    return True

async def delembed(id):
    del xdd[id]
    return True

async def checkimage(message: discord.Message, url=None):
    if url is not None:
        if "https://" in url:
            try:
                image_formats = ("image/png", "image/jpeg", "image/jpg", "image/gif", "image/webp")
                r = requests.head(url)
                if r.headers["content-type"] not in image_formats:
                    return 0
            except:
                return 0
            urll = url
        elif url == '$user_avatar':
            urll = message.author.display_avatar.url
        elif url == "$server_icon":
            if message.guild.icon:
                urll = message.guild.icon.url
            else:
                urll = None
        else:
            return 0
    else:
        urll = ""
        for xd in message.attachments:
            urll = xd.url
    if urll == "":
        return 0
    else:
        return urll

async def checkcolor(color):
    try:
        color = matplotlib.colors.cnames[color.lower()]
    except:
        color = color
    color = str(color).replace("#", "")
    try:
        color = int(color, base=16)
    except:
        return 0
    return color

class embedMenu(discord.ui.Select):
    def __init__(self, bot, ctx: commands.Context, id):
        options = [
            discord.SelectOption(label='Author', value="author"),
            discord.SelectOption(label='Author icon url', value="authoriurl"),
            discord.SelectOption(label='Author url', value="authorurl"),
            discord.SelectOption(label='Title', value="title"),
            discord.SelectOption(label='Description', value="des"),
            discord.SelectOption(label='Add Field', value="field"),
            discord.SelectOption(label='Thumbnail', value="thumb"),
            discord.SelectOption(label='Image', value="img"),
            discord.SelectOption(label='Footer', value="foot"),
            discord.SelectOption(label='Footer Icon', value="footi"),
            discord.SelectOption(label='Color', value="color")
        ]
        super().__init__(placeholder="Select specific element of embed you want to edit",
            min_values=1,
            max_values=1,
            options=options,
        )
        self.ctx = ctx
        self.bot = bot
        self.id = id

    async def on_timeout(self) -> None:
        try:
            if self.message:
                await self.message.edit(view=None)
        except:
            pass

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False, thinking=False)
        def message_check(m):
             return ( 
                 m.author.id == interaction.user.id
                 and m.channel == interaction.message.channel
             )
        em = await getembed(self.ctx.guild, self.ctx.author, self.id)
        em = discord.Embed.from_dict(em)
        if self.values[0] == 'author':
            init = await interaction.message.channel.send("What should be the author of the embed?\nType 'none' if don't want anything.")
            try:
                    user_response = await interaction.client.wait_for("message", timeout=120, check=message_check)
                    await user_response.delete()
            except asyncio.TimeoutError:
                await interaction.message.channel.send(embed=discord.Embed(
                    title="Error",
                    color=0xc283fe,
                    description="You took too long to answer this question"
                ))
                await interaction.delete_original_response()
                await init.delete()
                self.stop()
            if em.author.icon_url:
                i = em.author.icon_url
            else:
                i = None
            if em.author.url:
                u = em.author.url
            else:
                u = None
            if user_response.content.lower().strip() == "none":
                n = "\u200B"
            else:
                n = user_response.content
            if i is not None or u is not None or n != "\u200B":
                em.set_author(name=n, icon_url=i, url=u)
            elif user_response.content.lower().strip() == "none":
                em.remove_author()
            await updateembed(self.id, em.to_dict())
            em = await getembed(self.ctx.guild, self.ctx.author, self.id)
            em = discord.Embed.from_dict(em)
            try:
                await interaction.edit_original_response(embed=em, view=self.view)
            except:
                await interaction.message.channel.send("A error occured it may be because you exceeded the characters limit")
                await interaction.delete_original_response()
                await init.delete()
                self.stop()
            await init.delete()
        elif self.values[0] == 'authoriurl':
            init = await interaction.message.channel.send("What should be the author icon of the embed?\nType 'none' if don't want anything.\nYou can send a image attached with it or a image's url or $user_avatar for your avatar or $server_icon for server's icon only")
            try:
                    user_response = await interaction.client.wait_for("message", timeout=120, check=message_check)
                    await user_response.delete()
            except asyncio.TimeoutError:
                await interaction.message.channel.send(embed=discord.Embed(
                    title="Error",
                    color=0xc283fe,
                    description="You took too long to answer this question"
                ))
                await interaction.delete_original_response()
                self.stop()
            if user_response.content.lower().strip() == "none":
                c = 1
                ch = 1
                pass
            else:
                ch = await checkimage(user_response, user_response.content)
            while ch == 0:
                await init.edit(content="Please send a valid image\nWhat should be the author icon of the embed?\nType 'none' if don't want anything.\nYou can send a image attached with it or a image's url or $user_avatar for your avatar or $server_icon for server's icon only")
                try:
                        user_response = await interaction.client.wait_for("message", timeout=120, check=message_check)
                        await user_response.delete()
                        if user_response.content.lower().strip() == "none":
                            ch = 1
                            pass
                        else:
                            ch = await checkimage(user_response, user_response.content)
                except asyncio.TimeoutError:
                    await interaction.message.channel.send(embed=discord.Embed(
                        title="Error",
                        color=0xc283fe,
                        description="You took too long to answer this question"
                    ))
                    await interaction.delete_original_response()
                    await init.delete()
                    self.stop()
            if em.author.name:
                n = em.author.name
            else:
                n = "\u200B"
            if em.author.url:
                u = em.author.url
            else:
                u = None
            if user_response.content.lower().strip() == "none":
                i = None
            else:
                i = ch
            if i is not None or u is not None or n != "\u200B":
                em.set_author(name=n, icon_url=i, url=u)
            elif user_response.content.lower().strip() == "none":
                em.remove_author()
            await updateembed(self.id, em.to_dict())
            em = await getembed(self.ctx.guild, self.ctx.author, self.id)
            em = discord.Embed.from_dict(em)
            try:
                await interaction.edit_original_response(embed=em, view=self.view)
            except:
                await interaction.message.channel.send("A error occured it may be because you exceeded the characters limit")
                await interaction.delete_original_response()
                await init.delete()
                self.stop()
            await init.delete()
        elif self.values[0] == 'authorurl':
            init = await interaction.message.channel.send("What should be the author url of the embed?\nYou can send $user_profile for the direct link of the user\nType 'none' if don't want anything.")
            try:
                    user_response = await interaction.client.wait_for("message", timeout=120, check=message_check)
                    await user_response.delete()
            except asyncio.TimeoutError:
                await interaction.message.channel.send(embed=discord.Embed(
                    title="Error",
                    color=0xc283fe,
                    description="You took too long to answer this question"
                ))
                await interaction.delete_original_response()
                await init.delete()
                self.stop()
            if em.author.name:
                n = em.author.name
            else:
                n = "\u200B"
            if em.author.icon_url:
                i = em.author.icon_url
            else:
                i = None
            if user_response.content.lower().strip() == "none":
                u = None
            elif user_response.content.lower().strip() == "$user_profile":
                u = f"https://discord.com/users/{self.ctx.author.id}"
            else:
                u = user_response.content
            if u.startswith("http"):
                em.set_author(name=n,icon_url=i, url=u)
            if i is not None or n != "\u200B":
                pass
            elif user_response.content.lower().strip() == "none":
                em.remove_author()
            await updateembed(self.id, em.to_dict())
            em = await getembed(self.ctx.guild, self.ctx.author, self.id)
            em = discord.Embed.from_dict(em)
            try:
                await interaction.edit_original_response(embed=em, view=self.view)
            except:
                await interaction.message.channel.send("A error occured it may be because you exceeded the characters limit")
                await interaction.delete_original_response()
                await init.delete()
                self.stop()
            await init.delete()
        elif self.values[0] == 'title':
            init = await interaction.message.channel.send("What should be the title of the embed?\nType 'none' if don't want anything.")
            try:
                    user_response = await interaction.client.wait_for("message", timeout=120, check=message_check)
                    await user_response.delete()
            except asyncio.TimeoutError:
                await interaction.message.channel.send(embed=discord.Embed(
                    title="Error",
                    color=0xc283fe,
                    description="You took too long to answer this question"
                ))
                await interaction.delete_original_response()
                await init.delete()
                self.stop()
            if user_response.content.lower().strip() == "none":
                t = None
            else:
                t = user_response.content
            em.title = t
            await updateembed(self.id, em.to_dict())
            em = await getembed(self.ctx.guild, self.ctx.author, self.id)
            em = discord.Embed.from_dict(em)
            try:
                await interaction.edit_original_response(embed=em, view=self.view)
            except:
                await interaction.message.channel.send("A error occured it may be because you exceeded the characters limit")
                await interaction.delete_original_response()
                await init.delete()
                self.stop()
            await init.delete()
        elif self.values[0] == 'des':
            init = await interaction.message.channel.send("What should be the description of the embed?\nType 'none' if don't want anything.")
            try:
                    user_response = await interaction.client.wait_for("message", timeout=120, check=message_check)
                    await user_response.delete()
            except asyncio.TimeoutError:
                await interaction.message.channel.send(embed=discord.Embed(
                    title="Error",
                    color=0xc283fe,
                    description="You took too long to answer this question"
                ))
                await interaction.delete_original_response()
                await init.delete()
                self.stop()
            if user_response.content.lower().strip() == "none":
                d = "\u200b"
            else:
                d = user_response.content
            em.description = d
            await updateembed(self.id, em.to_dict())
            em = await getembed(self.ctx.guild, self.ctx.author, self.id)
            em = discord.Embed.from_dict(em)
            try:
                await interaction.edit_original_response(embed=em, view=self.view)
            except:
                await interaction.message.channel.send("A error occured it may be because you exceeded the characters limit")
                await interaction.delete_original_response()
                await init.delete()
                self.stop()
            await init.delete()
        elif self.values[0] == 'field':
            init = await interaction.message.channel.send("What should be the name of the field?")
            try:
                    name = await interaction.client.wait_for("message", timeout=120, check=message_check)
                    await name.delete()
            except asyncio.TimeoutError:
                await interaction.message.channel.send(embed=discord.Embed(
                    title="Error",
                    color=0xc283fe,
                    description="You took too long to answer this question"
                ))
                await interaction.delete_original_response()
                await init.delete()
                self.stop()
            await init.edit(content="What should be the value of the field?")
            try:
                    value = await interaction.client.wait_for("message", timeout=120, check=message_check)
                    await value.delete()
            except asyncio.TimeoutError:
                await interaction.message.channel.send(embed=discord.Embed(
                    title="Error",
                    color=0xc283fe,
                    description="You took too long to answer this question"
                ))
                await interaction.delete_original_response()
                await init.delete()
                self.stop()
            em.add_field(name=name.content, value=value.content, inline=False)
            await updateembed(self.id, em.to_dict())
            em = await getembed(self.ctx.guild, self.ctx.author, self.id)
            em = discord.Embed.from_dict(em)
            try:
                await interaction.edit_original_response(embed=em, view=self.view)
            except:
                await interaction.message.channel.send("A error occured it may be because you exceeded the characters limit")
                await interaction.delete_original_response()
                await init.delete()
                self.stop()
            await init.delete()
        elif self.values[0] == 'thumb':
            init = await interaction.message.channel.send("What should be the thumbnail of the embed?\nType 'none' if don't want anything.\nYou can send a image attached with it or a image's url or $user_avatar for your avatar or $server_icon for server's icon only")
            try:
                    user_response = await interaction.client.wait_for("message", timeout=120, check=message_check)
                    await user_response.delete()
            except asyncio.TimeoutError:
                await interaction.message.channel.send(embed=discord.Embed(
                    title="Error",
                    color=0xc283fe,
                    description="You took too long to answer this question"
                ))
                await interaction.delete_original_response()
                self.stop()
            if user_response.content.lower().strip() == "none":
                ch = 1
                pass
            else:
                ch = await checkimage(user_response, user_response.content)
            while ch == 0:
                await init.edit(content="Please send a valid image\nWhat should be the thumbnail of the embed?\nType 'none' if don't want anything.\nYou can send a image attached with it or a image's url or $user_avatar for your avatar or $server_icon for server's icon only")
                try:
                        user_response = await interaction.client.wait_for("message", timeout=120, check=message_check)
                        await user_response.delete()
                        if user_response.content.lower().strip() == "none":
                            ch = 1
                            pass
                        else:
                            ch = await checkimage(user_response, user_response.content)
                except asyncio.TimeoutError:
                    await interaction.message.channel.send(embed=discord.Embed(
                        title="Error",
                        color=0xc283fe,
                        description="You took too long to answer this question"
                    ))
                    await interaction.delete_original_response()
                    await init.delete()
                    self.stop()
            if user_response.content.lower().strip() == "none":
                t = None
            else:
                t = ch
            em.set_thumbnail(url=t)
            await updateembed(self.id, em.to_dict())
            em = await getembed(self.ctx.guild, self.ctx.author, self.id)
            em = discord.Embed.from_dict(em)
            try:
                await interaction.edit_original_response(embed=em, view=self.view)
            except:
                await interaction.message.channel.send("A error occured it may be because you exceeded the characters limit")
                await interaction.delete_original_response()
                await init.delete()
                self.stop()
            await init.delete()
        elif self.values[0] == 'img':
            init = await interaction.message.channel.send("What should be the image of the embed?\nType 'none' if don't want anything.\nYou can send a image attached with it or a image's url or $user_avatar for your avatar or $server_icon for server's icon only")
            try:
                    user_response = await interaction.client.wait_for("message", timeout=120, check=message_check)
                    await user_response.delete()
            except asyncio.TimeoutError:
                await interaction.message.channel.send(embed=discord.Embed(
                    title="Error",
                    color=0xc283fe,
                    description="You took too long to answer this question"
                ))
                await interaction.delete_original_response()
                self.stop()
            if user_response.content.lower().strip() == "none":
                ch = 1 
                pass
            else:
                ch = await checkimage(user_response, user_response.content)
            while ch == 0:
                await init.edit(content="Please send a valid image\nWhat should be the image of the embed?\nType 'none' if don't want anything.\nYou can send a image attached with it or a image's url or $user_avatar for your avatar or $server_icon for server's icon only")
                try:
                        user_response = await interaction.client.wait_for("message", timeout=120, check=message_check)
                        await user_response.delete()
                        if user_response.content.lower().strip() == "none":
                            ch = 1 
                            pass
                        else:
                            ch = await checkimage(user_response, user_response.content)
                except asyncio.TimeoutError:
                    await interaction.message.channel.send(embed=discord.Embed(
                        title="Error",
                        color=0xc283fe,
                        description="You took too long to answer this question"
                    ))
                    await interaction.delete_original_response()
                    await init.delete()
                    self.stop()
            if user_response.content.lower().strip() == "none":
                i = None
            else:
                i = ch
            em.set_image(url=i)
            await updateembed(self.id, em.to_dict())
            em = await getembed(self.ctx.guild, self.ctx.author, self.id)
            em = discord.Embed.from_dict(em)
            try:
                await interaction.edit_original_response(embed=em, view=self.view)
            except:
                await interaction.message.channel.send("A error occured it may be because you exceeded the characters limit")
                await interaction.delete_original_response()
                await init.delete()
                self.stop()
            await init.delete()
        elif self.values[0] == 'foot':
            init = await interaction.message.channel.send("What should be the footer of the embed?\nType 'none' if don't want anything.")
            try:
                    user_response = await interaction.client.wait_for("message", timeout=120, check=message_check)
                    await user_response.delete()
            except asyncio.TimeoutError:
                await interaction.message.channel.send(embed=discord.Embed(
                    title="Error",
                    color=0xc283fe,
                    description="You took too long to answer this question"
                ))
                await interaction.delete_original_response()
                await init.delete()
                self.stop()
            if user_response.content.lower().strip() == "none":
                n = "\u200B"
            else:
                n = user_response.content
            if em.footer.icon_url:
                i = em.footer.icon_url
            else:
                i = None
            if n != "\u200B" or i is not None:
                em.set_footer(text=n, icon_url=i)
            elif user_response.content.lower().strip() == "none":
                em.remove_footer()
            await updateembed(self.id, em.to_dict())
            em = await getembed(self.ctx.guild, self.ctx.author, self.id)
            em = discord.Embed.from_dict(em)
            try:
                await interaction.edit_original_response(embed=em, view=self.view)
            except:
                await interaction.message.channel.send("A error occured it may be because you exceeded the characters limit")
                await interaction.delete_original_response()
                await init.delete()
                self.stop()
            await init.delete()
        elif self.values[0] == 'footi':
            init = await interaction.message.channel.send("What should be the footer icon of the embed?\nType 'none' if don't want anything.\nYou can send a image attached with it or a image's url or $user_avatar for your avatar or $server_icon for server's icon only")
            try:
                    user_response = await interaction.client.wait_for("message", timeout=120, check=message_check)
                    await user_response.delete()
            except asyncio.TimeoutError:
                await interaction.message.channel.send(embed=discord.Embed(
                    title="Error",
                    color=0xc283fe,
                    description="You took too long to answer this question"
                ))
                await interaction.delete_original_response()
                self.stop()
            if user_response.content.lower().strip() == "none":
                ch = 1
                pass
            else:
                ch = await checkimage(user_response, user_response.content)
            while ch == 0:
                await init.edit(content="Please send a valid image\nWhat should be the footer icon of the embed?\nType 'none' if don't want anything.\nYou can send a image attached with it or a image's url or $user_avatar for your avatar or $server_icon for server's icon only")
                try:
                        user_response = await interaction.client.wait_for("message", timeout=120, check=message_check)
                        await user_response.delete()
                        if user_response.content.lower().strip() == "none":
                            ch = 1
                            pass
                        else:
                            ch = await checkimage(user_response, user_response.content)
                except asyncio.TimeoutError:
                    await interaction.message.channel.send(embed=discord.Embed(
                        title="Error",
                        color=0xc283fe,
                        description="You took too long to answer this question"
                    ))
                    await interaction.delete_original_response()
                    await init.delete()
                    self.stop()
            if em.footer.text:
                n = em.footer.text
            else:
                n = "\u200B"
            if user_response.content.lower().strip() == "none":
                i = None
            else:
                i = ch
            if n != "\u200B" or i is not None:
                em.set_footer(text=n, icon_url=i)
            elif user_response.content.lower().strip() == "none":
                em.remove_footer()
            await updateembed(self.id, em.to_dict())
            em = await getembed(self.ctx.guild, self.ctx.author, self.id)
            em = discord.Embed.from_dict(em)
            try:
                await interaction.edit_original_response(embed=em, view=self.view)
            except:
                await interaction.message.channel.send("A error occured it may be because you exceeded the characters limit")
                await interaction.delete_original_response()
                await init.delete()
                self.stop()
            await init.delete()
        elif self.values[0] == 'color':
            init = await interaction.message.channel.send("What should be the color of the embed?\nType 'none' if don't want anything.\nYou can send a hex code or the color name without any space between it only")
            try:
                    user_response = await interaction.client.wait_for("message", timeout=120, check=message_check)
                    await user_response.delete()
            except asyncio.TimeoutError:
                await interaction.message.channel.send(embed=discord.Embed(
                    title="Error",
                    color=0xc283fe,
                    description="You took too long to answer this question"
                ))
                await interaction.delete_original_response()
                self.stop()
            if user_response.content.lower().strip() == "none":
                ch = 1
                pass
            else:
                ch = await checkcolor(user_response.content)
            while ch == 0:
                await init.edit(content="Please send a valid color\nWhat should be the color of the embed?\nType 'none' if don't want anything.\nYou can send a hex code or the color name without any space between it only")
                try:
                        user_response = await interaction.client.wait_for("message", timeout=120, check=message_check)
                        await user_response.delete()
                        if user_response.content.lower().strip() == "none":
                            ch = 1
                            pass
                        else:
                            ch = await checkcolor(user_response.content)
                except asyncio.TimeoutError:
                    await interaction.message.channel.send(embed=discord.Embed(
                        title="Error",
                        color=0xc283fe,
                        description="You took too long to answer this question"
                    ))
                    await interaction.delete_original_response()
                    await init.delete()
                    self.stop()
            if user_response.content.lower().strip() == "none":
                ch = 3092790
            else:
                pass
            em.color = ch
            await updateembed(self.id, em.to_dict())
            em = await getembed(self.ctx.guild, self.ctx.author, self.id)
            em = discord.Embed.from_dict(em)
            try:
                await interaction.edit_original_response(embed=em, view=self.view)
            except:
                await interaction.message.channel.send("A error occured it may be because you exceeded the characters limit")
                await interaction.delete_original_response()
                await init.delete()
                self.stop()
            await init.delete()
