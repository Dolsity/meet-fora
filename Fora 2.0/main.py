import os
from dotenv import load_dotenv
import asyncpg
from discord.ext import commands, ipc
from database.levels import *
from database.prefix import get_prefix
from database.join import *
import logging
import discord
import aiohttp
import io

class Fora(commands.Bot):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.ipc = ipc.Server(self,secret_key = "Swas")

    # Greetings
    async def on_ready(self):
        print(f'Logged in as {bot.user} ({bot.user.id} | In {len(bot.guilds)} guilds')
        await bot.change_presence(status=discord.Status.online, activity = discord.Activity (type = discord.ActivityType.playing, name = f".help | Made with 💜"))

        # Loads all /commands
        for filename in os.listdir('./commands'):
            if filename.endswith('.py'):
                bot.load_extension(f'commands.{filename[: -3]}')

	# IPC ready
    async def on_ipc_ready(self):
        print("Ipc server is ready.")
        
    # IPC error
    async def on_ipc_error(self, endpoint, error):
        print(endpoint, "raised", error)

    # Guild on message XP
    async def on_message(self, message):
        await self.process_commands(message)

        if message.author.bot:
            return

        await increase_xp_guild(self.db, message)
        await increase_xp_global(self.db, message)

# Owner id -- Dolsity
owners = [795969792778698763]

bot = Fora(command_prefix=get_prefix, owner_ids = set(owners),
                   description='Fora Help | Developed by Dolsity#5720 | 795969792778698763')

# Both database ready
async def connect_db():
    load_dotenv()
    password = os.getenv('PASSWORD')
    bot.db = await asyncpg.create_pool(database = "fora", user = "Jay", password = password)
    await create_tables(bot.db)
    print(f'Fora database connected')

# Logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Returns the len of the guilds to the bot
@bot.ipc.route()
async def get_guild_count(data):
	return len(bot.guilds)
    
# Returns the guild ids to the client
@bot.ipc.route()
async def get_guild_ids(data):
	final = []
	for guild in bot.guilds:
		final.append(guild.id)
	return final

# Returns Discord username and ID
@bot.ipc.route()
async def get_guild(data):
	guild = bot.get_guild(data.guild_id)
	if guild is None: return None

	guild_data = {
		"name": guild.name,
		"id": guild.id,
	}

	return guild_data

# Loading data from .env file
load_dotenv()
bot.ipc.start()
token = os.getenv('TOKEN')
bot.loop.run_until_complete(connect_db())
bot.run(token, reconnect=True)