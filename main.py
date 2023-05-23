import discord
from discord.ext import commands
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Токены и пороли
SPOTIFY_CLIENT_ID = ''
SPOTIFY_CLIENT_SECRET = ''
token = ''
# Интенты дискорд

intents = discord.Intents.default()
intents.voice_states = True
intents.message_content = True
# Инициализация
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id = SPOTIFY_CLIENT_ID, client_secret = SPOTIFY_CLIENT_SECRET))
bot = commands.Bot(command_prefix=">", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def play(ctx, url):
    ffmpeg_path = r'C:\Users\thegoldendoge\Downloads\ffmpeg-n6.0-latest-win64-lgpl-shared-6.0\ffmpeg-n6.0-latest-win64-lgpl-shared-6.0\bin\ffmpeg.exe'
    channel = ctx.author.voice.channel

    if not channel:
        await ctx.send("You are not connected to a voice channel.")
        return

    voice_client = ctx.voice_client

    if voice_client and voice_client.is_playing():
        voice_client.stop()

    if not voice_client or not voice_client.is_connected():
        voice_client = await channel.connect()
        await ctx.send(f'** connected to {channel} **')
    audio_source = discord.FFmpegPCMAudio(url, executable=ffmpeg_path)
    voice_client.play(audio_source)
    await ctx.send("**playing...**")

@bot.command()
async def stop(ctx):
    voice_client = ctx.voice_client

    if voice_client and voice_client.is_playing():
        voice_client.stop()
        await ctx.send("**playback stopped :(**")
    else:
        await ctx.send("**no audio is currently playing**")

@bot.command()
async def disconnect(ctx):
    voice_client = ctx.voice_client

    if voice_client:
        await voice_client.disconnect()
        await ctx.send("**bot disconnected from the voice channel**")
    else:
        await ctx.send("**bot is not connected to a voice channel**")

bot.run(token)