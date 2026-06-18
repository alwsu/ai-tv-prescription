"""
@ai-generated true 2026-06-18
文件名: routes/preferences.py
作用: 用户偏好设置（单用户 Demo 模式，固定 id=1）
"""
import json
from fastapi import APIRouter

from database import db_cursor
from models import PreferencesDTO, CommonResponse

router = APIRouter(prefix="/api/preferences", tags=["preferences"])


# @ai-generated true 2026-06-18
@router.get("", response_model=PreferencesDTO)
def get_preferences() -> PreferencesDTO:
    """获取用户偏好"""
    with db_cursor() as cur:
        cur.execute("SELECT * FROM user_preferences WHERE id = 1")
        row = cur.fetchone()
    if row is None:
        return PreferencesDTO()
    return PreferencesDTO(
        liked_genres=json.loads(row["liked_genres"]),
        disliked_genres=json.loads(row["disliked_genres"]),
        dark_mode=row["dark_mode"],
        notifications=row["notifications"],
        daily_remind_time=row["daily_remind_time"],
    )


# @ai-generated true 2026-06-18
@router.put("", response_model=CommonResponse)
def update_preferences(payload: PreferencesDTO) -> CommonResponse:
    """更新用户偏好"""
    with db_cursor() as cur:
        cur.execute(
            """
            UPDATE user_preferences
            SET liked_genres = ?, disliked_genres = ?, dark_mode = ?,
                notifications = ?, daily_remind_time = ?
            WHERE id = 1
            """,
            (
                json.dumps(payload.liked_genres, ensure_ascii=False),
                json.dumps(payload.disliked_genres, ensure_ascii=False),
                payload.dark_mode,
                payload.notifications,
                payload.daily_remind_time,
            ),
        )
    return CommonResponse(message="updated")
