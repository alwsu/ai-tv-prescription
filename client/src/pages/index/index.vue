<script setup lang="ts">
// @ai-generated true 2026-06-18
// 文件名: pages/index/index.vue
// 作用: 首页 - 心情选片入口 (心情 + 时间 + 生成按钮)
import { computed } from 'vue'
import { useMoodStore } from '@/stores/mood'
import { usePrescriptionStore } from '@/stores/prescription'
import MoodSelector from '@/components/MoodSelector.vue'
import TimePicker from '@/components/TimePicker.vue'

const moodStore = useMoodStore()
const rxStore = usePrescriptionStore()

// @ai-generated true 2026-06-18
const canGenerate = computed(
  () => !!moodStore.selectedMood && moodStore.selectedTime > 0
)

// @ai-generated true 2026-06-18
async function onGenerate() {
  if (!canGenerate.value) {
    uni.showToast({ title: '请先选择心情和时间', icon: 'none' })
    return
  }
  uni.showLoading({ title: '正在开方...' })
  try {
    await rxStore.generate(moodStore.selectedMood, moodStore.selectedTime)
    uni.hideLoading()
    uni.navigateTo({ url: '/pages/prescription/index' })
  } catch (e) {
    uni.hideLoading()
  }
}

// @ai-generated true 2026-06-18
function goDuo() {
  uni.navigateTo({ url: '/pages/duo/index' })
}
</script>

<template>
  <view class="page">
    <!-- 上半部分：标题 + 表单 -->
    <view class="page__top">
      <view class="page__header">
        <text class="page__greet">🎬 今晚想看点什么？</text>
        <text class="page__sub">告诉 AI 你的心情和时间，为你开一剂追剧处方</text>
      </view>

      <view class="page__step-tag">STEP 01</view>
      <text class="page__step-title">你现在的心情是？</text>
      <view class="page__block">
        <MoodSelector
          :model-value="moodStore.selectedMood"
          @update:model-value="moodStore.setMood"
        />
      </view>

      <view class="page__step-tag">STEP 02</view>
      <text class="page__step-title">你有多少时间？</text>
      <view class="page__block">
        <TimePicker
          :model-value="moodStore.selectedTime"
          @update:model-value="moodStore.setTime"
        />
      </view>
    </view>

    <!-- 下半部分：操作区（贴近拇指可达区域） -->
    <view class="page__bottom">
      <button
        class="rx-btn rx-btn--primary page__gen"
        :class="{ 'rx-btn--disabled': !canGenerate }"
        @tap="onGenerate"
      >
        💊 生成追剧处方
      </button>
      <button class="rx-btn rx-btn--ghost page__duo" @tap="goDuo">
        👥 双人处方 — 两个人一起选
      </button>
    </view>
  </view>
</template>

<style scoped lang="scss">
/* @ai-generated true 2026-06-18 */
@import "@/styles/variables.scss";

.page {
  /* @ai-generated true 2026-06-18 */
  /* 一屏自适应：内容能挤就不滚动；挤不下时允许滚动避免内容被截断 */
  padding: 40rpx 32rpx 48rpx;
  min-height: 100vh;
  max-height: 100vh;
  background: $bg;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  overflow-x: hidden;
  box-sizing: border-box;

  &__top {
    flex: 1 1 auto;
    min-height: 0;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  &__bottom {
    flex: 0 0 auto;
    padding-top: 24rpx;
    padding-bottom: env(safe-area-inset-bottom, 0);
  }

  &__header {
    margin-bottom: 24rpx;
  }
  &__greet {
    display: block;
    font-size: 36rpx;
    font-weight: 800;
    color: $txt;
    margin-bottom: 8rpx;
  }
  &__sub {
    display: block;
    font-size: 22rpx;
    color: $txt-2;
  }
  &__step-tag {
    font-size: 18rpx;
    color: $gold;
    letter-spacing: 6rpx;
    margin-bottom: 6rpx;
  }
  &__step-title {
    display: block;
    font-size: 26rpx;
    font-weight: 700;
    color: $txt;
    margin-bottom: 14rpx;
  }
  &__block {
    margin-bottom: 16rpx;
  }
  &__gen {
    margin-bottom: 12rpx;
    height: 80rpx;
  }
  &__duo {
    height: 70rpx;
    font-size: 22rpx;
  }
}

/* @ai-generated true 2026-06-18 */
/* 收紧组件内部间距，配合一屏布局 */
.page :deep(.ms__item) {
  padding: 16rpx 4rpx;
}
.page :deep(.ms__emoji) {
  font-size: 36rpx;
  margin-bottom: 4rpx;
}
.page :deep(.ms__label) {
  font-size: 20rpx;
}
.page :deep(.tp__chip) {
  padding: 10rpx 22rpx;
  font-size: 22rpx;
}
</style>
