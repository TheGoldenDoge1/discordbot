import discord
from discord import app_commands
from discord.ext import commands
import yt_dlp as youtube_dl
import asyncio
import openai

# Токены
token = '123'
openai.api_key = '123'
# Все разрешения интентов
intents = discord.Intents.all()

# cfg
ffmpeg_options = {
    'executable': r'./ffmpeg/bin/ffmpeg.exe',
    'options': '-vn -b:a 128k',
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
}

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': 'song.mp3',
    'noplaylist': True,
    'ytdl_format_args': [
        '-f', 'bestaudio/best[abr<=128]/best[asr<=44100]',
        '--recode-video', 'mp4'
    ],
    'postprocessors': [
        {
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }
    ],
}
# Инициализация
bot = commands.Bot(command_prefix=">", intents=intents)

#бд бота
history=[]

@bot.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.listening, name="YouTube Music bot")
    print(f'** logged in as {bot.user.name} **')
    try:
        synced = await bot.tree.sync()
        print(f'** synced {len(synced)} command(s)')
    except Exception as e:
        print(e)
    await bot.change_presence(activity=activity)
@bot.tree.command(name='stop', description='Stop playing current song')
async def stop(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client
    await voice_client.disconnect()
    await interaction.response.send_message(f'**Stopped and disconnected from voice channel {voice_client.channel}**')

# Музика
@bot.tree.command(name='play', description='Playing music from link (currently supported: YouTube)')
async def play(interaction: discord.Interaction, link: str):
    voice_client = interaction.guild.voice_client
    await interaction.response.defer()

    if not voice_client:
        channel = interaction.user.voice.channel
        voice_client = await channel.connect(reconnect = True)
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(link, download=False)
        linkydl = info['url']
        print('EXTRACTED LINK: ', linkydl)
    if voice_client.is_playing():
        voice_client.stop()
    voice_client.play(discord.FFmpegPCMAudio(source=linkydl, **ffmpeg_options))
    await interaction.followup.send(f'**Now playing:** *{info["title"]}*\n**From link:** *{link}*')

@bot.tree.command(name='search', description='Search video on YouTube')
async def search(interaction: discord.Interaction, search: str):
    await interaction.response.defer()
    voice_client = interaction.guild.voice_client
    url = None
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{search}", download=False)
        print(info)
        for entry in info['entries']:
            for format in entry['formats']:
                url = format['url']
                if not url.startswith('https://i.ytimg.com'):
                    break
            if url:
                break
        print('EXTRACTED URL: ', url)
        if not voice_client:
            channel = interaction.user.voice.channel
            voice_client = await channel.connect(reconnect=True)
        if voice_client.is_playing():
            voice_client.stop()
        source = discord.FFmpegPCMAudio(url, **ffmpeg_options)
        voice_client.play(source)
        await interaction.followup.send(
            f'**Now playing:** ***{info["entries"][0]["title"]}***\n**From link:** ***https://youtube.com/watch?v=' + str(info["entries"][0]["id"]) + '***')

@bot.tree.command(name='chatgpt', description='Ask a Question to ChatGPT 3.5')
async def chatgpt(interaction: discord.Interaction, message: str):
    await interaction.response.defer()
    if len(message) > 500:
        message = message[:500]
    history.append({
        'role': 'user',
        'content': message
    })
    messages = [
        {'role': 'system', 'content': 'I am a girl and human.'},
        *history
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.9,
        max_tokens=500,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
    )
    reply = response['choices'][0]['message']['content']
    history.append({'role': 'assistant', 'content': reply})
    await interaction.followup.send(f'- {reply}')

bot.run(token)