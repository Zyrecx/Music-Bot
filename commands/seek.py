import asyncio
from discord.ext import commands
from config import EMBED_COLOR
from functions.check_vc import voice_check
from functions.convert_time import convert_from_ms, convert_to_ms

class Seek(commands.Cog):
    @commands.hybrid_command(name="seek", description="Seek to a specific timestamp in the currently playing song")
    @voice_check()
    async def seek(self, ctx: commands.Context, time):
        player = ctx.voice_client
        if not player:
            return await ctx.send("Not in voice channel to seek")
        if player.current is None:
            return await ctx.send("Not playing anything to seek")
        if player.is_paused():
            return await ctx.send("Paused can't seek")
        ms = convert_to_ms(time)
        await player.seek(ms)
        await asyncio.sleep(0.5)
        position = convert_from_ms(player.position)
        await ctx.send(f"Seeked player to {position}")


async def setup(bot):
    await bot.add_cog(Seek(bot))