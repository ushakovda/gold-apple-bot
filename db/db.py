import aiosqlite

DB_PATH = "sqlite.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price REAL,
            brand TEXT,
            description TEXT,
            url TEXT UNIQUE
        )
        """)
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tg_id INTEGER NOT NULL UNIQUE, 
            tg_username TEXT NOT NULL,
            created_at TEXT NOT NULL
                )
                """)
        await db.commit()



# async def add_product(data: dict):
#     async with aiosqlite.connect(DB_PATH) as db:
#         await db.execute("""
#             INSERT OR IGNORE INTO products (name, price, brand, description, url)
#             VALUES (?, ?, ?, ?, ?)
#         """, (
#             data.get("name"),
#             float(data.get("price")) if data.get("price") else None,
#             data.get("brand"),
#             data.get("description"),
#             data.get("url"),
#         ))
#         await db.commit()
#
# async def get_all_products():
#     async with aiosqlite.connect(DB_PATH) as db:
#         cursor = await db.execute("SELECT * FROM products")
#         rows = await cursor.fetchall()
#         return rows
