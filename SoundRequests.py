from discord.ext import commands, tasks
import discord
import Sound
import time
import threading

class SoundManagment(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.queue = []
        self.song_thread = None
   
    @commands.command()
    async def queue(self,ctx):
        string = "```"
        for i,audio in enumerate(self.queue):
            string += str(i)+". "+audio.title+" \n"
        string += "```"
        await ctx.send(string)



    @commands.command()
    async def play(self,ctx,url):
        new_youtube_audio =  Sound.YoutubeSound(ctx,str(url))
        if not new_youtube_audio.is_valid:
            await ctx.send("You have requested a invalid YouTube url.")
        else:
            self.queue.append(new_youtube_audio)
            await ctx.send(new_youtube_audio.title+" has been added to the queue. In position "+str(len(self.queue)))
            await self.audio_in_voice()

    @commands.command()
    async def say(self,ctx,name):
        new_audio =  Sound.LocalSound(ctx,name)
        if not new_audio.is_valid:
            await ctx.send("You have requested a invalid sound.")
        else:
            self.queue.append(new_audio)
            await ctx.send(new_audio.title+" has been added to the queue. In position "+str(len(self.queue)))
            await self.audio_in_voice()


    async def audio_in_voice(self):
        # have to use these options so it doesnt error out mid way thorugh song
        FFMPEG_OPTIONS = {
            'before_options': '-re reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn ',
            'executable' : "/bin/ffmpeg"}

        if len(self.queue) >= 1:
            track = self.queue[0]
            vc = await track.voice_channel.connect()
            vc.play(discord.FFmpegOpusAudio(track.path,options=FFMPEG_OPTIONS))
            # Sleep while audio is playing.
            while vc.is_playing():
                print(track.title)
                time.sleep(1)
            await vc.disconnect()
    '''
    @tasks.loop(seconds=1.0,reconnect=True)
    async def check_queue(self):
        self.trim_tracked_chores()

        # this check must be done because on the first run of loop it will return a None object because boot has 
        # not connected
        
        todays_chores = Info.ChoreInfo(self.bot.get_cog("ServerInformation").server_info).get_todays_chores()

        if todays_chores != None:
            channel = self.bot.get_channel(self.info["House"]["remind_channel"])
            for i in todays_chores:
                if i.id not in self.notified_chores:
                    if i.name == "garbage_carry" and 
                    message_string = "You have to"+i.name+ " . It requires you to "+i.description+"."
                    user = self.bot.get_user(self.info["House"]["users"][i.next_execution_assigned_user.first_name])

                    if user != None and channel != None:
                                    
                        self.notified_chores[i.id] =  time.localtime((time.time()))
                        
                        await channel.send(user.mention+" "+self.generate_open()+". "+message_string)
    '''       

