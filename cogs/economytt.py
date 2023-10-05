import sqlite3
import random
import disnake
from disnake.ext import commands

class Economy1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild_connections = {}

        # Register all guilds and users with a zero balance
        for guild in self.bot.guilds:
            self.bot.loop.create_task(self.register_guild(guild))

    async def register_guild(self, guild):
        conn, c = await self.get_connection(guild.id)
        c.execute("SELECT user_id FROM economy")
        registered_users = set(row[0] for row in c.fetchall())

        for member in guild.members:
            if member.id not in registered_users:
                c.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?)", (member.id, 0))

        conn.commit()

    async def get_connection(self, guild_id):
        if guild_id in self.guild_connections:
            return self.guild_connections[guild_id]

        conn = sqlite3.connect(f'economy/economy_{guild_id}.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS economy
                      (user_id INT PRIMARY KEY, balance INT)''')
        self.guild_connections[guild_id] = (conn, c)
        return conn, c

    async def close_connection(self, guild_id):
        if guild_id in self.guild_connections:
            conn, _ = self.guild_connections.pop(guild_id)
            conn.close()

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def top2(self, ctx):
        embed = disnake.Embed(title=f"Топ по балансу сервера {ctx.guild.name}")

        conn, c = await self.get_connection(ctx.guild.id)
        c.execute("SELECT user_id, balance FROM economy WHERE balance > 0 ORDER BY balance DESC LIMIT 10")
        top_users = c.fetchall()

        if len(top_users) == 0:
            embed.add_field(name="Топ пуст", value="Нет пользователей с балансом на этом сервере")
            await ctx.send(embed=embed)
            return

        for index, user in enumerate(top_users):
            user_obj = self.bot.get_user(user[0])
            if not user_obj:
                user_obj = await self.bot.fetch_user(user[0])
            embed.add_field(name=f"{index + 1}. {user_obj.name}", value=f"{user[1]} денег", inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def work2(self, ctx):
        earnings = random.randint(1, 100)
        user_id = ctx.author.id
        guild_id = ctx.guild.id

        self.update_balance(user_id, guild_id, earnings)
        await ctx.send(f"{ctx.author.mention}, вы поработали и заработали {earnings} денег!")

    @commands.command()
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def casino2(self, ctx, amount: int):
        if amount <= 0:
            await ctx.send("Введите сумму больше 0.")
            return

        user_id = ctx.author.id
        guild_id = ctx.guild.id
        balance = await self.get_balance(user_id, guild_id)

        if balance is None or balance < amount:
            await ctx.send("У вас недостаточно денег.")
            return

        outcome = random.choice(["win", "lose"])

        if outcome == "win":
            winnings = amount * 2
            self.update_balance(user_id, guild_id, winnings)
            await ctx.send(f"{ctx.author.mention}, вы выиграли {winnings} денег!")
        else:
            self.update_balance(user_id, guild_id, -amount)
            await ctx.send(f"{ctx.author.mention}, вы проиграли {amount} денег!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reset_economy2(self, ctx):
        conn, c = await self.get_connection(ctx.guild.id)
        c.execute("DELETE FROM economy")
        conn.commit()
        await ctx.send("Состояние экономики сервера сброшено.")

    @commands.command()
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def crime2(self, ctx):
        success = random.choice([True, False])
        user_id = ctx.author.id
        guild_id = ctx.guild.id

        if success:
            earnings = random.randint(1, 100)
            self.update_balance(user_id, guild_id, earnings)
            await ctx.send(f"{ctx.author.mention}, вы успешно совершили преступление и заработали {earnings} денег!")
        else:
            fine = random.randint(1, 50)
            self.update_balance(user_id, guild_id, -fine)
            await ctx.send(f"{ctx.author.mention}, вы попались при совершении преступления и заплатили штраф в размере {fine} денег.")

    @commands.command()
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def rob2(self, ctx, user: disnake.Member):
        if user.id == ctx.author.id:
            await ctx.send("Вы не можете ограбить сами себя.")
            return

        robber_balance = await self.get_balance(ctx.author.id, ctx.guild.id)
        victim_balance = await self.get_balance(user.id, ctx.guild.id)

        if robber_balance is None or victim_balance is None:
            await ctx.send("У одного из пользователей отсутствует баланс.")
            return

        amount = min(victim_balance, random.randint(1, victim_balance))
        self.update_balance(ctx.author.id, ctx.guild.id, amount)
        self.update_balance(user.id, ctx.guild.id, -amount)
        await ctx.send(f"{ctx.author.mention} ограбил {user.mention} и забрал {amount} денег!")

    @commands.command()
    async def transfer2(self, ctx, user: disnake.Member, amount: int):
        if user.id == ctx.author.id:
            await ctx.send("Вы не можете передать деньги самому себе.")
            return

        sender_balance = await self.get_balance(ctx.author.id, ctx.guild.id)
        recipient_balance = await self.get_balance(user.id, ctx.guild.id)

        if sender_balance is None or recipient_balance is None:
            await ctx.send("У одного из пользователей отсутствует баланс.")
            return

        if amount <= 0:
            await ctx.send("Введите сумму больше 0.")
            return

        if amount > sender_balance:
            await ctx.send("У вас недостаточно денег.")
            return

        self.update_balance(ctx.author.id, ctx.guild.id, -amount)
        self.update_balance(user.id, ctx.guild.id, amount)
        await ctx.send(f"{ctx.author.mention} передал {user.mention} {amount} денег!")

    async def register_user(self, user_id, guild_id):
        conn, c = await self.get_connection(guild_id)
        c.execute("INSERT INTO economy (user_id, balance) VALUES (?, ?)", (user_id, 0))
        conn.commit()

    async def get_balance(self, user_id, guild_id):
        conn, c = await self.get_connection(guild_id)
        c.execute("SELECT balance FROM economy WHERE user_id = ?", (user_id,))
        balance = c.fetchone()
        return balance[0] if balance else None

    def update_balance(self, user_id, guild_id, amount):
        conn, c = self.get_connection(guild_id)
        c.execute("UPDATE economy SET balance = balance + ? WHERE user_id = ?", (amount, user_id))
        conn.commit()

def setup(bot):
    bot.add_cog(Economy1(bot))