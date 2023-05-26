import discord
from discord import app_commands
from discord.ext import commands
import yt_dlp as youtube_dl
import asyncio
import openai

# Токены

# Все разрешения интентов
intents = discord.Intents.all()
# Инициализация
bot = commands.Bot(command_prefix=">", intents=intents)

@bot.event
async def on_ready():
    print(f'** logged in as {bot.user.name} **')
    try:
        synced = await bot.tree.sync()
        print(f'** synced {len(synced)} command(s)')
    except Exception as e:
        print(e)
@bot.tree.command(name='info', description='Only for developers ^_^')
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f'hello :)')

@bot.tree.command(name='stop', description='Stop playing current song')
async def stop(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client
    await voice_client.disconnect()
    await interaction.response.send_message(f'**Stopped and disconnected from voice channel {voice_client.channel}**')

@bot.tree.command(name='play', description='Playing music from link (currently supported: YouTube)')
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
        'outtmpl': 'song.mp3',
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192', }]
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(link, download=False)
        linkydl = info['url']
        print('EXTRACTED LINK: ', linkydl)
    if voice_client.is_playing():
        voice_client.stop()
    voice_client.play(discord.FFmpegPCMAudio(source=linkydl, **ffmpeg_options))
    await interaction.followup.send(f'**Now playing from YouTube:** {info["title"]}\n**From link:** {link}')
history = []
@bot.tree.command(name='chatgpt', description='Ask a Question to ChatGPT 3.5')
async def chatgpt(interaction: discord.Interaction, message: str):
    await interaction.response.defer()

    history.append({
        'role': 'user',
        'content': message
    })
    messages = [
        {'role': 'system', 'content': 'You are a girl.'},
        *history
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
    )
    reply = response['choices'][0]['message']['content']
    history.append({'role': 'assistant', 'content': reply})
    await interaction.followup.send(f'- {reply}')

bot.run(token)