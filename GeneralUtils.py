
import time
import re

from discord.ext import commands, tasks
import shutil
import discord.utils
import discord
from urllib.parse import urlparse
import requests

import Info
import Sound
class Utils(commands.Cog):
    def __init__(self,bot):
        self.info = Info.ServerInformation("Data Files/server_info.json")
        self.bot = bot


    def padding(self,string,length = 12):
        if len(string) >= length:
            return string
        else:
            return string + " "* (length-len(string))

    # returns the lenghth of max length string in the list 
    def max_length(self,strings):
        max_len = 0

        for i in strings:
            if len(i) > max_len:
                max_len = len(i)
        return max_len 


    @commands.command()
    async def help(self,ctx):
        self.info.update()
        commands = self.info.server_info["command_help"]
        keys = sorted(commands.keys())

        max_len = self.max_length(keys)
        message = "```Prefix for all commands is $ \n\n"
        message += "Commands: \n"

        for i in keys:
            message +=  8*" " + self.padding(i,length=max_len) +" : "+commands[i]+" \n"

        await ctx.send(message+"```")


    @commands.command()
    async def sounds(self,ctx):
        self.info.update()
        files = sorted(self.info.server_info["audio_files"])
        max_len = self.max_length(files)

        message = "```Sounds: \n"

        for i in files:
            message += 4*" "+ self.padding(i.split(".")[0],length=max_len)+"\n"

        await ctx.send(message+"```")

    @commands.Cog.listener()
    async def on_message(self,message):
        acceptable_formats = Sound.get_acceptable_audio_formats()
        request_channel = self.info.server_info["request_channel"]

        #so this function does not overide the other commands
        #await self.bot.process_commands(message)
        

        if str(message.author) == "Mood Bot#2255":
            return

        if "JOE" in message.content.upper():
            await message.channel.send("Joe Momma :sunglasses:")


        if str(message.channel.id) in request_channel:
            try:
                attachment = message.attachments[0]
            except:
                return

            file_name = attachment.filename
            url = attachment.url
            file_no_exstension = file_name[file_name.rfind("."):] 

            print(file_no_exstension)

            if not (file_no_exstension in acceptable_formats):
                await message.channel.send( "```You're Sending a Format That is Not Supported```")
            
            elif file_no_exstension in self.info.server_info["audio_files"]:
                await message.channel.send( "```A file with the same name has been sent```")
            
            else:
                r = requests.get(url,verify=False,stream=True)
                r.raw.decode_content = True

                with open(self.info.server_info["audio_dir"]+file_name, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)
                
                #sound = Sound.LocalSound(None,file_name,verify=False)
                #if sound.is_valid:
                await message.channel.send( "```Your Sound has Been Added Use $say "+file_name[:-4]+" to use it```")
                #else:
                #    await message.channel.send( "```There was a problem adding your sound```")
      
    @staticmethod
    def get_rss_xml(url):


        header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}    
        
        try:
            return requests.get(url,headers=header).text
        except:
            print("Failed to get : "+url)

    
