import asyncio
import asyncpg
import logging

from config import DB_HOST, DB_PASSWORD, DB_USER, DB_PORT, DB_NAME

async def create_db():
    create_db_command = open("create_db.sql", "r").read()
    conn: asyncpg.Connection = await asyncpg.connect(user=DB_USER,
                                                     password=DB_PASSWORD,
                                                     host=DB_HOST)
    await conn.execute(create_db_command)
    await conn.close()

async def create_pool():
    return await asyncpg.create_pool(user=DB_USER,
                                     password=DB_PASSWORD,
                                     host=DB_HOST,
                                     # database=DB_NAME
                                     )

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_db())