from discord.ext import commands
import discord
import aiohttp
import io
import requests
from database.gta_db import *
import aiohttp
import asyncio

class GTA(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # API that gives you any weapon stats in GTA
    @commands.command()
    async def weapon(self, ctx, weapon = None):
        if weapon is None:
            return await ctx.send(f"{ctx.author.mention} Please provide a weapon")

        response = requests.get(f'https://socialclub.rockstargames.com/games/gtav/api/mp/gun/1/{weapon}')
        data = response.json()

        gun = data["itemData"]

        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://s.rsg.sc/sc/images/games/GTAV/weapons/314x120_colour/{gun["Image"]}') as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "gun.png")
                    embed = discord.Embed(title=f"GTA V", description = f"{weapon} stats", color=0xffffff)
                    embed.add_field(name=f"Damage Percent", value=f'{gun["damagePercent"]}', inline=True)
                    embed.add_field(name=f"Firerate Percent", value=f'{gun["fireratePercent"]}', inline=True)
                    embed.add_field(name=f"Accuracy Percent", value=f'{gun["accuracyPercent"]}', inline=True)
                    embed.add_field(name=f"Ammo Percent", value=f'{gun["ammoPercent"]}', inline=True)
                    embed.add_field(name=f"Range Percent", value=f'{gun["rangePercent"]}', inline=True)
                    embed.add_field(name=f"Type", value=f'{gun["type"]}', inline=True)
                    embed.add_field(name=f"Has Attachments", value=f'{gun["hasAttachments"]}', inline=True)
                    embed.add_field(name=f"Attachments Count", value=f'{gun["attachmentsCount"]}', inline=True)
                    embed.add_field(name=f"Mode", value=f'{gun["mode"]}', inline=True)
                    embed.add_field(name=f"Is Unlocked", value=f'{gun["IsUnlocked"]}', inline=True)
                    embed.add_field(name=f"Is Purchased", value=f'{gun["IsPurchased"]}', inline=True)
                    embed.set_thumbnail(url="https://s.rsg.sc/sc/images/react/feed/rockstar-avatar.png")
                    embed.set_image(url="attachment://gun.png")
                    embed.set_footer(text=f'Requested by {ctx.author.display_name}',icon_url=ctx.author.avatar_url_as(format="png"))
                    await ctx.send(embed=embed, file=file)
                else:
                    await ctx.send('Weapon not found :(')
                    await session.close()

    # Sends your GTA Online character mugshot
    @commands.command()
    async def mugshot(self, ctx, character = None):
        # Checks for recent data
        check_for_data = await self.bot.db.fetchrow("SELECT * FROM gta WHERE user_id=$1", ctx.author.id)

        # If data is not found
        if check_for_data is None:
            return await ctx.send(f"{ctx.author.mention} We couldn't find you in our database. Please type `.addme` to fix this issue")

        if character is None:
            character = 0

        # If data is found
        if check_for_data:
            gta_url = check_for_data["gta_url"]

            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://prod.cloud.rockstargames.com/members/np/0000/{gta_url}/publish/gta5/mpchars/{character}_ps4.png') as af:
                    if 300 > af.status >= 200:
                        fp = io.BytesIO(await af.read())
                        file = discord.File(fp, "gta.png")
                        embed = discord.Embed(title=f"GTA V ONLINE CHARACTER {character} MUGSHOT", color=0xffffff)
                        embed.set_image(url="attachment://gta.png")
                        embed.set_footer(text=f'Requested by {ctx.author.display_name}',icon_url=ctx.author.avatar_url_as(format="png"))
                        await ctx.send(embed=embed, file=file)
                    else:
                        await ctx.send("This account is private or you didn't type the correct username :(")
                        await session.close()   
        else:
            await ctx.send("Something went wrong :(")

    # Adds you to database -- this allows you to use the GTA commands
    @commands.command()
    async def addme(self, ctx, rockstar):
        if rockstar is None:
            return await ctx.send(f"{ctx.author.mention} Please provide your rockstar username")

        data = await self.bot.db.fetchrow("SELECT * FROM gta WHERE user_id=$1", ctx.author.id)

        if data is None:
            await create_user_gta(self.bot.db, ctx.author.id, rockstar)
            await ctx.send(f"{ctx.author.mention} Your rockstar username was updated in the database")
            return

        if data:
            await self.bot.db.execute('UPDATE gta SET gta_url = $1 WHERE user_id = $2', rockstar, ctx.author.id)
            await ctx.send(f"Character name has been updated to {rockstar}")

    # Checks to see if you're in the database -- this allows you to use the GTA commands
    @commands.command()
    async def check(self, ctx):
        check_for_data = await self.bot.db.fetchrow("SELECT * FROM gta WHERE user_id=$1", ctx.author.id)
        gta_url = check_for_data["gta_url"]

        if check_for_data is None:
            await ctx.send(f"{ctx.author.mention} Your rockstar username is not in database")
            return

        if check_for_data:
            await ctx.send(f"Character name is {gta_url}")
            return


def setup(bot):
    bot.add_cog(GTA(bot))
