<script setup lang="ts">
// @ai-generated true 2026-06-18
// 文件名: pages/duo/index.vue
// 作用: 双人处方 - 两人各自选择心情 + 共同时间 + 生成
import { ref, computed } from 'vue'
import { useMoodStore } from '@/stores/mood'
import { usePrescriptionStore } from '@/stores/prescription'
import MoodSelector from '@/components/MoodSelector.vue'
import TimePicker from '@/components/TimePicker.vue'
import { MOOD_OPTIONS } from '@/api/types'

const moodStore = useMoodStore()
const rxStore = usePrescriptionStore()

const moodA = ref('')
const moodB = ref('')
const selectedTime = ref(0)

// @ai-generated true 2026-06-18
const canGenerate = computed(
  () => !!moodA.value && !!moodB.value && selectedTime.value > 0
)

// @ai-generated true 2026-06-18
async function onGenerate() {
  if (!canGenerate.value) {
    uni.showToast({ title: '请先选择双方心情和时间', icon: 'none' })
    return
  }
  uni.showLoading({ title: '正在生成双人处方...' })
  try {
    // 主心情用 A，把 B 传给后端做交集
    moodStore.setMood(moodA.value)
    moodStore.setTime(selectedTime.value)
    await rxStore.generate(moodA.value, selectedTime.value, false, moodB.value)
    uni.hideLoading()
    uni.navigateTo({ url: '/pages/prescription/index' })
  } catch (e) {
    uni.hideLoading()
  }
}

// @ai-generated true 2026-06-18
function goBack() {
  uni.navigateBack()
}
</script>

<template>
  <view class="page">
    <view class="page__nav">
      <text class="page__back" @tap="goBack">←</text>
      <text class="page__title">👥 双人处方</text>
    </view>
    <text class="page__sub">两个人一起看，各选一个心情</text>

    <!-- Person A -->
    <text class="page__person page__person--a">PERSON A</text>
    <text class="page__person-title">你的心情</text>
    <view class="page__block">
      <MoodSelector :model-value="moodA" @update:model-value="moodA = $event" />
    </view>

    <view class="divider"></view>

    <!-- Person B -->
    <text class="page__person page__person--b">PERSON B</text>
    <text class="page__person-title">TA 的心情</text>
    <view class="page__block">
      <MoodSelector
        :model-value="moodB"
        variant="teal"
        @update:model-value="moodB = $event"
      />
    </view>

    <!-- Time -->
    <text class="page__section-title">共同时间</text>
    <view class="page__block">
      <TimePicker
        :model-value="selectedTime"
        @update:model-value="selectedTime = $event"
      />
    </view>

    <button
      class="rx-btn rx-btn--primary page__btn"
      :class="{ 'rx-btn--disabled': !canGenerate }"
      @tap="onGenerate"
    >
      💊 生成双人处方
    </button>
  </view>
</template>

<style scoped lang="scss">
/* @ai-generated true 2026-06-18 */
@import "@/styles/variables.scss";

.page {
  padding: 56rpx 32rpx;
  min-height: 100vh;
  background: $bg;

  &__nav {
    display: flex;
    align-items: center;
    gap: 16rpx;
    margin-bottom: 8rpx;
  }
  &__back {
    font-size: 36rpx;
    color: $txt-2;
  }
  &__title {
    font-size: 28rpx;
    font-weight: 700;
    letter-spacing: 4rpx;
  }
  &__sub {
    display: block;
    font-size: 22rpx;
    color: $txt-2;
    margin-bottom: 36rpx;
  }
  &__person {
    display: block;
    font-size: 18rpx;
    letter-spacing: 6rpx;
    margin-bottom: 6rpx;
    &--a { color: $gold; }
    &--b { color: $teal; }
  }
  &__person-title {
    display: block;
    font-size: 26rpx;
    font-weight: 600;
    color: $txt;
    margin-bottom: 16rpx;
  }
  &__section-title {
    display: block;
    font-size: 26rpx;
    font-weight: 600;
    color: $txt;
    margin: 24rpx 0 16rpx;
  }
  &__block {
    margin-bottom: 24rpx;
  }
  &__btn {
    margin-top: 32rpx;
  }
}
</style>