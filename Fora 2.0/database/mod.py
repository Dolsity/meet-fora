from asyncpg import Pool
from discord.ext import commands

async def create_tables(pool: Pool):
    async with pool.acquire() as connection:
        # await connection.execute("DROP TABLE IF EXISTS moderation") # Uncomment this line if you have the database already created and have old data

        await connection.execute(
            """
            CREATE TABLE IF NOT EXISTS moderation(
                id BIGSERIAL PRIMARY KEY NOT NULL,
                user_id BIGINT NOT NULL,
                author_id BIGINT NOT NULL,
                guild_id BIGINT NOT NULL,
                what_reason CHARACTER VARYING NOT NULL,
                date_time CHARACTER VARYING NOT NULL,
                punishment_type CHARACTER VARYING NOT NULL
            )
        """
        )

async def create_user_moderation(pool: Pool, guild_id, user_id, author_id, what_reason, date_time, punishment_type):
    async with pool.acquire() as connection:
        record = await connection.fetchrow(
            "SELECT * FROM moderation WHERE guild_id=$1 AND user_id=$2 AND author_id=$3 AND what_reason=$4 AND date_time=$5 AND punishment_type=$6", guild_id, user_id, author_id, what_reason, date_time, punishment_type
        )
        if record:
            return

        await connection.execute(
            "INSERT INTO moderation(guild_id, user_id, author_id, what_reason, date_time, punishment_type) VALUES($1, $2, $3, $4, $5, $6)", guild_id, user_id, author_id, what_reason, date_time, punishment_type
        )


async def get_user_data_moderation(pool: Pool, guild_id, user_id, author_id, what_reason, date_time, punishment_type):

    async with pool.acquire() as connection:
        record = await connection.fetchrow(
            "SELECT * FROM moderation WHERE guild_id=$1 AND user_id=$2 AND author_id=$3 AND what_reason=$4 AND date_time=$5, AND punishment_type=$6", guild_id, user_id, author_id, what_reason, date_time, punishment_type
        )
        return dict(record)