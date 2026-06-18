// @ai-generated true 2026-06-18
// 文件名: api/request.ts
// 作用: 统一的 uni.request 封装 - 拦截器、错误提示、Base URL

import { BASE_URL } from './config'

interface RequestOptions {
  url: string
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE'
  data?: Record<string, any>
  showError?: boolean
}

// @ai-generated true 2026-06-18
export function request<T = any>(options: RequestOptions): Promise<T> {
  const { url, method = 'GET', data, showError = true } = options

  return new Promise<T>((resolve, reject) => {
    uni.request({
      url: BASE_URL + url,
      method,
      data,
      header: { 'Content-Type': 'application/json' },
      timeout: 15000,
      success: (res) => {
        const status = res.statusCode
        if (status >= 200 && status < 300) {
          resolve(res.data as T)
        } else {
          const message =
            (res.data as any)?.detail || `请求失败（${status}）`
          if (showError) {
            uni.showToast({ title: message, icon: 'none', duration: 2000 })
          }
          reject(new Error(message))
        }
      },
      fail: (err) => {
        // @ai-generated true 2026-06-18
        // 网络层失败（最常见：后端没启动 / 跨域 / DNS）
        const raw = err.errMsg || ''
        let friendly = '网络异常，请检查后端是否启动'
        if (raw.includes('timeout')) friendly = '请求超时，请检查网络'
        else if (raw.includes('fail')) friendly = `连接服务器失败（${BASE_URL}）`
        if (showError) {
          uni.showToast({
            title: friendly,
            icon: 'none',
            duration: 2500,
          })
        }
        console.error('[API] 请求失败:', url, raw)
        reject(new Error(friendly))
      },
    })
  })
}

export const http = {
  get: <T = any>(url: string, params?: Record<string, any>) =>
    request<T>({ url, method: 'GET', data: params }),
  post: <T = any>(url: string, data?: Record<string, any>) =>
    request<T>({ url, method: 'POST', data }),
  put: <T = any>(url: string, data?: Record<string, any>) =>
    request<T>({ url, method: 'PUT', data }),
  del: <T = any>(url: string, data?: Record<string, any>) =>
    request<T>({ url, method: 'DELETE', data }),
}
