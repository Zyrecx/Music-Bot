from discord import Embed
from discord.ext import commands
from config import EMBED_COLOR
from functions.check_vc import voice_check

class Stop(commands.Cog):
    @commands.hybrid_command(name="stop", description="Stop the music and clear the queue")
    @voice_check()
    async def stop(self, ctx: commands.Context):
        player = ctx.voice_client
        if not player:
            embed = Embed(title="Not in voice channel to pause", color=EMBED_COLOR)
            return await ctx.send(embed=embed)
        if player.current is None:
            embed = Embed(title="Not playing anything to pause", color=EMBED_COLOR)
            return await ctx.send(embed=embed)
        
        player.queue.clear()
        await player.stop()
        embed = Embed(title="Player Stopped", color=EMBED_COLOR)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Stop(bot))