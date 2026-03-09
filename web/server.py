"""
             Project By - @TEAM_X_OG Known As TEAMDEV
      
      Developer - @MR_ARMAN_08

This Is Open-source You Can Modify It And Use As You Want
butt Removing Credits It's Not Allowed.

GitHub - https://github.com/TeamDev-07/FileToLink-TeamDev

"""

import os, re, logging, mimetypes, hmac, hashlib
from flask import Flask, Response, render_template, abort, request, redirect

from config.config import (
    DOMAIN, PORT, FILES_DIR, DOWNLOAD_SECRET,
    SUPPORT_LINK, UPDATE_LINK, DEV_LINK, BOT_USERNAME,
)
from bot.database import get_file_by_hash
from bot.utils import is_streamable, human_size

log = logging.getLogger(__name__)
web = Flask(__name__, template_folder="templates", static_folder="static")
web.config["MAX_CONTENT_LENGTH"] = 4 * 1024 * 1024 * 1024

MIME_REMAP = {
    "video/x-matroska": "video/mp4",
    "video/x-msvideo":  "video/mp4",
    "video/avi":        "video/mp4",
    "video/divx":       "video/mp4",
    "video/x-flv":      "video/mp4",
    "video/3gpp":       "video/mp4",
    "video/quicktime":  "video/mp4",
    "video/x-ms-wmv":   "video/mp4",
}

POSSIBLE_HEVC = {"video/x-matroska", "video/x-msvideo", "video/avi"}

CHUNK = 1024 * 1024


def _hmac_token(fh):
    return hmac.new(DOWNLOAD_SECRET.encode(), fh.encode(), hashlib.sha256).hexdigest()[:32]

def _verify_token(fh, tok):
    return hmac.compare_digest(_hmac_token(fh), tok)


def _serve(rec, inline=True):
    path = rec.get("local_path","")
    if rec.get("status") != "ready" or not path or not os.path.exists(path):
        abort(503 if rec.get("status")=="pending" else 404)

    sz       = os.path.getsize(path)
    raw_mime = rec.get("mime_type") or mimetypes.guess_type(path)[0] or "application/octet-stream"
    mime     = MIME_REMAP.get(raw_mime, raw_mime)
    name     = rec["file_name"]

    rh = request.headers.get("Range","")
    s,e = 0, sz-1
    if rh:
        m = re.match(r"bytes=(\d+)-(\d*)", rh)
        if m:
            s = int(m.group(1))
            e = int(m.group(2)) if m.group(2) else sz-1
    e = min(e, sz-1); ln = e-s+1

    def gen():
        rem = ln
        with open(path,"rb") as f:
            f.seek(s)
            while rem>0:
                d = f.read(min(CHUNK,rem))
                if not d: break
                rem -= len(d); yield d

    hdrs = {
        "Content-Type":       mime,
        "Content-Range":      f"bytes {s}-{e}/{sz}",
        "Accept-Ranges":      "bytes",
        "Content-Length":     str(ln),
        "Content-Disposition":f'{"inline" if inline else "attachment"}; filename="{name}"',
        "Cache-Control":      "public, max-age=86400",
    }
    return Response(gen(), status=206 if rh else 200, headers=hdrs, direct_passthrough=True)


@web.route("/watch/teamdev/<fh>")
def watch_page(fh):
    rec = get_file_by_hash(fh)
    if not rec: abort(404)
    if rec.get("status")=="pending": return render_template("pending.html",file=rec),202
    if rec.get("status")=="error":   abort(404)
    if not (is_streamable(rec.get("mime_type","")) or rec.get("file_type") in ("video","audio")):
        return redirect(f"https://{DOMAIN}/download/{fh}")
    return render_template("player.html", file=rec,
        stream_url=f"https://{DOMAIN}/stream/{fh}",
        file_size=human_size(rec["file_size"]),
        may_be_hevc=(rec.get("mime_type","") in POSSIBLE_HEVC),
        raw_mime=rec.get("mime_type",""),
        support=SUPPORT_LINK, updates=UPDATE_LINK, dev=DEV_LINK)

@web.route("/stream/<fh>")
def stream_file(fh):
    rec = get_file_by_hash(fh)
    if not rec: abort(404)
    return _serve(rec, inline=True)

@web.route("/download/<fh>")
def download_page(fh):
    rec = get_file_by_hash(fh)
    if not rec: abort(404)
    if rec.get("status")=="pending": return render_template("pending.html",file=rec),202
    return render_template("download.html", file=rec,
        file_size=human_size(rec["file_size"]),
        support=SUPPORT_LINK, updates=UPDATE_LINK, dev=DEV_LINK)

@web.route("/dl/<fh>/<tok>")
def direct_dl(fh, tok):
    if not _verify_token(fh, tok): abort(403)
    rec = get_file_by_hash(fh)
    if not rec: abort(404)
    return _serve(rec, inline=False)

@web.route("/")
def index():
    return render_template("index.html", support=SUPPORT_LINK,
        updates=UPDATE_LINK, dev=DEV_LINK, bot_username=BOT_USERNAME)

@web.errorhandler(403)
def e403(e): return render_template("403.html"), 403
@web.errorhandler(404)
def e404(e): return render_template("404.html"), 404
@web.errorhandler(503)
def e503(e): return render_template("pending.html",file={}), 503

def set_client(c,l): pass
def start_web(client, loop, host="0.0.0.0", port=PORT):
    web.run(host=host, port=port, threaded=True, debug=False, use_reloader=False)
