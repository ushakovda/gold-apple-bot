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
        INSERT OR IGNORE INTO products (name, brand, price, url)
        VALUES (?, ?, ?, ?)
        """, (
            product_data.get("name"),
            product_data.get("brand"),
            product_data.get("price"),
            url
        ))

        cursor = await db.execute("SELECT id FROM users WHERE tg_id = ?", (tg_id,))
        user_row = await cursor.fetchone()
        if not user_row:
            return
        user_id = user_row[0]

        cursor = await db.execute("SELECT id FROM products WHERE url = ?", (url,))
        product_row = await cursor.fetchone()
        if not product_row:
            return
        product_id = product_row[0]

        await db.execute("""
        INSERT OR IGNORE INTO user_products (user_id, product_id)
        VALUES (?, ?)
        """, (user_id, product_id))
        await db.commit()

async def get_wish_list(tg_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("""
            SELECT p.id, p.name, p.brand, p.price 
            FROM products p
            JOIN user_products up ON up.product_id = p.id
            JOIN users u ON u.id = up.user_id
            WHERE u.tg_id = ?
        """, (tg_id,))
        return await cursor.fetchall()

async def delete_product_from_wishlist(tg_id: int, product_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            DELETE FROM user_products 
            WHERE user_id = (SELECT id FROM users WHERE tg_id = ?) AND product_id = ?
        """, (tg_id, product_id))
        await db.commit()
