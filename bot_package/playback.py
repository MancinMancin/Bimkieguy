from discord.ext import tasks, commands
import discord
import yt_dlp
import os
import shutil

class Playback(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.ydl_opts = {
            'format': 'bestaudio',
            'noplaylist': False,
            'quiet': True,
            'outtmpl': 'downloads/%(id)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        self.is_playing = False
        self.song_queue: list = []

    async def connect_to_invoker_channel(self, ctx: commands.Context) -> discord.VoiceChannel:
        if ctx.author.voice is None:
            await ctx.send("You're not in a voice channel")
            return
        elif ctx.voice_client is None:
            channel = ctx.author.voice.channel
            voice = await channel.connect()
        elif ctx.author.voice.channel != ctx.voice_client.channel:
            await ctx.voice_client.disconnect()
            channel = ctx.author.voice.channel
            voice = await channel.connect()
        else:
            voice = ctx.voice_client.channel
        return voice

    def gather_video_info_add_to_queue(self, url: str):
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                
                if "entries" in info: # If it's a playlist
                    for video in info["entries"]:
                        video_info = {
                            "id": video.get("id"),
                            "title": video.get("title"),
                            "url": video.get("webpage_url"),
                            "filename": ydl.prepare_filename(video).replace("webm", "mp3")
                        }
                        self.song_queue.append(video_info)
                    songs_number = len(info["entries"])
                    
                else: # If it's a single video
                    video_info = {
                        "id": info.get("id"),
                        "title": info.get("title"),
                        "url": url,
                        "filename": ydl.prepare_filename(info).replace("webm", "mp3")
                    }
                    songs_number = 1
                    self.song_queue.append(video_info)
            
            except Exception as e:
                return e
            
            return songs_number

    def download_audio_file(self, video: dict):
        """Download video."""
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            try:
                ydl.download([video["url"]])
            except Exception as e:
                return e
            
    def clear_downloads_folder(self):
        folder = "downloads"
        
        # Check if folder exists
        if os.path.exists(folder):
            # Remove all files in the folder
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)  # Remove the file
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)  # Remove the folder and its contents
                except Exception as e:
                    print(f'Failed to delete {file_path}. Reason: {e}')
        else:
            print(f"The folder '{folder}' does not exist.")        

    async def disconnect_bot(self, ctx: commands.Context) -> None:
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            self.clear_downloads_folder()
            self.song_queue.clear()

    async def play_next(self, ctx: commands.Context) -> None:
        """Play the next song in the queue."""
        if len(self.song_queue) > 0:
            self.is_playing = True
            video_info = self.song_queue.pop(0)
            filename = video_info['filename']

            # Download the song
            error = self.download_audio_file(video_info)
            # If error, return it to send it
            if error:
                return error

            # Play the song
            ctx.voice_client.play(discord.FFmpegPCMAudio(source=filename), after=lambda e: self.bot.loop.create_task(self.play_next(ctx)))

        else: # No more songs in the queue, disconnect
            self.is_playing = False
            await self.disconnect_bot(ctx)

    @commands.command()
    async def play(self, ctx: commands.Context, url: str = None) -> None:
        if not url:
            await ctx.send("Give me a link")
            return
        await self.connect_to_invoker_channel(ctx) # Connect the bot to channel
        songs_number = self.gather_video_info_add_to_queue(url) # Get info about songs from url and append them to the queue
        if type(songs_number) == Exception:
            await ctx.send(f"Error: {songs_number}")
            return

        await ctx.send(f"Added {songs_number} song(s) to the queue. Queue contains {len(self.song_queue)} song(s).")

        # If nothing is playing, start playback
        if not self.is_playing:
            error = await self.play_next(ctx)
            if error:
                await ctx.send(f"Error")

    @commands.command()
    async def skip(self, ctx: commands.Context):
        """Skip the current song."""
        if len(self.song_queue) == 0:
            await ctx.send("The queue is empty")
            return
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("Skipping current song")

    @commands.command()
    async def queue(self, ctx: commands.Context):
        """Display the current song queue"""
        if len(self.song_queue) == 0:
            await ctx.send("The queue is empty")
            return
        queue_list = []
        for i, video in enumerate(self.song_queue):
            video_title = video["title"]
            queue_list.append(f"{i+1}. {video_title}")
        songs = "\n".join(x for x in queue_list)
        await ctx.send(f"Current queue:\n{songs}")
            

async def setup(bot):
    await bot.add_cog(Playback(bot))