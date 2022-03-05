import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Ping slash command
    @cog_ext.cog_slash(name="Ping", description="My latency")
    async def _Ping(self, ctx: SlashContext):
        embed = discord.Embed(title=f"pong! {round(self.bot.latency*1000)}ms", colour = discord.Color.dark_purple())
        await ctx.send(embeds=[embed])

def setup(bot):
    bot.add_cog(Slash(bot))