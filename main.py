import discord
from discord.ext import commands
from config import TOKEN
from client import bot 

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    if hasattr(ctx.command, 'on_error'):
        return
    if "BotMissingPerms" in str(error):
        return
    if isinstance(error, commands.CheckFailure):
        return
    print(f"Error: {error}")
    
@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    try:
        await bot.load_extension(f'commands.{extension}')
        extension = extension.capitalize()
        embed = discord.Embed(title=f"{extension} Loaded", color=0x00FF00)
        await ctx.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(title=f"{extension} Failed", color=0xff0000)
        await ctx.send(embed=embed)
        print(e)

@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
    try:
        await bot.unload_extension(f'commands.{extension}')
        extension = extension.capitalize()
        embed = discord.Embed(title=f"{extension} Unloaded", color=0x00FF00)
        await ctx.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(title=f"{extension} Failed", color=0xff0000)
        await ctx.send(embed=embed)
        print(e)

@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
    try:
        await bot.reload_extension(f'commands.{extension}')
        extension = extension.capitalize()
        embed = discord.Embed(title=f"{extension} Reloaded", color=0x00FF00)
        await ctx.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(title=f"{extension} Failed to reload", color=0xff0000)
        await ctx.send(embed=embed)
        print(e)

bot.run(TOKEN)