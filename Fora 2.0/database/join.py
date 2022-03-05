from asyncpg import Pool
from discord.ext import commands

async def create_tables(pool: Pool):
    async with pool.acquire() as connection:
        # await connection.execute("DROP TABLE IF EXISTS join") # Uncomment this line if you have the database already created and have old data

        await connection.execute(
            """
            CREATE TABLE IF NOT EXISTS join_server(
                id BIGSERIAL PRIMARY KEY NOT NULL,
                guild_id BIGINT NOT NULL,
                channel_id BIGINT NOT NULL
            )
        """
        )

async def create_join_channel(pool: Pool, guild_id, channel_id):
    async with pool.acquire() as connection:
        record = await connection.fetchrow(
            "SELECT * FROM join_server WHERE guild_id=$1 AND channel_id=$2", guild_id, channel_id
        )
        if record:
            return

        await connection.execute(
            "INSERT INTO join_server(guild_id, channel_id) VALUES($1, $2)", guild_id, channel_id
        )

# PULLS USER DATA (RECENT URL)
async def get_guild_data(pool: Pool, guild_id, channel_id):
    await create_join_channel(pool, guild_id, channel_id)

    async with pool.acquire() as connection:
        record = await connection.fetchrow(
            "SELECT * FROM join_server WHERE guild_id=$1 AND channel_id=$2", guild_id, channel_id
        )
        return dict(record)