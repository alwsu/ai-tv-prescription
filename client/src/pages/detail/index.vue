<script setup lang="ts">
// @ai-generated true 2026-06-18
// 文件名: pages/detail/index.vue
// 作用: 处方记录详情页 - 展示单条历史处方的完整信息 + 跳转播放
import { ref, computed, onMounted } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { usePrescriptionStore } from '@/stores/prescription'
import type { HistoryItem } from '@/api/types'
import { openInPlatform } from '@/utils/playerLink'

const rxStore = usePrescriptionStore()
const recordId = ref<number>(0)
const record = ref<HistoryItem | null>(null)

// @ai-generated true 2026-06-18
// 接收路由 query 参数 id
onLoad((options) => {
  const id = Number(options?.id || 0)
  recordId.value = id
})

// @ai-generated true 2026-06-18
// 加载详情数据：优先从已加载的 history 中查找，缺失则拉取列表
onMounted(async () => {
  try {
    if (rxStore.history.length === 0) {
      await rxStore.loadHistory()
    }
    record.value =
      rxStore.history.find((it) => it.id === recordId.value) || null
  } catch (e) {
    record.value = null
  }
})

// @ai-generated true 2026-06-18
// 渐变海报样式
const posterStyle = computed(() => {
  if (!record.value) return ''
  return `background: linear-gradient(135deg, ${record.value.gradient_start}, ${record.value.gradient_end});`
})

// @ai-generated true 2026-06-18
// 创建时间格式化（YYYY-MM-DD HH:mm）
const createdTime = computed(() => {
  const s = record.value?.created_at || ''
  return s.replace('T', ' ').slice(0, 16)
})

// @ai-generated true 2026-06-18
// 切换已看状态
async function onToggleWatch() {
  if (!record.value) return
  const next = record.value.is_watched ? 0 : 1
  await rxStore.toggleWatch(record.value.id, next)
  record.value.is_watched = next
  uni.showToast({
    title: next ? '已标记为已看 ✓' : '取消已看',
    icon: 'none',
  })
}

// @ai-generated true 2026-06-18
// 跳转到对应平台搜索/播放
function onPlay() {
  if (!record.value) return
  const platform = record.value.platform || 'B站'
  uni.showToast({
    title: `正在打开 ${platform}...`,
    icon: 'none',
    duration: 1500,
  })
  openInPlatform(platform, record.value.movie_title)
}

// @ai-generated true 2026-06-18
function onDelete() {
  if (!record.value) return
  uni.showModal({
    title: '删除记录',
    content: '确认删除这条处方吗？',
    confirmColor: '#e85d75',
    success: async ({ confirm }) => {
      if (confirm && record.value) {
        await rxStore.removeOne(record.value.id)
        uni.showToast({ title: '已删除', icon: 'none' })
        setTimeout(() => uni.navigateBack(), 600)
      }
    },
  })
}

// @ai-generated true 2026-06-18
function goBack() {
  uni.navigateBack()
}
</script>

<template>
  <view class="page">
    <!-- 顶部海报 + 返回 -->
    <view class="page__hero" :style="posterStyle">
      <text class="page__back" @tap="goBack">←</text>
      <text class="page__title">{{ record?.movie_title || '加载中...' }}</text>
      <view v-if="record?.is_watched" class="page__watched">已看 ✓</view>
    </view>

    <view v-if="record" class="page__body">
      <!-- 元信息 -->
      <view class="page__meta">
        <text class="meta-tag">{{ record.movie_genre }}</text>
        <text class="meta-tag">{{ record.movie_duration }} min</text>
        <text class="meta-tag">{{ record.platform }}</text>
        <text class="meta-tag meta-tag--gold">⭐ {{ record.match_score }}% 匹配</text>
      </view>

      <!-- 处方单信息块 -->
      <view class="rx-card page__rx">
        <view class="page__rx-head">
          <text class="rx-symbol page__rx-sym">℞</text>
          <text class="page__rx-label">本次处方</text>
        </view>
        <view class="page__rx-row">
          <text class="page__rx-k">心情</text>
          <text class="page__rx-v">{{ record.mood_label }}</text>
        </view>
        <view class="page__rx-row">
          <text class="page__rx-k">用户预算</text>
          <text class="page__rx-v">{{ record.time_minutes }} 分钟</text>
        </view>
        <view class="page__rx-row">
          <text class="page__rx-k">影片时长</text>
          <text class="page__rx-v">{{ record.movie_duration }} 分钟</text>
        </view>
        <view class="page__rx-row">
          <text class="page__rx-k">开方时间</text>
          <text class="page__rx-v">{{ createdTime }}</text>
        </view>
      </view>

      <!-- AI 推荐理由 -->
      <text class="page__section">💡 AI 推荐理由</text>
      <view class="rx-card page__reason">
        <text class="page__reason-text">{{ record.movie_reason }}</text>
      </view>

      <!-- 操作区 -->
      <view class="page__actions">
        <button class="rx-btn rx-btn--primary page__play" @tap="onPlay">
          ▶ 去观看这部
        </button>
        <view class="page__sub-actions">
          <button
            class="rx-btn rx-btn--teal-line page__sub-act"
            @tap="onToggleWatch"
          >
            {{ record.is_watched ? '↩ 取消已看' : '✅ 标记已看' }}
          </button>
          <button class="rx-btn rx-btn--ghost page__sub-act" @tap="onDelete">
            🗑 删除记录
          </button>
        </view>
      </view>
    </view>

    <!-- 加载失败 -->
    <view v-else class="page__empty">
      <text class="page__empty-icon">📋</text>
      <text class="page__empty-text">未找到该处方记录</text>
      <button class="rx-btn rx-btn--ghost page__empty-btn" @tap="goBack">
        返回列表
      </button>
    </view>
  </view>
</template>

<style scoped lang="scss">
/* @ai-generated true 2026-06-18 */
@import "@/styles/variables.scss";

.page {
  min-height: 100vh;
  background: $bg;
  padding-bottom: 80rpx;

  &__hero {
    height: 360rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
  }
  &__back {
    position: absolute;
    top: 56rpx;
    left: 32rpx;
    width: 56rpx;
    height: 56rpx;
    line-height: 52rpx;
    text-align: center;
    border-radius: 50%;
    background: rgba(0, 0, 0, 0.35);
    color: #fff;
    font-size: 32rpx;
  }
  &__title {
    font-size: 56rpx;
    font-weight: 800;
    color: rgba(255, 255, 255, 0.95);
    letter-spacing: 8rpx;
  }
  &__watched {
    position: absolute;
    top: 56rpx;
    right: 32rpx;
    padding: 8rpx 20rpx;
    background: rgba(56, 178, 172, 0.85);
    color: #fff;
    border-radius: 24rpx;
    font-size: 22rpx;
    font-weight: 700;
  }

  &__body {
    padding: 32rpx;
    margin-top: -40rpx;
    position: relative;
  }
  &__meta {
    display: flex;
    flex-wrap: wrap;
    gap: 12rpx;
    margin-bottom: 28rpx;
  }
  &__rx {
    margin-bottom: 32rpx;
  }
  &__rx-head {
    display: flex;
    align-items: center;
    gap: 12rpx;
    margin-bottom: 20rpx;
    padding-bottom: 16rpx;
    border-bottom: 1rpx dashed $bdr;
  }
  &__rx-sym {
    font-size: 40rpx;
    line-height: 1;
  }
  &__rx-label {
    font-size: 22rpx;
    color: $txt-3;
    letter-spacing: 4rpx;
  }
  &__rx-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 14rpx 0;
    font-size: 24rpx;
  }
  &__rx-k {
    color: $txt-3;
  }
  &__rx-v {
    color: $txt;
    font-weight: 600;
  }
  &__section {
    display: block;
    font-size: 26rpx;
    font-weight: 700;
    color: $txt;
    margin: 8rpx 0 16rpx;
  }
  &__reason {
    border-left: 4rpx solid $gold;
    margin-bottom: 36rpx;
  }
  &__reason-text {
    font-size: 26rpx;
    color: $txt-2;
    line-height: 1.8;
  }

  &__actions {
    display: flex;
    flex-direction: column;
    gap: 16rpx;
  }
  &__play {
    height: 96rpx;
    font-size: 30rpx;
    letter-spacing: 4rpx;
  }
  &__sub-actions {
    display: flex;
    gap: 16rpx;
  }
  &__sub-act {
    flex: 1;
    height: 80rpx;
    font-size: 22rpx;
  }

  &__empty {
    text-align: center;
    padding: 200rpx 32rpx;
  }
  &__empty-icon {
    display: block;
    font-size: 96rpx;
    margin-bottom: 24rpx;
    opacity: 0.5;
  }
  &__empty-text {
    display: block;
    font-size: 26rpx;
    color: $txt-3;
    margin-bottom: 32rpx;
  }
  &__empty-btn {
    width: 60%;
    margin: 0 auto;
  }
}

/* @ai-generated true 2026-06-18 */
.meta-tag {
  display: inline-block;
  padding: 8rpx 20rpx;
  border-radius: 24rpx;
  background: $bg-card;
  border: 1rpx solid $bdr;
  font-size: 22rpx;
  color: $txt-2;

  &--gold {
    background: rgba(212, 168, 83, 0.1);
    border-color: rgba(212, 168, 83, 0.3);
    color: $gold;
    font-weight: 600;
  }
}
</style>
