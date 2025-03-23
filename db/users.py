from datetime import datetime
import aiosqlite
from db.db import DB_PATH


async def add_user(tg_id: str, tg_username: str):
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT OR IGNORE INTO users (tg_id, tg_username, created_at)
            VALUES (?, ?, ?)
        """, (tg_id, tg_username, created_at))
        await db.commit()


async def save_product_and_link_user(tg_id: int, product_data: dict, url: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
        INSERT OR IGNORE INTO products (name, price, brand, description, url)
        VALUES (?, ?, ?, ?, ?)
        """, (
            product_data.get("name"),
            product_data.get("price"),
            product_data.get("brand"),
            product_data.get("description"),
            url
        ))

        cursor = await db.execute("SELECT id FROM users WHERE tg_id = ?", (tg_id,))
        user_row = await cursor.fetchone()
        if not user_row:
            return  # или raise Exception("User not found")

        user_id = user_row[0]

        # 3. Получим id продукта
        cursor = await db.execute("SELECT id FROM products WHERE url = ?", (url,))
        product_row = await cursor.fetchone()
        if not product_row:
            return  # или raise Exception("Product not found")

        product_id = product_row[0]

        # 4. Добавим в таблицу связей
        await db.execute("""
        INSERT OR IGNORE INTO user_products (user_id, product_id)
        VALUES (?, ?)
        """, (user_id, product_id))

        await db.commit()
