import discord, wavelink
from discord.ext import commands
from config import EMBED_COLOR
from functions.convert_time import convert_from_ms

class NowPlaying(commands.Cog):
    @commands.hybrid_command(name="nowplaying", description="Display the currently playing song", aliases=["np"])
    async def nowplaying(self, ctx: commands.Context):
        player = ctx.voice_client
        if not player:
            embed = discord.Embed(title="I'm not in a voice channel", color=EMBED_COLOR)
            return await ctx.send(embed=embed)
        if player.current is None:
            embed = discord.Embed(title="Not playing anything", color=EMBED_COLOR)
            return await ctx.send(embed=embed)
        else:
            duration = player.current.duration
            duration_str = convert_from_ms(duration)
            position = player.position
            if position < 0:
                position = 0
            position_str = convert_from_ms(position)
            progress = position / duration
            progress_bar_length = 12
            progress_bar_current = round(progress * progress_bar_length)
            progress_bar = " " + "▬" * progress_bar_current + "🔘" + "▬" * (progress_bar_length - progress_bar_current - 1)
            embed = discord.Embed(title="Now Playing", description=f"{player.current.title}\n`{position_str}` {progress_bar}  `{duration_str}`", url=player.current.uri, timestamp=ctx.message.created_at, color=EMBED_COLOR)
            url = await wavelink.YouTubeTrack.fetch_thumbnail(player.current)
            try:
                embed.set_footer(text="Requested by " + player.current.requester.display_name, icon_url=player.current.requester.display_avatar)
            except:pass 
            embed.set_thumbnail(url=url)
            await ctx.send(embed=embed)
        
async def setup(bot):
    await bot.add_cog(NowPlaying(bot))