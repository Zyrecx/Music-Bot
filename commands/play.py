import discord, wavelink, urllib.parse
from discord.ext import commands
from wavelink.ext import spotify
from config import EMBED_COLOR

class Play(commands.Cog):
    def __init__(self, bot):
        self.bot:commands.Bot = bot

    @commands.hybrid_command(name="play", description="Play a song or add it to the queue", aliases=["p"])   
    async def play(self, ctx: commands.Context, *, song):
        await ctx.invoke(self.bot.get_command('connect'))

        type = None

        result = urllib.parse.urlparse(song)
        url = all([result.scheme, result.netloc])

        if url:
            if "yout" in song:
                if "list" in song:
                    type = "youtube playlist"
                else: # YT LINK NOT PLAYLIST
                    search = await wavelink.YouTubeTrack.convert(ctx, song)

            elif "spotify" in song:
                decoded = spotify.decode_url(song)
                if decoded['type'] == spotify.SpotifySearchType.playlist:
                    type = "spotify playlist"
                else:
                    search = await spotify.SpotifyTrack.search(song)

            else:
                search = await wavelink.GenericTrack.convert(ctx, song)
        else:
            search = await wavelink.YouTubeTrack.search(song)
            search = search[0]
            

        player: wavelink.Player = ctx.voice_client
        player.textchannel = ctx.channel

        if type == "spotify playlist":
            async for track in spotify.SpotifyTrack.iterator(query=song, type=spotify.SpotifySearchType.playlist):
                track.requester:discord.User = ctx.author
                if player.current is None:
                    await player.play(track)
                else:
                    await player.queue.put_wait(track)
            embed = discord.Embed(title="Added playlist to queue", color=EMBED_COLOR)
            embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.display_icon.url)
            return await ctx.send(embed=embed)
        
        elif type == "youtube playlist":
            embed = discord.Embed(title="",description="Youtube Playlists are not yet implemented :/", color=EMBED_COLOR)
            return await ctx.send(embed=embed)
        
        else:
            search.requester:discord.User = ctx.author

        if player.current is None:
            embed = discord.Embed(title="Added to queue", description=search.title, url=search.uri, color=EMBED_COLOR)
            await ctx.send(embed=embed)
            return await player.play(search)
            
        await player.queue.put_wait(search)
        embed = discord.Embed(title="Added to queue", description=search.title, url=search.uri, color=EMBED_COLOR)
        await ctx.send(embed=embed)    

    @commands.Cog.listener()
    async def on_wavelink_track_start(self, payload:wavelink.TrackEventPayload):
        try:
            channel:discord.TextChannel = payload.player.textchannel
        except:
            return
        embed = discord.Embed(title="Started Playing", description=f"{payload.track.title}", url=payload.track.uri, color=EMBED_COLOR)
        url = await wavelink.YouTubeTrack.fetch_thumbnail(payload.track)
        # embed.set_footer(text=payload.player.current.requester.display_name, icon_url=payload.player.current.requester.display_avatar)
        embed.set_thumbnail(url=url)
        await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Play(bot))