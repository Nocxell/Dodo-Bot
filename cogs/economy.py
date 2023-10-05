import disnake
from disnake.ext import commands
import random
import sqlite3
import asyncio

class ExampleCog(commands.Cog):
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
  
    @commands.command()
    @commands.has_permissions(administrator = True)
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

     
    @commands.command()
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
    @commands.command()
    async def rob(self, ctx, member: disnake.Member = None,):
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
    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def casino(self, ctx, bet: int = None):
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
    @commands.command()
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
  
    @commands.command()
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

    @commands.command()
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
  

    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def transfer(self, ctx, recipient: disnake.User = None, amount: int = None):
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

def setup(bot):
    bot.add_cog(ExampleCog(bot))