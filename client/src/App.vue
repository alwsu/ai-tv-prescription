<script setup lang="ts">
// @ai-generated true 2026-06-18
// 文件名: App.vue
// 作用: 应用根组件 - 全局生命周期、主题色注入、深浅色切换
import { onLaunch } from '@dcloudio/uni-app'
import { useUserStore } from '@/stores/user'

onLaunch(async () => {
  console.log('[Rx Drama] App Launched')
  // @ai-generated true 2026-06-18
  // 首次启动跳到登录/欢迎页（写入 onboarded 标记后下次跳过）
  const onboarded = uni.getStorageSync('onboarded')
  if (!onboarded) {
    // reLaunch 避免和 tabBar 路由冲突
    setTimeout(() => {
      uni.reLaunch({ url: '/pages/login/index' })
    }, 50)
  }

  // @ai-generated true 2026-06-18
  // 拉取用户偏好并应用主题
  const userStore = useUserStore()
  try {
    await userStore.loadPreferences()
    userStore.applyTheme(userStore.preferences.dark_mode)
  } catch (e) {
    userStore.applyTheme(1)
  }
})
</script>

<style lang="scss">
/* @ai-generated true 2026-06-18 */
@import "@/styles/variables.scss";
@import "@/styles/global.scss";

/* 深色主题（默认） */
:root,
:root[data-theme='dark'] {
  --bg: #060610;
  --bg-panel: #0c0c1a;
  --bg-card: #111125;
  --bg-phone: #0a0a18;

  --gold: #d4a853;
  --gold-l: #f0d080;
  --gold-d: #8a6e2f;
  --teal: #38b2ac;
  --teal-l: #5eeadb;
  --red: #e85d75;

  --txt: #eae6dd;
  --txt-2: #9a96a6;
  --txt-3: #5c586e;

  --bdr: rgba(255, 255, 255, 0.06);
}

/* 浅色主题 */
:root[data-theme='light'] {
  --bg: #f8f6f1;
  --bg-panel: #ffffff;
  --bg-card: #ffffff;
  --bg-phone: #ffffff;

  --gold: #b8893a;
  --gold-l: #d4a853;
  --gold-d: #8a6624;
  --teal: #2c8a85;
  --teal-l: #38b2ac;
  --red: #d94865;

  --txt: #1a1a26;
  --txt-2: #5c586e;
  --txt-3: #9a96a6;

  --bdr: rgba(0, 0, 0, 0.08);
}

page {
  background: var(--bg);
  color: var(--txt);
  font-family: -apple-system, 'PingFang SC', 'Microsoft YaHei', 'Helvetica Neue', Helvetica, sans-serif;
  font-size: 28rpx;
  line-height: 1.5;
  transition: background 0.3s ease, color 0.3s ease;
}
</style>
