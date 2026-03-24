![OpenClaw + Gemini 图片生成套件](poster.png)

# OpenClaw + Gemini 图片生成套件

> 🤖 AI 全自动图片生成 · 描述即生成 · 去水印全自动化 · 无需人工干预

---

## 简介

给 OpenClaw AI 助手使用的 Gemini 网页版图片生成完整解决方案。包含所有配置文件、脚本和使用说明。

---

## 包含内容

| 文件 | 说明 |
|------|------|
| `gemini-image-SKILL.md` | Gemini 生图技能（含去水印流程） |
| `browser-SETUP.md` | 浏览器配置指南 |
| `minimax-mcp-SETUP.md` | MiniMax MCP 图片审核配置 |
| `wait_download_cache.py` | Chrome 缓存监控脚本 |
| `lama_inpaint.py` | **Lama AI 去水印脚本（首选）** |
| `remove_watermark_cv.py` | **OpenCV 去水印脚本（备用）** |
| `问题排查指南.md` | 常见问题及解决方案 |
| `快速参考.txt` | 速查卡 |

---

## 快速配置（5分钟）

### 第一步：复制 Skill 文件
将 `gemini-image-SKILL.md` 复制到：
```
C:\Users\<用户名>\.openclaw\workspace\skills\gemini-image\SKILL.md
```

### 第二步：复制脚本文件
将以下文件复制到：
```
C:\Users\<用户名>\.openclaw\workspace\
```
- `wait_download_cache.py`（Chrome 缓存监控）
- `lama_inpaint.py`（Lama AI 去水印）
- `remove_watermark_cv.py`（OpenCV 去水印备用）

### 第三步：创建 Chrome 配置目录
```powershell
New-Item -Path "C:\Users\<用户名>\AppData\Local\Google\Chrome\OpenClaw" -ItemType Directory -Force
```

### 第四步：启动 Chrome 并登录
```powershell
Start-Process "C:\Program Files\Google\Chrome\Application\chrome.exe" -ArgumentList "--user-data-dir=C:\Users\<用户名>\AppData\Local\Google\Chrome\OpenClaw","--remote-debugging-port=9222"
```
然后打开 `https://gemini.google.com` 并登录 Google 账号。

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
Lama AI 去水印
     ↓
MCP 审核右下角（水印干净？）
     ↓
不干净 → 重新去水印 → 再次审核
干净 ↓
MiniMax MCP 内容审核 → 发送给用户
```

---

## 关键路径

| 项目 | 路径 |
|------|------|
| Chrome 配置目录 | `C:\Users\<用户名>\AppData\Local\Google\Chrome\OpenClaw` |
| Chrome 缓存目录 | `C:\Users\<用户名>\AppData\Local\Google\Chrome\OpenClaw\Default\Cache\Cache_Data` |
| 图片保存目录 | `C:\Users\<用户名>\.openclaw\media\` |
| Lama 去水印脚本 | `C:\Users\<用户名>\.openclaw\workspace\lama_inpaint.py` |
| OpenCV 去水印脚本 | `C:\Users\<用户名>\.openclaw\workspace\remove_watermark_cv.py` |
| 下载监控脚本 | `C:\Users\<用户名>\.openclaw\workspace\wait_download_cache.py` |
| Skill 文件 | `C:\Users\<用户名>\.openclaw\workspace\skills\gemini-image\SKILL.md` |
| Chrome 调试端口 | 9222 |

---

## 去水印工具说明

### 首选：Lama Inpainting（本地 AI，效果最好）

```bash
python lama_inpaint.py <输入图片> <输出图片>
```

- 使用本地深度学习模型（LLaMA）智能填充
- 自动识别右下角水印区域
- 水印区域：96×96（分辨率>1024）或 48×48
- 无需网络，完全离线运行
- 处理后用 MCP 审核确认无残留

### 备用：OpenCV TELEA（传统算法）

```bash
python remove_watermark_cv.py <输入图片> <输出图片>
```

- 使用 OpenCV 智能填充算法
- 速度较快但效果略逊于 Lama
- 当 Lama 多次不干净时使用

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

AI 会自动执行完整流程（生成 → 下载 → 去水印 → 审核 → 发送）。

---

*创建于: 2026-03-23 · 更新于: 2026-03-24 · [🇺🇸 English Version](README-en.md)*
