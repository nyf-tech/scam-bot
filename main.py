import discord
import random
import asyncio
import json
import io
import os
import requests
import contextlib
import datetime
from discord.ext import commands
from discord.ext.commands import Bot
from discord import File
from datetime import datetime, timedelta
from discord.ext import commands
import time
import sched
import io

import urllib.request

client = commands.Bot(command_prefix="$",intents=discord.Intents.all())



@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('> $help v2.2.2 '))

    print('Connected to bot: {}'.format(client.user.name))
    print('Bot ID: {}'.format(client.user.id))


@client.command()
async def ping(ctx):
 await ctx.send(f'Pong! 🏓 {round(client.latency * 1000)}ms')


@client.event
async def on_member_join(member):
   await client.get_channel(820935110429507637).send(f"{member.name} Dołączył")

@client.event
async def on_member_remove(member):
   await client.get_channel(820935110429507637).send(f"{member.name} opuścił")


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please pass in all requirements :rolling_eyes:.')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You dont have all the requirements :angry:")

#The below code bans player.
@client.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member, *, reason = None):
    await member.ban(reason = reason)

#The below code unbans player.
@client.command()
@commands.has_permissions(administrator = True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return


@client.command(aliases=["whois"])
async def userinfo(ctx, member: discord.Member = None):
    if not member:  # if member is no mentioned
        member = ctx.message.author  # set member as the author
    roles = [role for role in member.roles]
    embed = discord.Embed(colour=discord.Colour.purple(), timestamp=ctx.message.created_at,
                          title=f"User Info - {member}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Requested by {ctx.author}")

    embed.add_field(name="ID:", value=member.id)
    embed.add_field(name="Display Name:", value=member.display_name)

    embed.add_field(name="Created Account On:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
    embed.add_field(name="Joined Server On:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))

    embed.add_field(name="Roles:", value="".join([role.mention for role in roles]))
    embed.add_field(name="Highest Role:", value=member.top_role.mention)
    print(member.top_role.mention)
    await ctx.send(embed=embed)

@client.command(description="Mutes the specified user.")
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muteduser")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muteduser")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
    embed = discord.Embed(title="muted", description=f"{member.mention} was muted ", colour=discord.Colour.light_gray())
    embed.add_field(name="reason:", value=reason, inline=False)
    await ctx.send(embed=embed)
    await member.add_roles(mutedRole, reason=reason)
    await member.send(f" you have been muted from: {guild.name} reason: {reason}")



@client.command(description="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
   mutedRole = discord.utils.get(ctx.guild.roles, name="Muteduser")

   await member.remove_roles(mutedRole)
   await member.send(f" you have unmutedd from: - {ctx.guild.name}")
   embed = discord.Embed(title="unmute", description=f" unmuted-{member.mention}",colour=discord.Colour.light_gray())
   await ctx.send(embed=embed)


@client.command()
async def invites(ctx, usr=None):
    if usr == None:
       user = ctx.author
    else:
       user = usr
    total_invites = 0
    for i in await ctx.guild.invites():
        if i.inviter == user:
            total_invites += i.uses
    await ctx.send(f"{user.name} has invited {total_invites} member{'' if total_invites == 1 else 's'}!")


@client.command()
async def clear(ctx, amount=5):
        await ctx.channel.purge(limit=amount)


@client.event
async def on_message(message):
    if isinstance(message.channel, discord.channel.DMChannel) and message.author != client.user:
        await message.channel.send('Witaj na serverze zarabiamy ')







client.run("ODIwOTM2NDQyNjcwMDg4MTkz.YE8apA.ZbnHdUPmRAGIHnrzXCyjlQaRTYM")
