// @ai-generated true 2026-06-18
// 文件名: stores/mood.ts
// 作用: 心情和时间选择状态

import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useMoodStore = defineStore('mood', () => {
  const selectedMood = ref<string>('')
  const selectedTime = ref<number>(0)

  function setMood(id: string) {
    selectedMood.value = id
  }
  function setTime(minutes: number) {
    selectedTime.value = minutes
  }
  function reset() {
    selectedMood.value = ''
    selectedTime.value = 0
  }

  return { selectedMood, selectedTime, setMood, setTime, reset }
})
