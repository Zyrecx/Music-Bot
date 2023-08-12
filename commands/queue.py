import discord
from discord.ext import commands
from discord.ui import Button, View
from config import EMBED_COLOR

class Queue(commands.Cog):
    @commands.hybrid_command(name="queue", description="View the current song queue", aliases=["q"])
    async def queue(self, ctx: commands.Context):
        player = ctx.voice_client
        if not player:
            return await ctx.send("Not in a voice channel to have a queue.")
        if player.queue.count == 0:
            embed = discord.Embed(title="There are no songs in the queue", color=EMBED_COLOR)
            return await ctx.send(embed=embed)
        queue_list = [f'{i}. {song.title}' for i, song in enumerate(player.queue, start=1)]

        chunk_size = 10  
        chunks = [queue_list[i:i + chunk_size] for i in range(0, len(queue_list), chunk_size)]
        current_page = 0  

        embed = discord.Embed(title='Current Queue', color=EMBED_COLOR)
        embed.add_field(name="", value='\n'.join(chunks[current_page]), inline=False)

        view = View()
        
        if len(chunks) != 1:
            embed.set_footer(text=f'Page {current_page + 1}/{len(chunks)}')
            button_previous = Button(emoji='⬅️', style=discord.ButtonStyle.gray)
            button_next = Button(emoji='➡️', style=discord.ButtonStyle.gray)

            async def previous_button(interaction:discord.Interaction):
                nonlocal current_page
                current_page = (current_page - 1) % len(chunks)
                embed.set_field_at(0, name='', value='\n'.join(chunks[current_page]))
                embed.set_footer(text=f'Page {current_page + 1}/{len(chunks)}')
                await interaction.response.edit_message(embed=embed)

            async def next_button(interaction:discord.Interaction):
                nonlocal current_page
                current_page = (current_page + 1) % len(chunks)
                embed.set_field_at(0, name='', value='\n'.join(chunks[current_page]))
                embed.set_footer(text=f'Page {current_page + 1}/{len(chunks)}')
                await interaction.response.edit_message(embed=embed)

            button_previous.callback = previous_button
            button_next.callback = next_button
            view.add_item(button_previous)
            view.add_item(button_next)

        await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Queue(bot))