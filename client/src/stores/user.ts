// @ai-generated true 2026-06-18
// 文件名: stores/user.ts
// 作用: 用户偏好与统计数据

import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { PreferencesDTO, StatsResponse } from '@/api/types'
import { fetchPreferences, updatePreferences, fetchStats } from '@/api'

export const useUserStore = defineStore('user', () => {
  const preferences = ref<PreferencesDTO>({
    liked_genres: [],
    disliked_genres: [],
    dark_mode: 1,
    notifications: 1,
    daily_remind_time: '21:00',
  })
  const stats = ref<StatsResponse>({
    total_prescriptions: 0,
    watched_count: 0,
    watch_rate: 0,
    favorite_genre: '暂无',
  })

  // @ai-generated true 2026-06-18
  async function loadPreferences() {
    const res = await fetchPreferences()
    preferences.value = res
  }

  // @ai-generated true 2026-06-18
  async function savePreferences(payload: PreferencesDTO) {
    await updatePreferences(payload)
    preferences.value = payload
  }

  // @ai-generated true 2026-06-18
  async function loadStats() {
    const res = await fetchStats()
    stats.value = res
  }

  // @ai-generated true 2026-06-18
  function addLikedGenre(g: string) {
    if (!preferences.value.liked_genres.includes(g)) {
      preferences.value.liked_genres.push(g)
    }
  }
  function removeLikedGenre(g: string) {
    preferences.value.liked_genres = preferences.value.liked_genres.filter(
      (x) => x !== g
    )
  }

  // @ai-generated true 2026-06-18
  // 应用主题：切换 H5 根节点 data-theme + 同步底部 tabBar 颜色
  function applyTheme(darkMode: number) {
    const isDark = !!darkMode

    // @ai-generated true 2026-06-18
    // 1. H5 端写入 documentElement 的 data-theme，让 CSS 变量生效
    // #ifdef H5
    const theme = isDark ? 'dark' : 'light'
    if (typeof document !== 'undefined') {
      document.documentElement.setAttribute('data-theme', theme)
    }
    // #endif

    // @ai-generated true 2026-06-18
    // 2. 同步底部原生 tabBar 颜色（pages.json 配置无法运行时修改，必须用 API）
    try {
      uni.setTabBarStyle({
        color: isDark ? '#5c586e' : '#9a96a6',           // 未选中文字
        selectedColor: isDark ? '#d4a853' : '#b8893a',   // 选中文字
        backgroundColor: isDark ? '#0c0c1a' : '#ffffff', // 背景
        borderStyle: isDark ? 'black' : 'white',         // 顶部分割线
      })
    } catch (e) {
      // 部分端可能不支持，静默失败
    }
  }

  return {
    preferences,
    stats,
    loadPreferences,
    savePreferences,
    loadStats,
    addLikedGenre,
    removeLikedGenre,
    applyTheme,
  }
})
