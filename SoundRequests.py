from discord.ext import commands, tasks
import discord.utils
import discord
import Sound
import time
import threading
import io
import asyncio
import Info

class SoundManagment(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.queue = []
        self.task = None
        
    @commands.command()
    async def queue(self,ctx):
        if len(self.queue) > 0:
            string = "```"
            for i,audio in enumerate(self.queue):
                string += str(i+1)+". "+audio.title+" \n"
            string += "```"
            await ctx.send(string)
        else:
            await ctx.send("Queue is empty.")

    @commands.command()    
    async def stop(self,ctx):
        
        while len(self.queue) > 0:
            self.queue.pop()
        await self.skip.invoke(ctx)
        await ctx.send("The Queue have been cleared and I have stoped :(")
        

    @commands.command()
    async def play(self,ctx,url):
        new_youtube_audio =  Sound.YoutubeSound(ctx,str(url))
        if not new_youtube_audio.is_valid:
            await ctx.send("You have requested a invalid YouTube url.")
        else:
            self.queue.append(new_youtube_audio)
            await ctx.send(new_youtube_audio.title+" has been added to the queue. In position "+str(len(self.queue)))
            
    def get_non_volatile(self):
        dir = self.info.server_info["audio_dir"]
        return ""

    @commands.command()
    async def say(self,ctx,name):
        new_audio =  Sound.LocalSound(ctx,name)
        if not new_audio.is_valid:
            await ctx.send("You have requested a invalid sound.")
        else:
            self.queue.append(new_audio)
            await ctx.send(new_audio.title+" has been added to the queue. In position "+str(len(self.queue)))
            
       
    @tasks.loop(seconds=1.0,reconnect=True)
    async def check_queue(self):
        if self.task is None and len(self.queue) > 0:        
            self.task = asyncio.create_task(self.audio_in_voice())
    
        
    @commands.command()
    async def skip(self,ctx):
        vc = discord.utils.get(self.bot.voice_clients,guild=ctx.guild)
        if vc and vc.is_connected():
            await vc.disconnect()
    

    async def audio_in_voice(self):
        # have to use these options so it doesnt error out mid way thorugh song
        FFMPEG_OPTIONS = {
            'before_options': '-re ',
            'options': '-acodec pcm_s16be -ar 44100 -ac 2 -payload_type 10 ',
            'executable' : "/bin/ffmpeg"}

        if len(self.queue) >= 1:

            track = self.queue[0]

            vc = await track.voice_channel.connect()
            vc.play(discord.FFmpegPCMAudio(track.path,options=FFMPEG_OPTIONS))
            # Sleep while audio is playing.
            while vc.is_playing():
                await asyncio.sleep(1)
            print("Song is Over")
            self.queue.pop(0)
            self.task = None
            await vc.disconnect()

    
