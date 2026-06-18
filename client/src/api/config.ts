// @ai-generated true 2026-06-18
// 文件名: api/config.ts
// 作用: API Base URL 配置 - 支持开发/生产/局域网三种场景
//
// 使用说明：
// 1. 开发模式（H5 浏览器调试）：使用 LOCAL_URL，前后端都在本机
// 2. 局域网模式（手机扫码体验）：把 LAN_IP 改成你的电脑局域网 IP
// 3. 生产模式（部署后端到公网）：把 PROD_URL 改成你的服务器域名
//
// 切换方式：修改下方 ACTIVE_ENV 常量

// @ai-generated true 2026-06-18
// 各环境的 BASE_URL
const LOCAL_URL = 'http://localhost:8000'
const LAN_URL = 'http://192.168.124.13:8000'  // ← 打包前改成你的电脑局域网 IP
const PROD_URL = 'https://your-domain.com'    // ← 部署后改成线上域名

// @ai-generated true 2026-06-18
// 当前激活的环境：开发改 'local'，打包 APK 改 'lan' 或 'prod'
type Env = 'local' | 'lan' | 'prod'

// #ifdef H5
// H5 模式默认走 local（浏览器开发）
const ACTIVE_ENV: Env = 'local'
// #endif

// #ifdef APP-PLUS
// App 模式默认走 lan（手机访问电脑后端），上线时改 prod
const ACTIVE_ENV: Env = 'lan'
// #endif

// #ifdef MP-WEIXIN
// 小程序必须 https，走 prod
const ACTIVE_ENV: Env = 'prod'
// #endif

// @ai-generated true 2026-06-18
const URL_MAP: Record<Env, string> = {
  local: LOCAL_URL,
  lan: LAN_URL,
  prod: PROD_URL,
}

export const BASE_URL = URL_MAP[ACTIVE_ENV]
