import disnake
from disnake.ext import commands
import psutil
import time
import os
import asyncio
from asyncio import sleep
import json


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
            embed.add_field(name=f'd.top',
                            value=f'Показать топ по балансу на сервере',
                            inline=False)
            embed.add_field(name=f'd.reset_economy',
                            value=f'Удалить экономику на сервере',
                            inline=False)
            embed.add_field(name=f'd.balance',
                            value=f'Показать баланс',
                            inline=False)
            embed.add_field(name=f'd.casino ``[ставка]``',
                            value=f'Поиграть в казино',
                            inline=False)
            embed.add_field(name=f'd.work', 
                            value=f'Поработать', 
                            inline=False)
            embed.add_field(name=f'd.transfer ``[пользователь]`` ``[cумма]``',
                            value=f'Перевод денег пользователю',
                            inline=False)
            embed.add_field(name=f'd.rob ``[пользователь]``',
                            value=f'Ограбить пользователя',
                            inline=False)
            embed.add_field(name=f'd.crime',
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
            embed.add_field(name=f'd.logs_on ``[канал]``',
                            value=f'Включить логи на сервере',
                            inline=False)
            embed.add_field(name=f'd.logs_off', value=f'Выключить логи на сервере')
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
            embed.add_field(name=f'd.ben ``[вопрос]``',
                            value=f'Задать вопрос бену',
                            inline=False)
            embed.add_field(name=f'd.meme', value=f'Отправить рандомный мем')
            embed.add_field(name=f'd.ball ``[вопрос]``',
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
            embed.add_field(name=f'd.ban ``[пользователь]`` ``<причина>`` ',
                            value=f'Забанить кого-то',
                            inline=False)
            embed.add_field(name=f'd.kick ``[пользователь]`` ``<причина>`` ',
                            value=f'Кикнуть кого-то',
                            inline=False)
            embed.add_field(name=f'd.say ``[сообщение]``',
                            value=f'Написать через бота',
                            inline=False)
            embed.add_field(name=f'd.unban ``[пользователь]``',
                            value='Разбанить пользователя',
                            inline=False)
            embed.add_field(name=f'd.warn ``[пользователь]`` ``<причина>``',
                            value='Выдать варн пользователю',
                            inline=False)
            embed.add_field(name=f'd.unwarn ``[пользователь]``',
                            value='Снять варн пользователю',
                            inline=False)
            embed.add_field(name=f'd.warns ``[пользователь]``',
                            value='Посмотреть варны пользователя',
                            inline=False)
            embed.add_field(name = 'd.slowmode ``[секунды]``', 
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
            embed.add_field(name=f'd.info',
                            value=f'Информация о боте',
                            inline=False)
            embed.add_field(name=f'd.avatar ``[пользователь]``',
                            value=f'Узнать аватар пользователя',
                            inline=False)
            embed.add_field(name=f'd.userinfo',
                            value=f'Информация о пользователе',
                            inline=False)
            embed.add_field(name=f'd.serverinfo',
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
            embed.add_field(name=f'd.bug ``[баг]``',
                            value=f'Сообщить о баге',
                            inline=False)
            embed.add_field(name=f'd.idea ``[идея]``',
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


class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.shard_count = 2
        self.start_time = time.time()
        try:
            with open("json/count.json", "r") as f:
                self.counts = json.load(f)
        except FileNotFoundError:
            print("File not found. Creating a new one.")

    @commands.command(aliases=['h', 'hel'])
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
                        value=f'`d.top` '
                        '`d.balance` '
                        '`d.casino` '
                        '`d.work` '
                        '`d.transfer` '
                        '`d.rob` '
                        '`d.crime` '
                        '`d.reset_economy` ')
        embed.add_field(name=f':shield: Модерация',
                        value='`d.ban` '
                        '`d.kick` '
                        '`d.say` '
                        '`d.unban` '
                        '`d.warn` '
                        '`d.unwarn` '
                        '`d.warns` '
                        '`d.slowmode`',
                        inline=False)
       	embed.add_field(name=f':gear: Настройки', value=f'`d.logs_on` '
						f'`d.logs_off`', inline=False)
        embed.add_field(name=f':grin: Развлечения',
                        value='`d.ben` '
                        '`d.ball` '
                        '`d.meme` ',
                        inline=False)
        embed.add_field(name=f':sparkles: Утилиты',
                        value='`d.info` '
                        '`d.avatar` '
                        '`d.userinfo` '
                        '`d.serverinfo` ',
                        inline=False)
        embed.add_field(name=f':space_invader: Другое',
                        value='`d.idea` '
                        '`d.bug` ',
                        inline=False)
        embed.set_footer(
            text="© 2022, Dufl | Все права защищены ботом Dodo Bot",
            icon_url=
            "https://cdn.discordapp.com/avatars/1097452648627703828/8209152252ebfdfd463a7e31d8a28fb4.png?size=1024"
        )
        await ctx.send(embed=embed, view=view)

    @commands.command()
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

    @commands.command()
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
    bot.add_cog(Utils(bot))
