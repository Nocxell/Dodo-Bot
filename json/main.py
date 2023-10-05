import discord
import os
from discord.ext import commands
import pymongo
import setup
setup.main()

prefixes = 'd.', 'D.'

client = pymongo.MongoClient(os.environ['pymongo'])
db = client.user_messages
name = client["database"]
col = name["users"]
keys_collection = db["keys"]

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=prefixes, intents=discord.Intents.all(), shard_count=2)

    async def startup(self):
        await bot.wait_until_ready()
        await bot.tree.sync()

    async def setup_hook(self):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                try:
                    await bot.load_extension(f"cogs.{filename[:-3]}")
                    print(f"[ Успешно ] Загружено: {filename}")
                except Exception as e:
                    print(f"[ Ошибка ] Не получилось загрузить: {filename}: ( {e} ) ")
        self.loop.create_task(self.startup())


bot = Bot()
bot.remove_command('help')

# Команды для управления когами
@bot.command(name='reload', hidden=True)
async def reload_cog(ctx, cog: str):
    try:
        await bot.reload_extension(f'cogs.{cog}')
        embed = discord.Embed(title="Успешно", description=f"<:badgedeveloper:1099308577048498316> Ког {cog} перезагружен.", color=discord.Color.green())
        await ctx.send(embed = embed)
    except commands.ExtensionNotFound:
        embed = discord.Embed(title="Ошибка", description=f"Ког {cog} не найден.", color=discord.Color.red())
        await ctx.send(embed = embed)
    except Exception as e:
        print(e)

@bot.command(name='unload', hidden=True)
@commands.is_owner()
async def unload_cog(ctx, cog: str):
    try:
        await bot.unload_extension(f'cogs.{cog}')
        embed = discord.Embed(title="Успешно", description=f"<:badgedeveloper:1099308577048498316> Ког {cog} выгружен. ", color=discord.Color.green())
        await ctx.send(embed = embed)
    except commands.ExtensionNotFound:
        embed = discord.Embed(title="Ошибка", description=f"Ког {cog} не найден.", color=discord.Color.red())
        await ctx.send(embed = embed)
    except commands.ExtensionNotLoaded:
        embed = discord.Embed(title="Ошибка", description=f"Ког {cog} не был загружен.", color=discord.Color.red())
        await ctx.send(embed = embed)
    except Exception as e:
        print(e)
@bot.command(name='load', hidden=True)
@commands.is_owner()
async def load_cog(ctx, cog: str):
    try:
        await bot.load_extension(f'cogs.{cog}')
        embed = discord.Embed(title="Успешно", description=f"<:badgedeveloper:1099308577048498316> Ког {cog} загружен.", color=discord.Color.green())
        await ctx.send(embed = embed)
    except commands.ExtensionNotFound:
        embed = discord.Embed(title="Ошибка", description=f"Ког {cog} не найден.", color=discord.Color.red())
        await ctx.send(embed = embed)
    except commands.ExtensionAlreadyLoaded:
        embed = discord.Embed(title="Ошибка", description=f"Ког {cog} уже загружен.", color=discord.Color.red())
        await ctx.send(embed = embed)
    except Exception as e:
        await ctx.send(f'Ошибка: {e}')


bot.run(os.environ['to'])
