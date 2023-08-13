from discord import Embed
from discord.ext import commands
from player.player import MusicPlayer
from config import EMBED_COLOR
from functions.check_vc import voice_check

class Connect(commands.Cog):
    @commands.command()
    @voice_check()
    async def connect(self, ctx:commands.Context):
        if ctx.voice_client:
            player: MusicPlayer = ctx.voice_client
            if ctx.author.voice.channel != player.channel:
                await player.move_to(ctx.author.voice.channel)
    
        if not ctx.voice_client:
            player = MusicPlayer(textchannel=ctx.channel)
            vc = await ctx.author.voice.channel.connect(cls=player)
            embed = Embed(title=f"Joined {vc.channel}", color=EMBED_COLOR)
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Connect(bot))