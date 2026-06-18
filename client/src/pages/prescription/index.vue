<script setup lang="ts">
// @ai-generated true 2026-06-18
// 文件名: pages/prescription/index.vue
// 作用: 处方结果页 - 展示 AI 推荐结果 + 换一个/已看/分享
import { onMounted, computed } from 'vue'
import { useMoodStore } from '@/stores/mood'
import { usePrescriptionStore } from '@/stores/prescription'
import PrescriptionCard from '@/components/PrescriptionCard.vue'
import { openInPlatform } from '@/utils/playerLink'

const moodStore = useMoodStore()
const rxStore = usePrescriptionStore()

// @ai-generated true 2026-06-18
// 当前推荐影片的平台名（用于按钮文案）
const platformName = computed(() => rxStore.current?.movie?.platform || '播放平台')

// @ai-generated true 2026-06-18
// 进入页面后自动保存到历史（首次：新建记录，记录 sessionId）
onMounted(async () => {
  if (rxStore.current && moodStore.selectedMood) {
    try {
      await rxStore.saveCurrent(moodStore.selectedMood, moodStore.selectedTime)
    } catch (e) {
      // 静默失败，页面仍可浏览
    }
  }
})

// @ai-generated true 2026-06-18
async function onReroll() {
  if (!moodStore.selectedMood || !moodStore.selectedTime) return
  uni.showLoading({ title: '换一个...' })
  try {
    await rxStore.reroll(moodStore.selectedMood, moodStore.selectedTime)
    // 用 replaceLatest 更新本轮记录而不是新建，避免历史记录爆炸
    await rxStore.replaceLatest(moodStore.selectedMood, moodStore.selectedTime)
    uni.hideLoading()
  } catch (e) {
    uni.hideLoading()
  }
}

// @ai-generated true 2026-06-18
async function onWatched() {
  const latest = rxStore.history[0]
  if (!latest) {
    uni.showToast({ title: '记录尚未保存', icon: 'none' })
    return
  }
  await rxStore.toggleWatch(latest.id, latest.is_watched ? 0 : 1)
  uni.showToast({
    title: latest.is_watched ? '已看 ✓' : '取消标记',
    icon: 'none',
  })
}

// @ai-generated true 2026-06-18
function onShare() {
  uni.showToast({ title: '分享卡片生成中...', icon: 'none' })
}

// @ai-generated true 2026-06-18
// 跳转到对应视频平台搜索/播放该影片
function onPlay() {
  const movie = rxStore.current?.movie
  if (!movie) return
  uni.showToast({
    title: `正在打开 ${movie.platform}...`,
    icon: 'none',
    duration: 1500,
  })
  openInPlatform(movie.platform, movie.title)
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
      <text class="page__title">追剧处方 ℞</text>
    </view>

    <view v-if="rxStore.current" class="page__body">
      <PrescriptionCard :data="rxStore.current" />

      <!-- 主 CTA：去对应平台播放 -->
      <button class="rx-btn rx-btn--primary page__play" @tap="onPlay">
        ▶ 去 {{ platformName }} 观看
      </button>

      <view class="page__actions">
        <button class="rx-btn rx-btn--ghost page__act" @tap="onReroll">
          🔄 换一个
        </button>
        <button
          class="rx-btn rx-btn--teal-line page__act"
          @tap="onWatched"
        >
          ✅ 已看
        </button>
        <button class="rx-btn rx-btn--ghost page__act" @tap="onShare">
          📤 分享
        </button>
      </view>
    </view>

    <view v-else class="page__empty">
      <text>处方未生成，请返回首页重新选择</text>
    </view>
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
    margin-bottom: 28rpx;
  }
  &__back {
    font-size: 36rpx;
    color: $txt-2;
  }
  &__title {
    font-size: 28rpx;
    font-weight: 700;
    letter-spacing: 4rpx;
    color: $txt;
  }
  &__actions {
    display: flex;
    gap: 16rpx;
    margin-top: 28rpx;
  }
  &__play {
    margin-top: 28rpx;
    height: 88rpx;
    font-size: 28rpx;
    letter-spacing: 2rpx;
  }
  &__act {
    flex: 1;
    height: 80rpx;
    font-size: 22rpx;
  }
  &__empty {
    text-align: center;
    color: $txt-3;
    padding-top: 200rpx;
  }
}
</style>
