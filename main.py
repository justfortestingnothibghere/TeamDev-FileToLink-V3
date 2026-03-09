import asyncio, threading, logging, sys, os
sys.path.insert(0, os.path.dirname(__file__))

from bot.database import init_db, scan_and_recover
from bot.handlers import app
from web.server import start_web
from config.config import PORT, FILES_DIR

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
log = logging.getLogger(__name__)

from pyrogram import idle

def main():
    os.makedirs(FILES_DIR, exist_ok=True)

    init_db()
    log.info("Database initialized.")

    # ── Crash recovery: re-verify all files on disk ──────────────────────────
    recovered = scan_and_recover()
    if recovered:
        log.info(f"Crash recovery: {recovered} file(s) re-verified.")
    log.info("File recovery scan complete — all existing files accessible.")

    app.start()
    log.info("Bot started.")

    loop = asyncio.get_event_loop()
    web_thread = threading.Thread(
        target=start_web, args=(app, loop),
        kwargs={"host": "0.0.0.0", "port": PORT}, daemon=True)
    web_thread.start()
    log.info(f"Web server started on port {PORT}.")
    log.info("FileToLinkV3 is running. Press Ctrl+C to stop.")

    idle()
    app.stop()

if __name__ == "__main__":
    main()
