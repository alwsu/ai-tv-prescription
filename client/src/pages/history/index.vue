<script setup lang="ts">
// @ai-generated true 2026-06-18
// 文件名: pages/history/index.vue
// 作用: 历史处方列表 - 标记已看/删除
import { onShow } from '@dcloudio/uni-app'
import { usePrescriptionStore } from '@/stores/prescription'

const rxStore = usePrescriptionStore()

// @ai-generated true 2026-06-18
onShow(async () => {
  try {
    await rxStore.loadHistory()
  } catch (e) {}
})

// @ai-generated true 2026-06-18
async function onToggleWatch(id: number, current: number) {
  await rxStore.toggleWatch(id, current ? 0 : 1)
}

// @ai-generated true 2026-06-18
function onDelete(id: number) {
  uni.showModal({
    title: '删除记录',
    content: '确认删除这条处方吗？',
    success: async ({ confirm }) => {
      if (confirm) {
        await rxStore.removeOne(id)
        uni.showToast({ title: '已删除', icon: 'none' })
      }
    },
  })
}

// @ai-generated true 2026-06-18
function formatDate(s: string) {
  return s ? s.slice(0, 10) : ''
}

// @ai-generated true 2026-06-18
function firstChar(title: string) {
  return title?.charAt(0) || '?'
}

// @ai-generated true 2026-06-18
// 跳转到处方详情页
function onOpenDetail(id: number) {
  uni.navigateTo({ url: `/pages/detail/index?id=${id}` })
}
</script>

<template>
  <view class="page">
    <view class="page__head">
      <text class="page__title">📋 处方记录</text>
      <text class="page__count">共 {{ rxStore.history.length }} 条处方记录</text>
    </view>

    <view v-if="rxStore.history.length === 0" class="page__empty">
      <text class="page__empty-icon">💊</text>
      <text class="page__empty-text">还没有处方记录，去首页开一剂处方吧</text>
    </view>

    <view v-else>
      <view
        v-for="item in rxStore.history"
        :key="item.id"
        class="page__item"
        :class="{ 'page__item--watched': item.is_watched }"
        @tap="onOpenDetail(item.id)"
      >
        <view
          class="page__poster"
          :style="`background: linear-gradient(135deg, ${item.gradient_start}, ${item.gradient_end});`"
        >
          {{ firstChar(item.movie_title) }}
        </view>
        <view class="page__info">
          <text class="page__name">{{ item.movie_title }}</text>
          <text class="page__meta">
            {{ item.mood_label }} · {{ item.movie_genre }} ·
            {{ formatDate(item.created_at) }}
          </text>
        </view>
        <view class="page__actions" @tap.stop>
          <view
            class="page__btn"
            :class="{ 'page__btn--active': item.is_watched }"
            @tap.stop="onToggleWatch(item.id, item.is_watched)"
          >
            ✓
          </view>
          <view class="page__btn" @tap.stop="onDelete(item.id)">🗑</view>
        </view>
      </view>
    </view>
  </view>
</template>

<style scoped lang="scss">
/* @ai-generated true 2026-06-18 */
@import "@/styles/variables.scss";

.page {
  padding: 56rpx 32rpx 80rpx;
  min-height: 100vh;
  background: $bg;

  &__head {
    margin-bottom: 32rpx;
  }
  &__title {
    display: block;
    font-size: 36rpx;
    font-weight: 800;
    color: $txt;
    margin-bottom: 6rpx;
  }
  &__count {
    display: block;
    font-size: 22rpx;
    color: $txt-3;
  }
  &__empty {
    text-align: center;
    padding-top: 160rpx;
    color: $txt-3;
  }
  &__empty-icon {
    display: block;
    font-size: 80rpx;
    margin-bottom: 16rpx;
    opacity: 0.5;
  }
  &__empty-text {
    font-size: 26rpx;
  }
  &__item {
    display: flex;
    align-items: center;
    gap: 20rpx;
    padding: 20rpx;
    background: $bg-card;
    border-radius: $radius-md;
    border: 1rpx solid $bdr;
    margin-bottom: 16rpx;
    transition: all 0.2s ease;

    &:active {
      transform: scale(0.98);
      border-color: rgba(212, 168, 83, 0.25);
      background: rgba(212, 168, 83, 0.04);
    }

    &--watched {
      opacity: 0.55;
      .page__name {
        text-decoration: line-through;
        color: $txt-3;
      }
    }
  }
  &__poster {
    width: 80rpx;
    height: 80rpx;
    border-radius: $radius-sm;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 28rpx;
    font-weight: 800;
    color: rgba(255, 255, 255, 0.85);
    flex-shrink: 0;
  }
  &__info {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
  }
  &__name {
    font-size: 26rpx;
    font-weight: 600;
    color: $txt;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  &__meta {
    font-size: 20rpx;
    color: $txt-3;
    margin-top: 4rpx;
  }
  &__actions {
    display: flex;
    gap: 8rpx;
  }
  &__btn {
    width: 56rpx;
    height: 56rpx;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.04);
    color: $txt-2;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24rpx;

    &--active {
      background: rgba(56, 178, 172, 0.25);
      color: $teal-l;
    }
  }
}
</style>
