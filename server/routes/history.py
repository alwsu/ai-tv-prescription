"""
@ai-generated true 2026-06-18
文件名: routes/history.py
作用: 处方历史记录 CRUD - 支持分页
"""
from typing import List
from fastapi import APIRouter, HTTPException, Query

from database import db_cursor
from models import HistoryCreate, HistoryItem, WatchUpdate, CommonResponse

router = APIRouter(prefix="/api/history", tags=["history"])


# @ai-generated true 2026-06-18
@router.get("", response_model=List[HistoryItem])
def list_history(
    page: int = Query(1, ge=1, description="页码（从 1 开始）"),
    page_size: int = Query(20, ge=1, le=100, description="每页条数"),
) -> List[HistoryItem]:
    """获取处方记录列表，按时间倒序，支持分页"""
    offset = (page - 1) * page_size
    with db_cursor() as cur:
        cur.execute(
            "SELECT * FROM prescriptions ORDER BY id DESC LIMIT ? OFFSET ?",
            (page_size, offset),
        )
        rows = cur.fetchall()
    return [HistoryItem(**dict(r)) for r in rows]


# @ai-generated true 2026-06-18
@router.post("", response_model=HistoryItem)
def create_history(payload: HistoryCreate) -> HistoryItem:
    """新增一条处方记录"""
    with db_cursor() as cur:
        cur.execute(
            """
            INSERT INTO prescriptions (
                mood_id, mood_label, time_minutes, movie_id, movie_title,
                movie_genre, movie_duration, movie_reason, match_score,
                gradient_start, gradient_end, platform
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                payload.mood_id,
                payload.mood_label,
                payload.time_minutes,
                payload.movie_id,
                payload.movie_title,
                payload.movie_genre,
                payload.movie_duration,
                payload.movie_reason,
                payload.match_score,
                payload.gradient_start,
                payload.gradient_end,
                payload.platform,
            ),
        )
        new_id = cur.lastrowid
        cur.execute("SELECT * FROM prescriptions WHERE id = ?", (new_id,))
        row = cur.fetchone()
    return HistoryItem(**dict(row))


# @ai-generated true 2026-06-18
@router.put("/{record_id}", response_model=HistoryItem)
def replace_history(record_id: int, payload: HistoryCreate) -> HistoryItem:
    """替换已有历史记录（用于'换一个'更新最新记录的影片信息）"""
    with db_cursor() as cur:
        cur.execute(
            """
            UPDATE prescriptions SET
                mood_id = ?, mood_label = ?, time_minutes = ?,
                movie_id = ?, movie_title = ?, movie_genre = ?,
                movie_duration = ?, movie_reason = ?, match_score = ?,
                gradient_start = ?, gradient_end = ?, platform = ?
            WHERE id = ?
            """,
            (
                payload.mood_id,
                payload.mood_label,
                payload.time_minutes,
                payload.movie_id,
                payload.movie_title,
                payload.movie_genre,
                payload.movie_duration,
                payload.movie_reason,
                payload.match_score,
                payload.gradient_start,
                payload.gradient_end,
                payload.platform,
                record_id,
            ),
        )
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="记录不存在")
        cur.execute("SELECT * FROM prescriptions WHERE id = ?", (record_id,))
        row = cur.fetchone()
    return HistoryItem(**dict(row))


# @ai-generated true 2026-06-18
@router.put("/{record_id}/watch", response_model=CommonResponse)
def mark_watched(record_id: int, payload: WatchUpdate) -> CommonResponse:
    """标记已看 / 取消已看"""
    with db_cursor() as cur:
        cur.execute(
            "UPDATE prescriptions SET is_watched = ? WHERE id = ?",
            (payload.is_watched, record_id),
        )
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="记录不存在")
    return CommonResponse(message="updated")


# @ai-generated true 2026-06-18
@router.delete("/{record_id}", response_model=CommonResponse)
def delete_history(record_id: int) -> CommonResponse:
    """删除一条处方记录"""
    with db_cursor() as cur:
        cur.execute("DELETE FROM prescriptions WHERE id = ?", (record_id,))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="记录不存在")
    return CommonResponse(message="deleted")


# @ai-generated true 2026-06-18
@router.delete("", response_model=CommonResponse)
def clear_history() -> CommonResponse:
    """清空所有历史记录"""
    with db_cursor() as cur:
        cur.execute("DELETE FROM prescriptions")
    return CommonResponse(message="cleared")
