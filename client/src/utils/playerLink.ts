// @ai-generated true 2026-06-18
// 文件名: utils/playerLink.ts
// 作用: 根据影片 platform + title 生成对应平台的播放/搜索链接，并跨端跳转
//       优先使用各平台的网页搜索页 URL（H5 / 小程序 / App 三端通用）

// @ai-generated true 2026-06-18
// 平台名 → 搜索页 URL 模板，{q} 为影片名占位符
const PLATFORM_URL_MAP: Record<string, string> = {
  'B站': 'https://search.bilibili.com/all?keyword={q}',
  'bilibili': 'https://search.bilibili.com/all?keyword={q}',
  '爱奇艺': 'https://so.iqiyi.com/so/q_{q}',
  '腾讯视频': 'https://v.qq.com/x/search/?q={q}',
  '优酷': 'https://so.youku.com/search_video/q_{q}',
  'Netflix': 'https://www.netflix.com/search?q={q}',
  'Disney+': 'https://www.disneyplus.com/search?q={q}',
  'HBO': 'https://www.hbomax.com/search?q={q}',
}

// @ai-generated true 2026-06-18
// 默认回退到豆瓣搜索（保证任意平台都能跳）
const FALLBACK_URL = 'https://search.douban.com/movie/subject_search?search_text={q}'

/**
 * 根据平台名 + 影片名生成可观看的搜索 URL
 * @param platform 平台中文名，如 "B站" / "Netflix"
 * @param title 影片标题
 */
// @ai-generated true 2026-06-18
export function buildPlayUrl(platform: string, title: string): string {
  const template = PLATFORM_URL_MAP[platform] || FALLBACK_URL
  return template.replace('{q}', encodeURIComponent(title))
}

/**
 * 跨端打开链接
 *  - H5：window.open 新标签页
 *  - 小程序：copy 到剪贴板（小程序不能直接打开外链）
 *  - App：调用系统浏览器打开
 */
// @ai-generated true 2026-06-18
export function openInPlatform(platform: string, title: string): void {
  const url = buildPlayUrl(platform, title)

  // #ifdef H5
  window.open(url, '_blank')
  return
  // #endif

  // #ifdef MP-WEIXIN
  uni.setClipboardData({
    data: url,
    success: () => {
      uni.showToast({
        title: '播放链接已复制，可粘贴到浏览器打开',
        icon: 'none',
        duration: 2500,
      })
    },
  })
  return
  // #endif

  // #ifdef APP-PLUS
  // App 端：尝试调用系统浏览器
  // @ts-ignore
  if (typeof plus !== 'undefined' && plus.runtime?.openURL) {
    // @ts-ignore
    plus.runtime.openURL(url)
  } else {
    uni.showToast({ title: '打开失败', icon: 'none' })
  }
  // #endif
}
