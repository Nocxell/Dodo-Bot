import disnake
from disnake.ext import commands
from asyncio import sleep
import random
import os
import datetime
import asyncio
import json
from datetime import timedelta, datetime

with open('json/warnings.json', 'r') as f:
    warnings = json.load(f)

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True, manage_webhooks=True, administrator=True)
    @commands.bot_has_permissions(manage_messages=True, administrator=True)
    async def say(self, ctx, *, text=None):
       if len(text) >= 1000:
         await ctx.reply(f'Вы не можете написать больше 1000 символов!')
         return
       if ctx.message.author.bot:
          return
       if text is None:
          em = disnake.Embed(title="Ошибка", description="Укажите текст сообщения", color=disnake.Color.red())
          await ctx.send(embed=em)
          return
       elif "@everyone" in text or "@here" in text:
           embed = disnake.Embed(title="Ошибка!", description="> Упоминание **everyone** или **here** в сообщении запрещено.", color=0xFF0000)
           await ctx.send(embed=embed)
       else:
           try:
              await ctx.message.delete()
              await ctx.send(text)
           except disnake.errors.HTTPException:
               embed = disnake.Embed(title="Ошибка!", description="Не удалось удалить сообщение. Убедитесь, что бот имеет права управления сообщениями.", color=0xFF0000)
               await ctx.send(embed=embed)
       

    @commands.command()
    @commands.has_permissions(manage_channels = True,administrator = True)
    @commands.bot_has_permissions(manage_channels = True, administrator = True)
    async def slowmode(self, ctx, seconds: int):
      if ctx.message.author.bot:
        return
      if ctx.author.guild_permissions.administrator:
        max_slowmode = 86400 
        if seconds > max_slowmode:
          await ctx.send(f"Максимальное значение для медленного режима - {max_slowmode // 3600} часов ({max_slowmode} секунд)")
          return
        await ctx.channel.edit(slowmode_delay=seconds)
        embed = disnake.Embed(title='Медленный режим', description=f'Медленный режим поставлен на {seconds} секунд', color=disnake.Color.blue())
        await ctx.send(embed=embed)


    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(ban_members=True, administrator=True)
    async def ban(self, ctx, member: disnake.Member = None, *, reason="Причина не указана"):
       if member.bot:
          em = disnake.Embed(title="Ошибка", description="Вы не можете забанить бота!", color=disnake.Color.red())
          await ctx.send(embed=em)
          return
       if not member:
           em = disnake.Embed(title="Ошибка", description="Пожалуйста, укажите участника для бана.", color=disnake.Color.red())
           await ctx.send(embed=em)
           return
    
       if member == ctx.author:
           await ctx.send(f'{ctx.author.mention}, ты не можешь себя же забанить!')
           return
    
       em = disnake.Embed(title="Бан")
       em.add_field(name=f"<:maleicon:1085511328644464670> Участник:", value=f"{member.mention}")
       em.add_field(name=f"<:Moderator:993095417027899442> Модератор:", value=f"{ctx.author.mention}")
       em.add_field(name=f"<:reason:1085612059200331887> Причина:", value=f"{reason}")
    
       try:
          await member.ban(reason=reason)
          await ctx.send(embed=em)
       except disnake.Forbidden:
           em = disnake.Embed(title="Ошибка", description="У меня нет прав на бан участника.", color=disnake.Color.red())
           await ctx.send(embed=em)
       except disnake.HTTPException:
           em = disnake.Embed(title="Ошибка", description="Не удалось забанить участника.", color=disnake.Color.red())
           await ctx.send(embed=em)

    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(kick_members=True, administrator=True)
    async def kick(self, ctx, member: disnake.Member = None, *, reason="Причина не указана"):
       if member is None:
          em = disnake.Embed(title="Ошибка", description=" Укажите участника, которого необходимо кикнуть.", color=disnake.Color.red())
          await ctx.send(embed=em)
          return
       if member == ctx.author:
          em = disnake.Embed(title="Ошибка", description="Вы не можете кикнуть самого себя!", color=disnake.Color.red())
          await ctx.send(embed=em)
          return
       if member.bot:
          em = disnake.Embed(title="Ошибка", description="Вы не можете кикнуть бота!", color=disnake.Color.red())
          await ctx.send(embed=em)
          return
       em = disnake.Embed(title="Кик")
       em.add_field(name="<:maleicon:1085511328644464670> Участник:", value=member.mention, inline=False)
       em.add_field(name="<:Moderator:993095417027899442> Модератор:", value=ctx.author.mention, inline=False)
       em.add_field(name="<:reason:1085612059200331887> Причина:", value=reason, inline=False)
       try:
          await member.kick(reason=reason)
          await ctx.send(embed=em)
       except disnake.Forbidden:
           em = disnake.Embed(title="Ошибка", description="У меня нет прав на кик участника.", color=disnake.Color.red())
           await ctx.send(embed=em)
       except disnake.HTTPException:
           em = disnake.Embed(title="Ошибка", description="Не удалось кикнуть участника.", color=disnake.Color.red())
           await ctx.send(embed=em)

    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(ban_members=True, administrator=True)
    async def unban(self, ctx, member_id: int, *, reason="Причина не указана"):
      if ctx.message.author.bot:
        await ctx.send(f'{ctx.author.mention}, вы не можете разбанить бота!')
        return
    
      try:
        member = await self.bot.fetch_user(member_id)
        await ctx.guild.unban(member, reason=reason)
        em = disnake.Embed(title="Разбан", description=f"{member.mention} был успешно разбанен!", color=disnake.Color.green())
        em.add_field(name=f"<:Moderator:993095417027899442> Модератор:", value=f"{ctx.author.mention}")
        em.add_field(name=f"<:reason:1085612059200331887> Причина:", value=f"{reason}")
        await ctx.send(embed=em)
      except disnake.Forbidden:
        em = disnake.Embed(title="Ошибка", description="У меня нет прав на разбан участника.", color=disnake.Color.red())
        await ctx.send(embed=em)
      except disnake.NotFound:
        em = disnake.Embed(title="Ошибка", description="Указанный участник не был найден.", color=disnake.Color.red())
        await ctx.send(embed=em)
      except disnake.HTTPException:
        em = disnake.Embed(title="Ошибка", description="Не удалось разбанить участника.", color=disnake.Color.red())
        await ctx.send(embed=em)

    @commands.command()
    @commands.has_permissions(administrator=True, kick_members = True, ban_members = True)
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def warn(self, ctx, user: disnake.Member, *, reason='Модератор не указал причину.'):
      if user.bot:
        embed = disnake.Embed(title = f'Ошибка', description='Вы не можете предупредить бота!', color = disnake.Color.red())
        await ctx.send(embed = embed)
        return
      if user == ctx.author:
        embed = disnake.Embed(title = f'Ошибка', description='Вы не можете себя же предупредить!', color = disnake.Color.red())
        await ctx.send(embed = embed)
        return
      if str(ctx.guild.id) not in warnings:
        warnings[str(ctx.guild.id)] = {}
      if str(user.id) not in warnings[str(ctx.guild.id)]:
        warnings[str(ctx.guild.id)][str(user.id)] = 0

      warnings[str(ctx.guild.id)][str(user.id)] += 1
      with open('json/warnings.json', 'w') as f:
          json.dump(warnings, f)
      embed = disnake.Embed(description=f'Успешно! Пользователь {user.mention} получил предупреждение. Теперь у него `{warnings[str(ctx.guild.id)][str(user.id)]}` предупреждений.', color = disnake.Color.green(), timestamp = ctx.message.created_at)
      await ctx.send(embed = embed)

    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.has_permissions(administrator=True, kick_members = True, ban_members = True)
    async def unwarn(self, ctx, user: disnake.Member):
      if user.bot:
        embed = disnake.Embed(title = f'Ошибка', description='Вы не можете предупредить бота!', color = disnake.Color.red(), timestamp = ctx.message.created_at)
        await ctx.send(embed = embed)
        return
      if str(ctx.guild.id) in warnings and str(user.id) in warnings[str(ctx.guild.id)] and warnings[str(ctx.guild.id)][str(user.id)] > 0:
          warnings[str(ctx.guild.id)][str(user.id)] -= 1
          with open('json/warnings.json', 'w') as f:
            json.dump(warnings, f)
          embed = disnake.Embed(title = '', description=f':white_check_mark: {user.name} было снято 1 предупреждение. Теперь у него `{warnings[str(ctx.guild.id)][str(user.id)]}` предупреждений.', timestamp = ctx.message.created_at, color = disnake.Color.green())
          await ctx.send(embed = embed)
      else:
          embed = disnake.Embed(title = 'Ошибка', description=f'{user.name} не имеет предупреждений.', timestamp = ctx.message.created_at, color = disnake.Color.red())
          await ctx.send(embed = embed)

    @commands.command()
    @commands.cooldown(1, 25, commands.BucketType.user)
    @commands.has_permissions(administrator=True, kick_members = True, ban_members = True)
    async def warns(self, ctx, user: disnake.Member = None):
      if user is None:
        user = ctx.author

      if str(ctx.guild.id) in warnings and str(user.id) in warnings[str(ctx.guild.id)]:
          num_warnings = warnings[str(ctx.guild.id)][str(user.id)]
          embed = disnake.Embed(title = '', description=f'{user.name} имеет {num_warnings} предупреждений.', timestamp = ctx.message.created_at)
          await ctx.send(embed = embed)
      else:
          embed = disnake.Embed(title = 'Ошибка', description=f'{user.name} не имеет предупреждений.', timestamp = ctx.message.created_at, color = discord.Color.red())
          await ctx.send(embed = embed)


def setup(bot):
    bot.add_cog(Moderation(bot))