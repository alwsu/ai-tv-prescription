# AI 追剧处方 — 安卓 APK 打包指引

> 本指引帮你把项目打包成可以在手机上试用的 Android APK。
> 本机 IP（已写入 config.ts）：`192.168.124.13`

---

## 📋 打包前确认

### ✅ 已为你完成

- [x] [api/config.ts](file:///e:/zhuanqian/trae点子/app/client/src/api/config.ts) — 多环境 BASE_URL 配置（已预填本机 IP）
- [x] [manifest.json](file:///e:/zhuanqian/trae点子/app/client/src/manifest.json) — 应用名/图标/权限/SDK 配置
- [x] [static/app-icon/](file:///e:/zhuanqian/trae点子/app/client/src/static/app-icon) — 17 张应用图标（℞ 金色风格）
- [x] 后端 `0.0.0.0:8000` 监听（已支持局域网访问）

### ⚠️ 你需要做的事

打包必须用 **HBuilderX**（DCloud 官方 IDE），CLI 不支持出 APK。

---

## 🚀 完整打包流程（5 步）

### Step 1 — 启动后端（必须）

```bash
cd e:\zhuanqian\trae点子\app\server
python main.py
```

确认终端显示 `Uvicorn running on http://0.0.0.0:8000`，并在**手机和电脑同一 WiFi** 下，
用手机浏览器访问 `http://192.168.124.13:8000/docs`，能看到 Swagger 页面就成功。

> **如果手机访问不通**：检查 Windows 防火墙，允许 Python.exe 通过专用网络。
> 临时关防火墙测试：`netsh advfirewall set allprofiles state off`（用完记得开回来）

---

### Step 2 — 下载并安装 HBuilderX

1. 去 https://www.dcloud.io/hbuilderx.html
2. 选 **App 开发版**（约 200MB）
3. Windows 直接解压运行 `HBuilderX.exe`，免安装

---

### Step 3 — 把项目导入 HBuilderX

1. HBuilderX 顶部菜单 **文件 → 导入 → 从本地目录导入**
2. 选择目录：`e:\zhuanqian\trae点子\app\client`
3. 等待 HBuilderX 索引完成（左下角显示"就绪"）

---

### Step 4 — 注册并登录 DCloud 账号

云打包必须登录（免费账号即可）：
1. 顶部菜单 **工具 → 登录 / 注册**
2. 用手机号注册，免费

---

### Step 5 — 云打包出 APK

1. 在 HBuilderX 项目根目录右键 → **发行 → 原生 App-云打包**
2. 弹窗里：
   - 平台选 **Android**
   - 包名（应用 ID）：`com.rxdrama.app`（或你自定义）
   - 选 **使用公共测试证书**（DCloud 免费提供，仅供测试）
   - 渠道包 → **打正式包**
   - 不要勾「广告基础包」「广告渠道包」
3. 点 **打包**
4. 等待 5-15 分钟（DCloud 服务器编译）
5. 完成后 HBuilderX 会自动下载 APK 到 `unpackage/release/apk/` 目录

---

## 📱 安装到手机

把生成的 APK 拷贝到手机或微信发给自己，手机点开安装。
**首次安装可能需要在系统设置里允许"未知来源应用"。**

---

## ✅ 试用确认清单

打开 APP 后逐项检查：

- [ ] 能看到登录页（℞ 金色 logo）
- [ ] 点"💊 一键体验"能进首页
- [ ] 能选心情和时间
- [ ] 点"生成处方"能看到推荐影片
- [ ] 点"去 XX 观看"能跳转浏览器
- [ ] 历史/我的 Tab 能正常切换
- [ ] "我的"页能看到统计数据 → 说明 API 通了

---

## 🔧 常见问题

### Q1: APK 装好但是接口都失败
→ 后端没启动，或手机不在同一 WiFi，或防火墙挡住了。
→ 用手机浏览器访问 `http://192.168.124.13:8000/docs` 验证。

### Q2: 想换电脑或换 WiFi
→ 修改 [api/config.ts](file:///e:/zhuanqian/trae点子/app/client/src/api/config.ts) 里的 `LAN_URL` 为新 IP，重新打包。
→ 查 IP：Win+R → cmd → `ipconfig` → 看 IPv4 地址。

### Q3: 想给朋友试用，但他不在我家 WiFi
→ 必须把后端部署到公网（云服务器），把 `PROD_URL` 改为公网域名。
→ 推荐：阿里云/腾讯云轻量服务器（约 30 元/月），或免费的 Render.com / Railway.app。

### Q4: 不想注册 DCloud 账号
→ 唯一替代方案是离线打包，需要自己装 Android Studio + Gradle，
   流程长且复杂，**不推荐**。云打包是最简单的方式。

### Q5: 想打 iOS 版（iPhone）
→ 需要 Apple 开发者账号（688 元/年），证书申请流程复杂。
→ 流程类似，云打包时选 iOS 即可。

---

## 📦 项目目录速查

```
app/
├── server/                ← 后端 (启动: python main.py)
│   └── rx_drama.db        ← SQLite 数据库（自动创建）
└── client/                ← 前端 (HBuilderX 导入这个目录)
    ├── src/
    │   ├── api/config.ts  ← BASE_URL 配置
    │   ├── manifest.json  ← App 配置
    │   ├── pages.json     ← 路由
    │   └── static/
    │       ├── app-icon/  ← 17 张应用图标
    │       └── tabbar/    ← 6 张底部图标
    └── package.json
```

---

## 🎯 推荐打包流程时间预估

| 步骤 | 耗时 |
|------|------|
| 装 HBuilderX | 5 分钟 |
| 注册 DCloud 账号 | 2 分钟 |
| 项目导入 | 1 分钟 |
| 云打包等待 | 5-15 分钟 |
| 安装到手机 | 1 分钟 |
| **总计** | **约 15-25 分钟** |

打包完成后，APK 文件大小约 **15-20 MB**。
