import discord
from discord import app_commands
from discord.ext import commands
import youtube_dl

# Токены
token = ''

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
@bot.tree.command(name='test')
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f'test command succesfully! {interaction.user.mention}')

@bot.tree.command(name='play')
async def play(interaction: discord.Interaction, url: str):
    ffmpeg_path = r'C:\Users\thegoldendoge\Downloads\ffmpeg-2023-05-22-git-877ccaf776-full_build\bin\ffmpeg.exe'
    channel = interaction.user.voice.channel
    voice_client = interaction.guild.voice_client
    if voice_client is None:
        voice_client = await channel.connect()
    else:
        await voice_client.move_to(channel)

    audio_source = discord.FFmpegPCMAudio(url, executable=ffmpeg_path)
    voice_client.play(audio_source)

    await interaction.response.send_message('Playing song from url')
@bot.tree.command(name='stop', description='Stop playing current song')
async def stop(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client
    await voice_client.disconnect()
    await interaction.response.send_message('Stopped and disconnected from voice channel')

bot.run(token)