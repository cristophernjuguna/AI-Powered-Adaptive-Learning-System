import asyncio
import asyncpg
import os
from typing import Optional
from asyncpg.pool import Pool
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


class DB:
    def __init__(self):
        self.pool: Optional[Pool] = None

    async def connect(self) -> None:
        while True:
            try:
                self.pool = await asyncpg.create_pool(
                    DATABASE_URL,
                    min_size=int(os.getenv("DB_POOL_MIN_SIZE", 1)),
                    max_size=int(os.getenv("DB_POOL_MAX_SIZE", 2)),
                    command_timeout=60,
                )
                print("Connected to Aiven PostgreSQL")
                return
            except Exception as e:
                print(f"Failed to connect to DB: {e}; retrying in 5s...")
                await asyncio.sleep(5)

    async def disconnect(self) -> None:
        if self.pool:
            await self.pool.close()

    async def execute(self, query: str, *args):
        async with self.pool.acquire() as conn:
            return await conn.execute(query, *args)

    async def fetchone(self, query: str, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, *args)

    async def fetchall(self, query: str, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *args)