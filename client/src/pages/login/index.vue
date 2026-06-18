<script setup lang="ts">
// @ai-generated true 2026-06-18
// 文件名: pages/login/index.vue
// 作用: 登录页 (MVP Demo - 一键体验)

// @ai-generated true 2026-06-18
function onEnterDemo() {
  // 写入引导完成标记，下次启动直接进首页
  uni.setStorageSync('onboarded', true)
  uni.reLaunch({ url: '/pages/index/index' })
}
</script>

<template>
  <view class="page">
    <view class="page__brand">
      <text class="page__rx rx-symbol">℞</text>
      <text class="page__title">追剧处方</text>
      <text class="page__sub">按心情和碎片时间，AI 为你开方推片</text>
    </view>
    <button class="rx-btn rx-btn--primary page__btn" @tap="onEnterDemo">
      💊 一键体验
    </button>
    <text class="page__hint">Demo 模式 · 无需登录</text>
  </view>
</template>

<style scoped lang="scss">
/* @ai-generated true 2026-06-18 */
@import "@/styles/variables.scss";

.page {
  min-height: 100vh;
  background: $bg;
  padding: 200rpx 64rpx 80rpx;
  display: flex;
  flex-direction: column;
  align-items: center;

  &__brand {
    text-align: center;
    margin-bottom: 100rpx;
  }
  &__rx {
    display: block;
    font-size: 160rpx;
    line-height: 1;
  }
  &__title {
    display: block;
    font-size: 48rpx;
    font-weight: 800;
    letter-spacing: 12rpx;
    margin-top: 16rpx;
  }
  &__sub {
    display: block;
    font-size: 22rpx;
    color: $txt-2;
    margin-top: 16rpx;
    letter-spacing: 2rpx;
  }
  &__btn {
    width: 100%;
  }
  &__hint {
    margin-top: 24rpx;
    font-size: 22rpx;
    color: $txt-3;
  }
}
</style>
