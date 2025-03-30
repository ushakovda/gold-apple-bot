import aiosqlite
from db.db import DB_PATH

# Возвращает список всех товаров
async def get_all_tracked_products():
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("""
            SELECT p.id, p.name, p.brand, p.price, p.url
            FROM products p
        """)
        return await cursor.fetchall()

# Обновляет стоимость товаров если она изменилась
async def update_product_price(product_id: int, new_price: float):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            UPDATE products SET price = ? WHERE id = ?
        """, (new_price, product_id))
        await db.commit()

# Возвращает юзера по товару
async def get_user_by_product(product_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("""
            SELECT u.tg_id FROM users u
            JOIN user_products up ON u.id = up.user_id
            WHERE up.product_id = ?
        """, (product_id,))
        return await cursor.fetchone()

async def increase_all_prices_by(amount: float = 100.0):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            UPDATE products SET price = price + ?
        """, (amount,))
        await db.commit()
