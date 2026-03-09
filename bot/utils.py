"""
             Project By - @TEAM_X_OG Known As TEAMDEV
      
      Developer - @MR_ARMAN_08

This Is Open-source You Can Modify It And Use As You Want
butt Removing Credits It's Not Allowed.

GitHub - https://github.com/TeamDev-07/FileToLink-TeamDev

"""


import hashlib, secrets, string

ALPHABET = string.ascii_letters + string.digits

def generate_hash(file_unique_id: str) -> str:
    return hashlib.sha256(file_unique_id.encode()).hexdigest()[:24]

def generate_id(length=16) -> str:
    return ''.join(secrets.choice(ALPHABET) for _ in range(length))

def human_size(num_bytes):
    if not num_bytes: return "0 B"
    for unit in ("B","KB","MB","GB","TB"):
        if abs(num_bytes) < 1024.0:
            return f"{num_bytes:.1f} {unit}"
        num_bytes /= 1024.0
    return f"{num_bytes:.1f} PB"

def parse_size_arg(arg: str) -> int:
    arg = arg.strip().lower()
    if arg.endswith("gb"): return int(float(arg[:-2]) * 1024**3)
    if arg.endswith("mb"): return int(float(arg[:-2]) * 1024**2)
    return int(arg)

STREAMING_MIME = {
    "video/mp4","video/webm","video/ogg","video/x-matroska",
    "video/x-msvideo","video/avi","video/3gpp","video/quicktime",
    "audio/mpeg","audio/ogg","audio/wav","audio/flac",
    "audio/mp4","audio/aac","audio/webm","audio/x-m4a",
}

def is_streamable(mime_type: str) -> bool:
    if not mime_type: return False
    base = mime_type.split(";")[0].strip().lower()
    return base in STREAMING_MIME or base.startswith(("video/","audio/"))
