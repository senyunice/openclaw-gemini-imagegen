import os, time
from pathlib import Path

cache_dir = Path(r"%USERPROFILE%\AppData\Local\Google\Chrome\OpenClaw\Default\Cache\Cache_Data")
media_dir = Path(r"%USERPROFILE%\.openclaw\media")

# 记录当前最大的文件
current_files = {f.name: f.stat().st_size for f in cache_dir.iterdir() if f.is_file()}
current_max = max((f.stat().st_mtime for f in cache_dir.iterdir() if f.is_file()), default=0)
print(f"监控中，当前缓存文件数: {len(current_files)}")

max_wait = 180  # 最长等3分钟
interval = 5    # 每5秒检查一次
start = time.time()

newest_cache_file = None

while time.time() - start < max_wait:
    files = list(cache_dir.iterdir())
    new_files = [f for f in files if f.stat().st_mtime > current_max and f.name not in current_files]
    
    if new_files:
        # 有新文件出现，等待稳定（文件大小不再变化）
        newest = new_files[0]
        print(f"检测到新文件: {newest.name}")
        
        # 等待文件大小稳定（下载完成标志）
        for _ in range(60):  # 最多等5分钟
            time.sleep(5)
            size_now = newest.stat().st_size
            time.sleep(2)
            size_later = newest.stat().st_size
            if size_now == size_later and size_now > 10000:  # 大小不变且>10KB说明下载完成
                print(f"下载完成: {newest.name} ({size_now} bytes)")
                newest_cache_file = newest
                break
            print(f"  下载中... {size_now} bytes")
        
        if newest_cache_file:
            break
        current_max = newest.stat().st_mtime
    
    time.sleep(interval)

if newest_cache_file:
    # 读取文件头判断类型
    with open(newest_cache_file, 'rb') as f:
        header = f.read(16)
    
    if header[:8] == b'\x89PNG\r\n\x1a\n':
        ext = '.png'
    elif header[:3] == b'\xff\xd8\xff':
        ext = '.jpg'
    elif header[:4] == b'RIFF' and header[8:12] == b'WEBP':
        ext = '.webp'
    else:
        ext = '.png'  # 默认当png
    
    out_name = f"gemini_output{ext}"
    out_path = media_dir / out_name
    
    with open(newest_cache_file, 'rb') as f:
        data = f.read()
    with open(out_path, 'wb') as f:
        f.write(data)
    
    print(f"已保存: {out_path} ({len(data)} bytes)")
else:
    print("3分钟内未检测到新文件")
