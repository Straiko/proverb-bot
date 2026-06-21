import json
import aiosqlite
from pathlib import Path
from typing import Optional


class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path

    async def init(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            await db.execute("""
                CREATE TABLE IF NOT EXISTS favorites (
                    user_id INTEGER,
                    proverb_id INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (user_id, proverb_id),
                    FOREIGN KEY (proverb_id) REFERENCES proverbs(id)
                )
            """)
            await db.execute("""
                CREATE TABLE IF NOT EXISTS daily_history (
                    date TEXT PRIMARY KEY,
                    proverb_id INTEGER
                )
            """)
            await db.commit()

    async def add_user(self, user_id: int, username: Optional[str] = None):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)",
                (user_id, username)
            )
            await db.commit()

    async def add_favorite(self, user_id: int, proverb_id: int):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT OR IGNORE INTO favorites (user_id, proverb_id) VALUES (?, ?)",
                (user_id, proverb_id)
            )
            await db.commit()

    async def remove_favorite(self, user_id: int, proverb_id: int):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "DELETE FROM favorites WHERE user_id = ? AND proverb_id = ?",
                (user_id, proverb_id)
            )
            await db.commit()

    async def get_favorites(self, user_id: int) -> list[dict]:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute("""
                SELECT p.id, p.text, p.category_id
                FROM favorites f
                JOIN proverbs p ON f.proverb_id = p.id
                WHERE f.user_id = ?
            """, (user_id,))
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

    async def is_favorite(self, user_id: int, proverb_id: int) -> bool:
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT 1 FROM favorites WHERE user_id = ? AND proverb_id = ?",
                (user_id, proverb_id)
            )
            return await cursor.fetchone() is not None

    async def set_daily_proverb(self, date: str, proverb_id: int):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT OR REPLACE INTO daily_history (date, proverb_id) VALUES (?, ?)",
                (date, proverb_id)
            )
            await db.commit()

    async def get_daily_proverb_id(self, date: str) -> Optional[int]:
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                "SELECT proverb_id FROM daily_history WHERE date = ?", (date,)
            )
            row = await cursor.fetchone()
            return row[0] if row else None
