// @ai-generated true 2026-06-18
// 文件名: api/index.ts
// 作用: 业务 API 集中导出

import { http } from './request'
import type {
  RecommendResponse,
  HistoryItem,
  PreferencesDTO,
  StatsResponse,
} from './types'

// @ai-generated true 2026-06-18
// 心情推荐
export function fetchRecommend(payload: {
  mood: string
  mood_b?: string
  time_minutes: number
  excluded_ids?: string[]
}) {
  return http.post<RecommendResponse>('/api/recommend', payload)
}

// @ai-generated true 2026-06-18
// 历史记录 - 支持分页（默认拿前 20 条够用）
export function fetchHistory(page = 1, page_size = 20) {
  return http.get<HistoryItem[]>('/api/history', { page, page_size })
}

// @ai-generated true 2026-06-18
export function createHistory(payload: Omit<HistoryItem, 'id' | 'is_watched' | 'created_at'>) {
  return http.post<HistoryItem>('/api/history', payload)
}

// @ai-generated true 2026-06-18
// 替换已有历史记录（用于"换一个"更新最新记录而不是新建）
export function replaceHistory(
  id: number,
  payload: Omit<HistoryItem, 'id' | 'is_watched' | 'created_at'>
) {
  return http.put<HistoryItem>(`/api/history/${id}`, payload)
}

// @ai-generated true 2026-06-18
export function updateWatchStatus(id: number, is_watched: number) {
  return http.put(`/api/history/${id}/watch`, { is_watched })
}

// @ai-generated true 2026-06-18
export function deleteHistory(id: number) {
  return http.del(`/api/history/${id}`)
}

// @ai-generated true 2026-06-18
export function clearHistory() {
  return http.del('/api/history')
}

// @ai-generated true 2026-06-18
// 偏好
export function fetchPreferences() {
  return http.get<PreferencesDTO>('/api/preferences')
}

// @ai-generated true 2026-06-18
export function updatePreferences(payload: PreferencesDTO) {
  return http.put('/api/preferences', payload)
}

// @ai-generated true 2026-06-18
// 统计
export function fetchStats() {
  return http.get<StatsResponse>('/api/stats')
}
