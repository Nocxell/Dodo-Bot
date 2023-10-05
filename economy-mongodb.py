import discord
from discord.ext import commands
import pymongo
import os
from discord import app_commands
import random
import json
import asyncio
from asyncio import sleep


client = pymongo.MongoClient(os.environ['pymongo'])
db = client.user_messages
name = client["database"]
col = name["users"]

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def balance(self, ctx):
      user = ctx.author.id
      result = col.find_one({"user_id": user})
      if result is None:
        col.insert_one({"user_id": user, "balance": 0})
        embed = discord.Embed(title = f'Баланс {ctx.author}')
        embed.add_field(name = f'Ваш баланс:', value = '0')
        await ctx.send(embed = embed)
      else:
          balance = result["balance"]
          embed = discord.Embed(title = f'Баланс {ctx.author}')
          embed.add_field(name = f'Ваш баланс:', value = balance)
          await ctx.send(embed = embed)

    @commands.command()
    @commands.cooldown(1, 360, commands.BucketType.user)
    async def crime(self, ctx):
      user = col.find_one({"user_id": ctx.author.id})
      if user is None:
        col.insert_one({"user_id": ctx.author.id, "guild_id": str(ctx.guild.id), "balance": 0})
        user = col.find_one({"user_id": ctx.author.id})
      success_rate = random.randint(1, 100)
      if success_rate <= 70:
        reward = random.randint(350, 1000)
        col.update_one({"user_id": ctx.author.id}, {"$inc": {"balance": reward}})
        user = col.find_one({"user_id": ctx.author.id})
        embed = discord.Embed(title="Успех!", description=f"{ctx.author.mention}, вы смогли украсть {reward} денег!", color=discord.Color.green(), timestamp = ctx.message.created_at)
        embed.set_footer(text = f'Ваш баланс: {user["balance"]}')
      else:
        fine = random.randint(100, 500)
        col.update_one({"user_id": ctx.author.id}, {"$inc": {"balance": -fine}})
        user = col.find_one({"user_id": ctx.author.id})
        embed = discord.Embed(title="Провал!", description=f"{ctx.author.mention}, вы были пойманы и заплатили штраф в {fine} денег!.", color=discord.Color.red(), timestamp = ctx.message.created_at)
        embed.set_footer(text = f'Ваш баланс: {user["balance"]}')
      await ctx.send(embed=embed)
  
    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def top(self,ctx):
      tes = discord.Embed(title="Глобальный топ 10 пользователей по балансу")
      global_users = col.find().sort("balance", -1).limit(10)
      for index, user in enumerate(global_users):
        users = await self.bot.fetch_user(user["user_id"])
        tes.add_field(name=f"{index + 1}. {users.name}", value=f"{user['balance']} денег", inline=False)
      await ctx.send(embed=tes)

    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def transfer(self, ctx, recipient: discord.User = None, amount: int = None):
        if recipient == ctx.author.bot:
            await ctx.send(f"{ctx.author.mention}, Вы не можете перевести деньги боту!")
            return
        if recipient is None:
            await ctx.send(f"{ctx.author.mention}, Укажите получателя перевода.")
            return
        if amount is None:
            await ctx.send(f"{ctx.author.mention}, Укажите сумму перевода.")
            return

        sender_id = ctx.author.id
        sender_data = self.cursor.execute("SELECT * FROM users WHERE user_id=?", (sender_id,)).fetchone()
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
        recipient_data = self.cursor.execute("SELECT * FROM users WHERE user_id=?", (recipient_id,)).fetchone()
        if recipient_data is None:
            self.cursor.execute("INSERT INTO users (user_id, guild_id, balance) VALUES (?, ?, ?)", (recipient_id, ctx.guild.id, 0))
            self.connection.commit()
            recipient_data = (recipient_id, ctx.guild.id, 0)

        self.cursor.execute("UPDATE users SET balance = balance - ? WHERE user_id=?", (amount, sender_id))
        self.cursor.execute("UPDATE users SET balance = balance + ? WHERE user_id=?", (amount, recipient_id))
        self.connection.commit()

        transfer_embed = discord.Embed(title="Перевод денег", color=0x00ff00)
        transfer_embed.add_field(name="Отправил", value=ctx.author.name, inline=True)
        transfer_embed.add_field(name="Получатель", value=recipient.name, inline=True)
        transfer_embed.add_field(name="Сумма", value=amount, inline=True)
        await ctx.send(embed=transfer_embed)
  
    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def топ53(self, ctx, type: str = 'global'):
        if type == 'global':
            embed = discord.Embed(title="Глобальный топ 10 пользователей по балансу")
            users = col.find().sort("balance", -1).limit(10)
        elif type == 'server':
            embed = discord.Embed(title=f"Топ по балансу сервера {ctx.guild.name} ")
            users = col.find({"guild_id": str(ctx.guild.id)}).sort("balance", -1).limit(10)
        else:
            await ctx.send('Неправильный тип топа! Используйте "global" или "server".')
            return

        for index, user in enumerate(users):
            discord_user = await self.bot.fetch_user(user["user_id"])
            embed.add_field(name=f"{index + 1}. {discord_user.name}", value=f"{user['balance']} денег", inline=False)
        #embed.set_thumbnail(url=ctx.guild.icon.url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def casino(self, ctx, bet: int = None):
      if bet is None:
        embed = discord.Embed(title="Ошибка", description=f"{ctx.author.mention}, Вы не указали ставку.", color=discord.Color.red())
        await ctx.send(embed=embed)
        return
      
      user = col.find_one({"user_id": ctx.author.id})
      if user is None:
        col.insert_one({"user_id": ctx.author.id, "balance": 0})
        user = col.find_one({"user_id": ctx.author.id})
      if bet <= 0:
        embed = discord.Embed(title="Ошибка", description=f"{ctx.author.mention}, Ставка должна быть больше нуля.", color=discord.Color.red())
        await ctx.send(embed=embed)
        return
      if user["balance"] < bet:
        embed = discord.Embed(title="Ошибка", description=f"{ctx.author.mention}, У вас недостаточно денег на балансе.", color=discord.Color.red())
        await ctx.send(embed=embed)
        return
      result = random.choices(["win", "lose"], weights=[1.8, 1], k=1)[0]
      if result == "win":
          win_amount = bet * 2
          col.update_one({"user_id": ctx.author.id}, {"$inc": {"balance": win_amount}})
          user = col.find_one({"user_id": ctx.author.id})
          embed = discord.Embed(description=f"{ctx.author.mention}, Вы выиграли {win_amount} денег. Ваш баланс: {user['balance']}", color = discord.Color.green())
          await ctx.send(embed=embed)
      else:
        loss_amount = bet
        col.update_one({"user_id": ctx.author.id}, {"$inc": {"balance": -loss_amount}})
        user = col.find_one({"user_id": ctx.author.id})
        embed = discord.Embed(description=f"{ctx.author.mention}, Вы проиграли {loss_amount} денег. Ваш баланс: {user['balance']}", color = discord.Color.red())
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 900, commands.BucketType.user)
    async def rob(self, ctx, member: discord.Member = None,):
      if member is None:
        await ctx.send(f"{ctx.author.mention}, Укажите пользователя, которого вы хотите ограбить.")
        return
      if member == ctx.author:
        await ctx.send(f"{ctx.author.mention}, Вы не можете ограбить самого себя.")
        return
      if member == ctx.author.bot:
        await ctx.send(f"{ctx.author.mention}, Вы не можете ограбить бота!")
        return
      user = col.find_one({"user_id": ctx.author.id})
      target = col.find_one({"user_id": member.id})
      if user is None:
        col.insert_one({"user_id": user, "balance": 0})
        return
      if target is None:
        await ctx.send(f"Человек не найден.")
        return
      if user["balance"] < 50:
        await ctx.send(f"{ctx.author.mention}, У вас недостаточно средств на счету для ограбления.")
        return
      target_balance = target["balance"]
      success_rate = min(target_balance / 1000, 0.9)
      if random.random() < success_rate:
        amount = min(target_balance, 800)
        col.update_one({"user_id": ctx.author.id}, {"$inc": {"balance": amount}})
        col.update_one({"user_id": member.id}, {"$inc": {"balance": -amount}})
        await ctx.send(f"Вы успешно ограбили {member.mention} и получили {amount} денег!")
      else:
        amount = random.randint(10, 199)
        col.update_one({"user_id": ctx.author.id}, {"$inc": {"balance": -amount}})
        await ctx.send(f"Вы неудачно попытались ограбить {member.mention} и потеряли {amount} денег.")

    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def transfer(self, ctx, recipient: discord.User = None, amount: int = None):
      if recipient == ctx.author.bot:
        await ctx.send(f"{ctx.author.mention}, Вы не можете перевести деньги боту!")
        return
      if recipient is None:
        await ctx.send(f"{ctx.author.mention}, Укажите получателя перевода.")
        return
      if amount is None:
        await ctx.send(f"{ctx.author.mention}, Укажите сумму перевода.")
        return

      sender = col.find_one({"user_id": ctx.author.id})
      if sender is None:
        col.insert_one({"user_id": ctx.author.id, "balance": 0, "server_id": ctx.guild.id})
        sender = col.find_one({"user_id": ctx.author.id})
      if amount <= 0:
        await ctx.send("Сумма перевода должна быть больше нуля.")
        return
      if sender["balance"] < amount:
        await ctx.send("У вас недостаточно денег на балансе.")
        return
      if recipient == ctx.message.author:
        await ctx.send(f'{ctx.author.mention}, вы не можете самому себе переводить деньги!')
        return
      col.update_one({"user_id": ctx.author.id}, {"$inc": {"balance": -amount}})
      recipient_data = col.find_one({"user_id": recipient.id})
      if recipient_data is None:
        col.insert_one({"user_id": recipient.id, "balance": 0, "server_id": ctx.guild.id})
        recipient_data = col.find_one({"user_id": recipient.id})
      col.update_one({"user_id": recipient.id}, {"$inc": {"balance": amount}})
      transfer_embed = discord.Embed(title="Перевод денег", color=0x00ff00)
      transfer_embed.add_field(name="Отправил", value=ctx.author.name, inline=True)
      transfer_embed.add_field(name="Получатель", value=recipient.name, inline=True)
      transfer_embed.add_field(name="Сумма", value=amount, inline=True)
      await ctx.send(embed=transfer_embed)

    @commands.command()
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def work(self, ctx):
      user = col.find_one({"user_id": ctx.author.id})
      if not user:
        col.insert_one({"user_id": ctx.author.id, "balance": 0})
        user = {"user_id": ctx.author.id, "balance": 0}
      earnings = random.randint(125, 1250)
      col.update_one({"user_id": ctx.author.id}, {"$inc": {"balance": earnings}})
      await ctx.send(f"Вы поработали и заработали {earnings} денег. Ваш новый баланс: {user['balance'] + earnings}")

async def setup(bot):
  await bot.add_cog(Economy(bot))