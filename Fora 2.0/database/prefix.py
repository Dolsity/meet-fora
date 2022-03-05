from discord.ext import commands

# Defualt Prefix
default_prefix = '.'

# Prefix setup #
async def get_prefix(bot, message):
        if not message.guild:
            return commands.when_mentioned_or(default_prefix)(bot, message)

        prefix = await bot.db.fetch('SELECT prefix FROM prefixes WHERE "guild_id" = $1', message.guild.id)
        if len(prefix) == 0:
            await bot.db.execute('INSERT INTO prefixes("guild_id", prefix) VALUES ($1, $2)',message.guild.id, default_prefix)
            prefix = default_prefix
        else:
            prefix = prefix[0].get("prefix")
        return commands.when_mentioned_or(prefix)(bot,message)
