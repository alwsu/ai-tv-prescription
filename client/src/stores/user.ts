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
    // 加载偏好后自动应用主题，保证 tabBar / CSS 颜色都同步
    applyTheme(res.dark_mode)
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
    // 用 setTimeout 确保 tabBar DOM 已挂载，否则首次启动时 setTabBarStyle 会静默失败
    const applyTabBar = () => {
      try {
        uni.setTabBarStyle({
          color: isDark ? '#5c586e' : '#9a96a6',
          selectedColor: isDark ? '#d4a853' : '#b8893a',
          backgroundColor: isDark ? '#0c0c1a' : '#ffffff',
          borderStyle: isDark ? 'black' : 'white',
        })
      } catch (e) {
        // 部分端可能不支持，静默失败
      }
    }
    // 立即尝试一次（已挂载情况）
    applyTabBar()
    // 100ms 后再尝试一次（首次启动 onLaunch 阶段 tabBar 还没渲染）
    setTimeout(applyTabBar, 100)
    // 500ms 后再补一次（极端情况兜底）
    setTimeout(applyTabBar, 500)
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
