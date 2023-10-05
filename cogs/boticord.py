from disnake.ext import commands
from boticordpy import BoticordClient

class BoticordCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.boticord_client = BoticordClient("11ab3220-3ca5-4da2-83e2-b4662b3c1377", version=2)
        self.autopost = (
            self.boticord_client.autopost()
            .init_stats(self.get_stats)
            .on_success(self.on_success_posting)
            .start()
        )
    
    def get_stats(self):
        return {"servers": len(self.bot.guilds), "shards": 2, "users": len(self.bot.users)}
    
    def on_success_posting(self):
        print("Stats posted successfully")
        
    def cog_unload(self):
        self.autopost.stop()

def setup(bot):
    bot.add_cog(BoticordCog(bot))
