import disnake
from disnake.ext import commands
import time
import datetime
import pyfiglet
from colorama import Fore, init
import platform
start_time = time.time()
def time4logs():
    return f' {datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")} '

class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.command_prefix = 'd.'

    @commands.Cog.listener()
    async def on_ready(self):
      print(f'{Fore.GREEN}---------------------------------') # что? 
      print('Запущен бот: {0.user} ({0.user.id})'.format(self.bot))
      print('Префикс: {}'.format(self.command_prefix))
      print('Пинг: {}ms'.format(round(self.bot.latency * 1000)))
      print('Количество серверов: {}'.format(len(self.bot.guilds)))
      print(f'Бот работает с: {time4logs()}')
      print(f'--------------------------------- {Fore.RESET}')
      activity = disnake.Game(name="d.help | Экономический бот.", type=3)
      await self.bot.change_presence(status=disnake.Status.idle, activity=activity)
      

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
      dev_channel = self.bot.get_channel(1085213023590940672)
      avatar_url = guild.icon.url if guild.icon else None
      embed = disnake.Embed(
        title=f"Бот был удален с сервера {guild.name} ({guild.id})",
        color=disnake.Color.red())
      embed.add_field(name='Удалён в', value=f'<t:{start_time:.0f}:f>', inline=False)
      embed.add_field(name=f'Создатель сервера', value=f'{guild.owner}')
      if avatar_url:
          embed.set_thumbnail(url=avatar_url)
      await dev_channel.send(embed=embed)

def setup(bot):
  bot.add_cog(Events(bot))