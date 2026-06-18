// @ai-generated true 2026-06-18
// 文件名: main.ts
// 作用: uni-app 入口 - 创建 Vue 实例、挂载 Pinia
import { createSSRApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'

export function createApp() {
  const app = createSSRApp(App)
  app.use(createPinia())
  return { app }
}
