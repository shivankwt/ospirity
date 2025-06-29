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
            embed = discord.Embed( # maybe later i'll just make it a simple message instead of fancy embeds.
                title="member kicked",
                description=f"{member} has been kicked by {ctx.message.author.name}. reason: {reason}",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
        except Exception as e:
            await self.handle_error(ctx, e)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        try:
            await member.ban(reason=reason)
            embed = discord.Embed(
                title="member banned",
                description=f"{member} has been banned by {ctx.message.author.name}. reason: {reason or 'No reason provided.'}",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
        except Exception as e:
            await self.handle_error(ctx, e)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, id: int = None, *, reason=None):
        if id:
            try:
                user = await self.client.fetch_user(id)
                await ctx.guild.unban(user)
                embed = discord.Embed(
                    title="member unbanned",
                    description=f'{user} has been unbanned by {ctx.message.author.name}',
                    color=0x00FF00
                )
                await ctx.send(embed=embed)
            except Exception as e:
                await self.handle_error(ctx, e)