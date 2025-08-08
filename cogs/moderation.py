import discord
import datetime

from utils.err_handle import ErrorHandler  # inst utils.
from discord.ext import commands

# note: @command.error is just there for no reason, i don't know weather i'll keep it or remove it in future.

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.err_handler = ErrorHandler()

    @commands.Cog.listener()
    async def on_ready(self):
        print("moderation cog is ready")
    
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None): # kick
        reason = reason or "i don't need a reason. i am the reason"
        
        try:
            await member.kick(reason=reason)
            embed = discord.Embed(
                title="member kicked",
                description=f"{member.global_name} has been kicked by {ctx.message.author.name}, reason: {reason}",
                color=0xFF0000
            )

            await ctx.send(embed=embed)
        except Exception as err:
            await self.err_handler.handle_error(ctx, err)
    
    @kick.error
    async def kick_error(self, ctx, error): # havent' decided yet if i shoudl handle error locally or globally
        pass

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        reason = reason or "i don't need a reason. i am the reason"

        try:
            await member.ban(reason=reason)
            embed = discord.Embed(
                title="member banned",
                description=f"{member.global_name} has been kicked by {ctx.message.author.name}, reason: {reason}",
                color=0xFF0000
            )

            await ctx.send(embed=embed)
        except Exception as err:
            await self.err_handler.handle_error(ctx, err)

    @ban.error
    async def ban_error(self, ctx, error):
        pass

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, id: int = None, *, reason=None):

        try:
            user = await self.client.fetch_user(id)
            await ctx.unban(user)
            embed =  discord.Embed(
                title="member unbanned",
                description=f"{user} has been unbanned by {ctx.message.author.name}",
                color=0xFF0000
            )

            await ctx.send(embed=embed)
        except Exception as err:
            await self.err_handler.handle_error(ctx, err)
    
    @unban.error
    async def unban_error(self, ctx, error):
        pass

    @commands.command()
    @commands.has_permissions(manage_messages=True, read_message_history=True)
    async def purge(self, ctx, limit: int = 1):
        try:
            await ctx.channel.purge(limit=limit, bulk=True)
            embed = discord.Embed(
                title="messages purged",
                description=f"{limit} messages were removed by {ctx.message.author.name}",
                color=0xFF0000
            )

            await ctx.send(embed=embed)
        except Exception as err:
            await self.err_handler.handle_error(ctx, err)
    
    @purge.error
    async def purge_error(self, ctx, error):
        pass

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx, member: discord.Member, timelimit='0s', *, reason=None):

        try:
            if timelimit.isdigit() or ('s' in timelimit and timelimit[:-1].isdigit()):
                
                mute_time = int(timelimit.strip('s'))

                if mute_time > 2.419e+6:
                    raise ValueError("muting time can't be longer than 28 days, why not just ban the guy?")
                
                format_time = datetime.timedelta(seconds=mute_time)
                print(type(format_time))

                if mute_time:
                    timed_out_until_value = discord.utils.utcnow() + format_time 
                    description_message = f"{member} has been muted for {format_time} seconds by {ctx.message.author.name}"
                    color_value = 0xFF0000
                else:
                    timed_out_until_value = discord.utils.utcnow()
                    description_message = f"{member} has been unmuted by {ctx.message.author.name}"
                    color_value = 0x00FF00

                await member.edit(timed_out_until=timed_out_until_value)
                
                
                embed = discord.Embed(
                    title="member muted" if mute_time else "member unmuted",
                    description=description_message,
                    color=color_value
                )

                await ctx.send(embed=embed)
        except Exception as err:
            await self.err_handler.handle_error(ctx, err)
    
    @mute.error
    async def mute_error(self, ctx, error):
        pass

        

async def setup(client):
    await client.add_cog(Moderation(client=client))
