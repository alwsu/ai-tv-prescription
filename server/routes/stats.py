"""
@ai-generated true 2026-06-18
文件名: routes/stats.py
作用: 用户统计数据
"""
from collections import Counter
from fastapi import APIRouter

from database import db_cursor
from models import StatsResponse

router = APIRouter(prefix="/api/stats", tags=["stats"])


# @ai-generated true 2026-06-18
@router.get("", response_model=StatsResponse)
def get_stats() -> StatsResponse:
    """统计：总处方数、已看数、完看率、最爱类型"""
    with db_cursor() as cur:
        cur.execute("SELECT COUNT(*) AS c FROM prescriptions")
        total = cur.fetchone()["c"]

        cur.execute("SELECT COUNT(*) AS c FROM prescriptions WHERE is_watched = 1")
        watched = cur.fetchone()["c"]

        cur.execute("SELECT movie_genre FROM prescriptions WHERE is_watched = 1")
        rows = cur.fetchall()

    rate = int(watched * 100 / total) if total > 0 else 0

    # 取最高频类型（拆分 "韩剧/悬疑" -> 韩剧、悬疑）
    counter: Counter = Counter()
    for r in rows:
        for tag in r["movie_genre"].replace("/", " ").split():
            counter[tag] += 1
    favorite = counter.most_common(1)[0][0] if counter else "暂无"

    return StatsResponse(
        total_prescriptions=total,
        watched_count=watched,
        watch_rate=rate,
        favorite_genre=favorite,
    )
