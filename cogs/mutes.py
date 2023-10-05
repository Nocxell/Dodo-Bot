import datetime
import sqlite3
from disnake.ext import commands
import disnake

class TimeoutCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_conn = sqlite3.connect('timeout.db')  # Подключение к базе данных
        self.db_cursor = self.db_conn.cursor()
        self.db_cursor.execute('CREATE TABLE IF NOT EXISTS timeouts (member_id INTEGER PRIMARY KEY, timeout_until TEXT, reason TEXT, moderator_id INTEGER)')
        self.db_conn.commit()

    @commands.slash_command(
        name="mute",
        description="Выдать мьют участнику.",
        options=[
            disnake.Option(
                type=disnake.OptionType.user,
                name="member",
                description="Участник, которого нужно замутить.",
                required=True
            ),
            disnake.Option(
                type=disnake.OptionType.integer,
                name="time",
                description="Длительность мьюта в минутах.",
                required=True
            ),
            disnake.Option(
                type=disnake.OptionType.string,
                name="reason",
                description="Причина мьюта.",
                required=True
            )
        ]
    )
    async def mute(self, ctx, member: disnake.Member, time: int, reason: str):
        timeout_until = datetime.datetime.now() + datetime.timedelta(minutes=time)
        member_id = member.id
        moderator_id = ctx.author.id

        # Записываем информацию о мьюте в базу данных
        self.db_cursor.execute('INSERT INTO timeouts (member_id, timeout_until, reason, moderator_id) VALUES (?, ?, ?, ?)',
                               (member_id, timeout_until, reason, moderator_id))
        self.db_conn.commit()

        await member.timeout(reason=reason, until=timeout_until)

        embed = disnake.Embed(title="Мьют", color=disnake.Color.red())
        embed.add_field(name="Замьюченный участник", value=f"{member.display_name} (**``{member.id}``**)", inline=False)
        embed.add_field(name="Длительность", value=str(datetime.timedelta(minutes=time)), inline=False)
        embed.add_field(name="Причина", value=reason, inline=False)
        embed.add_field(name="Модератор", value=ctx.author.mention, inline=False)

        await ctx.send(embed=embed)

    @commands.slash_command(
        name="unmute",
        description="Снять мьют с участника.",
        options=[
            disnake.Option(
                type=disnake.OptionType.user,
                name="member",
                description="Участник, с которого нужно снять мьют.",
                required=True
            )
        ]
    )
    async def unmute(self, ctx, member: disnake.Member):
        member_id = member.id

        # Удаляем информацию о мьюте из базы данных
        self.db_cursor.execute('DELETE FROM timeouts WHERE member_id = ?', (member_id,))
        self.db_conn.commit()

        await member.timeout(reason=None, until=None)

        embed = disnake.Embed(title="Размьют", color=disnake.Color.green())
        embed.add_field(name="Размьюченный участник", value=f"{member.mention} (**``{member.id}``**)", inline=False)
        embed.add_field(name="Модератор", value=ctx.author.mention, inline=False)

        await ctx.send(embed=embed)

    @commands.slash_command(
        name="mutelist",
        description="Список замьюченых участников"
    )
    async def mutelist(self, ctx):
        self.db_cursor.execute('SELECT member_id, timeout_until, reason, moderator_id FROM timeouts')
        results = self.db_cursor.fetchall()

        embed = disnake.Embed(title="Список мьютов на сервере", color=disnake.Color.red())

        for row in results:
            member_id, timeout_until, reason, moderator_id = row
            member = ctx.guild.get_member(member_id)
            moderator = ctx.guild.get_member(moderator_id)

            if member and moderator:
                embed.add_field(name=f"{member.mention} (**``{member.id})``**",
                                value=f"Длительность: **``{timeout_until}``** \nПричина: **``{reason}``**\nЗамьютил: {moderator.mention}",
                                inline=False)

        await ctx.send(embed=embed)

    def cog_unload(self):
        self.db_conn.close()

def setup(bot):
    bot.add_cog(TimeoutCog(bot))
