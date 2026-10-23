import axios from 'axios'
import { API_URL } from '@/config'

export const getToken = () => localStorage.getItem('access_token')
export const setTokens = (a: string, r: string) => {
  localStorage.setItem('access_token', a)
  localStorage.setItem('refresh_token', r)
}
export const clearTokens = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
}

let refreshing: Promise<string | null> | null = null
export function refreshToken(): Promise<string | null> {
  refreshing ??= (async () => {
    const rt = localStorage.getItem('refresh_token')
    if (!rt) return null
    try {
      const res = await axios.post(`${API_URL}/api/refresh`, { refresh_token: rt })
      setTokens(res.data.access_token, res.data.refresh_token)
      return res.data.access_token as string
    } catch {
      return null
    }
  })().finally(() => { refreshing = null })
  return refreshing
}

const skip = (url?: string) => !!url && /\/api\/(login|signup|refresh)/.test(url)

axios.interceptors.request.use((cfg) => {
  const t = getToken()
  if (t && cfg.url?.startsWith(API_URL)) cfg.headers.Authorization = `Bearer ${t}`
  return cfg
})

axios.interceptors.response.use(
  (r) => r,
  async (err) => {
    const cfg = err.config
    if (err.response?.status === 401 && cfg && !cfg._retry && !skip(cfg.url) && getToken()) {
      cfg._retry = true
      const t = await refreshToken()
      if (t) {
        cfg.headers.Authorization = `Bearer ${t}`
        return axios(cfg)
      }
      clearTokens()
      window.location.href = '/login' 
    }
    return Promise.reject(err)
  },
)

export async function authFetch(url: string, init: RequestInit = {}) {
  const run = (t: string | null) => {
    const headers = new Headers(init.headers)
    if (t) headers.set('Authorization', `Bearer ${t}`)
    return fetch(url, { ...init, headers })
  }
  let res = await run(getToken())
  if (res.status === 401 && getToken()) {
    const t = await refreshToken()
    if (t) res = await run(t)
  }
  return res
}