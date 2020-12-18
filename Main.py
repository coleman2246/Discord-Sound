import discord
from discord.ext import commands
from Garbage import Garbage
from CalendarHandler import CalendarHandler
import Info
from Message import Message



bot = commands.Bot(command_prefix='!')

prefix = "Data Files"
info = Info.ServerInformation(prefix+"/server_info.json")


bot.add_cog(Message(bot,info.server_info['House']["server_id"]))
bot.add_cog(CalendarHandler(bot))

m = bot.get_cog("Message")





m.remind_garbage(750501948892905483,683864733535043624)




key = info["api_key"]
bot.run(key)
