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