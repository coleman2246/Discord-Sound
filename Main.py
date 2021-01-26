import discord
from discord.ext import commands
import Info
import SoundRequests
import GeneralUtils
import RandomFact

bot = commands.Bot(command_prefix='$')
bot.help_command = None


bot.add_cog(SoundRequests.SoundManagment(bot))
bot.get_cog("SoundManagment").check_queue.start()



bot.add_cog(GeneralUtils.Utils(bot))


bot.add_cog(RandomFact.Fact(bot))
bot.get_cog("Fact").send_image.start()



info = Info.ServerInformation("Data Files/server_info.json")
key = info.server_info["api_key"]




bot.run(key)
