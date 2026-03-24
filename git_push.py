import subprocess, os

repo = r"C:\Users\Administrator\Desktop\OpenClaw_ImageGen"

os.chdir(repo)

cmds = [
    ["git", "add", "-A"],
    ["git", "commit", "-m", "update: add watermark removal tools (Lama + OpenCV), update SKILL.md workflow"],
    ["git", "push"],
]

for cmd in cmds:
    r = subprocess.run(cmd, capture_output=True, text=True)
    print(f"{' '.join(cmd)}")
    if r.stdout:
        print(r.stdout)
    if r.stderr:
        print(r.stderr)
    print()
