from discord import Embed
from discord.ext import commands
from config import EMBED_COLOR
from functions.check_vc import voice_check

class Disconnect(commands.Cog):
    @commands.hybrid_command(name="disconnect", description="Disconnect the bot from the voice channel and clear the song queue", aliases=["dc", "leave"])
    @voice_check()
    async def disconnect(self, ctx:commands.Context):
        if not ctx.voice_client:
            embed = Embed(title="Not in Voice Chat", color=EMBED_COLOR)
            await ctx.send(embed=embed)
        else:  
            await ctx.voice_client.disconnect()
            embed = Embed(title="Left voice channel", color=EMBED_COLOR)
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Disconnect(bot))