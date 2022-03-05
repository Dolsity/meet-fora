from discord.ext import commands

class Error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Error Handlers
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await ctx.send(f":no_entry: {error}")

        # Unknown command
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(':no_entry: Invalid Command!')

        # Bot does not have permission
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(':no_entry: Bot Permission Missing!')

def setup(bot):
    bot.add_cog(Error(bot))
