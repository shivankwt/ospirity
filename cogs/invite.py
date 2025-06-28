import discord
import DiscordUtils
from discord.ext import commands

class Invite(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.tracker = DiscordUtils.InviteTracker(client)

    @commands.Cog.listener()
    async def on_ready(self):
        print("invide cog is ready")
        await self.tracker.cache_invites() # fetch current invites for the server maybe?

    @commands.Cog.listener()
    async def on_invite_create(self, invite): # updates the prev. cache invite but there's more to it than this.
        await self.tracker.update_invite_cache(invite=invite)

    @commands.Cog.listener()
    async def on_invite_delete(self, invite):
        await self.tracker.remove_invite_cache(invite=invite)
    
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        # the issue here is it depends on the logs channel but in the scenario "logs" named channel doesn't exist most of the cmd
        # won't work. i've to find a way around this issue
        pass

    async def setup(client):
        await client.add_cog(Invite(client=client))