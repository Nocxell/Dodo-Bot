import disnake
from disnake.ext import commands
import json
import psutil
import os
import time

class Counter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = time.time()
        self.counts = {}
        try:
            with open("json/count.json", "r") as f:
                self.counts = json.load(f)
        except FileNotFoundError:
            pass

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        command_name = 'all'
        self.counts[command_name] = self.counts.get(command_name, 0) + 1
        with open("json/count.json", "w") as f:
            json.dump(self.counts, f)

    @commands.command(aliases=['information', 'i'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def info(self, ctx):
        memory = psutil.virtual_memory()
        free_memory = round(memory.available / 1024**2, 2)
        total_memory = round(memory.total / 1024**2, 2)
        memory_usage = round((total_memory - free_memory) / total_memory * 100, 2)
        cpu_usage = psutil.cpu_percent()
        total_members = sum(g.member_count for g in self.bot.guilds)
        process = psutil.Process(os.getpid())
        ping = round(self.bot.latency * 1000, 2)
        em = disnake.Embed(title='Информация о боте')
        counts = "\n".join(f"{count}" for command_name, count in self.counts.items())
        em.add_field(
        name="Cистема",
        value=f"<a:ram:1089566518112694362> Использовано ОЗУ: **{memory_usage}%** ({free_memory}/{total_memory} Мб)\n"
              f"<:ram:1085612713885053042>  Нагрузка на процессор: **{cpu_usage}%**\n"
              f"<:ping:1085610368337977374> Средняя задержка бота: **{ping} мс**\n"
              f"<:online:1085505876787466302> Аптайм бота: **<t:{self.start_time:.0f}:R>**\n"
              f"<:shard:1085612041009631384> Шардов: **{self.bot.shard_count}**\n"
              f"<:command_count:1101806798148743230> Команд выполнено: **{counts}**",
        inline=False)
        em.add_field(
        name="Серверы",
        value=f":globe_with_meridians: Количество: **{len(self.bot.guilds)}**\n"
        f":busts_in_silhouette: Пользователей: **{total_members}**\n\n",
        inline=False)
  
        em.add_field(
        name="Прочее",
        value=f"<:dodo:1085603981969068042> Префикс: **d.**\n"
        f"<:dodo:1085603981969068042> Дата создания: **<t:1656220980:D>**\n\n"
        f":man_technologist: Разработчики: **Dufl#3937, Nocxel#3221**\n",
        inline=False)
        em.add_field(
        name="Ccылки",
        value=
        f":pushpin:[Сервер поддержки](https://discord.gg/dodo-support)\n"
        f":pushpin:[Пригласить бота](https://discord.com/api/oauth2/authorize?client_id=1097452648627703828&permissions=8&scope=bot%20applications.commands)\n"
        f":pushpin:**[Powered by Deplos](https://deplos.com/)**\n"
        f":pushpin:[Bots server](https://bots.server-discord.com/1097452648627703828)\n"
        f":pushpin:[Boticord](https://boticord.top/bot/1097452648627703828)",
        inline=False)
        em.set_footer(
        text="© 2022, Dufl | Все права защищены ботом Dodo Bot",
        icon_url=
        "https://images-ext-2.discordapp.net/external/R4f7aQq6kbWbI0C3yTs3b4pjW773EtckyYTu1TrvcTc/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1097452648627703828/8209152252ebfdfd463a7e31d8a28fb4.png"
    )
        await ctx.send(embed=em)
    @commands.slash_command(name = 'about', description = 'Информация о боте')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def botinfo(self, ctx):
        memory = psutil.virtual_memory()
        free_memory = round(memory.available / 1024**2, 2)
        total_memory = round(memory.total / 1024**2, 2)
        memory_usage = round((total_memory - free_memory) / total_memory * 100, 2)
        cpu_usage = psutil.cpu_percent()
        total_members = sum(g.member_count for g in self.bot.guilds)
        process = psutil.Process(os.getpid())
        ping = round(self.bot.latency * 1000, 2)
        em = disnake.Embed(title='Информация о боте')
        counts = "\n".join(f"{count}" for command_name, count in self.counts.items())
        em.add_field(
        name="Cистема",
        value=f"<a:ram:1089566518112694362> Использовано ОЗУ: **{memory_usage}%** ({free_memory}/{total_memory} Мб)\n"
              f"<:ram:1085612713885053042>  Нагрузка на процессор: **{cpu_usage}%**\n"
              f"<:ping:1085610368337977374> Средняя задержка бота: **{ping} мс**\n"
              f"<:online:1085505876787466302> Аптайм бота: **<t:{self.start_time:.0f}:R>**\n"
              f"<:shard:1085612041009631384> Шардов: **{self.bot.shard_count}**\n"
              f"<:command_count:1101806798148743230> Команд выполнено: **{counts}**",
        inline=False)
        em.add_field(
        name="Серверы",
        value=f":globe_with_meridians: Количество: **{len(self.bot.guilds)}**\n"
        f":busts_in_silhouette: Пользователей: **{total_members}**\n\n",
        inline=False)
  
        em.add_field(
        name="Прочее",
        value=f"<:dodo:1085603981969068042> Префикс: **d.**\n"
        f"<:dodo:1085603981969068042> Дата создания: **<t:1656220980:D>**\n\n"
        f":man_technologist: Разработчики: **Dufl#3937, Nocxel#3221**\n",
        inline=False)
        em.add_field(
        name="Ccылки",
        value=
        f":pushpin:[Сервер поддержки](https://discord.gg/dodo-support)\n"
        f":pushpin:[Пригласить бота](https://discord.com/api/oauth2/authorize?client_id=1097452648627703828&permissions=8&scope=bot%20applications.commands)\n"
        f":pushpin:**[Powered by Deplos](https://deplos.com/)**\n"
        f":pushpin:[Bots server](https://bots.server-discord.com/1097452648627703828)\n"
        f":pushpin:[Boticord](https://boticord.top/bot/1097452648627703828)",
        inline=False)
        em.set_footer(
        text="© 2022, Dufl | Все права защищены ботом Dodo Bot",
        icon_url=
        "https://images-ext-2.discordapp.net/external/R4f7aQq6kbWbI0C3yTs3b4pjW773EtckyYTu1TrvcTc/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1097452648627703828/8209152252ebfdfd463a7e31d8a28fb4.png"
    )
        await ctx.send(embed=em)
def setup(bot):
    bot.add_cog(Counter(bot))