import discord, wavelink
from discord.ext import commands
from config import TOKEN

bot = commands.Bot(command_prefix="", intents=discord.Intents.default())

@bot.event
async def on_ready():
    print("Bot Is Ready!")

bot.run(TOKEN)