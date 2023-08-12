from discord.ext import commands
from discord import Embed

def voice_check():
    async def predicate(ctx):
        if not ctx.author.voice:
            embed = Embed(title="", description="You need to be in a voice channel to use this command.")
            await ctx.send(embed=embed)
            return False
        return True
    return commands.check(predicate)
