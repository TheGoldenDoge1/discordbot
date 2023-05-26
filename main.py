import discord
from discord import app_commands
from discord.ext import commands
import yt_dlp as youtube_dl
import asyncio

# Токены
token = 'ODI4MTQ5Njg0MTIzMzM2NzM0.G3Q-V-.UWYPjLsPz3tn6k8WoMXA4PQVpRrM_9FVQ3UkQ8'

# Все разрешения интентов
intents = discord.Intents.all()
# Инициализация
bot = commands.Bot(command_prefix=">", intents=intents)

@bot.event
async def on_ready():
    print(f'**logged in as {bot.user.name}**')
    try:
        synced = await bot.tree.sync()
        print(f'** synced {len(synced)} command(s)')
    except Exception as e:
        print(e)
@bot.tree.command(name='test', description='only for developers ^_^')
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f'test command succesfully! {interaction.user.mention}')

@bot.tree.command(name='stop', description='Stop playing current song')
async def stop(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client
    await voice_client.disconnect()
    await interaction.response.send_message(f'**Stopped and disconnected from voice channel {voice_client.channel}**')

@bot.tree.command(name='play')
async def youtubedlplay(interaction: discord.Interaction, link: str):
    ffmpeg_options = {
        'executable': r'C:\Users\thegoldendoge\Downloads\ffmpeg-n4.4-latest-win64-gpl-4.4\ffmpeg-n4.4-latest-win64-gpl-4.4\bin\ffmpeg.exe',
    }
    voice_client = interaction.guild.voice_client
    await interaction.response.defer()


    if not voice_client:
        channel = interaction.user.voice.channel
        voice_client = await channel.connect()
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'song.mp3',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192', }]
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(link, download=False)
        linkydl = info['formats'][-20]['url']
    if voice_client.is_playing():
        voice_client.stop()
    voice_client.play(discord.FFmpegPCMAudio(source=linkydl, **ffmpeg_options))
    await interaction.followup.send(f'**Now playing from YouTube:** {info["title"]}\n**From link:** {link}')

bot.run(token)