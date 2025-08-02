import discord
import datetime
import pyquotegen

from utils.err_handle import ErrorHandler # inst utils. 
from discord.ext import commands

class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.err_handler = ErrorHandler()

    @commands.Cog.listener()
    async def on_ready(self):
        print("commmand cog is ready.")

    @commands.command(aliases=['stats', 'cs', 'cstats'])
    async def channelstats(self, ctx):

        print("channel stats command initiated")
        channel = ctx.channel
        
        try:
            embed = discord.Embed(title=f"test: {channel.name}", description=f"category name: {channel.category.name}")

            embed.add_field(name="channel id:", value=channel.id, inline=False)
            embed.add_field(name="channel topic:", value=channel.topic or "no topic given", inline=False) # add color too maybe later ig
            embed.add_field(name="channel position:", value=channel.position + 1, inline=False)
            embed.add_field(name="channel slowmode delay:", value=channel.slowmode_delay, inline=False)
            embed.add_field(name="channel environment:", value="nsfw: 18+" if channel.is_nsfw() else "not nsfw: 18-", inline=False)
            embed.add_field(name="channel permissions synced status:", value=channel.permissions_synced, inline=False)
            embed.add_field(name="channel at:", value=channel.created_at.strftime("%Y-%m-%d, %H-%M-%S"), inline=False)

            await ctx.send(embed=embed)

        except Exception as e:
            print(f"error in module {__file__}: ", e)
            await self.err_handler.handle_error(ctx, e)

    @commands.command(aliases=['info', 'inf'])
    async def about(self, ctx, member: discord.Member):
        print("member information command initiated")

        try:
            embed = discord.Embed(title=f"information about: {member.display_name}")
            
            embed.add_field(name="created on: ", value=member.created_at.strftime("%Y-%m-%d"), inline=False)
            embed.add_field(name="joined on", value=member.joined_at.strftime("%Y-%m-%d"), inline=False)
            embed.add_field(name="global name", value=member.global_name or "Not Available", inline=False)
            embed.add_field(name="id", value=member.id, inline=False) # color

            await ctx.send(embed=embed)

        except Exception as e:
            print(f"error in module {__file__}: ", e)
            await self.handle_error(ctx, e) # send error message with handle_error/ also create a separate utility.py ?

    @commands.command(aliases=['av', 'pp'])
    async def avatar(self, ctx, member: discord.Member=None):
        try:
            member = member or ctx.author # pinged member or self
            embed = discord.Embed(title=f"{member.display_name}'s avatar", color=0x0FF00)
            embed.set_image(url=member.display_avatar.url)
            embed.set_footer(text="created by ospirity")
            await ctx.send(embed=embed)
        
        except Exception as e:
            print(f"error in module {__file__}: ", e)
            await self.handle_error(ctx, e)


    @commands.command()
    async def ping(self, ctx):
        try: 
            await ctx.send(f"ping: {round(self.client.latency * 1000)} ms")
        except Exception as e:
            print(f"error in module {__file__}: ", e)
            await self.handle_error(ctx, e)

    @commands.command()
    async def quote(self, ctx, category: str = None):
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
                await ctx.send(quote)
            
            elif category.lower() in categories:
                quote = pyquotegen.get_quote(category.lower())
                await ctx.send(quote)
            
            else:
                await ctx.send("incorrect category! please choose from: " + ", ".join(categories))

        except Exception as e:
            print(f"error in module {__file__}: ", e)
            await self.err_handler.handle_error(ctx, e)

    @commands.command(aliases=['cap'])
    @commands.bot_has_guild_permissions(read_messages=True)
    async def caption(self, ctx):
        try:
            print("caption command")
            if ctx.message.reference:
                reference = ctx.message.reference.resolved
                print(ctx.messsage.reference)
                print(reference)

                if not reference:
                    reference = await ctx.channel.fetch_message(ctx.message.reference.message_id)
                    message, author, url = reference.content, reference.author, reference.jump_url 

                    print(url)
                    print(message, author)

        except Exception as e:
            await self.handle_error(ctx, e)

async def setup(client):
    await client.add_cog(Commands(client=client))