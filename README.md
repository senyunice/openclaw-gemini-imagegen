![OpenClaw + Gemini 图片生成套件](poster.png)

# OpenClaw + Gemini 图片生成套件

> 🤖 AI 全自动图片生成 · 描述即生成 · 无需人工干预

---

## 简介

给 OpenClaw AI 助手使用的 Gemini 网页版图片生成完整解决方案。包含所有配置文件、脚本和使用说明。

---

## 包含内容

| 文件 | 说明 |
|------|------|
| `gemini-image-SKILL.md` | Gemini 生图技能 |
| `gemini-image 完整流程.md` | 详细操作步骤 |
| `browser-SETUP.md` | 浏览器配置指南 |
| `minimax-mcp-SETUP.md` | MiniMax MCP 图片审核配置 |
| `wait_download_cache.py` | Chrome 缓存监控脚本 |
| `问题排查指南.md` | 21个常见问题及解决方案 |
| `快速参考.txt` | 速查卡 |

---

## 快速配置（5分钟）

### 第一步：复制 Skill 文件
将 `gemini-image-SKILL.md` 复制到：
```
C:\Users\<用户名>\.openclaw\workspace\skills\gemini-image\SKILL.md
```
> 如果 `skills` 目录不存在，先手动创建整个路径。

### 第二步：复制下载脚本
将 `wait_download_cache.py` 复制到：
```
C:\Users\<用户名>\.openclaw\workspace\wait_download_cache.py
```

### 第三步：创建 Chrome 配置目录
在 PowerShell 运行：
```powershell
New-Item -Path "C:\Users\<用户名>\AppData\Local\Google\Chrome\OpenClaw" -ItemType Directory -Force
```

### 第四步：启动 Chrome 并登录
在 PowerShell 运行：
```powershell
Start-Process "C:\Program Files\Google\Chrome\Application\chrome.exe" -ArgumentList "--user-data-dir=C:\Users\<用户名>\AppData\Local\Google\Chrome\OpenClaw","--remote-debugging-port=9222"
```
然后在 Chrome 中打开 `https://gemini.google.com` 并扫码/账号登录。

> 以后每次使用会自动记住登录状态，除非删除配置目录。

### 第五步：验证配置
重启 Chrome 后，确认 Gemini 页面右上角显示你的 Google 账号，即配置成功。

---

## 核心工作流程

```
用户请求 → 启动 Chrome → 打开 Gemini → 输入提示词 → 发送
     ↓
轮询检查图片（每3秒，最长1分钟）
     ↓
图片出现 → 点击下载完整尺寸图片
     ↓
Chrome 缓存监控（每5秒，最长3分钟）
     ↓
检测到文件 → 等待大小稳定 → 自动判断类型 → 保存到 media
     ↓
MiniMax MCP 审核 → 发送给用户
```

---

## 关键路径

| 项目 | 路径 |
|------|------|
| Chrome 配置目录 | `C:\Users\<用户名>\AppData\Local\Google\Chrome\OpenClaw` |
| Chrome 缓存目录 | `C:\Users\<用户名>\AppData\Local\Google\Chrome\OpenClaw\Default\Cache\Cache_Data` |
| 图片保存目录 | `C:\Users\<用户名>\.openclaw\media\` |
| 下载监控脚本 | `C:\Users\<用户名>\.openclaw\workspace\wait_download_cache.py` |
| Skill 文件 | `C:\Users\<用户名>\.openclaw\workspace\skills\gemini-image\SKILL.md` |
| Chrome 调试端口 | 9222 |

---

## 所需权限

- Chrome 浏览器控制（browser MCP 工具）
- Python 脚本执行
- 文件系统读写
- MiniMax MCP（图片审核）

---

## 日常使用

配置完成后，以后每次生图只需：
1. 启动专用 Chrome（含调试端口）
2. 告诉 AI 助手"生图 xxx"

AI 会自动执行完整流程。

---

*创建于: 2026-03-23 · [🇺🇸 English Version](README-en.md)*
