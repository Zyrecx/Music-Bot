import discord
from discord.ext import commands
from config import EMBED_COLOR
from functions.check_vc import voice_check

class Skip(commands.Cog):
    @commands.hybrid_command(name="skip", description="Skip the currently playing song and move to the next one", aliases=["next", "skp"])
    @voice_check()
    async def skip(self, ctx: commands.Context, song_num: int = 1):
        player = ctx.voice_client
        if not player:
            embed = discord.Embed(title="Not in voice channel to play next song", color=EMBED_COLOR)
            return await ctx.send(embed=embed)
        
        if player.queue.count == 0:
            embed = discord.Embed(title="There are no songs in the queue", color=EMBED_COLOR)
            return await ctx.send(embed=embed)
        
        if song_num < 1 or song_num > player.queue.count:
            embed = discord.Embed(title="Invalid song number", color=EMBED_COLOR)
            return await ctx.send(embed=embed)

        for _ in range(song_num - 1):
            player.queue.get()

        song = player.queue.get()
        await player.play(song)
        embed = discord.Embed(title=f"Skipped to {song.title}", color=EMBED_COLOR)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Skip(bot))