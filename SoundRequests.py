from discord.ext import commands, tasks


class SoundRequests(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.queue = []

    @bot.command()
    async def play(ctx,url):
        self.queue.append(url)
        msg = 
        
        await ctx.send(msg)



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
       

