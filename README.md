# AI 追剧处方（Rx Drama）

按心情和碎片时间，AI 为你开方推片。

## 项目结构

```
app/
├── server/   ← FastAPI + SQLite 后端
└── client/   ← uni-app + Vue3 + TS 前端
```

## 后端启动

```bash
cd app/server
pip install -r requirements.txt
python main.py
```

启动后访问：
- http://localhost:8000 — 健康检查
- http://localhost:8000/docs — Swagger API 文档

## 前端启动（H5 模式）

```bash
cd app/client
npm install
npm run dev:h5
```

启动后访问：http://localhost:5173

## 核心 API

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/recommend | 心情推荐 |
| GET  | /api/history | 历史列表 |
| POST | /api/history | 新增记录 |
| PUT  | /api/history/{id}/watch | 标记已看 |
| DELETE | /api/history/{id} | 删除记录 |
| GET  | /api/preferences | 获取偏好 |
| PUT  | /api/preferences | 更新偏好 |
| GET  | /api/stats | 统计数据 |

## 心情标识

| ID | 中文 | Emoji |
|----|------|-------|
| relax | 想放松 | 😴 |
| heal | 想治愈 | 🤗 |
| excite | 想刺激 | 🔥 |
| brain | 想烧脑 | 🧠 |
| release | 想解压 | 😭 |
| together | 一起看 | 👥 |

## 时间档位

15 / 30 / 60 / 120 / 180 分钟
