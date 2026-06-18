<script setup lang="ts">
// @ai-generated true 2026-06-18
// 文件名: MoodSelector.vue
// 作用: 心情选择器 - 6 种心情 3 列网格
import { MOOD_OPTIONS } from '@/api/types'

const props = defineProps<{
  modelValue: string
  variant?: 'gold' | 'teal'
}>()
const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
}>()

// @ai-generated true 2026-06-18
function onTap(id: string) {
  emit('update:modelValue', id)
}
</script>

<template>
  <view class="ms" :class="[`ms--${props.variant || 'gold'}`]">
    <view
      v-for="m in MOOD_OPTIONS"
      :key="m.id"
      class="ms__item"
      :class="{ 'ms__item--sel': props.modelValue === m.id }"
      @tap="onTap(m.id)"
    >
      <text class="ms__emoji">{{ m.emoji }}</text>
      <text class="ms__label">{{ m.label }}</text>
    </view>
  </view>
</template>

<style scoped lang="scss">
/* @ai-generated true 2026-06-18 */
@import "@/styles/variables.scss";

.ms {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16rpx;

  &__item {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 24rpx 8rpx;
    background: $bg-card;
    border-radius: $radius-md;
    border: 2rpx solid transparent;
    transition: all 0.2s ease;
    color: $txt-2;
  }
  &__emoji {
    font-size: 44rpx;
    line-height: 1;
    margin-bottom: 8rpx;
  }
  &__label {
    font-size: 22rpx;
  }

  /* gold 高亮 */
  &--gold .ms__item--sel {
    border-color: $gold;
    background: rgba(212, 168, 83, 0.08);
    color: $txt;
  }
  /* teal 高亮（双人模式 B 侧） */
  &--teal .ms__item--sel {
    border-color: $teal;
    background: rgba(56, 178, 172, 0.08);
    color: $txt;
  }
}
</style>
