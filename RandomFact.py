import re
import io
from os import listdir
import random            
            


from discord.ext import commands, tasks
import discord.utils
import discord
import cv2
from bs4 import BeautifulSoup
import numpy as np
import urllib.request

import GeneralUtils
class Fact(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        
        self.images_files = listdir("Data Files/Random Facts")
        self.channel_num = int(bot.get_cog("Utils").info.server_info["fact channel"])
        
    def get_fact_image(self):
        path = ""
        while(path == ""):
            num = random.randint(0,len(self.images_files)-1)
            if self.images_files[num] != "keep":
                path = self.images_files[num]

        img = cv2.imread("Data Files/Random Facts/"+path)[0:475, 0:-1]

        return img

    @tasks.loop(seconds=(60*60*24),reconnect=True)
    async def send_image(self):
        await self.bot.wait_until_ready()
        img = self.get_fact_image()

        is_success, buffer = cv2.imencode(".jpg", img)
        io_buf = io.BytesIO(buffer)
        io_buf.name = "file.jpg"

        channel = self.bot.get_channel(id=self.channel_num)
        await channel.send(file = discord.File(io_buf))

