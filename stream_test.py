from yt_dlp import YoutubeDL
import sys
import json

URL = 'https://www.youtube.com/watch?v=YVfCwRAyG5g&t=4879s'
f = open('info.json', 'w')

# ℹ️ See help(yt_dlp.YoutubeDL) for a list of available options and public functions
ydl_opts = {
    'format': 'best',
    'skip_download': True
}
with YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(URL, download=False)
    print(info["url"])
    print(info['duration'])

    # ℹ️ ydl.sanitize_info makes the info json-serializable
    json_info = json.dumps(ydl.sanitize_info(info))
    f.write(json_info)