# MiniMax MCP 配置指南

## 简介

MiniMax MCP 是图片审核的核心工具。生图完成后用它判断图片是否符合用户需求（审核结果不告知用户，自己判断）。

---

## MiniMax MCP 是什么

MiniMax MCP 是 OpenClaw 的 MiniMax 模型接入工具，提供两个核心功能：

| 工具 | 用途 |
|------|------|
| `minimax.web_search` | 网页搜索 |
| `minimax.understand_image` | **图片理解/审核** |

---

## 安装步骤

### 第一步：确认 mcporter 可用

在 PowerShell 运行：
```bash
mcporter tools
```
应该看到 `minimax` 相关工具。

### 第二步：安装 MiniMax MCP（如果未安装）

```bash
mcporter install minimax
```

### 第三步：验证安装成功

```bash
mcporter call minimax.web_search query="test"
```
返回搜索结果说明安装成功。

### 第四步：验证图片理解工具

```bash
mcporter call minimax.understand_image prompt="描述这张图片" image_source="测试图片路径"
```

---

## 配置 MiniMax API（如果 MCP 连不上）

### 问题现象

调用 `mcporter call minimax.*` 报 "Tool not found" 或 "connection refused"。

### 原因

MCP 服务器崩溃或未启动。

### 解决方案

```bash
# 重启 MiniMax MCP
mcporter restart minimax

# 如果还不行，重启 OpenClaw Gateway
openclaw gateway restart
```

---

## 图片审核使用方式

### 调用格式

```bash
mcporter call minimax.understand_image prompt="审核描述" image_source="图片路径"
```

### prompt 参数说明

prompt 是给 MiniMax 的指令，示例：

```
描述这张图片的内容：人物外貌特征、服装、背景、整体风格画质，和用户需求对比是否一致
```

### image_source 参数说明

图片的完整路径，示例：
```
%USERPROFILE%\.openclaw\media\gemini_output.png
```

### 返回结果

MCP 会返回图片分析内容，**这是给 AI 自己看的**，用于判断图片是否达标，不需要发给用户。

### 判断标准

| 情况 | 处理 |
|------|------|
| 图片清晰、内容完整、符合用户需求 | ✅ 发送给用户 |
| 图片模糊/内容不符/质量差 | ❌ 重新生成 |
| 图片有问题但可修复 | 调整提示词重新生成 |

---

## 常见问题

### Q：报 "Tool not found"

A：`mcporter restart minimax` 重启 MCP，如仍不行重启 Gateway

### Q：审核超时

A：大图片（8MB+）建议先压缩再审核：
```python
from PIL import Image
img = Image.open('gemini_output.png')
img = img.convert('RGB')
img.save('temp_small.jpg', quality=80)
# 用 temp_small.jpg 做审核
```

### Q：没有返回结果

A：检查图片路径是否存在，路径中不能有中文空格

### Q：MCP 崩溃

A：
```bash
mcporter restart minimax
```

---

## 注意事项

- 图片审核是**给 AI 自己看的**，审核结果不需要告知用户
- 图片审核不通过时，AI 自行重新生成，不告诉用户
- MiniMax MCP 是可选的，没有它也可以生成图片，只是少了自动审核环节

---

## 总结

| 项目 | 内容 |
|------|------|
| 安装命令 | `mcporter install minimax` |
| 验证命令 | `mcporter tools` |
| 重启命令 | `mcporter restart minimax` |
| 图片审核 | `mcporter call minimax.understand_image` |
| 问题解决 | 重启 MCP → 重启 Gateway |

---

*创建于: 2026-03-23*
