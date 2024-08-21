import asyncpg
from typing import Optional

class Database:
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(self.database_url)

    async def close(self):
        await self.pool.close()

    async def execute(self, query: str, *args) -> None:
        async with self.pool.acquire() as connection:
            await connection.execute(query, *args)

    async def fetch(self, query: str, *args) -> Optional[list]:
        async with self.pool.acquire() as connection:
            return await connection.fetch(query, *args)

    # Пример метода для создания таблицы
    async def create_table(self):
        await self.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                tgID INTEGER,
                username VARCHAR,
                who VARCHAR,
                active_orders INTEGER[],
                in_dialog INTEGER
            )
        ''')

    # Пример метода для добавления пользователя
    async def add_user(self, user_id: int, username: str, full_name: str):
        await self.execute('''
            INSERT INTO users (tgID, username, full_name) 
            VALUES ($1, $2, $3) 
            ON CONFLICT (user_id) DO NOTHING
        ''', user_id, username, full_name)

    # Пример метода для получения пользователя
    async def get_user(self, user_id: int):
        return await self.fetch('SELECT * FROM users WHERE user_id = $1', user_id)