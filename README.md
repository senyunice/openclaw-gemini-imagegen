# OpenClaw + Gemini 图片生成套件 / Image Generation Suite

> 🤖 AI 全自动图片生成 · 描述即生成 · 无需人工干预

---

## 🌍 选择语言 / Choose Language

| 🇨🇳 [中文详细介绍 →](docs/index-cn.html) | 🇺🇸 [English Details →](docs/index-en.html) |
|:---:|:---:|
| 中文海报 + 中文文档 | English Poster + English Docs |

---

## ⚡ 快速预览 Quick Preview

![中文海报](poster.png) ![English Poster](poster-en.png)

---

## 🚀 特性 Features

| | |
|---|---|
| 🖼️ **全自动流程** / Fully Automated | 一句话 = 一张图 / One prompt = One image |
| 🔍 **Chrome 缓存监控** / Cache Monitor | 自动捕获无需下载 / Auto-capture, no manual download |
| 🧠 **MCP 图片审核** / MCP Review | AI 质量把关 / AI quality check |
| 🔒 **独立 Profile** / Isolated Profile | 与日常 Chrome 完全隔离 / Separate from daily Chrome |
| 📚 **完整文档** / Complete Docs | 5 分钟上手 / Ready in 5 minutes |

## 工作流程 / Workflow

```
🚀 Launch Chrome → 🌐 Open Gemini → ✍️ AI Types Prompt
  → ✨ Gemini Generates → 📥 Auto-Download → 🧠 MCP Review → Send
```

---

## 📁 包含内容 / Contents

| 文件 | 说明 |
|---|---|
| `gemini-image-SKILL.md` | Gemini 生图技能 |
| `wait_download_cache.py` | Chrome 缓存监控脚本 |
| `gemini-image 完整流程.md` | 详细操作步骤 |
| `browser-SETUP.md` | 浏览器配置指南 |
| `minimax-mcp-SETUP.md` | MiniMax MCP 图片审核配置 |
| `问题排查指南.md` | 常见问题汇总 |

---

## 🌐 在线预览 / Live Preview

- 🇨🇳 [中文详情页](docs/index-cn.html) — 中文字体 + 中文海报
- 🇺🇸 [English Detail Page](docs/index-en.html) — English font + English poster

> ⚠️ 详情页需启用 GitHub Pages（Settings → Pages → Source: /docs）

---

## ⚙️ 快速配置 / Quick Setup

### Windows

```powershell
# 1. 创建 Chrome 配置目录
New-Item -Path "C:\Users\<用户名>\AppData\Local\Google\Chrome\OpenClaw" -ItemType Directory -Force

# 2. 启动 Chrome
Start-Process "C:\Program Files\Google\Chrome\Application\chrome.exe" `
  -ArgumentList "--user-data-dir=C:\Users\<用户名>\AppData\Local\Google\Chrome\OpenClaw","--remote-debugging-port=9222"

# 3. 在 Chrome 中打开 gemini.google.com 并登录
```

### 3. 复制文件

```powershell
# 复制 SKILL 文件
copy gemini-image-SKILL.md "$env:USERPROFILE\.openclaw\workspace\skills\gemini-image\SKILL.md"

# 复制脚本
copy wait_download_cache.py "$env:USERPROFILE\.openclaw\workspace\wait_download_cache.py"
```

---

*Created by senyunice · 2026-03-23*
