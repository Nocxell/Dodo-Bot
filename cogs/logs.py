import sqlite3
import disnake
import pytz
from disnake.ext import commands
import aiohttp
from datetime import datetime, timedelta

# Connect to the SQLite database
conn = sqlite3.connect('message_logs.db')
cursor = conn.cursor()

# Create the message_logs table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS message_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guild_id INTEGER,
        logging_channel_id INTEGER
    )
''')
conn.commit()

class MessageLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.timezone = pytz.timezone('UTC')


    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot:
            return
        if before.guild is None:
            return

        if not self.has_text_content(before):
            return

        guild_id = before.guild.id
        cursor.execute('SELECT logging_channel_id FROM message_logs WHERE guild_id = ?', (guild_id,))
        result = cursor.fetchone()

        if result is not None:
            logging_channel_id = result[0]
            logging_channel = self.bot.get_channel(logging_channel_id)

            webhook_url = await self.get_webhook_url(logging_channel)
            if webhook_url:
                async with aiohttp.ClientSession() as session:
                    webhook_payload = {
                        'username': 'Dodo Logs',
                        'embeds': [
                            {
                                'title': 'Сообщение изменено',
                                'color': disnake.Color.gold().value,
                                'thumbnail': {
                                    'url': str(before.author.avatar.url),
                                },
                                'fields': [
                                    {'name': 'Канал', 'value': f'{before.channel.mention} (**``{before.channel.name}``**/**``{before.channel.id}``**)'},
                                    {'name': 'Автор', 'value': f'{before.author.mention} (**``{before.author.name}#{before.author.discriminator}``**/ID: **``{before.author.id}``**)'},
                                    {'name': 'Сообщение', 'value': f'[Посмотреть сообщение]({before.jump_url})\n\n'
                                                             f'**Сообщение до изменения:**\n```{before.content}```\n\n'
                                                             f'**Сообщение после изменения:**\n```{after.content}```',
                                     'inline': False},
                                ]
                            }
                        ]
                    }
                    await session.post(webhook_url, json=webhook_payload)

    @commands.command()
    async def list_logging_channels(self, ctx):
        cursor.execute("SELECT guild_id, logging_channel_id FROM message_logs")
        results = cursor.fetchall()

        if results:
            message = "Logging is enabled in the following guilds and channels:\n\n"
            for guild_id, channel_id in results:
                guild = self.bot.get_guild(guild_id)
                channel = guild.get_channel(channel_id)
                message += f"Guild: {guild.name} ({guild.id})\nChannel: {channel.name} ({channel.id})\n\n"

            await ctx.send(message)
        else:
            await ctx.send("No guilds or channels found with logging enabled.")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        if message.guild is None:
            return

        if not self.has_text_content(message):
            return

        guild_id = message.guild.id
        cursor.execute('SELECT logging_channel_id FROM message_logs WHERE guild_id = ?', (guild_id,))
        result = cursor.fetchone()

        if result is not None:
            logging_channel_id = result[0]
            logging_channel = self.bot.get_channel(logging_channel_id)

            webhook_url = await self.get_webhook_url(logging_channel)
            if webhook_url:
                async with aiohttp.ClientSession() as session:
                    webhook_payload = {
                        'username': 'Dodo Logs',
                        'embeds': [
                            {
                                'title': 'Сообщение удалено',
                                'color': disnake.Color.red().value,
                                'fields': [
                                    {'name': 'Канал', 'value': f'{message.channel.mention} (**``{message.channel.name}``**/**``{message.channel.id}``**)'},
                                    {'name': 'Автор', 'value': f'{message.author.mention} (**``{message.author.name}#{message.author.discriminator}``**/ID: **``{message.author.id}``**)'},
                                    {'name': 'Сообщение', 'value': message.content or '*Сообщение пустое*'},
                                ]
                            }
                        ]
                    }
                    await session.post(webhook_url, json=webhook_payload)

    async def get_webhook_url(self, channel):
        webhooks = await channel.webhooks()
        for webhook in webhooks:
            if webhook.name == 'Dodo Logs':
                return webhook.url

        # If webhook doesn't exist, create a new one
        try:
            if channel.permissions_for(channel.guild.me).manage_webhooks:
                webhook = await channel.create_webhook(name='Dodo Logs')
                return webhook.url
        except:
            pass

        return None

    def has_text_content(self, message):
        if message.content:
            return True

        if message.attachments:
            # Проверяем, есть ли вложения, которые не являются фото или видео
            for attachment in message.attachments:
                if not attachment.is_spoiler() and attachment.content_type not in ["image/jpeg", "image/png", "image/gif", "video/mp4"]:
                    return True

        if message.embeds:
            # Проверяем, есть ли встроенные объекты, содержащие ссылки
            for embed in message.embeds:
                if embed.url:
                    return False

        return False


     
   
 
    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        if guild is None:
            return

        guild_id = guild.id
        cursor.execute('SELECT logging_channel_id FROM message_logs WHERE guild_id = ?', (guild_id,))
        result = cursor.fetchone()

        if result is not None:
            logging_channel_id = result[0]
            logging_channel = self.bot.get_channel(logging_channel_id)

            webhook_url = await self.get_webhook_url(logging_channel)
            if webhook_url:
                async with aiohttp.ClientSession() as session:
                    try:
                        ban_entries = await guild.fetch_ban(user)
                        unban_entry = next((entry for entry in ban_entries if entry.user.id == user.id), None) if ban_entries else None
                        if unban_entry is not None:
                            member_str = f'@{unban_entry.user} ({unban_entry.user.name}#{unban_entry.user.discriminator}/ID: {unban_entry.user.id})'
                            moderator = unban_entry.user
                        else:
                            member_str = f'@{unban_entry.user} ({unban_entry.user.name}#{unban_entry.user.discriminator}/ID: {unban_entry.user.id})' if unban_entry else f'Неизвестный пользователь (ID: {user})'
                            moderator = None
                    except disnake.NotFound:
                        member_str = f'{user.mention} (**``{user.name}#{user.discriminator}``**/ID:**``{user.id}``**)'
                        moderator = None

                    webhook_payload = {
                        'username': 'Dodo Logs',
                        'embeds': [
                            {
                                'title': 'Пользователь забанен',
                                'color': disnake.Color.red().value,
                                'thumbnail': {
                                    'url': str(user.avatar.url) if user.avatar else None,
                                },
                                'fields': [
                                    {'name': 'Пользователь', 'value': member_str},
                                    {'name': 'Модератор', 'value': f'{moderator.name} (**``{moderator.display_name}``**/**``{moderator.id}``**)' if moderator else 'Неизвестно'}
                                ]
                            }
                        ]
                    }
                    await session.post(webhook_url, json=webhook_payload)


    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = member.guild
        if guild is None:
            return

        guild_id = guild.id
        cursor.execute('SELECT logging_channel_id FROM message_logs WHERE guild_id = ?', (guild_id,))
        result = cursor.fetchone()

        if result is not None:
            logging_channel_id = result[0]
            logging_channel = self.bot.get_channel(logging_channel_id)

            webhook_url = await self.get_webhook_url(logging_channel)
            if webhook_url:
                async with aiohttp.ClientSession() as session:
                    member_str = f'{member.mention} (**``{member.name}#{member.discriminator}``**/**``{member.id}``**)'
                    webhook_payload = {
                        'username': 'Dodo Logs',
                        'embeds': [
                            {
                                'title': 'Пользователь покинул сервер',
                                'color': disnake.Color.red().value,
                                'thumbnail': {
                                    'url': str(member.avatar.url) if member.avatar else None,
                                },
                                'fields': [
                                    {'name': 'Пользователь', 'value': member_str},
                                    {'name': 'Роли', 'value': self.get_member_roles(guild, member)},
                                    {'name': 'Пребывание на сервере', 'value': self.get_member_join_duration(member)}
                                ]
                            }
                        ]
                    }
                    await session.post(webhook_url, json=webhook_payload)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        if guild is None:
            return

        guild_id = guild.id
        cursor.execute('SELECT logging_channel_id FROM message_logs WHERE guild_id = ?', (guild_id,))
        result = cursor.fetchone()

        if result is not None:
            logging_channel_id = result[0]
            logging_channel = self.bot.get_channel(logging_channel_id)

            webhook_url = await self.get_webhook_url(logging_channel)
            if webhook_url:
                async with aiohttp.ClientSession() as session:
                    try:
                        ban_entries = await guild.fetch_ban(user)
                        unban_entry = next((entry for entry in ban_entries if entry.user.id == user.id), None)
                        member_str = f'@{unban_entry.user} ({unban_entry.user.name}#{unban_entry.user.discriminator}/ID: {unban_entry.user.id})' if unban_entry else f'Неизвестный пользователь (ID: {user})'
                        async for entry in guild.audit_logs(limit=1, action=disnake.AuditLogAction.unban):
                            moderator = entry.user
                            break
                        else:
                            moderator = None

                    except disnake.NotFound:
                        member_str = f'{user.mention} (**``{user.name}#{user.discriminator}``**/ID:**``{user.id}``**)'
                        moderator = None

                    webhook_payload = {
                        'username': 'Dodo Logs',
                        'embeds': [
                            {
                                'title': 'Пользователь разбанен',
                                'color': disnake.Color.green().value,
                                'thumbnail': {
                                    'url': str(user.avatar.url) if user.avatar else None,
                                },
                                'fields': [
                                    {'name': 'Пользователь', 'value': member_str}
                                ]
                            }
                        ]
                    }
                    await session.post(webhook_url, json=webhook_payload)
                      

    def get_member_join_duration(self, member):
        now = datetime.now(self.timezone).replace(tzinfo=None)
        join_date = member.joined_at.replace(tzinfo=None)
        duration = now - join_date
        days = duration.days
        hours, remainder = divmod(duration.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f'{days} дней, {hours} часов, {minutes} минут'

    def get_member_roles(self, guild, member):
        roles = [role.mention for role in member.roles if role.name != "@everyone"]
        if roles:
            return ", ".join(roles)
        else:
            return "**``Нет ролей``**"

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild is None:
            return

        guild_id = member.guild.id
        cursor.execute('SELECT logging_channel_id FROM message_logs WHERE guild_id = ?', (guild_id,))
        result = cursor.fetchone()

        if result is not None:
            logging_channel_id = result[0]
            logging_channel = self.bot.get_channel(logging_channel_id)

            webhook_url = await self.get_webhook_url(logging_channel)
            if webhook_url:
                async with aiohttp.ClientSession() as session:
                    webhook_payload = {
                        'username': 'Dodo Logs',
                        'embeds': [
                            {
                                'title': 'Пользователь присоединился к серверу',
                                'color': disnake.Color.green().value,
                                'thumbnail': {
                                    'url': str(member.avatar.url) if member.avatar else None,
                                }, 
                                'fields': [
                                    {'name': 'Пользователь', 'value': f'{member.mention} (**``{member.name}#{member.discriminator}``**/**``{member.id}``**)'}
                                ]
                            }
                        ]
                    }
                    await session.post(webhook_url, json=webhook_payload)


    @commands.Cog.listener()
    async def on_member_kick(self, guild, user):
        if guild is None:
            return

        guild_id = guild.id
        cursor.execute('SELECT logging_channel_id FROM message_logs WHERE guild_id = ?', (guild_id,))
        result = cursor.fetchone()

        if result is not None:
            logging_channel_id = result[0]
            logging_channel = self.bot.get_channel(logging_channel_id)

            webhook_url = await self.get_webhook_url(logging_channel)
            if webhook_url:
                async with aiohttp.ClientSession() as session:
                    moderator = None
                    async for entry in guild.audit_logs(limit=1, action=disnake.AuditLogAction.kick):
                        if entry.target == user:
                            moderator = entry.user
                            break

                    webhook_payload = {
                        'username': 'Dodo Logs',
                        'embeds': [
                            {
                                'title': 'Пользователь кикнут',
                                'color': disnake.Color.green().value,
                                'fields': [
                                    {'name': 'Пользователь', 'value': f'{user.mention} ({user})'},
                                    {'name': 'Продолжительность пребывания', 'value': self.get_member_duration(guild, user)},
                                    {'name': 'Роли', 'value': self.get_member_roles(guild, user)},
                                    {'name': 'Модератор', 'value': f'{moderator.name} (**``{moderator.display_name}``**/**``{moderator.id}``**)' if moderator else 'Неизвестно'}
                                ]
                            }
                        ]
                    }
                    await session.post(webhook_url, json=webhook_payload)



    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        if before.guild is None:
            return

        guild_id = before.guild.id
        cursor.execute('SELECT logging_channel_id FROM message_logs WHERE guild_id = ?', (guild_id,))
        result = cursor.fetchone()

        if result is not None:
            logging_channel_id = result[0]
            logging_channel = self.bot.get_channel(logging_channel_id)

            webhook_url = await self.get_webhook_url(logging_channel)
            if webhook_url:
                async with aiohttp.ClientSession() as session:
                    if before.name != after.name:
                        event = 'Изменение имени роли'
                        description = f'Роль: {after.mention}\n\n**Старое имя:** **``{before.name}``**\n**Новое имя:** **``{after.name}``**'
                    elif before.permissions != after.permissions:
                        event = 'Изменение прав роли'
                        old_permissions = ', '.join([perm[0] for perm in before.permissions if perm[1]])
                        new_permissions = ', '.join([perm[0] for perm in after.permissions if perm[1]])

                        # Код для преобразования названий прав на русский язык
                        permissions_mapping = {
                            'create_instant_invite': 'Создание приглашений',
                            'kick_members': 'Исключение участников',
                            'ban_members': 'Блокировка участников',
                            'administrator': 'Администратор',
                            'manage_channels': 'Управление каналами',
                            'manage_guild': 'Управление сервером',
                            'add_reactions': 'Добавление реакций',
                            'view_audit_log': 'Просмотр журнала аудита',
                            'priority_speaker': 'Приоритетный режим',
                            'stream': 'Трансляция',
                            'read_messages': 'Чтение сообщений',
                            'send_messages': 'Отправка сообщений',
                            'send_tts_messages': 'Отправка TTS-сообщений',
                            'manage_messages': 'Управление сообщениями',
                            'embed_links': 'Вставка ссылок',
                            'attach_files': 'Прикрепление файлов',
                            'read_message_history': 'Чтение истории сообщений',
                            'mention_everyone': 'Упоминание всех',
                            'use_external_emojis': 'Использование внешних эмодзи',
                            'view_guild_insights': 'Просмотр статистики сервера',
                            'connect': 'Подключение к голосовым каналам',
                            'speak': 'Голосовой чат',
                            'mute_members': 'Заглушение участников',
                            'deafen_members': 'Отключение звука участникам',
                            'move_members': 'Перемещение участников',
                            'use_voice_activation': 'Использование голосового активации',
                            'change_nickname': 'Изменение никнейма',
                            'manage_nicknames': 'Управление никнеймами',
                            'manage_roles': 'Управление ролями',
                            'manage_webhooks': 'Управление вебхуками',
                            'manage_emojis_and_stickers': 'Управление эмодзи и стикерами',
                            'manage_threads': 'Управляет ветками',
                        	'request_to_speak': 'Запрос на выступление',
                        	'manage_events': 'Управление событиями',
                        	'manage_threads': 'Управление ветками',
                        	'create_public_threads': 'Создание публичных веток',
                        	'create_private_threads': 'Создание приватных веток',
                        	'external_stickers': 'Использование внешних стикеров',
                        	'send_messages_in_threads': 'Отправка сообщений в ветки',
                        	'use_embedded_activities': 'Использование встроенных активностей',
                        	'moderate_members': 'Модерирование участников',
                        	'external_emoji': 'Использование внешних эмодзи',
                        	'view_channel': 'Просмотр канала',
                        	'manage_emojis': 'Управление эмодзи'
                        }

                        old_permissions_str = ', '.join([permissions_mapping.get(perm, perm) for perm in old_permissions.split(', ')])
                        new_permissions_str = ', '.join([permissions_mapping.get(perm, perm) for perm in new_permissions.split(', ')])

                        description = f'Роль: {after.mention}\n\n**Старые права:** **``{old_permissions_str or "Не было прав"}``**\n\n**Новые права:** **``{new_permissions_str or "Не было прав"}``**\n'
                    else:
                        return

                    moderator = await self.get_audit_mod(before.guild, after)
                    if moderator:
                        moderator_str = f'{moderator.mention} (**``{moderator.name}#{moderator.discriminator}``**/**``{moderator.id}``**)'
                        description += f'\n**Модератор:** {moderator_str}'

                    webhook_payload = {
                        'username': 'Dodo Logs',
                        'embeds': [
                            {
                                'title': event,
                                'color': disnake.Color.blue().value,
                                'description': description,
                                'thumbnail': {
                                    'url': str(after.guild.icon.url) if after.guild.icon else None,
                                },                                
                            }
                        ]
                    }
                    await session.post(webhook_url, json=webhook_payload)



    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        if role.guild is None:
            return

        guild_id = role.guild.id
        cursor.execute('SELECT logging_channel_id FROM message_logs WHERE guild_id = ?', (guild_id,))
        result = cursor.fetchone()

        if result is not None:
            logging_channel_id = result[0]
            logging_channel = self.bot.get_channel(logging_channel_id)

            webhook_url = await self.get_webhook_url(logging_channel)
            if webhook_url:
                async with aiohttp.ClientSession() as session:
                    audit_logs = await role.guild.audit_logs(limit=1, action=disnake.AuditLogAction.role_create).flatten()
                    if audit_logs:
                        creator = audit_logs[0].user
                        webhook_payload = {
                            'username': 'Dodo Logs',
                            'embeds': [
                                {
                                    'title': 'Роль',
                                    'description': f'{role.mention} (**``{role.name}``**/**``{role.id}``**)',
                                    'color': disnake.Color.green().value,
                                    'thumbnail': {
                                        'url': str(role.guild.icon.url) if role.guild.icon else None,
                                    },
                                    'fields': [
                                        {'name': 'Модератор', 'value': f'{creator.mention} (**``{creator.name}#{creator.discriminator}``**/**``{creator.id})``**'},
                                    ]
                                }
                            ]
                        }
                        await session.post(webhook_url, json=webhook_payload)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        if role.guild is None:
            return

        guild_id = role.guild.id
        cursor.execute('SELECT logging_channel_id FROM message_logs WHERE guild_id = ?', (guild_id,))
        result = cursor.fetchone()

        if result is not None:
            logging_channel_id = result[0]
            logging_channel = self.bot.get_channel(logging_channel_id)

            webhook_url = await self.get_webhook_url(logging_channel)
            if webhook_url:
                async with aiohttp.ClientSession() as session:
                    audit_logs = await role.guild.audit_logs(limit=1, action=disnake.AuditLogAction.role_delete).flatten()
                    if audit_logs:
                        deleter = audit_logs[0].user
                        webhook_payload = {
                            'username': 'Dodo Logs',
                            'embeds': [
                                {
                                    'title': 'Удаление роли',
                                    'description': f'{role.mention} (**``{role.name}``**/**``{role.id})``** \nЦвет:**``{role.color.value}``**',
                                    'color': disnake.Color.red().value,
                                    'thumbnail': {
                                        'url': str(role.guild.icon.url) if role.guild.icon else None,
                                    },
                                    'fields': [
                                        {'name': 'Модератор', 'value': f'{deleter.mention} (**``{deleter.name}#{deleter.discriminator}``**/**``{deleter.id}``**)'},
                                    ]
                                }
                            ]
                        }
                        await session.post(webhook_url, json=webhook_payload)

    async def get_audit_mod(self, guild, role):
        async for entry in guild.audit_logs(limit=1, action=disnake.AuditLogAction.role_update):
            if entry.target.id == role.id:
                return entry.user
        return None

    
    
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        guild = channel.guild
        if guild is None:
            return

        guild_id = guild.id
        cursor.execute('SELECT logging_channel_id FROM message_logs WHERE guild_id = ?', (guild_id,))
        result = cursor.fetchone()

        if result is not None:
            logging_channel_id = result[0]
            logging_channel = self.bot.get_channel(logging_channel_id)

            webhook_url = await self.get_webhook_url(logging_channel)
            if webhook_url:
                async with aiohttp.ClientSession() as session:
                    channel_type = self.get_channel_type_russian(channel.type)
                    audit_logs = await guild.audit_logs(limit=1, action=disnake.AuditLogAction.channel_create).flatten()
                    moderator = audit_logs[0].user if audit_logs else None
                    moderator_info = f'{moderator.mention} (**``{moderator.name}#{moderator.discriminator}``**/**``{moderator.id}``**)' if moderator else 'Неизвестно'
                    webhook_payload = {
                        'username': 'Dodo Logs',
                        'embeds': [
                            {
                                'title': 'Создание канала',
                                'description': f'Канал: {channel.mention} (**``{channel.name}``**/**``{channel.id}``**)\nТип: {channel_type}\nПозиция: **``{channel.position}``**',
                                'color': disnake.Color.green().value,
                                'thumbnail': {
                                    'url': str(guild.icon.url) if guild.icon else None,
                                },
                                'fields': [
                                    {'name': 'Модератор', 'value': moderator_info}
                                ]
                            }
                        ]
                    }
                    await session.post(webhook_url, json=webhook_payload)
    
    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        guild = channel.guild
        if guild is None:
            return

        guild_id = guild.id
        cursor.execute('SELECT logging_channel_id FROM message_logs WHERE guild_id = ?', (guild_id,))
        result = cursor.fetchone()

        if result is not None:
            logging_channel_id = result[0]
            logging_channel = self.bot.get_channel(logging_channel_id)

            webhook_url = await self.get_webhook_url(logging_channel)
            if webhook_url:
                async with aiohttp.ClientSession() as session:
                    channel_type = self.get_channel_type_russian(channel.type)
                    audit_logs = await guild.audit_logs(limit=1, action=disnake.AuditLogAction.channel_delete).flatten()
                    moderator = audit_logs[0].user if audit_logs else None
                    moderator_info = f'{moderator.mention} (**``{moderator.name}#{moderator.discriminator}``**/**``{moderator.id}``**)' if moderator else 'Неизвестно'
                    webhook_payload = {
                        'username': 'Dodo Logs',
                        'embeds': [
                            {
                                'title': 'Удаление канала',
                                'description': f'Канал: **``{channel.name}``**/**``{channel.id}``**\nТип: {channel_type}',
                                'color': disnake.Color.red().value,
                                'thumbnail': {
                                    'url': str(guild.icon.url) if guild.icon else None,
                                },
                                'fields': [
                                    {'name': 'Модератор', 'value': moderator_info}
                                ]
                            }
                        ]
                    }
                    await session.post(webhook_url, json=webhook_payload)


    @staticmethod
    def get_channel_type_russian(channel_type):
        channel_types = {
            disnake.ChannelType.text: '<:discordchannel:1085506036171022376> Текстовый',
            disnake.ChannelType.voice: '<:discordvoice:1085506193977516032> Голосовой',
            disnake.ChannelType.category: '<:category:1112466158013136896> Категория',
            disnake.ChannelType.news: 'Новостной',
            disnake.ChannelType.stage_voice: 'Трибуна',
        }
        return channel_types.get(channel_type, 'Неизвестный')

    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild, before, after):
        guild_id = guild.id
        cursor.execute('SELECT logging_channel_id FROM message_logs WHERE guild_id = ?', (guild_id,))
        result = cursor.fetchone()

        if result is not None:
            logging_channel_id = result[0]
            logging_channel = self.bot.get_channel(logging_channel_id)

            webhook_url = await self.get_webhook_url(logging_channel)
            if webhook_url:
                async with aiohttp.ClientSession() as session:
                    added = [e for e in after if e not in before]
                    removed = [e for e in before if e not in after]
                    modified = [e for e in after if e in before and e.name != before[before.index(e)].name]
                    
                    for emoji in added:
                        moderator = await self.get_emoji_audit_log(guild, emoji.id, disnake.AuditLogAction.emoji_create)
                        moderator_info = self.get_moderator_info(moderator)
                        emoji_type = self.get_emoji_type(emoji)
                        webhook_payload = {
                            'username': 'Dodo Logs',
                            'embeds': [
                                {
                                    'title': 'Создание эмодзи',
                                    'description': f'Эмодзи: {emoji} (**``{emoji.name}``**/**``{emoji.id}``**)\nТип: {emoji_type}',
                                    'color': disnake.Color.green().value,
                                    'thumbnail': {
                                        'url': str(emoji.url) if emoji.url else None,
                                    },
                                    'fields': [
                                        {'name': 'Модератор', 'value': moderator_info}
                                    ]
                                }
                            ]
                        }
                        await session.post(webhook_url, json=webhook_payload)

                    for emoji in removed:
                        moderator = await self.get_emoji_audit_log(guild, emoji.id, disnake.AuditLogAction.emoji_delete)
                        moderator_info = self.get_moderator_info(moderator)
                        emoji_type = self.get_emoji_type(emoji)
                        webhook_payload = {
                            'username': 'Dodo Logs',
                            'embeds': [
                                {
                                    'title': 'Удаление эмодзи',
                                    'description': f'Эмодзи: {emoji} (**``{emoji.name}``**/**``{emoji.id}``**)\nТип: {emoji_type}',
                                    'color': disnake.Color.red().value,
                                    'thumbnail': {
                                        'url': str(emoji.url) if emoji.url else None,
                                    },
                                    'fields': [
                                        {'name': 'Модератор', 'value': moderator_info}
                                    ]
                                }
                            ]
                        }
                        await session.post(webhook_url, json=webhook_payload)

                    for emoji in modified:
                        moderator = await self.get_emoji_audit_log(guild, emoji.id, disnake.AuditLogAction.emoji_update)
                        moderator_info = self.get_moderator_info(moderator)
                        emoji_type = self.get_emoji_type(emoji)
                        previous_name = before[before.index(emoji)].name
                        webhook_payload = {
                            'username': 'Dodo Logs',
                            'embeds': [
                                {
                                    'title': 'Изменение эмодзи',
                                    'description': f'Название эмодзи: **``{previous_name}``** →**``{emoji.name}``**\n ID:**``{emoji.id}``**\nТип: {emoji_type}',
                                    'color': disnake.Color.orange().value,
                                    'thumbnail': {
                                        'url': str(emoji.url) if emoji.url else None,
                                    },
                                    'fields': [
                                        {'name': 'Модератор', 'value': moderator_info}
                                    ]
                                }
                            ]
                        }
                        await session.post(webhook_url, json=webhook_payload)

    async def get_emoji_audit_log(self, guild, emoji_id, action):
        async for entry in guild.audit_logs(limit=5, action=action):
            if entry.target.id == emoji_id:
                return entry.user
        return None

    @staticmethod
    def get_emoji_type(emoji):
        if emoji.animated:
            return '**``Анимированный``**'
        else:
            return '**``Статический``**'

    @staticmethod
    def get_moderator_info(moderator):
        if moderator:
            return f'{moderator.mention} (**``{moderator.name}#{moderator.discriminator}``**/**``{moderator.id}``**)'
        else:
            return 'Неизвестно'

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def logs_on(self, ctx, channel: disnake.TextChannel):
        guild_id = ctx.guild.id
        cursor.execute('SELECT * FROM message_logs WHERE guild_id = ?', (guild_id,))
        result = cursor.fetchone()

        if result is None:
            cursor.execute('INSERT INTO message_logs (guild_id, logging_channel_id) VALUES (?, ?)', (guild_id, channel.id))
            conn.commit()

            embed = disnake.Embed(title='Логирование сообщений включено', color=disnake.Color.green())
            embed.add_field(name='Канал', value=channel.mention)
            await ctx.send(embed=embed)

            webhook_url = await self.get_webhook_url(channel)
            if webhook_url:
                log_channel = self.bot.get_channel(channel.id)
                if log_channel:
                    webhook_payload = {
                        'username': 'Dodo Logs',
                        'embeds': [
                            {
                                'title': 'Логирование сообщений включено',
                                'color': disnake.Color.green().value,
                                'fields': [
                                    {'name': 'Канал', 'value': log_channel.mention},
                                    {'name': 'Статус', 'value': 'Включено'}
                                ]
                            }
                        ]
                    }
                    async with aiohttp.ClientSession() as session:
                        await session.post(webhook_url, json=webhook_payload)
        else:
            embed = disnake.Embed(title='❌ Ошибка', description='Логи уже былы включены для этого сервера.', color=disnake.Color.red())
            await ctx.send(embed=embed)

  
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def logs_off(self, ctx):
        guild_id = ctx.guild.id
        cursor.execute('SELECT * FROM message_logs WHERE guild_id = ?', (guild_id,))
        result = cursor.fetchone()

        if result is not None:
            cursor.execute('DELETE FROM message_logs WHERE guild_id = ?', (guild_id,))
            conn.commit()

            embed = disnake.Embed(title='Логирование сообщений выключено', color=disnake.Color.red())
            await ctx.send(embed=embed)

            channel_id = result[2]
            webhook_url = await self.get_webhook_url(ctx.guild.get_channel(channel_id))
            if webhook_url:
                log_channel = self.bot.get_channel(channel_id)
                if log_channel:
                    webhook_payload = {
                        'username': 'Dodo Logs',
                        'embeds': [
                            {
                                'title': 'Логирование сообщений выключено',
                                'color': disnake.Color.red().value,
                                'fields': [
                                    {'name': 'Канал', 'value': log_channel.mention},
                                    {'name': 'Статус', 'value': 'Выключено'}
                                ]
                            }
                        ]
                    }
                    async with aiohttp.ClientSession() as session:
                        await session.post(webhook_url, json=webhook_payload)
        else:
            embed = disnake.Embed(title='❌ Ошибка', description='Логи не былы включены для этого сервера.', color=disnake.Color.red())
            await ctx.send(embed=embed)

    @commands.slash_command(description='Включить логи')
    @commands.default_member_permissions(administrator=True)
    async def logs_setup(self, ctx, channel: disnake.TextChannel):
        guild_id = ctx.guild.id
        cursor.execute('SELECT * FROM message_logs WHERE guild_id = ?', (guild_id,))
        result = cursor.fetchone()

        if result is None:
            cursor.execute('INSERT INTO message_logs (guild_id, logging_channel_id) VALUES (?, ?)', (guild_id, channel.id))
            conn.commit()

            embed = disnake.Embed(title='Логирование сообщений включено', color=disnake.Color.green())
            embed.add_field(name='Канал', value=channel.mention)
            await ctx.send(embed=embed)

            webhook_url = await self.get_webhook_url(channel)
            if webhook_url:
                log_channel = self.bot.get_channel(channel.id)
                if log_channel:
                    webhook_payload = {
                        'username': 'Dodo Logs',
                        'embeds': [
                            {
                                'title': 'Логирование сообщений включено',
                                'color': disnake.Color.green().value,
                                'fields': [
                                    {'name': 'Канал', 'value': log_channel.mention},
                                    {'name': 'Статус', 'value': 'Включено'}
                                ]
                            }
                        ]
                    }
                    async with aiohttp.ClientSession() as session:
                        await session.post(webhook_url, json=webhook_payload)
        else:
            embed = disnake.Embed(title='❌ Ошибка', description='Логи уже былы включены для этого сервера.', color=disnake.Color.red())
            await ctx.send(embed=embed)

  
    @commands.slash_command(description='Выключить логи')
    @commands.default_member_permissions(administrator=True)
    async def logs_disable(self, ctx):
        guild_id = ctx.guild.id
        cursor.execute('SELECT * FROM message_logs WHERE guild_id = ?', (guild_id,))
        result = cursor.fetchone()

        if result is not None:
            cursor.execute('DELETE FROM message_logs WHERE guild_id = ?', (guild_id,))
            conn.commit()

            embed = disnake.Embed(title='Логирование сообщений выключено', color=disnake.Color.red())
            await ctx.send(embed=embed)

            channel_id = result[2]
            webhook_url = await self.get_webhook_url(ctx.guild.get_channel(channel_id))
            if webhook_url:
                log_channel = self.bot.get_channel(channel_id)
                if log_channel:
                    webhook_payload = {
                        'username': 'Dodo Logs',
                        'embeds': [
                            {
                                'title': 'Логирование сообщений выключено',
                                'color': disnake.Color.red().value,
                                'fields': [
                                    {'name': 'Канал', 'value': log_channel.mention},
                                    {'name': 'Статус', 'value': 'Выключено'}
                                ]
                            }
                        ]
                    }
                    async with aiohttp.ClientSession() as session:
                        await session.post(webhook_url, json=webhook_payload)
        else:
            embed = disnake.Embed(title='❌ Ошибка', description='Логи не былы включены для этого сервера.', color=disnake.Color.red())
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(MessageLogger(bot))