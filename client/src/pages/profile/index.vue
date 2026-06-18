<script setup lang="ts">
// @ai-generated true 2026-06-18
// 文件名: pages/profile/index.vue
// 作用: 个人中心 - 统计、偏好、设置、清除数据
import { ref } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { useUserStore } from '@/stores/user'
import { usePrescriptionStore } from '@/stores/prescription'
import GenrePicker from '@/components/GenrePicker.vue'

const userStore = useUserStore()
const rxStore = usePrescriptionStore()

// @ai-generated true 2026-06-18
// 弹窗状态
const pickerVisible = ref(false)
const pickerType = ref<'like' | 'dislike'>('like')

// @ai-generated true 2026-06-18
onShow(async () => {
  try {
    await Promise.all([userStore.loadStats(), userStore.loadPreferences()])
  } catch (e) {}
})

// @ai-generated true 2026-06-18
// 打开"喜欢的类型"编辑弹窗
function onEditLiked() {
  pickerType.value = 'like'
  pickerVisible.value = true
}

// @ai-generated true 2026-06-18
// 打开"不喜欢的类型"编辑弹窗
function onEditDisliked() {
  pickerType.value = 'dislike'
  pickerVisible.value = true
}

// @ai-generated true 2026-06-18
// 删除单个标签
async function onRemoveTag(kind: 'like' | 'dislike', tag: string) {
  const next = { ...userStore.preferences }
  if (kind === 'like') {
    next.liked_genres = next.liked_genres.filter((g) => g !== tag)
  } else {
    next.disliked_genres = next.disliked_genres.filter((g) => g !== tag)
  }
  try {
    await userStore.savePreferences(next)
    uni.showToast({ title: '已移除', icon: 'none' })
  } catch (e) {
    uni.showToast({ title: '保存失败', icon: 'none' })
  }
}

// @ai-generated true 2026-06-18
// 弹窗确认 -> 保存到后端
async function onPickerConfirm(list: string[]) {
  const next = { ...userStore.preferences }
  if (pickerType.value === 'like') {
    next.liked_genres = list
  } else {
    next.disliked_genres = list
  }
  try {
    await userStore.savePreferences(next)
    uni.showToast({ title: '已保存', icon: 'success' })
  } catch (e) {
    uni.showToast({ title: '保存失败', icon: 'none' })
  }
}

// @ai-generated true 2026-06-18
// 通用：保存单项设置
async function saveOne<K extends keyof typeof userStore.preferences>(
  key: K,
  value: (typeof userStore.preferences)[K]
) {
  const next = { ...userStore.preferences, [key]: value }
  try {
    await userStore.savePreferences(next)
  } catch (e) {
    uni.showToast({ title: '保存失败', icon: 'none' })
  }
}

// @ai-generated true 2026-06-18
// 切换深色模式
function onToggleDarkMode(e: any) {
  const v = e.detail.value ? 1 : 0
  saveOne('dark_mode', v)
  userStore.applyTheme(v)
  uni.showToast({ title: v ? '深色模式已开启' : '已切换浅色', icon: 'none' })
}

// @ai-generated true 2026-06-18
// 切换通知推送
function onToggleNotify(e: any) {
  const v = e.detail.value ? 1 : 0
  saveOne('notifications', v)
  uni.showToast({ title: v ? '通知已开启' : '通知已关闭', icon: 'none' })
}

// @ai-generated true 2026-06-18
// 修改每日推荐提醒时间
function onTimeChange(e: any) {
  const v: string = e.detail.value
  saveOne('daily_remind_time', v)
  uni.showToast({ title: `提醒时间设为 ${v}`, icon: 'none' })
}

// @ai-generated true 2026-06-18
function onClearAll() {
  uni.showModal({
    title: '清除所有数据',
    content: '将清空所有处方记录，此操作不可恢复',
    confirmColor: '#e85d75',
    success: async ({ confirm }) => {
      if (confirm) {
        await rxStore.clearAll()
        await userStore.loadStats()
        uni.showToast({ title: '已清空', icon: 'none' })
      }
    },
  })
}
</script>

<template>
  <view class="page">
    <text class="page__title">👤 我的</text>

    <!-- 统计卡片 -->
    <view class="page__stats">
      <view class="page__stat">
        <text class="page__stat-val text-gold">{{ userStore.stats.total_prescriptions }}</text>
        <text class="page__stat-label">总处方</text>
      </view>
      <view class="page__stat">
        <text class="page__stat-val text-teal">{{ userStore.stats.watched_count }}</text>
        <text class="page__stat-label">已看完</text>
      </view>
      <view class="page__stat">
        <text class="page__stat-val text-red">{{ userStore.stats.watch_rate }}%</text>
        <text class="page__stat-label">完看率</text>
      </view>
    </view>

    <!-- 类型偏好 -->
    <text class="page__section">类型偏好</text>
    <view class="rx-card">
      <view class="page__pref-row">
        <text class="page__pref-label text-gold">喜欢</text>
        <text class="page__pref-edit" @tap="onEditLiked">编辑</text>
      </view>
      <view class="page__tags">
        <text
          v-for="g in userStore.preferences.liked_genres"
          :key="g"
          class="page__tag page__tag--like"
          @tap="onRemoveTag('like', g)"
        >
          ❤ {{ g }} ✕
        </text>
        <text class="page__tag page__tag--add" @tap="onEditLiked">
          + 添加
        </text>
      </view>

      <view class="page__pref-row" style="margin-top: 24rpx">
        <text class="page__pref-label text-red">不喜欢</text>
        <text class="page__pref-edit" @tap="onEditDisliked">编辑</text>
      </view>
      <view class="page__tags">
        <text
          v-for="g in userStore.preferences.disliked_genres"
          :key="g"
          class="page__tag page__tag--dis"
          @tap="onRemoveTag('dislike', g)"
        >
          ✕ {{ g }}
        </text>
        <text class="page__tag page__tag--add" @tap="onEditDisliked">
          + 添加
        </text>
      </view>
    </view>

    <!-- 设置 -->
    <text class="page__section">设置</text>
    <view class="rx-card">
      <view class="page__row">
        <text>深色模式</text>
        <switch
          :checked="!!userStore.preferences.dark_mode"
          color="#d4a853"
          style="transform: scale(0.8)"
          @change="onToggleDarkMode"
        />
      </view>
      <view class="page__row">
        <text>通知推送</text>
        <switch
          :checked="!!userStore.preferences.notifications"
          color="#d4a853"
          style="transform: scale(0.8)"
          @change="onToggleNotify"
        />
      </view>
      <picker
        mode="time"
        :value="userStore.preferences.daily_remind_time"
        @change="onTimeChange"
      >
        <view class="page__row page__row--clickable">
          <text>每日推荐提醒</text>
          <text class="page__row-value">
            {{ userStore.preferences.daily_remind_time }} ›
          </text>
        </view>
      </picker>
      <view class="page__row">
        <text>版本</text>
        <text class="text-3">1.0.0</text>
      </view>
    </view>

    <button class="page__clear" @tap="onClearAll">🗑 清除所有数据</button>

    <!-- 类型偏好编辑弹窗 -->
    <GenrePicker
      v-model:visible="pickerVisible"
      :title="pickerType === 'like' ? '编辑喜欢的类型' : '编辑不喜欢的类型'"
      :selected="
        pickerType === 'like'
          ? userStore.preferences.liked_genres
          : userStore.preferences.disliked_genres
      "
      :excluded="
        pickerType === 'like'
          ? userStore.preferences.disliked_genres
          : userStore.preferences.liked_genres
      "
      :variant="pickerType"
      @confirm="onPickerConfirm"
    />
  </view>
</template>

<style scoped lang="scss">
/* @ai-generated true 2026-06-18 */
@import "@/styles/variables.scss";

.page {
  padding: 56rpx 32rpx 100rpx;
  min-height: 100vh;
  background: $bg;

  &__title {
    display: block;
    font-size: 36rpx;
    font-weight: 800;
    color: $txt;
    margin-bottom: 32rpx;
  }
  &__stats {
    display: flex;
    gap: 16rpx;
    margin-bottom: 32rpx;
  }
  &__stat {
    flex: 1;
    background: $bg-card;
    border-radius: $radius-md;
    border: 1rpx solid $bdr;
    padding: 28rpx 16rpx;
    text-align: center;
  }
  &__stat-val {
    display: block;
    font-size: 48rpx;
    font-weight: 800;
  }
  &__stat-label {
    display: block;
    font-size: 20rpx;
    color: $txt-3;
    margin-top: 4rpx;
  }
  &__section {
    display: block;
    font-size: 26rpx;
    font-weight: 700;
    color: $txt;
    margin: 36rpx 0 16rpx;
  }
  &__pref-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12rpx;
  }
  &__pref-edit {
    font-size: 22rpx;
    color: $gold;
    padding: 4rpx 16rpx;
    border-radius: 16rpx;
    background: rgba(212, 168, 83, 0.08);
  }
  &__pref-label {
    display: block;
    font-size: 20rpx;
    letter-spacing: 4rpx;
  }
  &__pref-empty {
    font-size: 22rpx;
    color: $txt-3;
  }
  &__tags {
    display: flex;
    flex-wrap: wrap;
    gap: 12rpx;
  }
  &__tag {
    padding: 8rpx 20rpx;
    border-radius: 28rpx;
    font-size: 22rpx;
    transition: all 0.2s ease;
    &:active {
      transform: scale(0.94);
    }
    &--like {
      background: rgba(56, 178, 172, 0.1);
      color: $teal;
    }
    &--dis {
      background: rgba(232, 93, 117, 0.06);
      color: $red;
      text-decoration: line-through;
      opacity: 0.85;
    }
    &--add {
      background: transparent;
      border: 1rpx dashed $bdr;
      color: $txt-3;
    }
  }
  &__row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12rpx 0;
    font-size: 24rpx;
    color: $txt-2;
    border-bottom: 1rpx solid $bdr;
    min-height: 72rpx;
    &:last-child { border: none; }

    &--clickable {
      transition: opacity 0.15s;
      &:active { opacity: 0.6; }
    }
  }
  &__row-value {
    color: $gold;
    font-size: 24rpx;
    font-weight: 600;
  }
  &__clear {
    margin-top: 32rpx;
    width: 100%;
    height: 80rpx;
    background: transparent;
    border: 1rpx solid rgba(232, 93, 117, 0.3);
    color: $red;
    border-radius: $radius-md;
    font-size: 24rpx;
  }
}
</style>
