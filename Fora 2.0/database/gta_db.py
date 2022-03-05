from asyncpg import Pool
from discord.ext import commands

async def create_tables(pool: Pool):
    async with pool.acquire() as connection:
        # await connection.execute("DROP TABLE IF EXISTS gta") # Uncomment this line if you have the database already created and have old data

        await connection.execute(
            """
            CREATE TABLE IF NOT EXISTS gta(
                id BIGSERIAL PRIMARY KEY NOT NULL,
                user_id BIGINT NOT NULL,
                gta_url CHARACTER VARYING NOT NULL
            )
        """
        )

# CREATES RECENTLY USED GTA URL
async def create_user_gta(pool: Pool, user_id, gta_url):
    async with pool.acquire() as connection:
        record = await connection.fetchrow(
            "SELECT * FROM gta WHERE user_id=$1 AND gta_url=$2", user_id, gta_url
        )
        if record:
            return

        await connection.execute(
            "INSERT INTO gta(user_id, gta_url) VALUES($1, $2)", user_id, gta_url
        )

# PULLS USER DATA (RECENT URL)
async def get_user_data_gta(pool: Pool, user_id, gta_url):
    await create_user_gta(pool, user_id, gta_url)

    async with pool.acquire() as connection:
        record = await connection.fetchrow(
            "SELECT * FROM gta WHERE user_id=$1 AND gta_url=$2", user_id, gta_url
        )
        return dict(record)
 ##