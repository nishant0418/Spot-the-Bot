import discord
from discord.ext import commands
from music_cog import music_cog
from help_cog import help_cog
import asyncio

# Intents setup
with open('token.txt', 'r') as file:
    token = file.readlines()[0].strip()

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.voice_states = True
intents.message_content = True 

# Create the bot instance with the desired command prefix and intents
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print("Bot is ready.")

# Load the music cog
async def setup():
    bot.remove_command('help')
    await bot.add_cog(music_cog(bot))
    await bot.add_cog(help_cog(bot))

# Ensure the bot loads the cog
asyncio.run(setup())

# Run the bot
bot.run(token)
