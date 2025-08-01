import discord
from discord.ext import commands
import datetime
from utils.err_handle import ErrorHandler # inst utils. 

class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.err_handler = ErrorHandler()

    @commands.Cog.listener()
    async def on_ready(self):
        print("commmand cog is ready.")

    @commands.command(aliases=['stats', 'cs', 'cstats'])
    @commands.bot_has_guild_permissions()
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
    @commands.bot_has_guild_permissions()
    async def about(self, ctx, member: discord.Member):
        print("member information command initiated")

        try:
            embed = discord.Embed(title=f"information about: {member.display_name}")
            
            embed.add_field(name="created on: ", value=member.created_at.strftime("%Y-%m-%d"), inline=False)
            embed.add_field(name="joined on", value=member.joined_at.strftime("%Y-%m-%d"), inline=False)
            embed.add_field(name="global name", value=member.global_name or "n/a", inline=False)
            embed.add_field(name="id", value=member.id, inline=False) # color

            await ctx.send(embed=embed)

        except Exception as e:
            print(f"error in module {__file__}: ", e)
            await self.handle_error(ctx, e) # send error message with handle_error/ also create a separate utility.py ?

    @commands.command(aliases=['av', 'pp'])
    @commands.bot_has_guild_permissions()
    async def avatar(self, ctx, member: discord.Member=None):
        try:
            member = member or ctx.author # pinged member or self
            embed = discord.Embed(title=f"{member.display_name}'s avatar", color=0x0FF00)
            embed.set_image(url=member.display_avatar.url)
            embed.set_footer(text="created by ospirity")
            await ctx.send(embed=embed)
        
        except Exception as e:
            await self.handle_error(ctx, e)


    @commands.command()
    async def ping(self, ctx):
        try: 
            await ctx.send(f"ping: {round(self.client.latency * 1000)} ms")
        except Exception as e:
            await self.handle_error(ctx, e)

    @commands.command(aliases=['q'])
    @commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
    async def quote(self, ctx, cagtegory: str = None): # not working!
        print("quote command initiated")

        try:
            if cagtegory:
                quote_data = get_quotes(category=cagtegory)
            else:
                print("random category")
                quote_data = get_quotes(random=True)
                print(quote_data)
            if not quote_data or "data" not in quote_data or not quote_data['data']:
                raise ValueError("no quotes found for the given category")
            
            for key in quote_data["data"]:
                embed = discord.Embed(color=0xFFFFFFF)
                embed.add_field(name="huh", value=key['quote'], inline=False)
                embed.set_footer(text=f" - {key['author']}")

                print(key['quote'])

                await ctx.send(embed=embed)
    
        except Exception as e:
            await self.handle_error(ctx, e)
# update later
    # @commands.command(aliases=['cap'])
    # @commands.bot_has_guild_permissions(read_messages=True)
    # async def caption(self, ctx):
    #     try:
    #         if ctx.message.reference:
    #             reference = ctx.message.reference.resolved
    #             if not reference:
    #                 reference = await ctx.channel.fetch_message(ctx.message.reference.message_id)
    #                 message, author, url = reference.content, reference.author, reference.jump_url 

    #                 print(url)
    #                 print(message, author)

    #                 embed = discord.Embed()
    #     except Exception as e:
    #         await self.handle_error(ctx, e)

async def setup(client):
    await client.add_cog(Commands(client=client))