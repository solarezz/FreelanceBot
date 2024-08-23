import aiosqlite


class Database:

    def __init__(self, db_name='./database.db'):
        self.db_name = db_name

    async def add_user(self, tgID: int, username: str, who: str):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute('INSERT OR IGNORE INTO users (tgID, username, who) VALUES (?, ?, ?)',
                             (tgID,
                              username,
                              who))
            await db.commit()

    async def info(self, tgID: int):
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute('SELECT * FROM users WHERE tgID = ?', (tgID,)) as cur:
                info = await cur.fetchall()
                return info

    async def orders(self):
        async with aiosqlite.connect('database.db') as db:
            async with db.execute("SELECT id FROM orders WHERE status = 'Ожидание'") as cur:
                orders = await cur.fetchall()
                return orders

    async def status(self, order_id):
        async with aiosqlite.connect('database.db') as db:
            cursor = await db.execute("SELECT status FROM orders WHERE id = ?", (order_id,))
            status = await cursor.fetchone()
            return status

    async def participants(self, order_id):
        async with aiosqlite.connect('database.db') as db:
            cursor = await db.execute("SELECT customer, executor FROM orders WHERE id = ?", (order_id,))
            participants = await cursor.fetchone()
            return participants

    async def change(self, order_id):
        async with aiosqlite.connect('database.db') as db:
            await db.execute("UPDATE orders SET status = 'Начат', dialog_start = 'on' WHERE id = ?",
                             (order_id,))
            await db.commit()
