import disnake
from disnake.ext import commands
import io
import textwrap
import traceback
from contextlib import redirect_stdout
import random
import os
import psutil
import json
import asyncio
from asyncio import sleep
import aiohttp
import platform
import pymongo
import nacl
import psutil
import time
import os 
import asyncio
from disnake.ext.commands import Cog, Bot
from psutil import Process
from dateutil.relativedelta import relativedelta
from pkg_resources import get_distribution
from datetime import datetime

start_time = time.time()

class Developers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def clean_code(self, code):
        if code.startswith("```") and code.endswith("```"):
            return "\n".join(code.split("\n")[1:-1])
        return code.strip("` \n")

    def get_syntax_error(self, e):
        if e.text is None:
            return f"{e.__class__.__name__}: {e}"
        return f"{e.text}\n{'^':>{e.offset}}\n{e.__class__.__name__}: {e}"


    @commands.command()
    async def servers(self, ctx):
      allowed_ids = [978960003471929364, 1026185010149072997] 
      if ctx.author.id not in allowed_ids:
        return
      server_list = []
      for guild in self.bot.guilds:
          server_list.append(f"{guild.name} - {guild.member_count} members ({guild.id})")
      await ctx.send("\n".join(server_list))  

    @commands.command()
    async def servers2(self, ctx):
      allowed_ids = [978960003471929364, 1026185010149072997] 
      if ctx.author.id not in allowed_ids:
        return
        
      embed = disnake.Embed(title="Список серверов", color=0x7289da)
        
      large_servers = []
      medium_servers = []
        
      for guild in self.bot.guilds:
        member_count = guild.member_count
        shard_id = guild.shard_id
        server_info = f"{guild.name} - **``{member_count}``** участников (шард **``{shard_id}``**)"
        if member_count > 100:
            large_servers.append(server_info)
        elif member_count > 25:
            medium_servers.append(server_info)

      if large_servers:
        embed.add_field(name="Крупные сервера (100+):", value="\n".join(large_servers), inline=False)
      if medium_servers:
        # изменено условие проверки длины текста в поле value
        if len("\n".join(medium_servers)) <= 1024:
            embed.add_field(name="Средние сервера (25+):", value="\n".join(medium_servers), inline=False)
        else:
            medium_servers_chunks = [medium_servers[i:i+10] for i in range(0, len(medium_servers), 10)]
            for chunk in medium_servers_chunks:
                embed.add_field(name="Средние сервера (25+):", value="\n".join(chunk), inline=False)
        
      message = await ctx.send(embed=embed)

    # проверка, если сообщение слишком длинное, то разбиваем его на несколько сообщений
      if len(embed) > 6000:
        embed_list = list(embed._fields.values())
        for embed_part in embed_list:
            new_embed = disnake.Embed(title="Список серверов", color=0x7289da)
            new_embed.add_field(name=embed_part.name, value=embed_part.value)
            await ctx.send(embed=new_embed)
        await message.delete()
   

    @commands.command(name="eval", aliases=["exec", "e"])
    async def eval_command(self, ctx, *, code: str):
        # погоди ща лаги
        allowed_ids = [978960003471929364, 1026185010149072997, 1109107581584154664] 
        if ctx.author.id not in allowed_ids:
            return
        print(code)

        env = {
            "bot": self.bot,
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "_": None,
            "print": lambda *args, **kwargs: None,
            "disnake": disnake,
        }
        env.update(globals())

        code = self.clean_code(code)
        stdout = io.StringIO()

        try:
            exec(f"async def func():\n{textwrap.indent(code, '    ')}", env)
            func = env["func"]
        except Exception as e:
            return await ctx.send(f"```py\n{e.__class__.__name__}: {e}\n```")

        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(
                embed=disnake.Embed(
                    title="Eval",
                    description=f"```py\n{value}{traceback.format_exc()}\n```",
                    color=0xFF5733,
                )
            )
        else:
            value = stdout.getvalue()
            if ret is None:
                if value:
                    await ctx.send(
                        embed=disnake.Embed(
                            title="Eval",
                            description=f"```py\n{value}\n```",
                            color=0x2ECC71,
                        )
                    )
            else:
                env["_"] = ret
                await ctx.send(
                    embed=disnake.Embed(
                        title="Eval",
                        description=f"```py\n{value}{ret}\n```",
                        color=0x2ECC71,
                    )
                )


def setup(bot):
  bot.add_cog(Developers(bot))