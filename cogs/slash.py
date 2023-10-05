import disnake
from disnake import Embed, Member
from disnake.ext import commands
import os
import pymongo
import random
import psutil
import json
import time
import aiohttp
import sqlite3
import asyncio
from asyncio import sleep

class Dropdown(disnake.ui.Select):
    def __init__(self):
        options = [
            disnake.SelectOption(label='Экономика', emoji='🏛️'),
            disnake.SelectOption(label='Модерация', emoji='🛡'),
            disnake.SelectOption(label='Настройки', emoji='⚙'),
            disnake.SelectOption(label='Развлечения', emoji='😁'),
            disnake.SelectOption(label='Утилиты', emoji='✨'),
            disnake.SelectOption(label='Другое', emoji='👾'),
        ]
        super().__init__(placeholder='Выберите категорию',
                         min_values=1,
                         max_values=1,
                         options=options)

    async def callback(self, interaction: disnake.Interaction):
        if self.values[0] == 'Экономика':
            embed = disnake.Embed(
                title="Команды экономики",
                description=
                f'``[обязательный аргумент] <необязательный аргумент>`` \n**Не используйте скобочки при указании аргументов**',
                color=disnake.Colour.green())
            embed.set_thumbnail(
                url=
                'https://cdn.discordapp.com/avatars/1097452648627703828/8209152252ebfdfd463a7e31d8a28fb4.png?size=1024'
            )
            embed.add_field(name=f'/top',
                            value=f'Показать топ по балансу на сервере',
                            inline=False)
            embed.add_field(name=f'/reset_economy',
                            value=f'Удалить экономику на сервере',
                            inline=False)
            embed.add_field(name=f'/balance',
                            value=f'Показать баланс',
                            inline=False)
            embed.add_field(name=f'/casino ``[ставка]``',
                            value=f'Поиграть в казино',
                            inline=False)
            embed.add_field(name=f'/work', 
                            value=f'Поработать', 
                            inline=False)
            embed.add_field(name=f'/transfer ``[пользователь]`` ``[cумма]``',
                            value=f'Перевод денег пользователю',
                            inline=False)
            embed.add_field(name=f'/rob ``[пользователь]``',
                            value=f'Ограбить пользователя',
                            inline=False)
            embed.add_field(name=f'/crime',
                            value=f'Попытать удачу',
                            inline=False)
            embed.set_footer(
                text="© 2022, Dufl | Все права защищены ботом Dodo Bot",
                icon_url=
                "https://cdn.discordapp.com/avatars/1097452648627703828/8209152252ebfdfd463a7e31d8a28fb4.png?size=1024"
            )
            await interaction.response.send_message(embed=embed,
                                                    ephemeral=True)
        elif self.values[0] == 'Настройки':
            embed = disnake.Embed(
                title="Команды настройки",
                description=
                f'``[обязательный аргумент] <необязательный аргумент>`` \n**Не используйте скобочки при указании аргументов**'
            )
            embed.set_thumbnail(
                url=
                'https://cdn.discordapp.com/avatars/1097452648627703828/8209152252ebfdfd463a7e31d8a28fb4.png?size=1024'
            )
            embed.add_field(name=f'/logs_setup ``[канал]``',
                            value=f'Включить логи на сервере',
                            inline=False)
            embed.add_field(name=f'/logs_disable', value=f'Выключить логи на сервере')
            embed.set_footer(
                text="© 2022, Dufl | Все права защищены ботом Dodo Bot",
                icon_url=
                "https://cdn.discordapp.com/avatars/1097452648627703828/8209152252ebfdfd463a7e31d8a28fb4.png?size=1024"
            )
            await interaction.response.send_message(embed=embed,
                                                    ephemeral=True)
        elif self.values[0] == 'Развлечения':
            embed = disnake.Embed(
                title="Команды развлечения",
                description=
                f'``[обязательный аргумент] <необязательный аргумент>`` \n**Не используйте скобочки при указании аргументов**'
            )
            embed.set_thumbnail(
                url=
                'https://cdn.discordapp.com/avatars/1097452648627703828/8209152252ebfdfd463a7e31d8a28fb4.png?size=1024'
            )
            embed.add_field(name=f'/ben ``[вопрос]``',
                            value=f'Задать вопрос бену',
                            inline=False)
            embed.add_field(name=f'/meme', value=f'Отправить рандомный мем')
            embed.add_field(name=f'/question ``[вопрос]``',
                            value=f'Задать вопрос шару')
            embed.set_footer(
                text="© 2022, Dufl | Все права защищены ботом Dodo Bot",
                icon_url=
                "https://cdn.discordapp.com/avatars/1097452648627703828/8209152252ebfdfd463a7e31d8a28fb4.png?size=1024"
            )
            await interaction.response.send_message(embed=embed,
                                                    ephemeral=True)
        elif self.values[0] == 'Модерация':
            embed = disnake.Embed(
                title="Команды модерации",
                description=
                f'``[обязательный аргумент] <необязательный аргумент>`` \n**Не используйте скобочки при указании аргументов**',
                color=disnake.Colour.red())
            embed.set_thumbnail(
                url=
                'https://cdn.discordapp.com/avatars/1097452648627703828/8209152252ebfdfd463a7e31d8a28fb4.png?size=1024'
            )
            embed.add_field(name=f'/ban ``[пользователь]`` ``<причина>`` ',
                            value=f'Забанить кого-то',
                            inline=False)
            embed.add_field(name=f'/kick ``[пользователь]`` ``<причина>`` ',
                            value=f'Кикнуть кого-то',
                            inline=False)
            embed.add_field(name=f'/say ``[сообщение]``',
                            value=f'Написать через бота',
                            inline=False)
            embed.add_field(name=f'/unban ``[пользователь]``',
                            value='Разбанить пользователя',
                            inline=False)
            embed.add_field(name=f'/warn ``[пользователь]`` ``<причина>``',
                            value='Выдать варн пользователю',
                            inline=False)
            embed.add_field(name=f'/unwarn ``[пользователь]``',
                            value='Снять варн пользователю',
                            inline=False)
            embed.add_field(name=f'/warns ``[пользователь]``',
                            value='Посмотреть варны пользователя',
                            inline=False)
            embed.add_field(name = '/slowmode ``[секунды]``', 
                            value = 'Поставить медленный режим',
                            inline=False)

            embed.set_footer(
                text="© 2022, Dufl | Все права защищены ботом Dodo Bot",
                icon_url=
                "https://cdn.discordapp.com/avatars/1097452648627703828/8209152252ebfdfd463a7e31d8a28fb4.png?size=1024"
            )
            await interaction.response.send_message(embed=embed,
                                                    ephemeral=True)
        elif self.values[0] == 'Утилиты':
            embed = disnake.Embed(
                title="Команды утилиты",
                description=
                f'``[обязательный аргумент] <необязательный аргумент>``\n**Не используйте скобочки при указании аргументов**',
                color=disnake.Colour.blue())
            embed.set_thumbnail(
                url=
                'https://cdn.discordapp.com/avatars/1097452648627703828/8209152252ebfdfd463a7e31d8a28fb4.png?size=1024'
            )
            embed.add_field(name=f'/info',
                            value=f'Информация о боте',
                            inline=False)
            embed.add_field(name=f'/avatar ``[пользователь]``',
                            value=f'Узнать аватар пользователя',
                            inline=False)
            embed.add_field(name=f'/userinfo',
                            value=f'Информация о пользователе',
                            inline=False)
            embed.add_field(name=f'/serverinfo',
                            value=f'Информация о сервере',
                            inline=False)
            embed.set_footer(
                text="© 2022, Dufl | Все права защищены ботом Dodo Bot",
                icon_url=
                "https://cdn.discordapp.com/avatars/1097452648627703828/8209152252ebfdfd463a7e31d8a28fb4.png?size=1024"
            )
            await interaction.response.send_message(embed=embed,
                                                    ephemeral=True)
        elif self.values[0] == 'Другое':
            embed = disnake.Embed(
                title="Другие команды",
                description=
                f'``[обязательный аргумент] <необязательный аргумент>``\n**Не используйте скобочки при указании аргументов**',
                color=disnake.Colour.blue())
            embed.set_thumbnail(
                url=
                'https://cdn.discordapp.com/avatars/1097452648627703828/8209152252ebfdfd463a7e31d8a28fb4.png?size=1024'
            )
            embed.add_field(name=f'/bug ``[баг]``',
                            value=f'Сообщить о баге',
                            inline=False)
            embed.add_field(name=f'/idea ``[идея]``',
                            value=f'Сообщить о идеи',
                            inline=False)
            embed.set_footer(
                text="© 2022, Dufl | Все права защищены ботом Dodo Bot",
                icon_url=
                "https://cdn.discordapp.com/avatars/1097452648627703828/8209152252ebfdfd463a7e31d8a28fb4.png?size=1024"
            )
            await interaction.response.send_message(embed=embed,
                                                    ephemeral=True)


class DropdownView(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Dropdown())

with open('json/warnings.json', 'r') as f:
    warnings = json.load(f)

tt = ['Да', 'Хохохо', 'Нет']
chair = ['Это точно 👌', 'Очень даже вряд-ли 🤨', 'Нет ❌', 'Да, безусловно ✔', 'Вы можете рассчитывать на это 👌', 'Вероятно 🤨', 'Перспектива хорошая 🤔', 'Да ✔', 'Знаки указывают да 👍', 'Ответ туманный, попробуйте еще раз 👀', 'Спроси позже 👀', 'Лучше не говорить тебе сейчас 🥵', 'Не могу предсказать сейчас 👾', 'Сконцентрируйтесь и спросите снова 🤨', 'Не рассчитывай на это 🙉', 'Мой ответ - Нет 😕','Мои источники говорят нет 🤨', 'Перспективы не очень 🕵️‍♂️', 'Очень сомнительно 🤔']


class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.connection = sqlite3.connect('economy.db')
        self.cursor = self.connection.cursor()
        self.cache = {}
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                guild_id INTEGER,
                balance INTEGER DEFAULT 0
            )
        """)
        self.connection.commit()
    @commands.slash_command(description='Показать помощь по командам')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def help(self, ctx):
        view = DropdownView()
        embed = disnake.Embed(
            title=f'Команды бота',
            description=
            f'``[обязательный аргумент] <необязательный аргумент>``\n**Не используйте скобочки при указании аргументов**',
            color=0xa84300)
        embed.set_thumbnail(
            url=
            'https://cdn.discordapp.com/avatars/1097452648627703828/8209152252ebfdfd463a7e31d8a28fb4.png?size=1024'
        )
        embed.add_field(name=f'🏛️ Экономика',
                        value=f'`/top` '
                        '`/balance` '
                        '`/casino` '
                        '`/work` '
                        '`/transfer` '
                        '`/rob` '
                        '`/crime` '
                        '`/reset_economy` ')
        embed.add_field(name=f':shield: Модерация',
                        value='`/ban` '
                        '`/kick` '
                        '`/say` '
                        '`/unban` '
                        '`/warn` '
                        '`/unwarn` '
                        '`/warns` '
                        '`/slowmode`',
                        inline=False)
       	embed.add_field(name=f':gear: Настройки', value=f'`/logs_setup` '
						f'`/logs_disable`', inline=False)
        embed.add_field(name=f':grin: Развлечения',
                        value='`/ben` '
                        '`/question` '
                        '`/meme` ',
                        inline=False)
        embed.add_field(name=f':sparkles: Утилиты',
                        value='`/info` '
                        '`/avatar` '
                        '`/userinfo` '
                        '`/serverinfo` ',
                        inline=False)
        embed.add_field(name=f':space_invader: Другое',
                        value='`/idea` '
                        '`/bug` ',
                        inline=False)
        embed.set_footer(
            text="© 2022, Dufl | Все права защищены ботом Dodo Bot",
            icon_url=
            "https://cdn.discordapp.com/avatars/1097452648627703828/8209152252ebfdfd463a7e31d8a28fb4.png?size=1024"
        )
        await ctx.send(embed=embed, view=view)

    @commands.slash_command(description="Узнать аватар пользователя")
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def avatar(self, ctx, *, member: disnake.Member = None):
      if member is None:
        member = ctx.author
        embed = disnake.Embed(title=f"{member.name} аватар",
                              color=disnake.Color.green())
        embed.set_image(url='{}'.format(member.display_avatar))
        embed.set_footer(
            text="© 2022, Dufl | Все права защищены ботом Dodo Bot",
            icon_url=
            "https://cdn.discordapp.com/avatars/1097452648627703828/8209152252ebfdfd463a7e31d8a28fb4.png?size=1024"
        )
        await ctx.send(embed=embed)
      else:
        embed = disnake.Embed(title=f"{member.name} аватар",
                              color=disnake.Color.green())
        embed.set_image(url='{}'.format(member.display_avatar))
        embed.set_footer(
            text="© 2022, Dufl | Все права защищены ботом Dodo Bot",
            icon_url=
            "https://cdn.discordapp.com/avatars/1097452648627703828/8209152252ebfdfd463a7e31d8a28fb4.png?size=1024"
        )
        await ctx.send(embed=embed)
    @commands.slash_command(description = 'Сообщить о баге')
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def bug(self, ctx, *, bug):
    #  invite = await ctx.channel.create_invite(max_uses=60, unique=True)
      channel = self.bot.get_channel(1084823051813802014)
      await channel.send(
        f"**Баг!** <@&990626380997853204> \n**Баг от {ctx.author}#{ctx.author.discriminator} | {ctx.author.id}.** \n**Сервер:** {ctx.guild.name} | {ctx.guild.id}. \n**Баг:** {bug}"
    )
      await ctx.send("**Ваш баг успешно отправлен!**")

    @commands.slash_command(description = 'Сообщить об идеи')
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def idea(self, ctx, *, idea):
      #invite = await ctx.channel.create_invite(max_uses=60, unique=True)
      channel = self.bot.get_channel(1084821796676718592)
      await channel.send(
        f"**Идея!** <@&990626380997853204> \n**Идея от {ctx.author}#{ctx.author.discriminator} | {ctx.author.id}.** \n**Сервер:** {ctx.guild.name} | {ctx.guild.id}. \n**Идея:** {idea}"
    )
      await ctx.send("**Ваша идея успешно отправлена!**")

    @commands.slash_command(description = 'Спросить шар')
    async def question(self, ctx, *, question:str):
        if question != None:
          	emb = disnake.Embed(title = f'{question}', description=f"{random.choice(chair)}")
          	emb.set_image(url='https://sun9-15.userapi.com/impg/P2ZAiM3V4XyF-evI1sMWvnm1slzHVoXsoQNtjg/eGZsFoXfDFE.jpg?size=604x604&quality=96&sign=8055a0af19a00238cfed5e6c6d77c30c&type=album')
        await ctx.response.send_message(embed=emb)


    @commands.slash_command(description = 'Сказать от имени бота')
    @commands.default_member_permissions(ban_members=True, administrator=True)
    @commands.bot_has_permissions(manage_messages=True, administrator=True)
    async def say(self, ctx, *, text):
       if len(text) >= 1000:
         await ctx.reply(f'Вы не можете написать больше 1000 символов!')
         return
       if ctx.author.bot:
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
              await ctx.send('Успешно', ephemeral=True)
              await ctx.send(text)
           except disnake.errors.HTTPException:
               embed = disnake.Embed(title="Ошибка!", description="Не удалось удалить сообщение. Убедитесь, что бот имеет права управления сообщениями.", color=0xFF0000)
               await ctx.send(embed=embed)
       

    @commands.slash_command(description = 'Установить медленый режим в канале')
    @commands.default_member_permissions(manage_guild=True, ban_members=True, administrator=True)
    async def slowmode(self, ctx, seconds: int):
      if ctx.author.bot:
        return
      if ctx.author.guild_permissions.administrator:
        max_slowmode = 86400 
        if seconds > max_slowmode:
          await ctx.send(f"Максимальное значение для медленного режима - {max_slowmode // 3600} часов ({max_slowmode} секунд)")
          return
        await ctx.channel.edit(slowmode_delay=seconds)
        embed = disnake.Embed(title='Медленный режим', description=f'Медленный режим поставлен на {seconds} секунд', color=disnake.Color.blue())
        await ctx.send(embed=embed)


    @commands.slash_command(description = 'Забанить пользователя')
    @commands.default_member_permissions(ban_members=True, administrator=True)
    @commands.bot_has_permissions(ban_members=True, administrator=True)
    async def ban(self, ctx, member: disnake.Member, *, reason="Причина не указана"):
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

    @commands.slash_command(description = 'Кикнуть пользователя')
    @commands.default_member_permissions(kick_members=True, administrator=True)
    @commands.bot_has_permissions(kick_members=True, administrator=True)
    async def kick(self, ctx, member: disnake.Member, *, reason="Причина не указана"):
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

    @commands.slash_command(description = 'Разбанить пользователя')
    @commands.default_member_permissions(ban_members=True, administrator=True)
    async def unban(self, ctx, member_id: int, *, reason="Причина не указана"):
      if ctx.author.bot:
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

    @commands.slash_command(description = 'Выдать варн пользователю')
    @commands.default_member_permissions(moderate_members=True, ban_members=True, administrator=True)
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
      embed = disnake.Embed(description=f'Успешно! Пользователь {user.mention} получил предупреждение. Теперь у него `{warnings[str(ctx.guild.id)][str(user.id)]}` предупреждений.', color = disnake.Color.green())
      await ctx.send(embed = embed)

    @commands.slash_command(description = 'Снять варн с пользователя')
    @commands.default_member_permissions(moderate_members=True, ban_members=True, administrator=True)
    async def unwarn(self, ctx, user: disnake.Member):
      if user.bot:
        embed = disnake.Embed(title = f'Ошибка', description='Вы не можете предупредить бота!', color = disnake.Color.red())
        await ctx.send(embed = embed)
        return
      if str(ctx.guild.id) in warnings and str(user.id) in warnings[str(ctx.guild.id)] and warnings[str(ctx.guild.id)][str(user.id)] > 0:
          warnings[str(ctx.guild.id)][str(user.id)] -= 1
          with open('json/warnings.json', 'w') as f:
            json.dump(warnings, f)
          embed = disnake.Embed(title = '', description=f':white_check_mark: {user.name} было снято 1 предупреждение. Теперь у него `{warnings[str(ctx.guild.id)][str(user.id)]}` предупреждений.', color = disnake.Color.green())
          await ctx.send(embed = embed)
      else:
          embed = disnake.Embed(title = 'Ошибка', description=f'{user.name} не имеет предупреждений.', color = disnake.Color.red())
          await ctx.send(embed = embed)

    @commands.slash_command(description = 'Посмотреть список варнов')
    @commands.default_member_permissions(manage_guild=True, moderate_members=True, ban_members=True, administrator=True)
    async def warns(self, ctx, user: disnake.Member = None):
      if user is None:
        user = ctx.author

      if str(ctx.guild.id) in warnings and str(user.id) in warnings[str(ctx.guild.id)]:
          num_warnings = warnings[str(ctx.guild.id)][str(user.id)]
          embed = disnake.Embed(title = '', description=f'{user.name} имеет {num_warnings} предупреждений.')
          await ctx.send(embed = embed)
      else:
          embed = disnake.Embed(title = 'Ошибка', description=f'{user.name} не имеет предупреждений.', color = disnake.Color.red())
          await ctx.send(embed = embed)
    @commands.slash_command(description = 'Обнулить экономику')
    @commands.default_member_permissions(manage_guild=True, administrator=True)
    async def reset_economy(self, ctx):
      def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

      embed = disnake.Embed(title="Сброс экономики", description="Вы уверены, что хотите сбросить экономику для данного сервера? Это действие нельзя отменить.", color=0xff0000)
      embed.add_field(name="Подтвердите действие", value="Напишите `да`, чтобы подтвердить, или `нет`, чтобы отменить.")
      prompt = await ctx.send(embed=embed)

      try:
        msg = await self.bot.wait_for('message', timeout=15.0, check=check)
      except asyncio.TimeoutError:
        await prompt.edit(embed=disnake.Embed(description="Вы не успели ответить. Экономика не будет сброшена.", color=0xff0000))
        return

      if msg.content.lower() == 'да':
        guild_id = ctx.guild.id
        self.cursor.execute("SELECT * FROM users WHERE guild_id = ?", (guild_id,))
        rows = self.cursor.fetchall()
        if len(rows) > 0:
            self.cursor.execute("DELETE FROM users WHERE guild_id = ?", (guild_id,))
            self.connection.commit()
            await prompt.edit(embed=disnake.Embed(description=f"Экономика была сброшена для сервера `{ctx.guild.name}`!", color=0x00ff00))
        else:
            await prompt.edit(embed=disnake.Embed(description=f"На сервере `{ctx.guild.name}` нет записей в экономике.", color=0xff0000))
      else:
        await prompt.edit(embed=disnake.Embed(description="Экономика не будет сброшена.", color=0xff0000))

     
    @commands.slash_command(description = 'Посмотреть свой баланс')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def balance(self, ctx):
        user_id = ctx.author.id
        guild_id = ctx.guild.id
        self.cursor.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
        result = self.cursor.fetchone()
        if result is None:
            self.cursor.execute("INSERT INTO users(user_id, guild_id) VALUES(?, ?)", (user_id, ctx.guild.id))
            self.connection.commit()
            embed = disnake.Embed(title=f'Баланс {ctx.author}')
            embed.add_field(name=f'Ваш баланс:', value='0')
            await ctx.send(embed=embed)
        else:
            balance = result[0]
            embed = disnake.Embed(title=f'Баланс {ctx.author}')
            embed.add_field(name=f'Ваш баланс:', value=balance)
            await ctx.send(embed=embed)
    @commands.slash_command(description = 'Ограбить пользователя')
    async def rob(self, ctx, member: disnake.Member):
      if member is None:
        await ctx.send(f"{ctx.author.mention}, Укажите пользователя, которого вы хотите ограбить.")
        return
      if member == ctx.author:
        await ctx.send(f"{ctx.author.mention}, Вы не можете ограбить самого себя.")
        return
      if member.bot:
        await ctx.send(f"{ctx.author.mention}, Вы не можете ограбить бота!")
        return
      user = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (ctx.author.id,)).fetchone()
      target = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (member.id,)).fetchone()
      if user is None:
        self.cursor.execute("INSERT INTO users (user_id, guild_id, balance) VALUES (?, ?, ?)", (ctx.author.id, ctx.guild.id, 0))
        self.connection.commit()
        return
      if target is None:
        await ctx.send(f"Человек не найден.")
        return
      if user[2] < 50:
        await ctx.send(f"{ctx.author.mention}, У вас недостаточно средств на счету для ограбления.")
        return
      target_balance = target[2]
      success_rate = min(target_balance / 1000, 0.9)
      if random.random() < success_rate:
        amount = min(target_balance, 800)
        self.cursor.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (amount, ctx.author.id))
        self.cursor.execute("UPDATE users SET balance = balance - ? WHERE user_id = ?", (amount, member.id))
        self.connection.commit()
        await ctx.send(f"Вы успешно ограбили {member.mention} и получили {amount} денег!")
      else:
        amount = random.randint(50, 199)
        self.cursor.execute("UPDATE users SET balance = balance - ? WHERE user_id = ?", (amount, ctx.author.id))
        self.connection.commit()
        await ctx.send(f"Вы неудачно попытались ограбить {member.mention} и потеряли {amount} денег.")
    @commands.slash_command(description = 'Поиграть в казино')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def casino(self, ctx, bet: int):
        if bet is None:
            embed = disnake.Embed(title="Ошибка", description=f"{ctx.author.mention}, Вы не указали ставку.", color=disnake.Color.red())
            await ctx.send(embed=embed)
            return
      
        user = self.cursor.execute("SELECT * FROM users WHERE user_id=?", (ctx.author.id,)).fetchone()
        if user is None:
            self.cursor.execute("INSERT INTO users (user_id, guild_id, balance) VALUES (?, ?, ?)", (ctx.author.id, ctx.guild.id, 0))
            self.connection.commit()
            user = self.cursor.execute("SELECT * FROM users WHERE user_id=?", (ctx.author.id,)).fetchone()
        if bet <= 0:
            embed = disnake.Embed(title="Ошибка", description=f"{ctx.author.mention}, Ставка должна быть больше нуля.", color=disnake.Color.red())
            await ctx.send(embed=embed)
            return
        if user[2] < bet:
            embed = disnake.Embed(title="Ошибка", description=f"{ctx.author.mention}, У вас недостаточно денег на балансе.", color=disnake.Color.red())
            await ctx.send(embed=embed)
            return
        result = random.choices(["win", "lose"], weights=[1.8, 1], k=1)[0]
        if result == "win":
            win_amount = bet * 2
            self.cursor.execute("UPDATE users SET balance = balance + ? WHERE user_id=?", (win_amount, ctx.author.id))
            self.connection.commit()
            user = self.cursor.execute("SELECT * FROM users WHERE user_id=?", (ctx.author.id,)).fetchone()
            embed = disnake.Embed(description=f"{ctx.author.mention}, Вы выиграли {win_amount} денег. Ваш баланс: {user[2]}", color = disnake.Color.green())
            await ctx.send(embed=embed)
        else:
            loss_amount = bet
            self.cursor.execute("UPDATE users SET balance = balance - ? WHERE user_id=?", (loss_amount, ctx.author.id))
            self.connection.commit()
            user = self.cursor.execute("SELECT * FROM users WHERE user_id=?", (ctx.author.id,)).fetchone()
            embed = disnake.Embed(description=f"{ctx.author.mention}, Вы проиграли {loss_amount} денег. Ваш баланс: {user[2]}", color = disnake.Color.red())
            await ctx.send(embed=embed)
    @commands.slash_command(description = 'Поработать')
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def work(self, ctx):
        user = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (ctx.author.id,)).fetchone()
        if user is None:
            self.cursor.execute("INSERT INTO users (user_id, guild_id) VALUES (?, ?)", (ctx.author.id, ctx.guild.id))
            self.connection.commit()
            user = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (ctx.author.id,)).fetchone()

        amount = random.randint(50, 200)
        self.cursor.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (amount, ctx.author.id))
        self.connection.commit()

        embed = disnake.Embed(title="Работа выполнена", description=f"{ctx.author.mention}, Вы заработали {amount} денег.", color=disnake.Color.green())
        await ctx.send(embed=embed)
  
    @commands.slash_command(description = 'Попытать удачу')
    @commands.cooldown(1, 360, commands.BucketType.user)
    async def crime(self, ctx):
        user_id = ctx.author.id
        self.cursor.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
        result = self.cursor.fetchone()
        if result is None:
            self.cursor.execute("INSERT INTO users(user_id, guild_id) VALUES(?, ?)", (user_id, ctx.guild.id))
            self.connection.commit()
            result = (0,)
        balance = result[0]
        success_rate = random.randint(1, 100)
        if success_rate <= 70:
            reward = random.randint(350, 1000)
            self.cursor.execute("UPDATE users SET balance=balance+? WHERE user_id=?", (reward, user_id))
            self.connection.commit()
            embed = disnake.Embed(title="Успех!", description=f"{ctx.author.mention}, вы смогли украсть {reward} денег!", color=disnake.Color.green(), timestamp=ctx.message.created_at)
            embed.set_footer(text=f'Ваш баланс: {balance+reward}')
        else:
            fine = random.randint(100, 500)
            self.cursor.execute("UPDATE users SET balance=balance-? WHERE user_id=?", (fine, user_id))
            self.connection.commit()
            embed = disnake.Embed(title="Провал!", description=f"{ctx.author.mention}, вы были пойманы и заплатили штраф в {fine} денег!.", color=disnake.Color.red(), timestamp=ctx.message.created_at)
            embed.set_footer(text=f'Ваш баланс: {balance-fine}')
        await ctx.send(embed=embed)

    @commands.slash_command(description = 'Посмотреть топ')
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def top(self, ctx):
      embed = disnake.Embed(title=f"Топ по балансу сервера {ctx.guild.name}")
# Используем коннектор для базы данных
      conn = sqlite3.connect('economy.db')
# Используем курсор для выполнения SQL-запроса
      cursor = conn.cursor()
# Выполняем запрос для получения топ-10 пользователей на сервере
      cursor.execute("SELECT user_id, balance FROM users WHERE guild_id=? ORDER BY balance DESC LIMIT 10", (ctx.message.guild.id,))
      top_users = cursor.fetchall()
# Закрываем соединение с базой данных
      conn.close()

      if len(top_users) == 0:
        embed.add_field(name="Топ пуст", value="Нет пользователей с балансом на этом сервере")
        await ctx.send(embed=embed)
        return

# Проходим по каждому пользователю в топ-10 и добавляем его в Embed-объект
      for index, user in enumerate(top_users):
        disnake_user = await self.bot.fetch_user(user[0])
        embed.add_field(name=f"{index + 1}. {disnake_user.name}", value=f"{user[1]} денег", inline=False)
      await ctx.send(embed=embed)
  

    @commands.slash_command(description = 'Перевод денег пользователю')
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def transfer(self, ctx, recipient: disnake.User, amount: int):
       if recipient.bot:
           await ctx.send(f"{ctx.author.mention}, Вы не можете перевести деньги боту!")
           return
       if recipient is None:
           await ctx.send(f"{ctx.author.mention}, Укажите получателя перевода.")
           return
       if amount is None:
           await ctx.send(f"{ctx.author.mention}, Укажите сумму перевода.")
           return

       sender_id = ctx.author.id
       self.cursor.execute("SELECT * FROM users WHERE user_id=?", (sender_id,))
       sender_data = self.cursor.fetchone()
       if sender_data is None:
           self.cursor.execute("INSERT INTO users (user_id, guild_id, balance) VALUES (?, ?, ?)", (sender_id, ctx.guild.id, 0))
           self.connection.commit()
           sender_data = (sender_id, ctx.guild.id, 0)
       if amount <= 0:
           await ctx.send("Сумма перевода должна быть больше нуля.")
           return
       if sender_data[2] < amount:
           await ctx.send("У вас недостаточно денег на балансе.")
           return
       if recipient == ctx.message.author:
        await ctx.send(f'{ctx.author.mention}, вы не можете самому себе переводить деньги!')
        return

       recipient_id = recipient.id
       self.cursor.execute("SELECT * FROM users WHERE user_id=?", (recipient_id,))
       recipient_data = self.cursor.fetchone()
       if recipient_data is None:
           self.cursor.execute("INSERT INTO users (user_id, guild_id, balance) VALUES (?, ?, ?)", (recipient_id, ctx.guild.id, 0))
           self.connection.commit()
           recipient_data = (recipient_id, ctx.guild.id, 0)

       self.cursor.execute("UPDATE users SET balance = balance - ? WHERE user_id=?", (amount, sender_id))
       self.cursor.execute("UPDATE users SET balance = balance + ? WHERE user_id=?", (amount, recipient_id))
       self.connection.commit()

       transfer_embed = disnake.Embed(title="Перевод денег", color=0x00ff00)
       transfer_embed.add_field(name="Отправил", value=ctx.author.name, inline=True)
       transfer_embed.add_field(name="Получатель", value=recipient.name, inline=True)
       transfer_embed.add_field(name="Сумма", value=amount, inline=True)
       await ctx.send(embed=transfer_embed)

    @commands.slash_command(description = 'Информация о сервере')
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def serverinfo(self, ctx):
        member = ctx.author
        server = ctx.guild
        user = await self.bot.fetch_guild(server.id)
        members_total = server.member_count
        members = sum(not member.bot for member in server.members)
        bots = sum(member.bot for member in server.members)
        channels_total = len(server.channels)
        text_channels = len(server.text_channels)
        roles = [role.name for role in member.roles]
        voice_channels = len(server.voice_channels)
        owner = server.owner
        verification_level = {
            disnake.VerificationLevel.none.value: "Нет",
            disnake.VerificationLevel.low.value: "Низкий",
            disnake.VerificationLevel.medium.value: "Средний",
            disnake.VerificationLevel.high.value: "Высокий",
            disnake.VerificationLevel.highest.value: "Очень высокий"
        }.get(server.verification_level.value, "Неизвестно")
        created_at = int(server.created_at.timestamp())
        embed = disnake.Embed(title=f"Информация о сервере **{server.name}**",
                              color=0x00ff00)
        if server.icon:
            embed.set_thumbnail(url=server.icon.url)
        if user.banner is not None:
            embed.set_image(url=user.banner.url)
        embed.add_field(
            name="Участники",
            value=
            f"<:blurplemembers:1085511354196168725> Всего: {members_total}\n<:maleicon:1085511328644464670> Людей: {members}\n<:discordboten:1085505982387474482> Ботов: {bots}"
        )
        embed.add_field(
            name="Каналы",
            value=
            f"<:discordchannels:1085506066009301084> Всего: {channels_total}\n<:discordchannel:1085506036171022376> Текстовых: {text_channels}\n<:discordvoice:1085506193977516032> Голосовых: {voice_channels}"
        )
        embed.add_field(name="Владелец", value=f"{owner}")
        embed.add_field(name="Уровень проверки", value=f"{verification_level}")
        embed.add_field(name="Дата создания",
                        value=f"<t:{created_at}:D>\n (<t:{created_at}:R>)")
        embed.add_field(name='ID', value=f"{server.id}")
        await ctx.send(embed=embed)

    @commands.slash_command(description = 'Информация о пользователе')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def userinfo(self, ctx, member: disnake.Member = None):
        member = member or ctx.author
        roles = [role.name for role in member.roles if role.name != "@everyone"]
        user = await self.bot.fetch_user(member.id)
        embed = disnake.Embed(
            title=f'',
            description=
            f'**Имя пользователя:** {member.nick or member.name}#{member.discriminator}\n**Присоединился:** <t:{int(member.joined_at.timestamp())}:D> (<t:{int(member.joined_at.timestamp())}:R>) \n**Аккаунт создан:** <t:{int(member.created_at.timestamp())}:D> (<t:{int(member.created_at.timestamp())}:R>)\n**Роли:** {", ".join(roles)}',
            color=0x00ff00)
        embed.set_author(name=f'Информация о {member.name}',
                         icon_url=member.avatar.url)
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name='ID', value=f"{member.id}")
        if user.banner is not None:
            embed.set_image(url=user.banner.url)
        await ctx.send(embed=embed)
def setup(bot):
  bot.add_cog(Slash(bot))