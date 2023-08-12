from discord.ext import commands
from config import EMBED_COLOR
from functions.check_vc import voice_check

class Stop(commands.Cog):
    @commands.hybrid_command(name="stop", description="Stop the music and clear the queue")
    @voice_check()
    async def stop(self, ctx: commands.Context):
        player = ctx.voice_client
        if not player:
            return await ctx.send("Not in voice channel to pause")
        if player.current is None:
            return await ctx.send("Not playing anything to pause")
        player.queue.clear()
        await player.stop()
        await ctx.send(f"Player Stopped")

async def setup(bot):
    await bot.add_cog(Stop(bot))