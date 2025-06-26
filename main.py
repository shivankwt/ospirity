import os
import asyncio 
import discord
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()

# bot intents 

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True


# instance 

client = commands.Bot(command_prefix='.', intents=intents)


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle) # defualt status: idle
    print("bot started")

@client.event
async def on_message(message):
    if message.author.bot:
        return 
    await client.process_commands(message)


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
    try:
        await load_cogs()

        async with client:
            await client.start(os.getenv('DISCORD_API_KEY'))
    
    except KeyboardInterrupt:
        print("bot has been shut down")

asyncio.run(main())