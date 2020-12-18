from ics import Calendar, Event
import time
import json
from pygrocy import Grocy
import CalendarHandler
from discord.ext import commands



class ServerInformation(commands.Cog):

    def __init__(self,server_info_path):
        self.server_info = None


        with open(server_info_path,'r') as f:
            self.server_info = json.load(f)

