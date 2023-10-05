import disnake
import os
import requests
import schedule
import asyncio
from disnake.ext import commands
import setup
from colorama import Fore, init
import time
import datetime
import aiohttp

start_time = time.time()

def time4logs():
    return f' {datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")}'

setup.main()
prefixes = 'd.', 'D.'

class Bot(commands.Bot):
    def __init__(self):
        intents = disnake.Intents.all()
        intents.typing = False
        intents.presences = False
        super().__init__(command_prefix=prefixes, intents=intents, shard_count=2)
    async def startup(self):
        await bot.wait_until_ready()
    async def setup_hook(self):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                try:
                    bot.load_extension(f"cogs.{filename[:-3]}")
                    print(f"[ Успешно ] Загружено: {filename}")
                except Exception as e:
                    print(f"[ Ошибка ] Не получилось загрузить: {filename}: ( {e} ) ")
        self.loop.create_task(self.startup())

bot = Bot()
bot.remove_command('help')

@bot.command(name='reload', hidden=True)
@commands.is_owner()
async def reload_cog(ctx, cog: str):
    try:
        bot.reload_extension(f'cogs.{cog}')
        embed = disnake.Embed(title="Успешно", description=f"<:badgedeveloper:1099308577048498316> Ког {cog} перезагружен.", color=disnake.Color.green())
        await ctx.send(embed=embed)
    except commands.ExtensionNotFound:
        embed = disnake.Embed(title="Ошибка", description=f"Ког {cog} не найден.", color=disnake.Color.red())
        await ctx.send(embed=embed)
    except Exception as e:
        print(e)

@bot.command(name='unload', hidden=True)
@commands.is_owner()
async def unload_cog(ctx, cog: str):
    try:
        bot.unload_extension(f'cogs.{cog}')
        embed = disnake.Embed(title="Успешно", description=f"<:badgedeveloper:1099308577048498316> Ког {cog} выгружен. ", color=disnake.Color.green())
        await ctx.send(embed=embed)
    except commands.ExtensionNotFound:
        embed = disnake.Embed(title="Ошибка", description=f"Ког {cog} не найден.", color=disnake.Color.red())
        await ctx.send(embed=embed)
    except commands.ExtensionNotLoaded:
        embed = disnake.Embed(title="Ошибка", description=f"Ког {cog} не был загружен.", color=disnake.Color.red())
        await ctx.send(embed=embed)
    except Exception as e:
        print(e)

@bot.command(name='load', hidden=True)
@commands.is_owner()
async def load_cog(ctx, cog: str):
    try:
        bot.load_extension(f'cogs.{cog}')
        embed = disnake.Embed(title="Успешно", description=f"<:badgedeveloper:1099308577048498316> Ког {cog} загружен.", color=disnake.Color.green())
        await ctx.send(embed=embed)
    except commands.ExtensionNotFound:
        embed = disnake.Embed(title="Ошибка", description=f"Ког {cog} не найден.", color=disnake.Color.red())
        await ctx.send(embed=embed)
    except commands.ExtensionAlreadyLoaded:
        embed = disnake.Embed(title="Ошибка", description=f"Ког {cog} уже загружен.", color=disnake.Color.red())
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f'Ошибка: {e}')



@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
         return
    elif isinstance(error, commands.MissingRequiredArgument):
        emb = disnake.Embed(title='Ошибка', description=f'Недостаточно аргументов для выполнения команды.', color=disnake.Color.red())
        await ctx.send(embed=emb)
    elif isinstance(error, commands.BadArgument):
        emb = disnake.Embed(title='Ошибка', description=f'Неверный аргумент.', color=disnake.Color.red())
        await ctx.send(embed=emb)
    elif isinstance(error, commands.CommandOnCooldown):
        emb = disnake.Embed(title='Ошибка', description=f'Пожалуйста, подождите `{error.retry_after:.2f}` секунд, прежде чем использовать эту команду снова.', color=disnake.Color.red())
        await ctx.send(embed=emb)
    elif isinstance(error, commands.MissingPermissions):
        emb = disnake.Embed(title='Ошибка', description=f'{ctx.message.author.mention}, У вас недостаточно прав для выполнения этой команды.', color=disnake.Color.red())
        await ctx.send(embed=emb)
    elif isinstance(error, commands.BotMissingPermissions):
        emb = disnake.Embed(title='Ошибка', description=f'У меня недостаточно прав для выполнения этой команды.', color=disnake.Color.red())
        await ctx.send(embed=emb)
    else:
        embed = disnake.Embed(title = 'Ошибка', description=f'Произошла ошибка при выполнении команды. Пожалуйста, попробуйте еще раз позже.', color=disnake.Color.red())
        raise error

@bot.event
async def on_ready():
    await bot.setup_hook()
    print(f'{Fore.GREEN}---------------------------------')
    print('Запущен бот: {0.user} ({0.user.id})'.format(bot))
    print('Префикс: {}'.format(bot.command_prefix))
    print('Пинг: {}ms'.format(round(bot.latency * 1000)))
    print('Количество серверов: {}'.format(len(bot.guilds)))
    print(f'Бот работает с: {time4logs()}')
    print(f'--------------------------------- {Fore.RESET}')
    activity = disnake.Game(name="d.help | Экономический бот.", type=3)
    await bot.change_presence(status=disnake.Status.idle, activity=activity)
    bot.loop.create_task(update_stats())

@bot.event
async def on_guild_remove(guild):
    dev_channel = bot.get_channel(1085213023590940672)
    avatar_url = guild.icon.url if guild.icon else None
    embed = disnake.Embed(
        title=f"Бот был удален с сервера {guild.name} ({guild.id})",
        color=disnake.Color.red())
    embed.add_field(name='Удалён в', value=f'<t:{start_time:.0f}:f>', inline=False)
    embed.add_field(name=f'Создатель сервера', value=f'{guild.owner}')
    if avatar_url:
        embed.set_thumbnail(url=avatar_url)
    await dev_channel.send(embed=embed)

@bot.event
async def on_guild_join(guild):
    dev_channel = bot.get_channel(1085213023590940672)
    avatar_url = guild.icon.url if guild.icon else None
    embed = disnake.Embed(
        title=f"Бот добавлен на сервер {guild.name} ({guild.id})",
        color=disnake.Color.green())
    if avatar_url:
        embed.set_thumbnail(url=avatar_url)
    await dev_channel.send(embed=embed)


bot.run("TOKEN")
