import json, os

# Only modify the OpenClaw profile
pref_file = r"%USERPROFILE%\AppData\Local\Google\Chrome\OpenClaw\Default\Preferences"
media_dir = r"%USERPROFILE%\.openclaw\media"

with open(pref_file, 'r', encoding='utf-8') as f:
    prefs = json.load(f)

# Set download directory
prefs.setdefault('download', {})
prefs['download']['default_directory'] = media_dir
prefs['download']['prompt_for_download'] = False

with open(pref_file, 'w', encoding='utf-8') as f:
    json.dump(prefs, f, indent=2)

print(f"OK: download dir = {media_dir}")
print(f"File: {pref_file}")
