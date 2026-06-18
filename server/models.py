"""
@ai-generated true 2026-06-18
文件名: models.py
作用: Pydantic 请求/响应模型定义
"""
from typing import List, Optional
from pydantic import BaseModel, Field


# @ai-generated true 2026-06-18
class RecommendRequest(BaseModel):
    """心情推荐请求"""
    mood: str = Field(..., description="心情标识，如 relax/heal/excite/brain/release/together")
    time_minutes: int = Field(..., ge=10, le=300, description="可用时间（分钟）")
    excluded_ids: Optional[List[str]] = Field(default_factory=list, description="排除的影片 ID 列表")


# @ai-generated true 2026-06-18
class MovieDTO(BaseModel):
    """影片信息"""
    id: str
    title: str
    duration: int
    genre: str
    mood_tags: List[str]
    reason: str
    platform: str
    rating: float
    gradient_start: str
    gradient_end: str
    year: int = 2020
    summary: str = ""


# @ai-generated true 2026-06-18
class RecommendResponse(BaseModel):
    """心情推荐响应"""
    movie: MovieDTO
    match_score: int
    reason: str
    mood_label: str


# @ai-generated true 2026-06-18
class HistoryCreate(BaseModel):
    """新增历史记录请求体"""
    mood_id: str
    mood_label: str
    time_minutes: int
    movie_id: str
    movie_title: str
    movie_genre: str
    movie_duration: int
    movie_reason: str
    match_score: int
    gradient_start: str = "#4a7c59"
    gradient_end: str = "#8fbc8f"
    platform: str = "B站"


# @ai-generated true 2026-06-18
class HistoryItem(BaseModel):
    """历史记录条目"""
    id: int
    mood_id: str
    mood_label: str
    time_minutes: int
    movie_id: str
    movie_title: str
    movie_genre: str
    movie_duration: int
    movie_reason: str
    match_score: int
    is_watched: int
    gradient_start: str
    gradient_end: str
    platform: str = "B站"
    created_at: str


# @ai-generated true 2026-06-18
class WatchUpdate(BaseModel):
    """已看状态更新"""
    is_watched: int = Field(..., ge=0, le=1)


# @ai-generated true 2026-06-18
class PreferencesDTO(BaseModel):
    """用户偏好"""
    liked_genres: List[str] = []
    disliked_genres: List[str] = []
    dark_mode: int = 1
    notifications: int = 1
    daily_remind_time: str = "21:00"


# @ai-generated true 2026-06-18
class StatsResponse(BaseModel):
    """统计数据响应"""
    total_prescriptions: int
    watched_count: int
    watch_rate: int
    favorite_genre: str


# @ai-generated true 2026-06-18
class CommonResponse(BaseModel):
    """通用响应"""
    code: int = 0
    message: str = "ok"
