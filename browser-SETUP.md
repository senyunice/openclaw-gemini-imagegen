# Chrome 专用浏览器配置指南

## 概述

本配置用于 OpenClaw AI 助手通过 Chrome 远程调试协议（CDP）控制专用 Chrome 实例，实现网页自动化操作。

**核心特点：**
- 使用独立的 Chrome 配置文件（OpenClaw），与用户正常使用的 Chrome 完全隔离
- 远程调试端口：9222
- 可执行：网页截图、元素点击、文本输入、内容提取、图片下载等

---

## 一、Chrome 配置文件路径

```
专用目录：%USERPROFILE%\AppData\Local\Google\Chrome\OpenClaw
```

**重要：** 使用独立的 `OpenClaw` 目录，与主配置完全隔离。

---

## 二、每次使用浏览器前的启动步骤

### 步骤 1：杀掉所有 Chrome 进程
```powershell
Stop-Process -Name chrome -Force -ErrorAction SilentlyContinue
```
**必须先杀干净，不能跳过！**

### 步骤 2：启动专用 Chrome
```powershell
Start-Process 'C:\Program Files\Google\Chrome\Application\chrome.exe' -ArgumentList '--user-data-dir=%USERPROFILE%\AppData\Local\Google\Chrome\OpenClaw','--remote-debugging-port=9222'
```

### 步骤 3：等待启动
```powershell
Start-Sleep -Seconds 5
```

### 步骤 4：验证端口
```powershell
Invoke-WebRequest -Uri 'http://localhost:9222/json/version' -TimeoutSec 5
```
**端口通才能连接，否则重试步骤 1-4**

### 步骤 5：连接浏览器
```
browser action=open target=host url=目标URL
```

**禁止复用已有 Chrome，禁止连接非 OpenClaw 的 Chrome。**

---

## 三、连接浏览器（OpenClaw browser 工具）

### 3.1 打开网页
```
browser action=open target=host url=https://gemini.google.com/app
```

### 3.2 等待页面加载
```powershell
Start-Sleep -Seconds 5
```

### 3.3 获取页面快照（查看当前界面）
```
browser action=snapshot target=host targetId=<targetId> compact=true
```

### 3.4 截图
```
browser action=screenshot target=host targetId=<targetId>
```

---

## 四、页面操作指令

### 4.1 点击元素
```
browser action=act target=host targetId=<targetId> ref=<元素ref> kind=click
```

### 4.2 输入文本
```
browser action=act target=host targetId=<targetId> ref=<元素ref> kind=type text=<文本内容>
```

### 4.3 使用 JavaScript 获取数据
```
browser action=act target=host targetId=<targetId> kind=evaluate fn=<JS函数>
```

**示例 - 获取页面中所有图片 URL：**
```javascript
() => {
    const imgs = document.querySelectorAll('img');
    return Array.from(imgs)
        .map(i => ({src: i.src, w: i.naturalWidth, h: i.naturalHeight}))
        .filter(x => x.w > 200);
}
```

---

## 五、Gemini 网页版生图工作流

### 5.1 打开 Gemini
```
browser action=open target=host url=https://gemini.google.com/app
```

### 5.2 等待加载后点击"制作图片"按钮
```
browser action=act target=host targetId=<targetId> ref=e9 kind=click
```
（ref=e9 是"🖼️ 制作图片"按钮）

### 5.3 输入图片描述（必须加前缀 "Generate Image"）
```
browser action=act target=host targetId=<targetId> ref=e8 kind=type text=Generate Image <你的描述>
```

### 5.4 点击发送
```
browser action=act target=host targetId=<targetId> ref=e14 kind=click
```

### 5.5 等待图片生成（约 45 秒）
```powershell
Start-Sleep -Seconds 50
```

### 5.6 获取图片（两种方式）

**方式 A：通过"分享图片"获取公开链接**
1. 点击"分享图片"按钮
2. 从弹窗中获取 `gemini.google.com/share/xxx` 链接
3. 打开分享链接，获取 `lh3.googleusercontent.com` 图片 URL

**方式 B：用 JavaScript 直接提取图片 URL**
```javascript
() => {
    const imgs = document.querySelectorAll('img');
    return Array.from(imgs)
        .map(i => ({src: i.src, w: i.naturalWidth, h: i.naturalHeight}))
        .filter(x => x.w > 200);
}
```

### 5.7 下载图片（Python）
```python
import urllib.request, ssl

url = 'https://lh3.googleusercontent.com/...'
headers = {
    'User-Agent': 'Mozilla/5.0',
    'Referer': 'https://gemini.google.com/'
}
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, timeout=60, context=ctx) as resp:
    data = resp.read()
    with open(r'%USERPROFILE%\.openclaw\media\output.png', 'wb') as f:
        f.write(data)
    print(f'下载成功: {len(data)} bytes')
```

---

## 六、关键参数速查

| 项目 | 值 |
|------|-----|
| Chrome 路径 | `C:\Program Files\Google\Chrome\Application\chrome.exe` |
| 调试端口 | 9222 |
| 用户数据目录 | `%USERPROFILE%\AppData\Local\Google\Chrome\OpenClaw` |
| Gemini 网址 | https://gemini.google.com/app |
| 图片保存目录 | `%USERPROFILE%\.openclaw\media\` |
| 截图保存目录 | `%USERPROFILE%\.openclaw\media\browser\` |

---

## 七、常见问题

**Q: 端口连接失败？**
A: 先检查 Chrome 是否启动，再确认端口是否被占用：`netstat -an | findstr 9222`

**Q: 图片下载 403 错误？**
A: Google CDN 需要 Referer header，用 Python 下载时必须带上 headers（含 Referer）

**Q: 下载的文件没有扩展名？**
A: `lh3.googleusercontent.com` 的 URL 不带扩展名，保存文件时手动加 `.png`

**Q: 如何确认是专用 Chrome？**
A: 截图右上角应显示"登录"按钮（全新空白 Profile）或已记住的登录状态
