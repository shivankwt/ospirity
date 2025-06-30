import discord
from discord.ext import commands
import datetime

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("moderation cog is ready!")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if not reason:
            reason = "no reason provided."
        try:
            await member.kick(reason=reason)
            await ctx.send(f"{member} has been kicked by {ctx.message.author.name}. reason: {reason}")
        except Exception as e:
            await self.handle_error(ctx, e)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        try:
            await member.ban(reason=reason)
            await ctx.send(f"{member} has been banned by {ctx.message.author.name}. reason: {reason or 'No reason provided.'}")
        except Exception as e:
            await self.handle_error(ctx, e)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, id: int = None, *, reason=None):
        if id:
            try:
                user = await self.client.fetch_user(id)
                await ctx.guild.unban(user)
                await ctx.send(f'{user} has been unbanned by {ctx.message.author.name}')
            except Exception as e:
                await self.handle_error(ctx, e)