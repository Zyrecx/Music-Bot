from discord import Embed
from discord.ext import commands
from config import EMBED_COLOR
from functions.check_vc import voice_check

class Pause(commands.Cog):
    @commands.hybrid_command(name="pause", description="Pause the currently playing song")
    @voice_check()
    async def pause(self, ctx: commands.Context):
        player = ctx.voice_client
        if not player:
            embed = Embed(title="Not in voice channel to pause", color=EMBED_COLOR)
            return await ctx.send(embed=embed)
        if player.current is None:
            embed = Embed(title="Not playing anything to pause", color=EMBED_COLOR)
            return await ctx.send(embed=embed)
        if player.is_paused():
            embed = Embed(title="Already paused", color=EMBED_COLOR)
            return await ctx.send(embed=embed)
        await player.pause()
        embed = Embed(title="Player Paused", color=EMBED_COLOR)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Pause(bot))