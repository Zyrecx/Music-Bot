import asyncio
from discord import Embed
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
            embed = Embed(title="Not in voice channel to seek", color=EMBED_COLOR)
            return await ctx.send(embed=embed)
        if player.current is None:
            embed = Embed(title="Not playing anything to seek", color=EMBED_COLOR)
            return await ctx.send(embed=embed)
        if player.is_paused():
            embed = Embed(title="Paused can't seek", color=EMBED_COLOR)
            return await ctx.send(embed=embed)
        
        ms = convert_to_ms(time)

        await player.seek(ms)
        await asyncio.sleep(0.5)

        position = convert_from_ms(player.position)

        embed = Embed(title=f"Seeked player to {position}", color=EMBED_COLOR)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Seek(bot))