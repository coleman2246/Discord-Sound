import discord
from discord.ext import commands
import Info
import SoundRequests


bot = commands.Bot(command_prefix='$')



bot.add_cog(SoundRequests.SoundManagment(bot))
bot.get_cog("SoundManagment").check_queue.start()






info = Info.ServerInformation("Data Files/server_info.json")
key = info.server_info["api_key"]
bot.run(key)
