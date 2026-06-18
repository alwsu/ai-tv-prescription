// @ai-generated true 2026-06-18
// 文件名: api/types.ts
// 作用: 与后端契合的 TS 类型定义

export interface MovieDTO {
  id: string
  title: string
  duration: number
  genre: string
  mood_tags: string[]
  reason: string
  platform: string
  rating: number
  gradient_start: string
  gradient_end: string
  year: number
  summary: string
}

export interface RecommendResponse {
  movie: MovieDTO
  match_score: number
  reason: string
  mood_label: string
}

export interface HistoryItem {
  id: number
  mood_id: string
  mood_label: string
  time_minutes: number
  movie_id: string
  movie_title: string
  movie_genre: string
  movie_duration: number
  movie_reason: string
  match_score: number
  is_watched: number
  gradient_start: string
  gradient_end: string
  platform: string
  created_at: string
}

export interface PreferencesDTO {
  liked_genres: string[]
  disliked_genres: string[]
  dark_mode: number
  notifications: number
  daily_remind_time: string
}

export interface StatsResponse {
  total_prescriptions: number
  watched_count: number
  watch_rate: number
  favorite_genre: string
}

export interface MoodOption {
  id: string
  emoji: string
  label: string
}

export const MOOD_OPTIONS: MoodOption[] = [
  { id: 'relax', emoji: '😴', label: '想放松' },
  { id: 'heal', emoji: '🤗', label: '想治愈' },
  { id: 'excite', emoji: '🔥', label: '想刺激' },
  { id: 'brain', emoji: '🧠', label: '想烧脑' },
  { id: 'release', emoji: '😭', label: '想解压' },
  { id: 'together', emoji: '👥', label: '一起看' },
]

export const TIME_OPTIONS: { minutes: number; label: string }[] = [
  { minutes: 15, label: '15 分钟' },
  { minutes: 30, label: '30 分钟' },
  { minutes: 60, label: '1 小时' },
  { minutes: 120, label: '2 小时' },
  { minutes: 180, label: '3 小时+' },
]
