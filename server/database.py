"""
@ai-generated true 2026-06-18
文件名: database.py
作用: SQLite 数据库连接、建表、初始化预置数据
说明: 使用原生 sqlite3，不引入 ORM，保持轻量可控
"""
import sqlite3
import os
import json
from contextlib import contextmanager
from typing import Generator

# @ai-generated true 2026-06-18
# 数据库文件路径，与本文件同目录下
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rx_drama.db")


# @ai-generated true 2026-06-18
def get_connection() -> sqlite3.Connection:
    """获取一个新的数据库连接（启用 Row 工厂以便按字段名取值）"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# @ai-generated true 2026-06-18
@contextmanager
def db_cursor() -> Generator[sqlite3.Cursor, None, None]:
    """上下文管理器，自动提交或回滚"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        yield cursor
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


# @ai-generated true 2026-06-18
def init_database() -> None:
    """初始化数据库结构与预置数据，幂等执行"""
    with db_cursor() as cur:
        # 影片表（预置数据）
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS movies (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                duration INTEGER NOT NULL,
                genre TEXT NOT NULL,
                mood_tags TEXT NOT NULL,
                reason TEXT NOT NULL,
                platform TEXT NOT NULL,
                rating REAL NOT NULL,
                gradient_start TEXT NOT NULL,
                gradient_end TEXT NOT NULL,
                year INTEGER DEFAULT 2020,
                summary TEXT DEFAULT ''
            )
            """
        )

        # 处方记录表
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS prescriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mood_id TEXT NOT NULL,
                mood_label TEXT NOT NULL,
                time_minutes INTEGER NOT NULL,
                movie_id TEXT NOT NULL,
                movie_title TEXT NOT NULL,
                movie_genre TEXT NOT NULL,
                movie_duration INTEGER NOT NULL,
                movie_reason TEXT NOT NULL,
                match_score INTEGER NOT NULL,
                is_watched INTEGER DEFAULT 0,
                gradient_start TEXT DEFAULT '#4a7c59',
                gradient_end TEXT DEFAULT '#8fbc8f',
                platform TEXT DEFAULT 'B站',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        # @ai-generated true 2026-06-18
        # 已存在表的兼容迁移：补 platform 列
        cur.execute("PRAGMA table_info(prescriptions)")
        cols = [row["name"] for row in cur.fetchall()]
        if "platform" not in cols:
            cur.execute(
                "ALTER TABLE prescriptions ADD COLUMN platform TEXT DEFAULT 'B站'"
            )

        # 用户偏好表（单用户 Demo 模式，固定 id=1）
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS user_preferences (
                id INTEGER PRIMARY KEY,
                liked_genres TEXT DEFAULT '[]',
                disliked_genres TEXT DEFAULT '[]',
                dark_mode INTEGER DEFAULT 1,
                notifications INTEGER DEFAULT 1,
                daily_remind_time TEXT DEFAULT '21:00'
            )
            """
        )

        # 默认偏好行
        cur.execute("SELECT id FROM user_preferences WHERE id = 1")
        if cur.fetchone() is None:
            cur.execute(
                """
                INSERT INTO user_preferences (id, liked_genres, disliked_genres, dark_mode, notifications, daily_remind_time)
                VALUES (1, ?, ?, 1, 1, '21:00')
                """,
                (json.dumps(["悬疑推理", "韩剧", "日剧"], ensure_ascii=False),
                 json.dumps(["恐怖"], ensure_ascii=False)),
            )

    # 影片种子数据导入
    _seed_movies_if_empty()


# @ai-generated true 2026-06-18
def _seed_movies_if_empty() -> None:
    """若 movies 表为空则导入种子数据"""
    from data.seed_data import MOVIES_SEED

    with db_cursor() as cur:
        cur.execute("SELECT COUNT(*) AS c FROM movies")
        count = cur.fetchone()["c"]
        if count > 0:
            return

        cur.executemany(
            """
            INSERT INTO movies (
                id, title, duration, genre, mood_tags, reason,
                platform, rating, gradient_start, gradient_end, year, summary
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    m["id"],
                    m["title"],
                    m["duration"],
                    m["genre"],
                    json.dumps(m["mood_tags"], ensure_ascii=False),
                    m["reason"],
                    m["platform"],
                    m["rating"],
                    m["gradient_start"],
                    m["gradient_end"],
                    m.get("year", 2020),
                    m.get("summary", ""),
                )
                for m in MOVIES_SEED
            ],
        )
