import discord
from discord.ext import commands

class ErrorHandler:
    def error_embed(self, title, description):
        embed = discord.Embed(
            title=title,
            description=description,
            color=0xFF0000,  # no idea aoub this colour
        )
        embed.set_footer(text=" - by ospirity")
        return embed

    async def handle_error(self, ctx, error):
        print("error occurred:", error)

        if isinstance(error, discord.Forbidden):
            embed = self.error_embed("permission denied", "I don't have permission to perform this action.")
            
        elif isinstance(error, discord.HTTPException):
            embed = self.error_embed("http error", "An error occurred, please try again.")

        elif isinstance(error, discord.NotFound):
            embed = self.error_embed("not found!", "Requested resource was not found.")

        elif isinstance(error, ValueError):
            embed = self.error_embed("invalid input", "Please provide correct format, use `.help`.")

        elif isinstance(error, commands.MissingRequiredArgument):
            embed = self.error_embed("missing argument", "You must provide the required argument. Use `.help`.")

        elif isinstance(error, commands.MissingPermissions):
            embed = self.error_embed("missing permissions", "You don't have required permissions!")

        else:
            embed = self.error_embed("unexpected error", f"An unexpected error occurred: {error}")

        await ctx.send(embed=embed)
