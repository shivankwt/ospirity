import discord
import datetime
import pyquotegen

from utils.err_handle import ErrorHandler  # inst utils.
from discord.ext import commands

class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.err_handler = ErrorHandler() 

    @commands.Cog.listener()
    async def on_ready(self):
        print("command cog is ready.")

    @commands.command(aliases=['stats', 'cs', 'cstats'])
    async def channelstats(self, ctx):
        print("channel stats command")
        channel = ctx.channel

        try:
            embed = discord.Embed(title="channel details")
            embed.add_field(name=f"channel id -- {channel.id}", value="\u200b", inline=False)
            embed.add_field(name=f"channel topic -- {channel.topic or 'no topic given'}", value="\u200b", inline=False)
            embed.add_field(name=f"channel position -- {channel.position + 1}", value="\u200b", inline=False)
            embed.add_field(name=f"channel in category -- {channel.category.name}", value="\u200b", inline=False)
            embed.add_field(name=f"channel slowmode delay -- {channel.slowmode_delay}", value="\u200b", inline=False)
            embed.add_field(name=f"channel environment -- {'nsfw: 18+' if channel.is_nsfw() else 'not nsfw: 18-'}", value="\u200b", inline=False)
            embed.add_field(name=f"permissions synced -- {channel.permissions_synced}", value="\u200b", inline=False)
            embed.add_field(name=f"channel created at -- {channel.created_at.strftime('%Y-%m-%d')}", value="\u200b", inline=False)

            await ctx.send(embed=embed)

        except Exception as err:
            print(f"error in module {__file__}:: ", err)
            await self.err_handler.handle_error(ctx, err)

    @commands.command(aliases=['info', 'inf'])
    async def about(self, ctx, member: discord.Member):
        print("about command")

        try:
            embed = discord.Embed(title=f"information about -- {member.display_name}")
            embed.add_field(name=f"created on -- {member.created_at.strftime('%Y-%m-%d')}", value="\u200b", inline=False)
            embed.add_field(name=f"joined on -- {member.joined_at.strftime('%Y-%m-%d')}", value="\u200b", inline=False)
            embed.add_field(name=f"global name -- {member.global_name or 'not available'}", value="\u200b", inline=False)
            embed.add_field(name=f"id -- {member.id}", value="\u200b", inline=False) 

            await ctx.send(embed=embed)

        except Exception as err:
            print(f"error in module {__file__}:: ", err)
            await self.handle_error(ctx, err)

    @commands.command(aliases=['av', 'pp'])
    async def avatar(self, ctx, member: discord.Member = None):
        try:
            member = member or ctx.author
            embed = discord.Embed(title=f"{member.display_name}'s avatar", color=0x0FF00)
            embed.set_image(url=member.display_avatar.url)
            embed.set_footer(text=" -- created by ospirity")
            await ctx.send(embed=embed)

        except Exception as err:
            print(f"error in module {__file__}::", err)
            await self.handle_error(ctx, err)

    @commands.command()
    async def ping(self, ctx):
        try:
            await ctx.send(f"ping: {round(self.client.latency * 1000)} ms")
        except Exception as err:
            print(f"error in module {__file__}:: ", err)
            await self.handle_error(ctx, err)

    @commands.command()
    async def quote(self, ctx, category: str = None): # will add author based filter and diff/ lib for this later.
        categories = [
            "motivational",
            "friendship",
            "technology",
            "inspirational",
            "funny",
            "nature",
            "success",
            "attitude",
            "coding"
        ]
        try:
            if category is None:
                quote = pyquotegen.get_quote()

            elif category.lower() in categories:
                quote = pyquotegen.get_quote(category.lower())

            else:
                quote = ("incorrect category, please choose from: " + ", ".join(categories))

            embed = discord.Embed()
            embed.add_field(name="quotation", value=quote, inline=False)
            embed.set_footer(text=f" - requested by: {ctx.author}")
            await ctx.send(embed=embed)

        except Exception as err:
            print(f"error in module {__file__}:: ", err)
            await self.err_handler.handle_error(ctx, err)

    @commands.command()
    async def caption(self, ctx):
        print("caption command")
        try:
            reply = ctx.message.reference # Message.Reply won't work because that's for bots
            if reply is not None:
                print(reply.resolved)
                embed = discord.Embed(color=0x0FF00)
                embed.add_field(name="", value=f"{reply.resolved.content}") # add name here
                embed.set_author(name=reply.resolved.author)
                embed.set_footer(text=f" - requested by: {ctx.author}")
                await ctx.send(embed=embed)
            else:
                await ctx.send("this command doesn't work unless pinged someone's message")

        except Exception as err:
            print(f"error in module {__file__}:: ", err)
            await self.handle_error(ctx, err)

async def setup(client):
    await client.add_cog(Commands(client=client))