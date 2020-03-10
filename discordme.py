from scrumpy_modules import tags as tag_system
from scrumpy_modules import customcommands as customcommands
from db import db_autorespond as db_ar

# discord
import discord
from discord import *
from discord.ext.commands import Bot
from discord.ext import commands
from discord.ext import *
from discord import *
from discord.ext import tasks

# extra imports
import datetime
from datetime import timedelta as dt_td
import asyncio
import time

bot_token = "YOUR TOKEN"
bot_prefix = "!"
bot_status = "!help | Attempting to support you."


Client = discord.Client()
bot = commands.Bot(command_prefix = bot_prefix, case_insensitive=True)
#######################################
###        ON_READY() EVENT         ###
#######################################

@bot.event
async def on_ready():
      global startup_time
      startup_time = time.time()
      print("Bot Started... [%s]" % (startup_time))
      game = discord.Game(bot_status)
      changeStatus = await bot.change_presence(status=discord.Status.online, activity=game)
      daily_support.start()


bot.remove_command("help")
@bot.command(aliases=['h', 'helppage', 'helpme', 'commands', 'cmds'])
async def help(ctx):
      embed=discord.Embed(title=("Help"), description=("""`!tag {tag_name}` Displays information for the requested tag.
`!tags` Shows all available tags.
`!ping` See the bots current latency.
`!uptime` See the bots current uptime.
`!join {@user}` See when a user joined this server (leave blank for your own)."""), color=0xF6678E)
      guild = bot.get_guild(112926209867870208)
      role_ids = [role.id for role in ctx.author.roles]
      if 345080290051620875 in role_ids:
            embed.add_field(name="Staff Commands", value=("""`!cc_create {trigger} {response}` Create a custom command with a predefined response.
> Example: `!cc_create hello Hiya! I'm Discord.Me Support.` would make `!hello` respond with `Hiya! I'm Discord.Me Support.`
`!cc_change {trigger} {new response}` Changes a custom commands response.
**Leave {new response} blank to disable the trigger.**

`!tag_create {tag} {response}` Create a tag.
> Example: `!tag_create help I'll save you!` will make `!tag help` respond with `I'll save you!`
`!tag_delete {tag}` Deletes a tag.

**Community Support members bypass all command cooldowns.**"""), inline=False)
      embed.set_footer(text="Made with love by Megumin.")
      try:
            await ctx.author.send(embed=embed)
            await ctx.send("**%s**, check your DMs!" % (ctx.author.name))
      except:
            await ctx.send("**%s**, please enable your DMs!" % (ctx.author.name))


@tasks.loop(hours=24)
async def daily_support():
      await db_ar.clear()
      print("Cleared the daily support cases")


class NoPrivateMessages(commands.CheckFailure):
    pass

class NoSupport(commands.CheckFailure):
    pass

class NotOwner(commands.CheckFailure):
    pass


def guild_only():
    async def predicate(ctx):
        if ctx.guild is None:
            raise NoPrivateMessages('That command is disabled in DMs! Try <#479797846917513226> instead.')
        return True
    return commands.check(predicate)

def no_support():
    async def predicate(ctx):
        if ctx.channel.id == 112926209867870208:
            raise NoSupport('That command is disabled in that channel! Try <#479797846917513226> instead.')
        return True
    return commands.check(predicate)

def is_owner():
    async def predicate(ctx):
        if ctx.author.id == 654096379085455371:
            return True
        else:
            raise NotOwner()
    return commands.check(predicate)


@commands.cooldown(1, 15, commands.BucketType.user)
@bot.command()
async def tag(ctx, name=None):
      guild = bot.get_guild(112926209867870208)
      role_ids = [role.id for role in ctx.author.roles]
      if 345080290051620875 in role_ids:
            await tag.reset_cooldown(ctx)
      if name == None:
            message = await ctx.send("**%s**, you need to add a tag name! `!tag {tag}`\n\tSee: `!tags` for a list of tags." % (ctx.author.name))
            await tag.reset_cooldown(ctx)
      else:
            content = await tag_system.get_info(name)
            if tag == "None":
                  message = await ctx.send("**%s**, I don't know that tag!\n\tSee: `!tags` for a list of tags." % (ctx.author.name))
                  await tag.reset_cooldown(ctx)
            else:
                  embed=discord.Embed(title=(name), description=(content), color=0xF6678E)
                  await ctx.send(embed=embed)

@commands.cooldown(1, 30, commands.BucketType.user)
@bot.command()
async def tags(ctx):
      guild = bot.get_guild(112926209867870208)
      role_ids = [role.id for role in ctx.author.roles]
      if 345080290051620875 in role_ids:
            await tags.reset_cooldown(ctx)
      content = await tag_system.get_info("tags")
      embed=discord.Embed(title=("Current !tags"), description=(content), color=0xF6678E)
      message = await ctx.send(embed=embed)

@commands.has_permissions(view_audit_log=True)
@bot.command()
async def tag_create(ctx, name=None, *, text=None):
      if name == None:
            message = await ctx.send("**%s**, you need to add a name to the tag! `!tag_create {tag_name} {tag_info}`" % (ctx.author.name))
      elif text == None:
            message = await ctx.send("**%s**, you need to add a text message to the tag! `!tag_create {tag_name} {tag_info}`" % (ctx.author.name))
      else:
            if '"' in text or '"' in name:
                  message = await ctx.send("**%s**, The tag cannot have a `\"` in it! (try `'` instead)" % (ctx.author.name))
                  await ctx.author.send(ctx.message.content)
            else:
                  await tag_system.create(name, text)
                  embed=discord.Embed(title=(name), description=(text), color=0xF6678E)
                  await ctx.send(content="Tag Created!", embed=embed)

@commands.has_permissions(view_audit_log=True)
@bot.command()
async def tag_delete(ctx, name=None):
      if name == None:
            message = await ctx.send("**%s**, you need to add a name to the tag! `!tag_delete {tag_name}`" % (ctx.author.name))
      else:
            await tag_system.delete(name)
            message = await ctx.send("Tag Deleted.")


@no_support()
@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def ping(ctx):
      guild = bot.get_guild(112926209867870208)
      role_ids = [role.id for role in ctx.author.roles]
      if 345080290051620875 in role_ids:
            await ping.reset_cooldown(ctx)
      await ctx.send("**%s**, my ping is **%sms**!" % (ctx.author.name, round((bot.latency*1000), 1)))

@no_support()
@commands.cooldown(1, 30, commands.BucketType.user)
@bot.command(aliases=['up', 'time', 'online'])
async def uptime(ctx):
      guild = bot.get_guild(112926209867870208)
      role_ids = [role.id for role in ctx.author.roles]
      if 345080290051620875 in role_ids:
            await uptime.reset_cooldown(ctx)
      global startup_time
      command_time = time.time()
      bot_uptime = int(round(command_time - startup_time))
      m, s = divmod(bot_uptime, 60)
      h, m = divmod(m, 60)
      d, h = divmod(h, 24)
      if m <= 0:
            text = ("**%ss**" % (s))
      elif h <= 0:
            text = ("**%sm %ss**" % (m, s))
      elif h > 0 and h < 24:
            text = ("**%sh %sm %ss**" % (h, m, s))
      else:
            text = ("**%sd %sh %sm %ss**" % (d, h, m, s))
      await ctx.send("**%s**, my current uptime is %s." % (ctx.author.name, text))

@no_support()
@guild_only()
@bot.command(aliases=['joined', 'joindate'])
async def join(ctx, member: discord.Member=None):
      if member == None:
            await ctx.send("**%s**, you joined **%s** at `%s`." % (ctx.author.name, ctx.guild.name, ctx.author.joined_at))
      else:
            await ctx.send("**%s** joined **%s** at `%s`." % (member.name, ctx.guild.name, member.joined_at))

@is_owner()
@bot.command()
@commands.has_permissions(administrator=True)
async def cc_create(ctx, name=None, *, response=None):
      if name == None or response == None:
            await ctx.send("`!cc_create [command_name] [command response]`")
      else:
            await customcommands.create(name, response)
            await ctx.send("Custom command `%s` has been created with the response of `%s`!" % (name, response))

@is_owner()
@bot.command()
@commands.has_permissions(administrator=True)
async def cc_change(ctx, name=None, *, response=None):
      if name == None:
            await ctx.send("`!cc_change [command_name] [command response]` (leave [command response] blank to disable).")
      if response == None:
            await customcommands.change(name, "False")
            await ctx.send("Custom command `%s` has been disabled.`" % (name))
      else:
            await customcommands.change(name, response)
            await ctx.send("Custom command `%s` has been updated to respond with `%s`!" % (name, response))

@bot.event
async def on_message(message):
      if message.guild == None:
            await bot.process_commands(message)
      elif message.author.bot:
            pass
      elif (message.content).startswith("!"):
            await bot.process_commands(message)
      else:
            guild = bot.get_guild(112926209867870208)
            role_ids = [role.id for role in message.author.roles]
            if 345080290051620875 in role_ids:
                  await bot.process_commands(message)
            else:
                  content = (message.content).lower()
                  if "413" in content:
                        if (await db_ar.check(message.author.id, "413")) == True:
                              pass
                        else:
                              await db_ar.add(message.author.id, "413")
                              tag = await tag_system.get_info("413")
                              embed=discord.Embed(title=("Automatic - 413 Error: Entity too large."), description=(tag), color=0xF6678E)
                              embed.set_footer(text="You'll see this once per 24hrs per user per response.")
                              message = await message.channel.send(embed=embed)
                  elif "offline" in content:
                        if (await db_ar.check(message.author.id, "offline")) == True:
                              pass
                        else:
                              await db_ar.add(message.author.id, "offline")
                              tag = await tag_system.get_info("offline")
                              embed=discord.Embed(title=("Automatic - Bot offline help."), description=(tag), color=0xF6678E)
                              embed.set_footer(text="You'll see this once per 24hrs per user per response.")
                              message = await message.channel.send(embed=embed)
                  elif "url taken" in content:
                        if (await db_ar.check(message.author.id, "urltaken")) == True:
                              pass
                        else:
                              await db_ar.add(message.author.id, "urltaken")
                              tag = await tag_system.get_info("urltaken")
                              embed=discord.Embed(title=("Automatic - URL Taken Error."), description=(tag), color=0xF6678E)
                              embed.set_footer(text="You'll see this once per 24hrs per user per response.")
                              message = await message.channel.send(embed=embed)
                  elif "serverid taken" in content or "server id taken" in content or "id taken" in content:
                        if (await db_ar.check(message.author.id, "idtaken")) == True:
                              pass
                        else:
                              await db_ar.add(message.author.id, "idtaken")
                              tag = await tag_system.get_info("idtaken")
                              embed=discord.Embed(title=("Automatic - ServerID Taken Error."), description=(tag), color=0xF6678E)
                              embed.set_footer(text="You'll see this once per 24hrs per user per response.")
                              message = await message.channel.send(embed=embed)
                  elif "unable to bumb" in content:
                        if (await db_ar.check(message.author.id, "unablebump")) == True:
                              pass
                        else:
                              await db_ar.add(message.author.id, "unablebump")
                              tag = await tag_system.get_info("unablebump")
                              embed=discord.Embed(title=("Automatic - Unable to Bump."), description=(tag), color=0xF6678E)
                              embed.set_footer(text="You'll see this once per 24hrs per user per response.")
                              message = await message.channel.send(embed=embed)
                  elif "premium role" in content or "premium rank" in content:
                        if (await db_ar.check(message.author.id, "role")) == True:
                              pass
                        else:
                              await db_ar.add(message.author.id, "role")
                              tag = await tag_system.get_info("role")
                              embed=discord.Embed(title=("Automatic - Premium role."), description=(tag), color=0xF6678E)
                              embed.set_footer(text="You'll see this once per 24hrs per user per response.")
                              message = await message.channel.send(embed=embed)
                  elif "no longer valid" in content or "invalid session" in content or "session invalid" in content:
                        if (await db_ar.check(message.author.id, "invalid")) == True:
                              pass
                        else:
                              await db_ar.add(message.author.id, "invalid")
                              tag = await tag_system.get_info("invalid")
                              embed=discord.Embed(title=("Automatic - Invalid Session."), description=(tag), color=0xF6678E)
                              embed.set_footer(text="You'll see this once per 24hrs per user per response.")
                              message = await message.channel.send(embed=embed)
                  elif "can't get invite" in content or "cant get invite" in content or "couldn't get you a server invite" in content or "couldn't get you an invite" in content or "couldnt get you a server invite" in content or "couldnt get you an invite" in content:
                        if (await db_ar.check(message.author.id, "noinvite")) == True:
                              pass
                        else:
                              await db_ar.add(message.author.id, "noinvite")
                              tag = await tag_system.get_info("noinvite")
                              embed=discord.Embed(title=("Automatic - Couldn't get you an invite."), description=(tag), color=0xF6678E)
                              embed.set_footer(text="You'll see this once per 24hrs per user per response.")
                              message = await message.channel.send(embed=embed)
                  else:
                        await bot.process_commands(message)






@bot.event
async def on_command_error(ctx, error):
      if isinstance(error, commands.CommandOnCooldown):
            await ctx.message.add_reaction("⏰")
            time_left = int(error.retry_after)
            m, s = divmod(time_left, 60)
            h, m = divmod(m, 60)
            d, h = divmod(h, 24)
            if m <= 0 and h <= 0 and d <= 0:
                  await ctx.send("**%s**, you are on cooldown. | Try again in **%ss**." % (ctx.author.name, s))
      elif isinstance(error, commands.MissingPermissions):
            string = ""
            for permission in list(error.missing_perms):
                string = str(string)+str(permission)+", "
            message = await ctx.send("%s, you're lacking the following permission(s) `%s`." % (ctx.author.name, string[0:((len(string))-2)]))
      elif isinstance(error, NoPrivateMessages):
            await ctx.send(error)
      elif isinstance(error, NoSupport):
            await ctx.send(error)
      elif isinstance(error, NotOwner):
            await ctx.send("**%s**, only the bot owner can run that command." % (ctx.author.name))
      else:
            print(error) # Print error if it is not a cooldown issue.


bot.run(bot_token)


