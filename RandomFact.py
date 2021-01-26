import re
import io

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
        
        self.rss_link = bot.get_cog("Utils").info["rss_link"]
        self.channel_num = int(bot.get_cog("Utils").info["fact channel"])
        
    # returns the url 
    def get_fact_image(self):
        xml = GeneralUtils.Utils.get_rss_xml(self.rss_link)

        soup = BeautifulSoup(xml,"xml")
        
        # finds first occurnce, should always be newest
        picture_urls = soup.find("item").find("description")
        url = re.findall('"([^"]*)"',str(picture_urls))[0]
       
        req = urllib.request.urlopen(url)
        arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        img = cv2.imdecode(arr, -1)[0:475, 0:-1]

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
