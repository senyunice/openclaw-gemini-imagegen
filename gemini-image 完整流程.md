# Gemini 图片生成 - 完整操作流程

## 第一部分：初始配置（一次性）

### 1.1 安装 OpenClaw 和 Chrome

确保已安装：
- OpenClaw AI 助手
- Google Chrome 浏览器
- Python 3.x（用于下载脚本）

### 1.2 安装 MiniMax MCP
```bash
mcporter install minimax
```
验证：`mcporter call minimax.web_search query="test"`

### 1.3 创建 Skill 目录
将 `gemini-image-SKILL.md` 复制到：
```
C:\Users\<用户名>\.openclaw\workspace\skills\gemini-image\SKILL.md
```

### 1.4 复制下载脚本
将 `wait_download_cache.py` 复制到：
```
C:\Users\<用户名>\.openclaw\workspace\wait_download_cache.py
```

### 1.5 创建 Chrome 专用 Profile

**第一步：创建 Chrome 配置目录**
```powershell
# 创建专用配置目录
New-Item -Path 'C:\Users\<用户名>\AppData\Local\Google\Chrome\OpenClaw' -ItemType Directory -Force
```

**第二步：首次启动专用 Chrome**
```powershell
Start-Process 'C:\Program Files\Google\Chrome\Application\chrome.exe' -ArgumentList '--user-data-dir=C:\Users\<用户名>\AppData\Local\Google\Chrome\OpenClaw','--remote-debugging-port=9222'
```

**第三步：登录 Gemini**
在打开的 Chrome 中访问 `https://gemini.google.com`，扫码或输入账号登录。

> 以后每次启动会自动记住登录状态，除非清除浏览器数据。

---

## 第二部分：日常使用（每次生图）

### 2.1 启动 Chrome

```powershell
# 1. 杀掉所有 Chrome 进程（必须先杀，不能跳过）
Stop-Process -Name chrome -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 3

# 2. 启动专用 Chrome（含调试端口）
Start-Process 'C:\Program Files\Google\Chrome\Application\chrome.exe' -ArgumentList '--user-data-dir=C:\Users\<用户名>\AppData\Local\Google\Chrome\OpenClaw','--remote-debugging-port=9222'

# 3. 等待启动
Start-Sleep -Seconds 5

# 4. 验证端口
Invoke-WebRequest -Uri 'http://localhost:9222/json/version' -TimeoutSec 5
```

### 2.2 连接浏览器

```powershell
browser action=open target=host url=https://gemini.google.com/app
```

### 2.3 验证登录
截图查看页面右上角是否显示 Google 账号（而非"登录"按钮）。

---

## 第三部分：生成图片（详细步骤）

### 步骤 1：点击制作图片
```
browser action=act target=host targetId=<页面ID> ref=e10 kind=click
```
（e10 = 🖼️ 制作图片按钮）

### 步骤 2：等待风格选择器出现
```powershell
Start-Sleep -Seconds 2
```

### 步骤 3：输入图片描述
```
browser action=act target=host targetId=<页面ID> ref=e8 kind=type text=Generate Image <你的描述>
```

**⚠️ 必须加前缀 "Generate Image" 或 "生成图片"，否则图片生成功能被禁用！**

### 步骤 4：（可选）选择风格
- 绚彩 / 油画 / 素描 / 电影效果 等

### 步骤 5：发送
```
browser action=act target=host targetId=<页面ID> ref=e14 kind=click
```

### 步骤 6：等待图片生成（轮询检查）

每 3 秒检查一次页面，最长等 1 分钟：

```powershell
# 方法：执行 JS 检查页面中是否有生成的图片
browser action=act target=host targetId=<页面ID> kind=evaluate fn=() => { const imgs = document.querySelectorAll('img'); const candidates = Array.from(imgs).filter(i => i.src.includes('lh3.googleusercontent.com') && i.naturalWidth > 200); return candidates.length; }
```

返回数量 > 0 说明图片已生成。

### 步骤 7：点击下载完整尺寸的图片

找到下载按钮（ref=e17 或 e18）：
```
browser action=act target=host targetId=<页面ID> ref=e17 kind=click
```

### 步骤 8：启动缓存监控脚本

**立即在后台运行下载监控：**
```powershell
python "C:\Users\<用户名>\.openclaw\workspace\wait_download_cache.py"
```

脚本会自动：
1. 监控 Chrome 缓存目录
2. 每 5 秒检查新文件
3. 等待大小稳定（确认下载完成）
4. 读取文件头判断类型（PNG/JPEG）
5. 自动复制到 `C:\<用户名>\.openclaw\media\gemini_output.png`

### 步骤 9：等待下载完成

大文件（8MB+）通常需要 30-90 秒，脚本会自动轮询等待。

---

## 第四部分：审核与发送

### 步骤 10：MiniMax MCP 审核

图片保存后，用 MCP 审核（审核结果给自己看，不发用户）：

```bash
mcporter call minimax.understand_image prompt="描述这张图片的内容：主题、风格、构图、是否符合用户需求" image_source="C:\<用户名>\.openclaw\media\gemini_output.png"
```

**判断：**
- ✅ 符合需求 → 步骤 11
- ❌ 不符合 → 重新生成（回到步骤 1）

### 步骤 11：发送给用户

```powershell
message action=send channel=openclaw-weixin accountId=<你的accountId> message=<说明文字> media=C:\<用户名>\.openclaw\media\gemini_output.png
```

---

## 第五部分：常见问题排查

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 工具按钮是灰的 | 未登录 Google | 在 Chrome 中登录 gemini.google.com |
| 点不了发送 | 图片工具未激活 | 先点制作图片按钮，再输入内容 |
| 1分钟还没图片 | 网络慢或请求失败 | 重新发送，或刷新页面重试 |
| 下载按钮点不了 | 图片未完全加载 | 等更长时间，确认 JS 检查返回 > 0 |
| 缓存监控没反应 | Chrome 进程锁文件 | 等 3 分钟以上，Chrome 会释放文件 |
| MCP 审核失败 | 图片路径错误或文件损坏 | 检查文件是否存在、大小是否正常 |
| 文件没有后缀 | Chrome 行为 | 用缓存监控脚本自动检测文件头并加后缀 |

---

## 关键参数速查

| 项目 | 值 |
|------|-----|
| Chrome 路径 | `C:\Program Files\Google\Chrome\Application\chrome.exe` |
| 调试端口 | 9222 |
| Chrome 配置目录 | `C:\Users\<用户名>\AppData\Local\Google\Chrome\OpenClaw` |
| Chrome 缓存目录 | `C:\Users\<用户名>\AppData\Local\Google\Chrome\OpenClaw\Default\Cache\Cache_Data` |
| 图片保存目录 | `C:\Users\<用户名>\.openclaw\media\` |
| Gemini 网址 | https://gemini.google.com/app |
| 下载监控脚本 | `C:\Users\<用户名>\.openclaw\workspace\wait_download_cache.py` |

---

## Chrome 缓存文件识别

Chrome 下载的图片没有扩展名，存在缓存目录：

```
C:\Users\<用户名>\AppData\Local\Google\Chrome\OpenClaw\Default\Cache\Cache_Data\
```

文件格式识别（文件头）：
- `89 50 4E 47 0D 0A 1A 0A` → PNG 格式
- `FF D8 FF` → JPEG 格式
- `RIFF....WEBP` → WebP 格式

---

*创建于: 2026-03-23*
