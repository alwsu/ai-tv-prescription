<script setup lang="ts">
// @ai-generated true 2026-06-18
// 文件名: TimePicker.vue
// 作用: 时间选择器 - 5 档 chip 横向选择
import { TIME_OPTIONS } from '@/api/types'

const props = defineProps<{ modelValue: number }>()
const emit = defineEmits<{
  (e: 'update:modelValue', value: number): void
}>()

// @ai-generated true 2026-06-18
function onTap(minutes: number) {
  emit('update:modelValue', minutes)
}
</script>

<template>
  <view class="tp">
    <view
      v-for="t in TIME_OPTIONS"
      :key="t.minutes"
      class="rx-chip tp__chip"
      :class="{ 'rx-chip--active': props.modelValue === t.minutes }"
      @tap="onTap(t.minutes)"
    >
      {{ t.label }}
    </view>
  </view>
</template>

<style scoped lang="scss">
/* @ai-generated true 2026-06-18 */
@import "@/styles/variables.scss";

.tp {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;

  &__chip {
    flex: 0 0 auto;
  }
}
</style>
