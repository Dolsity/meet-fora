from discord.ext import commands
import asyncio
from database.mod import *

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # Get a list of banned members in your guild
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def banlist(self, ctx):
        async with ctx.typing():
            await asyncio.sleep(1)
            bans = await ctx.guild.bans()
            loop = [f"{u[1]} ({u[1].id})" for u in bans]
            _list = "\r\n".join([f"[{str(num).zfill(2)}] {data}" for num, data in enumerate(loop, start=1)])
            await ctx.send(f"```ini\n{_list}```")

def setup(bot):
    bot.add_cog(Moderation(bot))