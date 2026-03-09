"""
             Project By - @TEAM_X_OG Known As TEAMDEV
      
      Developer - @MR_ARMAN_08

This Is Open-source You Can Modify It And Use As You Want
butt Removing Credits It's Not Allowed.

GitHub - https://github.com/TeamDev-07/FileToLink-TeamDev

"""

import os

BOT_TOKEN    = os.getenv("BOT_TOKEN",    "8204737808xxxxxxx")       # Your Bot Token Here
API_ID       = int(os.getenv("API_ID",   "379xxxx"))                         # Your Api Id Here
API_HASH     = os.getenv("API_HASH",     "e52fa6619b386fxxxxxxx")     # Your Api hash here
BOT_USERNAME = os.getenv("BOT_USERNAME", "FileToLinkv3_Bot")
l
LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", "-1003580719468"))        # Your Log Channel Id
ADMINS      = list(map(int, os.getenv("ADMINS", "8163739723").split()))     # Your Admins Id

DOMAIN = os.getenv("DOMAIN", "watch.teamdev.sbs")  # Your Domain
PORT   = int(os.getenv("PORT", "8080")) # Don't Change

DB_PATH        = os.getenv("DB_PATH",    "data/filetolink.db")
FILES_DIR      = os.getenv("FILES_DIR",  "data/files")
MAX_FILE_SIZE  = int(os.getenv("MAX_FILE_SIZE", str(4 * 1024 * 1024 * 1024)))   # 4 GB
MIN_FREE_BYTES = int(os.getenv("MIN_FREE_BYTES", str(2 * 1024 * 1024 * 1024)))  # 2 GB free required
DEFAULT_USER_LIMIT = MAX_FILE_SIZE

COMMAND_RATE_LIMIT = 5
FLOOD_RATE_LIMIT   = 10

UPI_ID   = os.getenv("UPI_ID",   "mr-arman-01@fam")
UPI_NAME = os.getenv("UPI_NAME", "MR. D [TeamDev]")

PREMIUM_PLANS = {
    "1m": {"label": "1 Month",  "price": 149,  "days": 30},
    "3m": {"label": "3 Months", "price": 329, "days": 90},
    "1y": {"label": "1 Year",   "price": 999, "days": 365},
}

DOWNLOAD_SECRET = os.getenv("DOWNLOAD_SECRET", "5e00fe5c8326ed065a2d5581eca2b8cfad94567cd1e999608e513ac859fec353")

SUPPORT_LINK = "https://t.me/Team_x_og"
UPDATE_LINK  = "https://t.me/CRIMEZONE_UPDATE"
DEV_LINK     = "https://t.me/MR_ARMAN_08"
DEV_USERNAME = "@MR_ARMAN_08"

BOT_NAME      = "FileToLinkV3"
OWNER_NAME    = "MR. D [TeamDev]"
