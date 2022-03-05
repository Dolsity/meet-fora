from discord.ext import commands
import os
from dotenv import load_dotenv
from database.join import *
from discord_components import *
import asyncio
from datetime import datetime
import discord

load_dotenv()
password = os.getenv('PASSWORD')
user = "Jay"

# Buttons for bot command
set = [
[
    Button(style=ButtonStyle.green, label='Online'),
    Button(style=ButtonStyle.grey, label='Idle'),
    Button(style=ButtonStyle.red, label='DO not disturb'),
    Button(style=ButtonStyle.grey, label='Invisible')
],

[
    Button(style=ButtonStyle.blue, label='Clear'),
    Button(style=ButtonStyle.red, label='Not now')
],
]

set1 = [
[
    Button(style=ButtonStyle.green, label='Online', disabled=True),
    Button(style=ButtonStyle.grey, label='Idle', disabled=True),
    Button(style=ButtonStyle.red, label='DO not disturb', disabled=True),
    Button(style=ButtonStyle.grey, label='Invisible')
],

[
    Button(style=ButtonStyle.blue, label='Clear'),
    Button(style=ButtonStyle.red, label='Not now')
],
]

set2 = [
[
    Button(style=ButtonStyle.green, label='Online', disabled=True),
    Button(style=ButtonStyle.grey, label='Idle', disabled=True),
    Button(style=ButtonStyle.red, label='DO not disturb', disabled=True),
    Button(style=ButtonStyle.grey, label='Invisible', disabled=True)
],

[
    Button(style=ButtonStyle.blue, label='Clear', disabled=True),
    Button(style=ButtonStyle.red, label='Not now', disabled=True)
],
]

class Developer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Shutdown the bot -- needs connected to database to store reason --
    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx, reason=None):
        if reason is None:
            return await ctx.send(":no_entry: Please provide a reason")

        await ctx.send(f'Shutting down, I will miss you {ctx.author.mention}')
        await self.bot.logout()
        await self.bot.close()
    
    # Disable any command -- needs connected to database to keep commands off --
    @commands.command()
    @commands.is_owner()
    async def toggle(self, ctx, *, command):
        command = self.bot.get_command(command)
        if command == None:
            await ctx.send(":no_entry: Couldn't find that command!")
        elif ctx.command == command:
            await ctx.send(":no_entry: You can't disable this command!")
        else:
            command.enabled = not command.enabled
            turnary = "enabled" if command.enabled else "disabled"
            await ctx.send(f"command **{command.qualified_name}** has been {turnary}")

    @commands.command()
    @commands.is_owner()
    async def bot(ctx, *, reason=None):
        m = await ctx.send(content='Loading Status.')

        expression = f'Activity is ***{reason}***. Please select a status option...'
        delta = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
        e = discord.Embed(title=f'{ctx.author.name}\'s Bot Controls | {ctx.author.id}', description=expression,
                            timestamp=delta)

        Embed1 = discord.Embed(title = f"__**BOT PANNEL CLOSED • {ctx.guild.name}**__", description = f"{ctx.author.mention} This interaction failed!", colour = discord.Color.red())
        
        Embed = discord.Embed(title = f"__**BOT CHANGED • {ctx.guild.name}**__", description = f"{ctx.author.mention} has changed the bots Activity/status!", colour = discord.Color.red())
        Embed.set_thumbnail(url = f"{ctx.author.avatar_url}")
        Embed.add_field(name = "***Member info:***", value = f'{ctx.author.mention} / ***{ctx.author.display_name}*** | ***ID:*** __{ctx.author.id}__', inline = False)
        Embed.add_field(name = "***Time:***", value = datetime.datetime.utcnow(), inline = False)
        Embed.add_field(name = "***Activity:***", value = reason, inline = False)
        await m.edit(components=set, embed=e)
        if reason is None:
            await m.edit(components=set1, embed=e)

        while m.created_at < delta:
                res = await client.wait_for('button_click')
                Embed.add_field(name = "***Option selected:***", value = f'{res.component.label}', inline = False)
                if res.author.id == int(res.message.embeds[0].title.split('|')[1]) and res.message.embeds[
                    0].timestamp < delta:
                    expression = res.message.embeds[0].description
                    if expression == 'None' or expression == 'An error occurred.':
                        expression = ''

                    if res.component.label == 'Not now':
                        await res.respond(content='Bot activity', type=7)
                        res = await m.edit(embed=Embed1, inline = False)
                        res = await m.edit(components=set2)
                        res = await asyncio.sleep(5)
                        res = await m.edit(content='***This message will delete in 5 seconds...***')
                        res = await asyncio.sleep(5)
                        res = await m.delete()
                        break

                    elif res.component.label == 'Clear':
                        expression = 'Clearing...'
                        res = await client.change_presence(status=discord.Status.online, activity = discord.Activity (type = discord.ActivityType.playing, name = f"Bot Status Cleared by {ctx.author.name}"))
                        res = await m.edit(embed=Embed)
                        res = await m.edit(components=set2)
                        res = await client.get_channel(922711948439724062).send(embed=Embed)
                        res = await asyncio.sleep(5)
                        res = await client.change_presence(status=discord.Status.online, activity = discord.Activity (type = discord.ActivityType.playing, name = f".help | Made by Dolsity"))
                        res = await m.edit(content='***This message will delete in 5 seconds...***')       
                        res = await asyncio.sleep(5)
                        res = await m.delete()
                        break

                    elif res.component.label == 'Online':
                        expression = 'Awake and Online'
                        res = await client.change_presence(status=discord.Status.online, activity = discord.Activity (type = discord.ActivityType.playing, name = f"{reason}"))
                        res = await m.edit(embed=Embed)
                        res = await m.edit(components=set2)
                        res = await client.get_channel(922711948439724062).send(embed=Embed)
                        res = await asyncio.sleep(5)
                        res = await m.edit(content='***This message will delete in 5 seconds...***')
                        res = await asyncio.sleep(5)
                        res = await m.delete()
                        break

                    elif res.component.label == 'Idle':
                        expression = 'Sleeping on Idle'
                        res = await client.change_presence(status=discord.Status.idle, activity = discord.Activity (type = discord.ActivityType.playing, name = f"{reason}"))
                        res = await m.edit(embed=Embed)
                        res = await m.edit(components=set2)
                        res = await client.get_channel(922711948439724062).send(embed=Embed)
                        res = await asyncio.sleep(5)
                        res = await m.edit(content='***This message will delete in 5 seconds...***')
                        res = await asyncio.sleep(5)
                        res = await m.delete()
                        break

                    elif res.component.label == 'DO not disturb':
                        expression = 'DO not disturb'
                        res = await client.change_presence(status=discord.Status.dnd, activity = discord.Activity (type = discord.ActivityType.playing, name = f"{reason}"))
                        res = await m.edit(embed=Embed)
                        res = await m.edit(components=set2)
                        res = await client.get_channel(922711948439724062).send(embed=Embed)
                        res = await asyncio.sleep(5)
                        res = await m.edit(content='***This message will delete in 5 seconds...***')
                        res = await asyncio.sleep(5)
                        res = await m.delete()
                        break

                    elif res.component.label == 'Invisible':
                        expression = 'Going Invisible'
                        res = await client.change_presence(status=discord.Status.invisible)
                        res = await m.edit(embed=Embed)
                        res = await m.edit(components=set2)
                        res = await client.get_channel(922711948439724062).send(embed=Embed)
                        res = await asyncio.sleep(5)
                        res = await m.edit(content='***This message will delete in 5 seconds...***')
                        res = await asyncio.sleep(5)
                        res = await m.delete()
                        break

                    else:
                        expression += res.component.label
                    f = discord.Embed(title=f'{res.author.name}\'s Bot Controls |{res.author.id}', description=expression,
                                        timestamp=delta)
                    await res.respond(content='', embed=f, components=set, type=7)
                    await res.respond(content='', embed=f, components=set1, type=7)
                    await res.respond(content='', embed=f, components=set2, type=7)



def setup(bot):
    bot.add_cog(Developer(bot))
