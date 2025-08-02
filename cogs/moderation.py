import discord

from discord.ext import commands
from utils.err_handle import ErrorHandler

# purge error: enable tracemalloc


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.err_handler = ErrorHandler()

    @commands.Cog.listener()
    async def on_ready(self):
        print("moderation cog is ready")
    
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        try:
            print("kick command")
            await member.kick(reason=reason or "")
            await ctx.send(f"{member} has been kicked by {ctx.message.author.name}")
        
        except Exception as e:
            print(f"error in module {__file__}: ", e)
            await self.err_handler.handle_error(e)
            # maybe write another separate func to handle all sorts of error?
    
    # async def kick_errora(self, ctx, error): 

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        try:
            if not member:
                await ctx.send("i need a member id to ban or their ping")

            await member.ban(reason=reason or "")
            await ctx.send(f"{member} has been banned by {ctx.message.author.name}")
            # i can maybe setup a util.. that'll send either embed as the message or simple message

        except Exception as e:
            print(f"error in module {__file__}: ", e)
            await self.err_handler.handle_error(e)
    
    # async ban_error(self, ctx, error):

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def unban(self, ctx, id: int = None, *, reason=None):
        if id:
            try:
                if not id:
                    await ctx.send("no id given")                
                user = await self.client.fetch_user(id)
                await ctx.guild.unban(user)
                await ctx.send(f"{user} has been unbanned by {ctx.member.author.mame}")
            
            except Exception as e:
                print(f"error in module {__file__}: ", e)
                await self.err_handler.handle_error(e)
    
    # async def unban_error(self, ctx, error)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, limit: int = 1):
        try:
            await ctx.channel.purge(limit=limit, bulk=True)
            ctx.channel.send(f"{limit} messages were removed by {ctx.message.author.name}")
        except Exception as e:
            print(f"error in module {__file__}: ", e)
            await self.err_handler.handle_error(e)
    
    # async def purge_error(self, ctx, error)

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx, member: discord.Member, timelimit='0s', *, reason=None):
        try:
            pass
            # maybe parse the timelimit?? or smth? to fetch it correct?
        except Exception as e:
            print(f"error in module {__file__}: ", e)
            await self.err_handler.handle_error(e)

async def setup(client):
    await client.add_cog(Moderation(client=client))