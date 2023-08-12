from discord import Embed
from discord.ext import commands
from commands.config import EMBED_COLOR
from functions.check_vc import voice_check

class Resume(commands.Cog):
    @commands.hybrid_command(name="resume", description="Resume playback of the paused song", aliases=["r"])
    @voice_check()
    async def resume(self, ctx: commands.Context):
        player = ctx.voice_client
        if not player:
            embed = Embed(title="Not in voice channel to resume", color=EMBED_COLOR)
            return await ctx.send(embed=embed)
        if player.is_paused():
            await player.resume()
            embed = Embed(title="Resuming", color=EMBED_COLOR)
            return await ctx.send(embed=embed)
        embed = Embed(title="Player not Paused", color=EMBED_COLOR)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Resume(bot))