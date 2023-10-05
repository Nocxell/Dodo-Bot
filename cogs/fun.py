import disnake
from disnake.ext import commands
from asyncio import sleep
import random
import aiohttp
import requests


tt = ['Да', 'Хохохо', 'Нет']
chair = ['Это точно 👌', 'Очень даже вряд-ли 🤨', 'Нет ❌', 'Да, безусловно ✔', 'Вы можете рассчитывать на это 👌', 'Вероятно 🤨', 'Перспектива хорошая 🤔', 'Да ✔', 'Знаки указывают да 👍', 'Ответ туманный, попробуйте еще раз 👀', 'Спроси позже 👀', 'Лучше не говорить тебе сейчас 🥵', 'Не могу предсказать сейчас 👾', 'Сконцентрируйтесь и спросите снова 🤨', 'Не рассчитывай на это 🙉', 'Мой ответ - Нет 😕','Мои источники говорят нет 🤨', 'Перспективы не очень 🕵️‍♂️', 'Очень сомнительно 🤔']

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ben(self, ctx, *, ben = None):
      if ben is None:
        await ctx.send("Вы не указали, что хотите спросить у Бена.")
        return
      embed = disnake.Embed(title = f'{ben}', description = f'Бен отвечает: {random.choice(tt)}')
      await ctx.send(embed = embed)
  
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def meme(self, ctx):
      color_int = random.randint(0, 0xFFFFFF)

    # Create a discord.Color object from the integer
      color = disnake.Color(color_int)
      async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/memes/new.json?sort=hot') as r:
            res = await r.json()

            # Filter out non-image posts and stickied posts
            posts = [p for p in res['data']['children'] if not p['data']['stickied'] and 'preview' in p['data']]

            if len(posts) == 0:
                await ctx.send("Мемов не найдено.")
                return

            # Choose a random post and create an embed
            post = random.choice(posts)
            embed = disnake.Embed(title=post['data']['title'], url=f"https://reddit.com{post['data']['permalink']}", color=color)
            embed.set_author(name=ctx.message.author.name,icon_url=ctx.message.author.avatar.url)
            embed.set_image(url=post['data']['url'])
            embed.set_footer(text=f"👍 {post['data']['ups']} | 💬 {post['data']['num_comments']}")
            await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def ball(self, ctx, *, question=None):
      if question is None:
        await ctx.send("Вы не указали, что хотите узнать у шара.")
        return
      if question != None:
        emb = disnake.Embed(title = f'{question}', description=f"{random.choice(chair)}")
        emb.set_image(url='https://sun9-15.userapi.com/impg/P2ZAiM3V4XyF-evI1sMWvnm1slzHVoXsoQNtjg/eGZsFoXfDFE.jpg?size=604x604&quality=96&sign=8055a0af19a00238cfed5e6c6d77c30c&type=album')
        await ctx.send(embed=emb)

    @commands.command(description="Аватар юзера")
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
    @commands.command()
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def bug(self, ctx, *, t):
    #  invite = await ctx.channel.create_invite(max_uses=60, unique=True)
      channel = self.bot.get_channel(1084823051813802014)
      await channel.send(
        f"**Баг!** <@&990626380997853204> \n**Баг от {ctx.message.author}#{ctx.message.author.discriminator} | {ctx.message.author.id}.** \n**Сервер:** {ctx.message.guild.name} | {ctx.message.guild.id}. \n**Баг:** {t}"
    )
      await ctx.send("**Ваш баг успешно отправлен!**")

    @commands.command()
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def idea(self, ctx, *, t):
      #invite = await ctx.channel.create_invite(max_uses=60, unique=True)
      channel = self.bot.get_channel(1084821796676718592)
      await channel.send(
        f"**Идея!** <@&990626380997853204> \n**Идея от {ctx.message.author}#{ctx.message.author.discriminator} | {ctx.message.author.id}.** \n**Сервер:** {ctx.message.guild.name} | {ctx.message.guild.id}. \n**Идея:** {t}"
    )
      await ctx.send("**Ваша идея успешно отправлена!**")
def setup(bot):
    bot.add_cog(Fun(bot))