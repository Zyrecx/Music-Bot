import wavelink
from discord.ext import commands
from commands.config import EMBED_COLOR
from functions.check_vc import voice_check
from discord import Embed

class Filters(commands.Cog):
    @commands.hybrid_command(name="8d", description="Apply an 8D audio effect to the player", aliases=["3d"])
    @voice_check()
    async def spatial(self, ctx: commands.Context):
        player: wavelink.Player = ctx.voice_client
        speed = 0.1

        try:
            filter = player.filter
            if filter.get('rotation')['rotationHz'] == speed:
                embed = Embed(title="Disabling spatial", color=EMBED_COLOR)
                await player.set_filter(wavelink.Filter(rotation=None))
                await ctx.send(embed=embed)
        except:
            await player.set_filter(wavelink.Filter(rotation=wavelink.filters.Rotation(speed=speed)))
            embed = Embed(title="Enabling spatial", color=EMBED_COLOR)
            await ctx.send(embed=embed)
            return

    @commands.hybrid_command(name="nightcore", description="Speed up the audio of the player and add a nightcore effect", aliases=["nc"])
    @voice_check()
    async def nightcore(self, ctx: commands.Context):
        player: wavelink.Player = ctx.voice_client
        pitch = 1.35
        speed = 1.25

        try:
            filter = player.filter
            if filter.get('timescale')['speed'] == speed:
                await player.set_filter(wavelink.Filter(timescale=wavelink.filters.Timescale()))
                embed = Embed(title="Disabling nightcore", color=EMBED_COLOR)
                await ctx.send(embed=embed)
                
            if filter.get('timescale')['speed'] == 1 or filter.get('timescale')['speed'] != speed:
                await player.set_filter(wavelink.Filter(timescale=wavelink.filters.Timescale(speed=speed, pitch=pitch)))
                embed = Embed(title="Enabling nightcore", color=EMBED_COLOR)
                await ctx.send(embed=embed)

        except:
            await player.set_filter(wavelink.Filter(timescale=wavelink.filters.Timescale(speed=speed, pitch=pitch)))
            await ctx.send("Enabling nightcore")
            return

    @commands.hybrid_command(name="vaporwave", description="Transform the audio of the currently playing song into a vaporwave style")
    @voice_check()
    async def daycore(self, ctx: commands.Context):
        player: wavelink.Player = ctx.voice_client
        pitch = 0.85
        speed = 0.8

        try:
            filter = player.filter
            if filter.get('timescale')['speed'] == speed:
                await player.set_filter(wavelink.Filter(timescale=wavelink.filters.Timescale()))
                embed = Embed(title="Disabling daycore", color=EMBED_COLOR)
                await ctx.send(embed=embed)
                
            if filter.get('timescale')['speed'] == 1 or filter.get('timescale')['speed'] != speed:
                await player.set_filter(wavelink.Filter(timescale=wavelink.filters.Timescale(speed=speed, pitch=pitch)))
                embed = Embed(title="Enabling daycore", color=EMBED_COLOR)
                await ctx.send(embed=embed)

        except:
            await player.set_filter(wavelink.Filter(timescale=wavelink.filters.Timescale(speed=speed, pitch=pitch)))
            embed = Embed(title="Enabling daycore", color=EMBED_COLOR)
            await ctx.send(embed=embed)
            return

async def setup(bot):
    await bot.add_cog(Filters(bot))