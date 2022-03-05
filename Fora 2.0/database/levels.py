from asyncpg import Pool
from discord.ext import commands

async def create_tables(pool: Pool):
    async with pool.acquire() as connection:
        # await connection.execute("DROP TABLE IF EXISTS leveling") # Uncomment this line if you have the database already created and have old data
        # await connection.execute("DROP TABLE IF EXISTS global") # Uncomment this line if you have the database already created and have old data

        await connection.execute(
            """
            CREATE TABLE IF NOT EXISTS leveling(
                id BIGSERIAL PRIMARY KEY NOT NULL,
                user_id BIGINT NOT NULL,
                guild_id BIGINT NOT NULL,
                xp BIGINT NOT NULL DEFAULT 5,
                level BIGINT NOT NULL DEFAULT 0
            )
        """
        )
        await connection.execute(
            """
            CREATE TABLE IF NOT EXISTS global(
                id BIGSERIAL PRIMARY KEY NOT NULL,
                user_id BIGINT NOT NULL,
                xp BIGINT NOT NULL DEFAULT 5,
                level BIGINT NOT NULL DEFAULT 0
            )
        """
        )

async def create_user_guild(pool: Pool, user_id, guild_id):
    async with pool.acquire() as connection:
        record = await connection.fetchrow(
            "SELECT * FROM leveling WHERE user_id=$1 AND guild_id=$2", user_id, guild_id
        )
        if record:
            return

        await connection.execute(
            "INSERT INTO leveling(user_id, guild_id) VALUES($1, $2)", user_id, guild_id
        )

async def increase_xp_guild(pool: Pool, message, rate=5):
    await create_user_guild(pool, message.author.id, message.guild.id)

    async with pool.acquire() as connection:
        record = await connection.fetchrow(
            "SELECT * FROM leveling WHERE user_id=$1 AND guild_id=$2", message.author.id, message.guild.id
        )
        xp = record["xp"]
        level = record["level"]
        new_level = int((xp + rate) / 100)

        if new_level > level:
            new_level = new_level
        else:
            new_level = level

        await connection.execute(
            "UPDATE leveling SET xp = $1, level = $2 WHERE user_id = $3 AND guild_id=$4",
            xp + rate,
            new_level,
            message.author.id,
            message.guild.id,
        )

async def get_user_data_guild(pool: Pool, user_id, guild_id):
    await create_user_guild(pool, user_id, guild_id)

    async with pool.acquire() as connection:
        record = await connection.fetchrow(
            "SELECT * FROM leveling WHERE user_id=$1 AND guild_id=$2", user_id, guild_id
        )
        return dict(record)

async def get_rank_guild(pool: Pool, user_id, guild_id):
    await create_user_guild(pool, user_id, guild_id)

    async with pool.acquire() as connection:
        records = await connection.fetch(
            "SELECT * FROM leveling WHERE guild_id=$1 ORDER BY xp DESC", guild_id
        )
        rank = 0
        for record in records:
            rank += 1
            if record["user_id"] == user_id:
                break

        return rank



# GLOBAL RANK FUNCTIONS -----------------------
async def create_user_global(pool: Pool, user_id):
    async with pool.acquire() as connection:
        record = await connection.fetchrow(
            "SELECT * FROM global WHERE user_id=$1", user_id
        )
        if record:
            return

        await connection.execute(
            "INSERT INTO global(user_id) VALUES($1)", user_id
        )

async def increase_xp_global(pool: Pool, message, rate=5):
    await create_user_global(pool, message.author.id)

    async with pool.acquire() as connection:
        record = await connection.fetchrow(
            "SELECT * FROM global WHERE user_id=$1", message.author.id
        )
        xp = record["xp"]
        level = record["level"]
        new_level = int((xp + rate) / 100)

        if new_level > level:
            new_level = new_level
        else:
            new_level = level

        await connection.execute(
            "UPDATE global SET xp = $1, level = $2 WHERE user_id = $3",
            xp + rate,
            new_level,
            message.author.id,
        )

async def get_user_data_global(pool: Pool, user_id):
    await create_user_global(pool, user_id)

    async with pool.acquire() as connection:
        record = await connection.fetchrow(
            "SELECT * FROM global WHERE user_id=$1", user_id
        )
        return dict(record)

async def get_rank_global(pool: Pool, user_id):
    await create_user_global(pool, user_id)

    async with pool.acquire() as connection:
        records = await connection.fetch(
            "SELECT * FROM global WHERE user_id=$1 ORDER BY xp DESC", user_id
        )
        rank = 0
        for record in records:
            rank += 1
            if record["user_id"] == user_id:
                break

        return rank