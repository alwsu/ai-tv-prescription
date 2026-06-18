"""
@ai-generated true 2026-06-18
文件名: routes/recommend.py
作用: 心情推荐核心算法
增强:
  - 合入用户偏好：disliked_genres 排除 + liked_genres 加分
  - 支持 mood_b 双人模式：两人心情交集优先，无交集时合并打分
"""
import json
import random
from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from database import db_cursor
from models import RecommendResponse, MovieDTO
from data.seed_data import MOOD_LABELS

router = APIRouter(prefix="/api", tags=["recommend"])


# @ai-generated true 2026-06-18
class RecommendRequestEx(BaseModel):
    """心情推荐请求（支持双人模式）"""
    mood: str = Field(..., description="主心情")
    mood_b: Optional[str] = Field(None, description="第二人心情（双人模式）")
    time_minutes: int = Field(..., ge=10, le=400)
    excluded_ids: Optional[List[str]] = Field(default_factory=list)


# @ai-generated true 2026-06-18
def _row_to_movie(row) -> MovieDTO:
    return MovieDTO(
        id=row["id"],
        title=row["title"],
        duration=row["duration"],
        genre=row["genre"],
        mood_tags=json.loads(row["mood_tags"]),
        reason=row["reason"],
        platform=row["platform"],
        rating=row["rating"],
        gradient_start=row["gradient_start"],
        gradient_end=row["gradient_end"],
        year=row["year"],
        summary=row["summary"],
    )


# @ai-generated true 2026-06-18
def _load_preferences() -> tuple:
    """加载用户喜欢/不喜欢的类型"""
    try:
        with db_cursor() as cur:
            cur.execute("SELECT liked_genres, disliked_genres FROM user_preferences WHERE id = 1")
            row = cur.fetchone()
        if not row:
            return [], []
        return (
            json.loads(row["liked_genres"] or "[]"),
            json.loads(row["disliked_genres"] or "[]"),
        )
    except Exception:
        return [], []


# @ai-generated true 2026-06-18
def _genre_overlap(movie_genre: str, target_genres: List[str]) -> int:
    """统计影片 genre 字段与目标类型列表的命中次数"""
    if not target_genres:
        return 0
    parts = set()
    for token in movie_genre.replace("/", " ").split():
        parts.add(token.strip())
    return sum(1 for g in target_genres if any(g in p or p in g for p in parts))


# @ai-generated true 2026-06-18
def _calc_match_score(
    movie_duration: int,
    target_minutes: int,
    mood_hit: bool,
    liked_hits: int,
    is_duo_intersect: bool,
) -> int:
    """
    计算匹配度评分（0-98）
    - 心情命中：+50；双人交集：+10
    - 时长契合度：最高 +30
    - 喜欢类型加分：每命中 +5（最多 +15）
    """
    base = 50 if mood_hit else 25
    if is_duo_intersect:
        base += 10

    delta = abs(movie_duration - target_minutes)
    if delta <= 5:
        time_score = 30
    elif delta <= 15:
        time_score = 24
    elif delta <= 30:
        time_score = 16
    elif delta <= 60:
        time_score = 8
    else:
        time_score = 3

    pref_score = min(15, liked_hits * 5)
    return min(98, base + time_score + pref_score)


# @ai-generated true 2026-06-18
@router.post("/recommend", response_model=RecommendResponse)
def recommend(req: RecommendRequestEx) -> RecommendResponse:
    """
    心情推荐主接口（增强版）
    单人：mood 命中过滤；双人：mood + mood_b 求交集优先
    """
    if req.mood not in MOOD_LABELS:
        raise HTTPException(status_code=400, detail=f"未知心情标识: {req.mood}")
    if req.mood_b and req.mood_b not in MOOD_LABELS:
        raise HTTPException(status_code=400, detail=f"未知心情标识: {req.mood_b}")

    excluded = set(req.excluded_ids or [])
    liked, disliked = _load_preferences()

    with db_cursor() as cur:
        cur.execute("SELECT * FROM movies")
        rows = cur.fetchall()

    if not rows:
        raise HTTPException(status_code=500, detail="影片库为空")

    # @ai-generated true 2026-06-18
    # 第一轮过滤：排除已看 + 不喜欢的类型
    filtered = []
    for row in rows:
        if row["id"] in excluded:
            continue
        # 不喜欢类型完全排除（命中即过滤）
        if disliked and _genre_overlap(row["genre"], disliked) > 0:
            continue
        filtered.append(row)

    if not filtered:
        # 兜底：如果偏好太严格全过滤了，放开 disliked 限制
        filtered = [r for r in rows if r["id"] not in excluded]
    if not filtered:
        raise HTTPException(status_code=404, detail="没有更多可推荐的影片")

    # @ai-generated true 2026-06-18
    # 第二轮分池：心情命中池 / 双人交集池 / 未命中池
    intersect_pool = []
    hit_pool = []
    miss_pool = []
    for row in filtered:
        tags = json.loads(row["mood_tags"])
        if req.mood_b and req.mood in tags and req.mood_b in tags:
            intersect_pool.append(row)
        elif req.mood in tags or (req.mood_b and req.mood_b in tags):
            hit_pool.append(row)
        else:
            miss_pool.append(row)

    is_duo = bool(req.mood_b)
    candidates = intersect_pool or hit_pool or miss_pool
    if not candidates:
        raise HTTPException(status_code=404, detail="没有更多可推荐的影片")

    # @ai-generated true 2026-06-18
    # 综合排序：时长契合度 + 偏好加分（评分高的先）
    def sort_key(r):
        time_delta = abs(r["duration"] - req.time_minutes)
        liked_bonus = -_genre_overlap(r["genre"], liked) * 10
        return (time_delta + liked_bonus, -r["rating"])

    candidates.sort(key=sort_key)
    top_n = candidates[: min(5, len(candidates))]
    chosen = random.choice(top_n)

    movie = _row_to_movie(chosen)
    mood_hit = (req.mood in movie.mood_tags) or (
        req.mood_b is not None and req.mood_b in movie.mood_tags
    )
    liked_hits = _genre_overlap(movie.genre, liked)
    is_intersect = is_duo and chosen in intersect_pool

    score = _calc_match_score(
        movie.duration, req.time_minutes,
        mood_hit=mood_hit,
        liked_hits=liked_hits,
        is_duo_intersect=is_intersect,
    )

    # 双人模式标签拼接
    if is_duo:
        mood_label = f"{MOOD_LABELS[req.mood]} & {MOOD_LABELS[req.mood_b]}"
    else:
        mood_label = MOOD_LABELS[req.mood]

    return RecommendResponse(
        movie=movie,
        match_score=score,
        reason=movie.reason,
        mood_label=mood_label,
    )
