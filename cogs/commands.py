import discord
from discord.ext import commands


class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("commmand cog is ready.")

    def error_embed(self, title, description):
        embed = discord.Embed(title=title, description=description, color=0xFF0000)
        return embed
    
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
            await self.error_handle(ctx, e)

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
            await self.error_handle(ctx, e) # send error message with error_handle/ also create a separate utility.py ?




async def setup(client):
    await client.add_cog(Commands(client=client))


