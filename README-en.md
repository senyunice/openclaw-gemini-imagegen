![OpenClaw + Gemini Image Generation Suite](poster-en.png)

# OpenClaw + Gemini Image Generation Suite

> 🤖 AI-powered image generation for OpenClaw · Describe it. AI generates it. Fully automated.

---

## Overview

A complete AI-powered image generation solution for OpenClaw AI assistants using Gemini web. Includes all config files, scripts, and documentation.

---

## Contents

| File | Description |
|------|-------------|
| `gemini-image-SKILL.md` | Gemini Image Generation Skill |
| `gemini-image-complete-guide.md` | Full Operation Guide |
| `browser-SETUP.md` | Browser Configuration Guide |
| `minimax-mcp-SETUP.md` | MiniMax MCP Image Review Setup |
| `wait_download_cache.py` | Chrome Cache Monitor Script |
| `troubleshooting-guide.md` | 21 Common Issues & Solutions |
| `quick-ref.txt` | Quick Reference Card |

---

## Quick Setup (5 minutes)

### Step 1: Copy Skill File
Copy `gemini-image-SKILL.md` to:
```
C:\Users\<Username>\.openclaw\workspace\skills\gemini-image\SKILL.md
```
> If the `skills` directory doesn't exist, create the full path first.

### Step 2: Copy Download Script
Copy `wait_download_cache.py` to:
```
C:\Users\<Username>\.openclaw\workspace\wait_download_cache.py
```

### Step 3: Create Chrome Profile Directory
Run in PowerShell:
```powershell
New-Item -Path "C:\Users\<Username>\AppData\Local\Google\Chrome\OpenClaw" -ItemType Directory -Force
```

### Step 4: Launch Chrome & Login
Run in PowerShell:
```powershell
Start-Process "C:\Program Files\Google\Chrome\Application\chrome.exe" -ArgumentList "--user-data-dir=C:\Users\<Username>\AppData\Local\Google\Chrome\OpenClaw","--remote-debugging-port=9222"
```
Then open `https://gemini.google.com` in the Chrome window and sign in.

> The login state is remembered automatically. No need to re-login unless you delete the profile directory.

### Step 5: Verify Setup
After restarting Chrome, confirm your Google account appears in the top-right corner of the Gemini page — setup is successful.

---

## Workflow

```
User Request → Launch Chrome → Open Gemini → Enter Prompt → Send
     ↓
Poll for Image (every 3s, up to 1 min)
     ↓
Image Appears → Click "Download Full Size"
     ↓
Chrome Cache Monitor (every 5s, up to 3 min)
     ↓
File Detected → Wait for Size Stable → Detect Type → Save to media
     ↓
MiniMax MCP Review → Send to User
```

---

## Key Paths

| Item | Path |
|------|------|
| Chrome Profile | `C:\Users\<Username>\AppData\Local\Google\Chrome\OpenClaw` |
| Chrome Cache | `C:\Users\<Username>\AppData\Local\Google\Chrome\OpenClaw\Default\Cache\Cache_Data` |
| Image Save | `C:\Users\<Username>\.openclaw\media\` |
| Download Script | `C:\Users\<Username>\.openclaw\workspace\wait_download_cache.py` |
| Skill File | `C:\Users\<Username>\.openclaw\workspace\skills\gemini-image\SKILL.md` |
| Debug Port | 9222 |

---

## Required Permissions

- Chrome browser control (browser MCP tool)
- Python script execution
- File system read/write
- MiniMax MCP (image review)

---

## Daily Usage

After setup, generating images is effortless:
1. Launch the dedicated Chrome (with debug port)
2. Tell your AI assistant: "Generate an image of..."

AI handles the rest automatically.

---

*Created: 2026-03-23 · [🇨🇳 中文版](README.md)*
