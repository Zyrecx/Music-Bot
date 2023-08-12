from discord import Embed
from discord.ext import commands
from commands.config import EMBED_COLOR
from functions.check_vc import voice_check

class Pause(commands.Cog):
    @commands.hybrid_command(name="pause", description="Pause the currently playing song")
    @voice_check()
    async def pause(self, ctx: commands.Context):
        player = ctx.voice_client
        if not player:
            embed = Embed(title="Not playing anything", color=EMBED_COLOR)

            return await ctx.send("Not in voice channel to pause")
        if player.current is None:
            return await ctx.send("Not playing anything to pause")
        if player.is_paused():
            return await ctx.send("Already paused")
        await player.pause()
        await ctx.send(f"Player Paused")

async def setup(bot):
    await bot.add_cog(Pause(bot))