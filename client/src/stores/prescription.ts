// @ai-generated true 2026-06-18
// 文件名: stores/prescription.ts
// 作用: 当前处方结果 + 历史记录的状态管理

import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { RecommendResponse, HistoryItem } from '@/api/types'
import {
  fetchRecommend,
  fetchHistory,
  createHistory,
  replaceHistory,
  updateWatchStatus,
  deleteHistory,
  clearHistory,
} from '@/api'

export const usePrescriptionStore = defineStore('prescription', () => {
  const current = ref<RecommendResponse | null>(null)
  const excludedIds = ref<string[]>([])
  const history = ref<HistoryItem[]>([])
  const loading = ref(false)
  // @ai-generated true 2026-06-18
  // 记录"本轮处方"对应的历史 id，用于 reroll 时替换而不是新建
  const currentSessionId = ref<number | null>(null)

  // @ai-generated true 2026-06-18
  // 单人/双人通用：mood_b 可选传入用于双人交集
  async function generate(
    mood: string,
    time_minutes: number,
    isReroll = false,
    mood_b?: string,
  ) {
    loading.value = true
    try {
      if (!isReroll) {
        excludedIds.value = []
        currentSessionId.value = null
      }
      const res = await fetchRecommend({
        mood,
        mood_b,
        time_minutes,
        excluded_ids: excludedIds.value,
      })
      current.value = res
      return res
    } finally {
      loading.value = false
    }
  }

  // @ai-generated true 2026-06-18
  async function reroll(mood: string, time_minutes: number, mood_b?: string) {
    if (current.value?.movie?.id) {
      excludedIds.value.push(current.value.movie.id)
    }
    return generate(mood, time_minutes, true, mood_b)
  }

  // @ai-generated true 2026-06-18
  // 构造历史记录 payload — 用户预算时间 vs 影片时长严格区分
  function buildPayload(moodId: string, userBudgetMinutes: number) {
    if (!current.value) return null
    const m = current.value.movie
    return {
      mood_id: moodId,
      mood_label: current.value.mood_label,
      // ⚠ 用户预算时间，不是影片时长
      time_minutes: userBudgetMinutes,
      movie_id: m.id,
      movie_title: m.title,
      movie_genre: m.genre,
      movie_duration: m.duration,
      movie_reason: m.reason,
      match_score: current.value.match_score,
      gradient_start: m.gradient_start,
      gradient_end: m.gradient_end,
      platform: m.platform,
    }
  }

  // @ai-generated true 2026-06-18
  // 首次保存：新增记录并记下 sessionId
  async function saveCurrent(moodId: string, userBudgetMinutes: number) {
    const payload = buildPayload(moodId, userBudgetMinutes)
    if (!payload) return
    const item = await createHistory(payload)
    history.value.unshift(item)
    currentSessionId.value = item.id
    return item
  }

  // @ai-generated true 2026-06-18
  // "换一个"专用：更新已有记录而不是新建
  async function replaceLatest(moodId: string, userBudgetMinutes: number) {
    const payload = buildPayload(moodId, userBudgetMinutes)
    if (!payload) return
    // 没有 sessionId（首次进入或被清空）则降级为新建
    if (!currentSessionId.value) {
      return saveCurrent(moodId, userBudgetMinutes)
    }
    const item = await replaceHistory(currentSessionId.value, payload)
    const idx = history.value.findIndex((it) => it.id === item.id)
    if (idx >= 0) history.value[idx] = item
    return item
  }

  // @ai-generated true 2026-06-18
  async function loadHistory() {
    const list = await fetchHistory()
    history.value = list
  }

  // @ai-generated true 2026-06-18
  async function toggleWatch(id: number, is_watched: number) {
    await updateWatchStatus(id, is_watched)
    const target = history.value.find((it) => it.id === id)
    if (target) target.is_watched = is_watched
  }

  // @ai-generated true 2026-06-18
  async function removeOne(id: number) {
    await deleteHistory(id)
    history.value = history.value.filter((it) => it.id !== id)
    if (currentSessionId.value === id) currentSessionId.value = null
  }

  // @ai-generated true 2026-06-18
  async function clearAll() {
    await clearHistory()
    history.value = []
    currentSessionId.value = null
  }

  return {
    current,
    excludedIds,
    history,
    loading,
    currentSessionId,
    generate,
    reroll,
    saveCurrent,
    replaceLatest,
    loadHistory,
    toggleWatch,
    removeOne,
    clearAll,
  }
})
