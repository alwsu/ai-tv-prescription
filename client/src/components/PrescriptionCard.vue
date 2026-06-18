<script setup lang="ts">
// @ai-generated true 2026-06-18
// 文件名: PrescriptionCard.vue
// 作用: 处方结果卡片 - 头部 + 渐变海报 + 标签 + 推荐理由
import { computed } from 'vue'
import type { RecommendResponse } from '@/api/types'

const props = defineProps<{ data: RecommendResponse }>()

// @ai-generated true 2026-06-18
const posterStyle = computed(() => {
  const m = props.data.movie
  return `background: linear-gradient(135deg, ${m.gradient_start}, ${m.gradient_end});`
})
</script>

<template>
  <view class="rx rx-card">
    <view class="rx__head">
      <view class="rx__head-l">
        <text class="rx-symbol rx__symbol">℞</text>
        <text class="rx__label">AI 追剧处方单</text>
      </view>
      <view class="rx__match">{{ data.match_score }}% 匹配</view>
    </view>

    <view class="rx__poster" :style="posterStyle">
      <text class="rx__poster-text">{{ data.movie.title }}</text>
    </view>

    <view class="rx__tags">
      <text class="tag">{{ data.movie.duration }} min</text>
      <text class="tag">{{ data.movie.genre }}</text>
      <text class="tag">{{ data.movie.platform }}</text>
    </view>

    <view class="rx__reason">
      <text class="rx__reason-label">💡 为什么推荐这部</text>
      <text class="rx__reason-text">{{ data.reason }}</text>
    </view>
  </view>
</template>

<style scoped lang="scss">
/* @ai-generated true 2026-06-18 */
@import "@/styles/variables.scss";

.rx {
  &__head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 24rpx;
  }
  &__head-l {
    display: flex;
    align-items: center;
    gap: 12rpx;
  }
  &__symbol {
    font-size: 44rpx;
    line-height: 1;
  }
  &__label {
    font-size: 20rpx;
    color: $txt-3;
  }
  &__match {
    padding: 6rpx 20rpx;
    background: rgba(56, 178, 172, 0.1);
    border-radius: 24rpx;
    font-size: 22rpx;
    color: $teal-l;
    font-weight: 700;
  }
  &__poster {
    width: 100%;
    height: 240rpx;
    border-radius: $radius-md;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 24rpx;
  }
  &__poster-text {
    font-size: 44rpx;
    font-weight: 800;
    color: rgba(255, 255, 255, 0.92);
    letter-spacing: 6rpx;
  }
  &__tags {
    display: flex;
    flex-wrap: wrap;
    margin-bottom: 20rpx;
  }
  &__reason {
    padding: 20rpx;
    background: rgba(255, 255, 255, 0.02);
    border-radius: $radius-sm;
    border-left: 4rpx solid $gold;
    display: flex;
    flex-direction: column;
  }
  &__reason-label {
    font-size: 20rpx;
    color: $gold;
    letter-spacing: 2rpx;
    margin-bottom: 8rpx;
  }
  &__reason-text {
    font-size: 24rpx;
    color: $txt-2;
    line-height: 1.7;
  }
}
</style>
