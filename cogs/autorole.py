import discord
from ast import literal_eval
import sqlite3
from discord.ext import commands
class autorole(commands.Cog):
  def __init__(self, bot):
    self.bot=bot

  @commands.Cog.listener()
  async def on_member_join(self, user):
                await self.bot.wait_until_ready()
                if not user.guild.me.guild_permissions.manage_roles:
                  return
                query = "SELECT * FROM  auto WHERE guild_id = ?"
                val = (user.guild.id,)
                with sqlite3.connect('./database.sqlite3') as db1:
                  db1.row_factory = sqlite3.Row
                  cursor1 = db1.cursor()
                  cursor1.execute(query, val)
                  auto_db = cursor1.fetchone()
                  if auto_db is None:
                    return
                try:
                  humans = literal_eval(auto_db['humans'])
                except:
                  humans = None
                try:
                  bots = literal_eval(auto_db['bots'])
                except:
                  bots = None
                if not user.bot:
                 if humans is not None:
                  for i in humans:
                    role = discord.utils.get(user.guild.roles, id=i)
                    if role is None:
                      continue
                    if role.position >= user.guild.me.top_role.position:
                      continue 
                    await user.add_roles(role, reason='Autorole Humans')
                else:
                 if bots is not None:
                  for i in bots:
                    role = discord.utils.get(user.guild.roles, id=i)
                    if role is None:
                      continue
                    if role.position >= user.guild.me.top_role.position:
                      continue
                    await user.add_roles(role, reason='Autorole Bots')
                db1.commit()
                cursor1.close()
                db1.close()
            
async def setup(bot):
  await bot.add_cog(autorole(bot))