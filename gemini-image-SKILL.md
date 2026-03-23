# Gemini 图片生成技能 - 完整工作流

## 功能
使用 Gemini 网页版生成 AI 图片，完成后自动审核并发送给用户

## 核心流程
1. 打开 Gemini → 2. 点击制作图片 → 3. 输入描述（必须加前缀）→ 4. 发送 → 5. **轮询检查图片是否生成（3秒/次，最长1分钟）** → 6. **点击下载完整尺寸图片** → 7. **Chrome缓存轮询监控（每5秒/次，最长3分钟），自动判断文件类型** → 8. **MiniMax MCP 审核图片** → 9. 审核通过后发送给用户

---

## 详细步骤

### 步骤0: 启动专用 Chrome（如未运行）
**每次必须从步骤 1 开始，不能跳过！**

#### 1. 杀掉所有 Chrome 进程
```powershell
Stop-Process -Name chrome -Force -ErrorAction SilentlyContinue
```

#### 2. 启动专用 Chrome
```powershell
Start-Process 'C:\Program Files\Google\Chrome\Application\chrome.exe' -ArgumentList '--user-data-dir=%USERPROFILE%\AppData\Local\Google\Chrome\OpenClaw','--remote-debugging-port=9222'
```

#### 3. 等待启动
```powershell
Start-Sleep -Seconds 5
```

#### 4. 验证端口
```powershell
Invoke-WebRequest -Uri 'http://localhost:9222/json/version' -TimeoutSec 5
```

#### 5. 连接浏览器
```
browser action=open target=host url=https://gemini.google.com/app
```

### 步骤1: 打开Gemini
```
URL: https://gemini.google.com/app
```
**等待 10 秒让页面加载完成**

### 步骤2: 点击"制作图片"按钮
```
引用: e10 (🖼️ 制作图片)
```

### 步骤3: 选择风格(可选)
- 绚彩/油画/素描/电影效果等

### 步骤4: 输入图片描述（必须加前缀）
**⚠️ 关键：在描述前面必须加 "Generate Image" 或 "生成图片"，否则图片生成会被禁用！**

```
引用: e8 (文本框)
前缀: "Generate Image " 或 "生成图片 "
建议: 使用英文描述获得更好效果
示例: Generate Image A modern AI design service poster, colorful gradient background, robot designing graphics, futuristic style
```

### 步骤5: 发送
```
引用: e14 (发送按钮)
```

### 步骤6: 轮询检查图片是否生成
- **每 3 秒执行一次 snapshot，检查页面中是否有生成的图片元素**
- 最长轮询时间：**1 分钟**（20 次轮询）
- 条件：页面 DOM 中出现 `<img>` 元素且 `src` 包含 `lh3.googleusercontent.com` 且宽度 > 200px
- 出现图片后立即进入下一步
- **1 分钟内未出现图片则重新发送请求**

### 步骤7: 下载图片

#### 标准方法（每次都这样做）

1. 点击"下载完整尺寸的图片"按钮（ref=e17 或 e18）
2. **立即执行**缓存监控脚本：

```powershell
python "%USERPROFILE%\.openclaw\workspace\wait_download_cache.py"
```

**缓存监控逻辑：**
- 监控 Chrome 缓存目录 `Cache_Data`（每 5 秒轮询一次）
- 检测到新文件后，持续检查文件大小是否稳定
- 大小连续不变且 >10KB → 认为下载完成
- 自动读取文件头判断类型（PNG/JPEG）
- 自动复制到 `media\gemini_output.png` 或 `.jpg`
- 最长等待 3 分钟

**文件头自动判断：**
- PNG：`89 50 4E 47 0D 0A 1A 0A` → `.png`
- JPEG：`FF D8 FF` → `.jpg`
- 其他 → 默认 `.png`

**下载完成后再进入下一步（MiniMax MCP 审核）**

#### 备用下载方案（仅在缓存监控超过 3 分钟仍未检测到新文件时启用）
```python
import os, time

download_dir = r"%USERPROFILE%\Downloads"
target_files = set(os.listdir(download_dir))  # 记录下载前的文件列表

# 点击下载按钮后，持续轮询等待文件出现
max_wait = 120  # 最多等 120 秒
interval = 3    # 每 3 秒检查一次
start = time.time()

while time.time() - start < max_wait:
    current_files = set(os.listdir(download_dir))
    new_files = current_files - target_files
    
    # 检查是否有新文件（png/jpg/webp）
    new_imgs = [f for f in new_files if f.lower().endswith(('.png','.jpg','.jpeg','.webp'))]
    if new_imgs:
        # 取最新下载的文件
        newest = max([os.path.join(download_dir, f) for f in new_imgs], key=os.path.getmtime)
        print(f"下载完成: {newest}")
        break
    
    time.sleep(interval)
else:
    print("下载超时，尝试备用方案")
    # 触发备用下载方案

# 移动到目标目录
import shutil
output = r"%USERPROFILE%\.openclaw\media\gemini_output.png"
shutil.copy(newest, output)
print(f"已保存到: {output}")
```

**下载完成后保存路径：** `%USERPROFILE%\.openclaw\media\gemini_output.png`

#### 备用下载方案（仅在缓存监控超过 3 分钟仍未检测到新文件时启用）
从页面提取图片 URL，用 Python 直接下载：

```python
import urllib.request, ssl, re

# 从页面 HTML 提取图片 URL
# 执行 JS: document.querySelectorAll('img') 获取所有图片元素
# 找到 src 包含 lh3.googleusercontent.com 且宽度 > 200px 的

img_url = "https://lh3.googleusercontent.com/gg/..."

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://gemini.google.com/",
}
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
req = urllib.request.Request(img_url, headers=headers)
with urllib.request.urlopen(req, timeout=60, context=ctx) as resp:
    data = resp.read()
    with open(r'%USERPROFILE%\.openclaw\media\gemini_output.png', 'wb') as f:
        f.write(data)
    print(f"下载成功: {len(data)} bytes")
```

#### 分享链接下载（备用）
1. 点击"分享图片"按钮
2. 等待分享对话框弹出
3. 从对话框 URL 获取分享链接
4. 打开分享链接，执行 `document.querySelectorAll('img')` 提取图片 URL
5. 用 Python 下载

---

### 步骤9: MiniMax MCP 审核图片

**审核给自己看，不发给用户！**

调用 MiniMax MCP 图片理解工具：
```bash
mcporter call minimax.understand_image prompt="描述这张图片的内容：主题、风格、颜色、构图、文字内容等细节，和用户需求对比是否一致" image_source="%USERPROFILE%\.openclaw\media\gemini_output.png"
```

**审核判断标准：**
- 图片是否清晰、内容完整
- 图片是否符合用户的原始需求（人物/场景/风格/动作等）
- 质量是否达标

**审核结果处理：**
- ✅ **通过**：图片符合需求 → 直接发送给用户
- ❌ **不通过**：图片不符合需求 → 重新生成，不告知用户审核过程

---

### 步骤10: 发送图片给用户
审核通过后，使用 message 工具发送图片给用户：
```
message action=send channel=openclaw-weixin media=图片路径
```

---

## 元素引用表
| 引用 | 元素 |
|------|------|
| e1 | Google账号 |
| e8 | 图片描述输入框 |
| e10 | 🖼️制作图片按钮 |
| e14 | 发送按钮 |
| e16 | 复制图片（放大模式下） |
| e17 | 下载图片 |
| e18 | 下载完整尺寸的图片 |
| e19 | 灯箱模式关闭按钮 |

---

## 提示词示例

### 小红书风格
```
Generate Image A modern AI design service poster, colorful gradient background, robot designing graphics, futuristic style, Chinese social media style, trending on Xiaohongshu, clean and professional, 3D cartoon
```

### 电商主图
```
Generate Image E-commerce product banner, clean background, AI robot assistant, modern tech style, professional lighting, 3D render
```

### 头像/头像框
```
Generate Image Cute cartoon avatar, robot character, colorful gradient, soft lighting, pastel colors, minimal background
```

---

## 注意事项
1. **每次 snapshot 后元素引用可能会变化**，必须重新获取
2. 需要登录 Google 账号
3. **下载必须等待图片加载完成后再操作**，不要提前点击
4. **MCP 审核不需要告知用户**，自己判断即可
5. 建议使用英文描述
6. 下载位置默认: `%USERPROFILE%\Downloads\`
7. MCP 审核判断不通过时，自行重新生成，不向用户说明

---

## 下载等待脚本（Python）
```python
import time, re, urllib.request, ssl

def wait_and_download_gemini_image(page_url, output_path, timeout=120):
    """等待图片出现并下载"""
    import urllib.request, ssl, time
    # 1. 从分享链接提取图片URL
    # 2. 用 ssl context 下载
    # 3. 保存到 output_path
    pass
```

---

## 快速排查

| 问题 | 解决方案 |
|------|---------|
| 工具按钮是灰的 | 未登录，Chrome 需重新登录 Google 账号 |
| 下载按钮点不了 | 图片还没加载完，等待更长时间 |
| 下载后文件未出现 | 继续等待，图片大下载慢，最长等 120 秒 |
| 下载 403 错误 | 用分享链接方式或 Python ssl 方式下载 |
| MCP 审核失败 | 检查图片路径是否正确 |
| 图片模糊 | 点击"下载完整尺寸的图片"而非"复制图片" |

---

## 工作流程图
```
用户发送图片需求
     ↓
启动 Chrome（专用Profile） → 打开 Gemini
     ↓
点击制作图片 → 输入描述(加前缀) → 发送
     ↓
轮询检查图片（每3秒/次，最长1分钟）
     ↓
图片出现 → 点击下载完整尺寸的图片
     ↓
Chrome缓存轮询监控（每5秒/次，最长3分钟）
     ↓
检测到文件 → 等待大小稳定 → 自动判断类型 → 保存到media
     ↓
MiniMax MCP 审核（自己判断，不告知用户）
     ↓
通过 → message 工具发送给用户
不通过 → 重新生成，重复以上步骤
```

---

*创建于: 2026-03-07*
*更新于: 2026-03-23*
