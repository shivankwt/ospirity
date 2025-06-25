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
        embed = discord.Embed(title=f"test: {channel.name}", description=f"dlksfaj: {channel.category.name}")

        embed.add_field(name = 'ch_id', value=channel.id) # maybe add inline later??

        await ctx.send(embed = embed)

async def setup(client):
    await client.add_cog(Commands(client=client))


