import discord, wavelink, os, commands.config as config
from discord.ext import commands
from wavelink.ext import spotify

extentions = []
for files in os.listdir("commands"):
	if files.endswith(".py"):
		extentions.append(files[:-3])

class MusicBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="z!", intents=discord.Intents().all())
        self.synced=False

    async def setup_hook(self):
        for extention in extentions:
                try:
                    await self.load_extension("commands."+extention)
                    print(f'Loaded {extention}')
                except Exception as e:
                    print(f"{extention} cannot be loaded: {e}")
                    
    async def on_ready(self):
        #Sync slash commands
        await self.wait_until_ready()
        if not self.synced:
            await bot.tree.sync()
            self.synced=True

        await bot.loop.create_task(self.connect_nodes())

    async def connect_nodes(self):
        await bot.wait_until_ready()
        sc = spotify.SpotifyClient(client_id=config.SPOTIFY_ID, client_secret=config.SPOTIFY_SECRET)
        node: wavelink.Node = wavelink.Node(uri=config.HOST, password=config.PASSWORD, secure=config.SECURE)
        await wavelink.NodePool.connect(client=bot, nodes=[node], spotify=sc)

        await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.competing, name="iunno"))
        
        for guild in bot.guilds:
            print(f"Joined {guild.name}")
        print("Startup complete!")

bot = MusicBot()
