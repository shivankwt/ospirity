import os,  asyncio, discord
from discord.ext import commands

# bot intents 

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True


# instance 

client = commands.Bot(command_prefix='.', intents=intents)


async def load_cogs(): # loading cogs from "cogs" dir.
    try:
        cogs_directory = "./cogs"
        for file in os.listdir(cogs_directory):

            if file.endswith(".py"):
                await client.load_extension(f"cogs.{file[:-3]}")
                print("loaded cog: ", file)
    except Exception as e:
        print("failed: ", e)

async def main(): # start the bot
    
    await load_cogs()

    async with client:
        await client.start(os.getenv("DISCORD_API_KEY"))

asyncio.run(main())