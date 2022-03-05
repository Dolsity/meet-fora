from discord.ext import commands
import discord
import aiohttp
import requests
import io
from dotenv import load_dotenv
import os

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get(session: object, url: object) -> object:
        async with session.get(url) as response:
            return await response.text()

    # Tells you a joke
    @commands.command()
    async def joke(self, ctx):
        response = requests.get('https://some-random-api.ml/joke')
        data = response.json()

        embed = discord.Embed(title="JOKE", description=f'{data["joke"]}', color=0xffffff)
        embed.set_footer(text=f'Requested by {ctx.author.display_name}',icon_url=ctx.author.avatar_url_as(format="png"))
        await ctx.send(embed=embed)

    # Gives hug
    @commands.command()
    async def hug(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        response = requests.get('https://some-random-api.ml/animu/hug')
        data = response.json()

        embed = discord.Embed(title="", description=f'***{ctx.author.display_name} hugged {member.display_name}***', color=0xffffff)
        embed.set_image(url=data['link'])
        embed.set_footer(text=f'Requested by {ctx.author.display_name}',icon_url=ctx.author.avatar_url_as(format="png"))
        await ctx.send(embed=embed)

    # Displays real looking bot token
    @commands.command()
    async def token(self, ctx):
        response = requests.get('https://some-random-api.ml/bottoken')
        data = response.json()

        embed = discord.Embed(title="TOKEN", description=f'{data["token"]}', color=0xffffff)
        embed.set_footer(text=f'Requested by {ctx.author.display_name}',icon_url=ctx.author.avatar_url_as(format="png"))
        await ctx.send(embed=embed)

    # Gives you a cat fact
    @commands.command()
    async def catfact(self, ctx):
        response = requests.get('https://some-random-api.ml/animal/cat')
        data = response.json()

        embed = discord.Embed(title="FACT", description=f'{data["fact"]}', color=0xffffff)
        embed.set_image(url=data['image'])
        embed.set_footer(text=f'Requested by {ctx.author.display_name}',icon_url=ctx.author.avatar_url_as(format="png"))
        await ctx.send(embed=embed)

     # Gives you a dog fact
    @commands.command()
    async def dogfact(self, ctx):
        response = requests.get('https://some-random-api.ml/animal/dog')
        data = response.json()

        embed = discord.Embed(title="FACT", description=f'{data["fact"]}', color=0xffffff)
        embed.set_image(url=data['image'])
        embed.set_footer(text=f'Requested by {ctx.author.display_name}',icon_url=ctx.author.avatar_url_as(format="png"))
        await ctx.send(embed=embed)

     # Sends a wasted image over avatar 
    @commands.command()
    async def wasted(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        await ctx.trigger_typing()
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://some-random-api.ml/canvas/wasted?avatar={member.avatar_url_as(format="png")}') as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "wasted.png")
                    embed = discord.Embed(title="WASTED", color=0xffffff)
                    embed.set_image(url="attachment://wasted.png")
                    embed.set_footer(text=f'Requested by {ctx.author.display_name}',icon_url=ctx.author.avatar_url_as(format="png"))
                    await ctx.send(embed=embed, file=file)
                else:
                    await ctx.send('No wasted :(')
                    await session.close()

    # Sends a triggered gif over avatar 
    @commands.command()
    async def triggered(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        await ctx.trigger_typing()
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://some-random-api.ml/canvas/triggered?avatar={member.avatar_url_as(format="png")}') as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "triggered.gif")
                    embed = discord.Embed(title="TRIGGERED", color=0xffffff)
                    embed.set_image(url="attachment://triggered.gif")
                    embed.set_footer(text=f'Requested by {ctx.author.display_name}',icon_url=ctx.author.avatar_url_as(format="png"))
                    await ctx.send(embed=embed, file=file)
                else:
                    await ctx.send('No triggered :(')
                    await session.close()

    # Sends a gay rambow image over avatar 
    @commands.command()
    async def gay(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        await ctx.trigger_typing()
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://some-random-api.ml/canvas/gay?avatar={member.avatar_url_as(format="png")}') as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "gay.png")
                    embed = discord.Embed(title="GAY", color=0xffffff)
                    embed.set_image(url="attachment://gay.png")
                    embed.set_footer(text=f'Requested by {ctx.author.display_name}',icon_url=ctx.author.avatar_url_as(format="png"))
                    await ctx.send(embed=embed, file=file)
                else:
                    await ctx.send('No gay :(')
                    await session.close()

    # Sends mission passed image over avatar 
    @commands.command()
    async def passed(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        await ctx.trigger_typing()
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://some-random-api.ml/canvas/passed?avatar={member.avatar_url_as(format="png")}') as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "passed.png")
                    embed = discord.Embed(title="MISSION PASSED", color=0xffffff)
                    embed.set_image(url="attachment://passed.png")
                    embed.set_footer(text=f'Requested by {ctx.author.display_name}',icon_url=ctx.author.avatar_url_as(format="png"))
                    await ctx.send(embed=embed, file=file)
                else:
                    await ctx.send('No mission passed :(')
                    await session.close()

    # Sends jail image over avatar 
    @commands.command()
    async def jail(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        await ctx.trigger_typing()
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://some-random-api.ml/canvas/jail?avatar={member.avatar_url_as(format="png")}') as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "jail.png")
                    embed = discord.Embed(title="JAIL", color=0xffffff)
                    embed.set_image(url="attachment://jail.png")
                    embed.set_footer(text=f'Requested by {ctx.author.display_name}',icon_url=ctx.author.avatar_url_as(format="png"))
                    await ctx.send(embed=embed, file=file)
                else:
                    await ctx.send('No jail passed :(')
                    await session.close()

    # Write a fake YouTube commant
    @commands.command()
    async def youtube(self, ctx, *, text=None):
        if text is None:
            return await ctx.send(":no_entry: Please provide text")
        await ctx.trigger_typing()
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://some-random-api.ml/canvas/youtube-comment?username={ctx.author.display_name}&comment={text}&avatar={ctx.author.avatar_url_as(format="png")}') as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "youtube.png")
                    embed = discord.Embed(title="LOOK AT THIS", color=0xffffff)
                    embed.set_image(url="attachment://youtube.png")
                    embed.set_footer(text=f'Requested by {ctx.author.display_name}',icon_url=ctx.author.avatar_url_as(format="png"))
                    await ctx.send(embed=embed, file=file)
                else:
                    await ctx.send('No youtube :(')
                    await session.close()

    # Write a fake tweet
    @commands.command()
    async def tweet(self, ctx, *, text=None):
        if text is None:
            return await ctx.send(":no_entry: Please provide text")
        await ctx.trigger_typing()
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://some-random-api.ml/canvas/tweet?displayname={ctx.author.display_name}&username={ctx.author.display_name}&comment={text}&avatar={ctx.author.avatar_url_as(format="png")}') as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "tweet.png")
                    embed = discord.Embed(title="LOOK AT THIS", color=0xffffff)
                    embed.set_image(url="attachment://tweet.png")
                    embed.set_footer(text=f'Requested by {ctx.author.display_name}',icon_url=ctx.author.avatar_url_as(format="png"))
                    await ctx.send(embed=embed, file=file)
                else:
                    await ctx.send('No tweet :(')
                    await session.close()

    # On member join example
    @commands.command()
    @commands.is_owner()
    async def join_example(self, ctx):
        load_dotenv()
        key = os.getenv('API_KEY')
        await ctx.trigger_typing()
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://some-random-api.ml/welcome/img/2/stars2?type=join&username={ctx.author.display_name}&discriminator={ctx.author.discriminator}&guildName={ctx.guild.name}&memberCount={ctx.guild.member_count}&avatar={ctx.author.avatar_url_as(format="png")}&textcolor=white&key={key}') as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "welcome.png")
                    embed = discord.Embed(title="WELCOME EXAMPLE", color=0xffffff)
                    embed.set_image(url="attachment://welcome.png")
                    embed.set_footer(text=f'Requested by {ctx.author.display_name}',icon_url=ctx.author.avatar_url_as(format="png"))
                    await ctx.send(embed=embed, file=file)
                else:
                    await ctx.send('No welcome card :(')
                    await session.close()

    # Sends simpcard image over avatar 
    @commands.command()
    async def simp(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        await ctx.trigger_typing()
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://some-random-api.ml/canvas/simpcard?avatar={member.avatar_url_as(format="png")}') as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "simp.png")
                    embed = discord.Embed(title="SIMP", color=0xffffff)
                    embed.set_image(url="attachment://simp.png")
                    embed.set_footer(text=f'Requested by {ctx.author.display_name}',icon_url=ctx.author.avatar_url_as(format="png"))
                    await ctx.send(embed=embed, file=file)
                else:
                    await ctx.send('Out of simp cards :(')
                    await session.close()

    # Sends amongus gif over avatar 
    @commands.command()
    async def amongus(self, ctx, member: discord.Member = None):
        load_dotenv()
        key = os.getenv('API_KEY')
        member = member or ctx.author
        await ctx.trigger_typing()
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://some-random-api.ml/premium/amongus?avatar={member.avatar_url_as(format="png")}&username={member.name}&key={key}') as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "sus.gif")
                    embed = discord.Embed(title="AMONG US", color=0xffffff)
                    embed.set_image(url="attachment://sus.gif")
                    embed.set_footer(text=f'Requested by {ctx.author.display_name}',icon_url=ctx.author.avatar_url_as(format="png"))
                    await ctx.send(embed=embed, file=file)
                else:
                    await ctx.send('No imposter found :(')
                    await session.close()

    # Sends pet pet gif over avatar 
    @commands.command()
    async def petpet(self, ctx, member: discord.Member = None):
        load_dotenv()
        key = os.getenv('API_KEY')
        member = member or ctx.author
        await ctx.trigger_typing()
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://some-random-api.ml/premium/petpet?avatar={member.avatar_url_as(format="png")}&key={key}') as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "pet.gif")
                    embed = discord.Embed(title="PET PET", color=0xffffff)
                    embed.set_image(url="attachment://pet.gif")
                    embed.set_footer(text=f'Requested by {ctx.author.display_name}',icon_url=ctx.author.avatar_url_as(format="png"))
                    await ctx.send(embed=embed, file=file)
                else:
                    await ctx.send('No pet :(')
                    await session.close()

    # Chatbox doesn't work
    @commands.command()
    @commands.is_owner()
    async def chatbox(self, ctx, *, text = None):
        if text is None:
            return
        load_dotenv()
        key = os.getenv('API_KEY')

        response = requests.get(f'https://some-random-api.ml/chatbot?message={text}&key={key}')
        data = response.json()

        embed = discord.Embed(title="Chatbox", color=0xffffff)
        embed.add_field(name=f"Response", value=f'{data["chatbox"]}', inline=True)
        embed.set_image(url=data['link'])
        embed.set_footer(text=f'Requested by {ctx.author.display_name}',icon_url=ctx.author.avatar_url_as(format="png"))
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Fun(bot))