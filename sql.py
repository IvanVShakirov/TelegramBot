import asyncio
import asyncpg
import logging

from config import DB_HOST, DB_PASSWORD, DB_USER, DB_PORT, DB_NAME


async def create_pool():
    return await asyncpg.create_pool(user=DB_USER,
                                     password=DB_PASSWORD,
                                     host=DB_HOST,
                                     database=DB_NAME
                                     )
