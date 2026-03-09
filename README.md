<div align="center">

# 🎬 FileToLink V3

### _Convert Telegram Files into Streaming & Download Links — Instantly_

[![Telegram Bot](https://img.shields.io/badge/Bot-FileToLinkV3-blue?logo=telegram&style=for-the-badge)](https://t.me/FileToLinkv3_Bot)
[![Support](https://img.shields.io/badge/Support-Team__x__og-green?logo=telegram&style=for-the-badge)](https://t.me/Team_x_og)
[![Updates](https://img.shields.io/badge/Updates-CRIMEZONE-red?logo=telegram&style=for-the-badge)](https://t.me/CRIMEZONE_UPDATE)
[![Developer](https://img.shields.io/badge/Dev-MR__ARMAN__08-purple?logo=telegram&style=for-the-badge)](https://t.me/MR_ARMAN_08)

---

> **Project by [@TEAM_X_OG](https://t.me/Team_x_og) · Known as TEAMDEV**  
> Open-source — Free to use & modify · **Removing credits is NOT allowed.**  
> 🔗 [GitHub](https://github.com/TeamDev-07/FileToLink-TeamDev)

</div>

---

## ✨ Features

| Feature | Details |
|---|---|
| 🎬 **Video Streaming** | In-browser player with a sleek modern UI |
| 🎵 **Audio Streaming** | Built-in audio player support |
| 📁 **File Downloads** | Direct download links for any file type |
| 🛡️ **Rate Limiting** | Flood + command rate limit protection |
| 📦 **Upload Limits** | Per-user configurable size limits (up to 4 GB) |
| 👮 **Admin Panel** | Ban/unban, delete files, set limits, broadcast |
| 📋 **Activity Logs** | Every action logged to your Telegram channel |
| 🐳 **Docker Ready** | One-command deployment with Docker |
| 💎 **Premium Plans** | Built-in UPI-based premium subscription system |

---

## 📋 Prerequisites

Before you start, get these ready:

- ✅ A **Telegram Bot Token** — from [@BotFather](https://t.me/BotFather)
- ✅ **API ID & API Hash** — from [my.telegram.org](https://my.telegram.org)
- ✅ A **Log Channel** — create a channel, add your bot as admin, copy the channel ID
- ✅ Your **Telegram User ID** — to set yourself as admin

---

## ⚙️ Configuration

All settings live in `config/config.py` and can be set via environment variables:

```env
BOT_TOKEN      = your_bot_token
API_ID         = your_api_id
API_HASH       = your_api_hash
BOT_USERNAME   = FileToLinkv3_Bot

LOG_CHANNEL    = -1003580719468      # Your log channel ID
ADMINS         = 8163739723          # Space-separated admin user IDs

DOMAIN         = watch.yourdomain.com
PORT           = 8080

DB_PATH        = data/filetolink.db
FILES_DIR      = data/files
MAX_FILE_SIZE  = 4294967296          # 4 GB
MIN_FREE_BYTES = 2147483648          # 2 GB minimum free space

UPI_ID         = your-upi@bank
UPI_NAME       = Your Name

DOWNLOAD_SECRET = your_random_secret_string
```

---

## 🚀 Quick Start

### Option 1 — Docker (Recommended)

```bash
git clone https://github.com/TeamDev-07/FileToLink-TeamDev
cd FileToLink-TeamDev
cp .env.example .env
nano .env          # Fill in your values
docker-compose up -d
```

### Option 2 — Manual

```bash
git clone https://github.com/TeamDev-07/FileToLink-TeamDev
cd FileToLink-TeamDev
pip install -r requirements.txt
python main.py
```

---

## 🤖 Bot Commands

### 👤 User Commands
| Command | Description |
|---|---|
| `/start` | Register and see welcome message |
| `/help` | Show help menu |
| `/myfiles` | List your uploaded files |
| `/stats` | Your account statistics |

### 🔧 Admin Commands
| Command | Description |
|---|---|
| `/ban [user_id]` | Ban a user |
| `/unban [user_id]` | Unban a user |
| `/delfile [file_id]` | Delete a file from the database |
| `/limit [user_id] [size]gb/mb` | Set per-user upload limit |
| `/broadcast [message]` | Send message to all registered users |

---

## 🌐 URL Format

Once deployed with your domain, files are accessible as:

```
https://watch.yourdomain.com/watch/teamdev/hash?{hash}/id?{file_id}   ← Stream page
https://watch.yourdomain.com/download/hash?{hash}/id?{file_id}         ← Download page
https://watch.yourdomain.com/stream/hash?{hash}/id?{file_id}           ← Raw stream
```

---

## 📁 Project Structure

```
FileToLink/
├── 📄 main.py                  ← Entry point
├── 📄 requirements.txt
├── 🐳 Dockerfile
├── 🐳 docker-compose.yml
├── 🌐 nginx.conf
├── config/
│   └── config.py               ← All configuration
├── bot/
│   ├── handlers.py             ← Telegram bot handlers
│   ├── database.py             ← SQLite database helpers
│   └── utils.py                ← Utility functions
├── web/
│   ├── server.py               ← Flask web server + streaming
│   └── templates/
│       ├── player.html         ← Modern video/audio player
│       ├── download.html       ← Download page
│       ├── index.html          ← Landing page
│       ├── pending.html        ← Pending page
│       ├── 403.html            ← Forbidden error page
│       └── 404.html            ← Not found error page
└── data/
    ├── filetolink.db           ← SQLite database (auto-created)
    └── files/                  ← Uploaded files storage
```

---

## 💎 Premium Plans

| Plan | Price | Duration |
|---|---|---|
| 🥉 1 Month | ₹149 | 30 days |
| 🥈 3 Months | ₹329 | 90 days |
| 🥇 1 Year | ₹999 | 365 days |

Payments via UPI · Contact [@MR_ARMAN_08](https://t.me/MR_ARMAN_08)

---

## ⚠️ Default Limits

- **Max file size:** 4 GB (configurable per-user by admin)
- **Command rate limit:** 5 seconds between commands
- **Flood protection:** 10 messages per 10 seconds
- **Min free disk space:** 2 GB required to accept uploads

---

## 🌍 Hosting Options

| Guide | Best For |
|---|---|
| [VPS Hosting](VPS_HOSTING.md) | Full control, persistent storage, custom domain |
| [Render Hosting](RENDER_HOSTING.md) | Free tier, easy deployment, no server management |
| [Railway Hosting](RAILWAY_HOSTING.md) | Fast deploy, generous free tier, great DX |

---

## 📜 License

**MIT License** — Free to use, modify, and distribute.  
⚠️ Removing credits/attribution is **NOT** allowed.

---

<div align="center">

**Made with ❤️ by [TEAMDEV](https://t.me/Team_x_og)**  
🔔 [Updates](https://t.me/CRIMEZONE_UPDATE) · 💬 [Support](https://t.me/Team_x_og) · 👨‍💻 [Developer](https://t.me/MR_ARMAN_08)

</div>
