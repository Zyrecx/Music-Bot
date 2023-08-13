import discord, wavelink
from discord.ui import Button, View, Modal, TextInput
from discord.ext import commands
from config import EMBED_COLOR
from functions.check_vc import voice_check

class AddSong(Modal, title="Add Song"):
    def __init__(self, bot, *args, **kwargs):
        self.bot:commands.Bot = bot
        super().__init__(*args, **kwargs)

    input = TextInput(label="Enter song name to add it to the queue", style=discord.TextStyle.short, required=True)

    async def on_submit(self, interaction:discord.Interaction):
        msg = str(self.input)

        search = await wavelink.YouTubeTrack.search(msg)
        search = search[0]
        player: wavelink.Player = interaction.guild.voice_client
        player.textchannel = interaction.channel
        search.requester:discord.User = interaction.user
        embed = discord.Embed(title="Added to queue", description=search.title, url=search.uri, color=EMBED_COLOR)
        if player.current is None:
            await player.play(search)
        else:
            await player.queue.put_wait(search)
        await interaction.response.send_message(embed=embed, delete_after=5)
        
class Controls(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name="controls", description="View the music player controls with interactive buttons")
    @voice_check()
    async def controls(self, ctx:commands.Context):
        if not ctx.voice_client: return await ctx.send("I'm not in a voice channel")
        if ctx.author.voice.channel.id != ctx.voice_client.channel.id:
            return await ctx.reply("You must be in the same voice channel as the bot", ephemeral=True)
        
        view = View()
        embed = discord.Embed(title="Control Music Player", description=f"<#{ctx.author.voice.channel.id}>", color=EMBED_COLOR)

        stop = Button(emoji="⏹️", style=discord.ButtonStyle.blurple)
        playpause = Button(emoji="⏯️", style=discord.ButtonStyle.blurple)
        next = Button(emoji="⏭️", style=discord.ButtonStyle.blurple)
        addsong = Button(emoji="➕", style=discord.ButtonStyle.blurple)

        Buttons = [stop, playpause, next, addsong]

        async def ppButton(Interaction:discord.Interaction):
            player:wavelink.Player = Interaction.guild.voice_client
            paused = player.is_paused()

            if paused:
                await player.resume()
                await Interaction.response.send_message("Resuming!", delete_after=4)
            else:
                await player.pause()
                await Interaction.response.send_message("Paused!", delete_after=4)

        async def stopButton(Interaction:discord.Interaction):
            player:wavelink.Player = Interaction.guild.voice_client
            if player.current is None:
                return await Interaction.response.send_message("Not playing anything to pause")
            player.queue.clear()
            await player.stop()
            await Interaction.response.send_message("Player Stopped!", delete_after=4)

        async def nextButton(Interaction:discord.Interaction):
            player:wavelink.Player = Interaction.guild.voice_client
            if player.queue.count == 0:
                embed = discord.Embed(title="There are no songs in the queue", color=EMBED_COLOR)
                return await Interaction.response.send_message(embed=embed, delete_after=2)

            song = player.queue.get()
            await player.play(song)
            await Interaction.response.send_message(f"Skipped to {song.title}")

        async def addsongButton(Interaction:discord.Interaction):
            await Interaction.response.send_modal(AddSong(bot=self.bot))
                
        stop.callback = stopButton
        playpause.callback = ppButton
        next.callback = nextButton
        addsong.callback = addsongButton
        for button in Buttons:
            view.add_item(button)
        await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Controls(bot))