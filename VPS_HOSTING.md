<div align="center">

# 🖥️ VPS Hosting Guide

### _Deploy FileToLink V3 on Your Own VPS Server_

[![Support](https://img.shields.io/badge/Support-Team__x__og-green?logo=telegram&style=for-the-badge)](https://t.me/Team_x_og)
[![Updates](https://img.shields.io/badge/Updates-CRIMEZONE-red?logo=telegram&style=for-the-badge)](https://t.me/CRIMEZONE_UPDATE)
[![Developer](https://img.shields.io/badge/Dev-MR__ARMAN__08-purple?logo=telegram&style=for-the-badge)](https://t.me/MR_ARMAN_08)

</div>

---

> **Best for:** Full control · Persistent file storage · Custom domain · Large file support (up to 4 GB)

---

## 📦 Requirements

| Item | Minimum Spec |
|---|---|
| OS | Ubuntu 20.04 / 22.04 LTS |
| RAM | 1 GB (2 GB recommended) |
| Storage | 20 GB+ (depends on file usage) |
| CPU | 1 vCPU |
| Open Port | 8080 (or 80/443 with Nginx) |

---

## 🔧 Step 1 — Server Setup

SSH into your VPS and update the system:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git python3 python3-pip curl wget
```

---

## 📥 Step 2 — Clone the Repository

```bash
git clone https://github.com/TeamDev-07/FileToLink-TeamDev
cd FileToLink-TeamDev
```

---

## ⚙️ Step 3 — Configure Environment

Create your `.env` file:

```bash
nano .env
```

Paste and fill in your values:

```env
BOT_TOKEN=your_bot_token_here
API_ID=your_api_id
API_HASH=your_api_hash
BOT_USERNAME=YourBotUsername

LOG_CHANNEL=-100xxxxxxxxxx
ADMINS=your_telegram_user_id

DOMAIN=watch.yourdomain.com
PORT=8080

DB_PATH=data/filetolink.db
FILES_DIR=data/files
MAX_FILE_SIZE=4294967296
MIN_FREE_BYTES=2147483648

DOWNLOAD_SECRET=generate_a_random_secret_here
```

> 💡 **Tip:** Generate a secure secret with `openssl rand -hex 32`

---

## 🐳 Step 4A — Deploy with Docker (Recommended)

### Install Docker

```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
newgrp docker
```

### Install Docker Compose

```bash
sudo apt install -y docker-compose
```

### Start the Bot

```bash
docker-compose up -d
```

### Useful Docker Commands

```bash
docker-compose logs -f          # View live logs
docker-compose restart          # Restart the bot
docker-compose down             # Stop the bot
docker-compose pull && docker-compose up -d   # Update
```

---

## 🐍 Step 4B — Deploy Manually (Without Docker)

```bash
pip3 install -r requirements.txt
mkdir -p data/files

# Run in background with screen
sudo apt install -y screen
screen -S filetolink
python3 main.py

# Press Ctrl+A then D to detach
# Re-attach with: screen -r filetolink
```

Or use `nohup`:

```bash
nohup python3 main.py > logs.txt 2>&1 &
```

---

## 🌐 Step 5 — Domain Setup

### ✅ If You Have a Domain

**A) Add DNS Record**

Go to your domain registrar (Cloudflare, Namecheap, GoDaddy, etc.) and add:

| Type | Name | Value | TTL |
|---|---|---|---|
| A | watch | `YOUR_VPS_IP` | Auto |

So `watch.yourdomain.com` → your VPS IP.

**B) Install Nginx**

```bash
sudo apt install -y nginx
```

**C) Create Nginx Config**

```bash
sudo nano /etc/nginx/sites-available/filetolink
```

Paste:

```nginx
server {
    listen 80;
    server_name watch.yourdomain.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name watch.yourdomain.com;

    ssl_certificate     /etc/letsencrypt/live/watch.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/watch.yourdomain.com/privkey.pem;

    location / {
        proxy_pass         http://127.0.0.1:8080;
        proxy_http_version 1.1;
        proxy_set_header   Host              $host;
        proxy_set_header   X-Real-IP         $remote_addr;
        proxy_set_header   X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto $scheme;
        proxy_buffering    off;
        proxy_request_buffering off;
        client_max_body_size 600M;
        proxy_read_timeout   600s;
        proxy_send_timeout   600s;
    }
}
```

**D) Enable Site & Install SSL**

```bash
sudo ln -s /etc/nginx/sites-available/filetolink /etc/nginx/sites-enabled/
sudo nginx -t

# Install Certbot for free SSL
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d watch.yourdomain.com

# Reload Nginx
sudo systemctl reload nginx
```

Set `DOMAIN=watch.yourdomain.com` in your `.env` file.

---

### ❌ If You Don't Have a Domain

No problem! You can use your **VPS IP address** directly.

**Option 1 — Use IP + Port directly:**

In your `.env`:
```env
DOMAIN=YOUR_VPS_IP:8080
PORT=8080
```

The bot will generate links like:
```
http://YOUR_VPS_IP:8080/watch/...
```

Make sure port `8080` is open in your VPS firewall:
```bash
sudo ufw allow 8080/tcp
sudo ufw reload
```

**Option 2 — Use a Free Subdomain (No domain purchase needed)**

You can get a free domain/subdomain from:
- 🔗 [freedns.afraid.org](https://freedns.afraid.org) — Free DNS with many subdomain options
- 🔗 [noip.com](https://www.noip.com) — Free dynamic DNS hostname
- 🔗 [duckdns.org](https://www.duckdns.org) — Free `.duckdns.org` subdomains

Register, create a subdomain pointing to your VPS IP, then use it as your `DOMAIN` in `.env`.

> ⚠️ Without HTTPS, some browser features like autoplay may be limited. For best experience, using a real domain with SSL is recommended.

---

## 🔁 Step 6 — Auto-Start on Reboot

Create a systemd service:

```bash
sudo nano /etc/systemd/system/filetolink.service
```

Paste:

```ini
[Unit]
Description=FileToLink V3 Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/FileToLink-TeamDev
ExecStart=/usr/bin/python3 main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable filetolink
sudo systemctl start filetolink
sudo systemctl status filetolink
```

---

## 📊 Monitoring & Logs

```bash
# If using systemd
sudo journalctl -u filetolink -f

# If using Docker
docker-compose logs -f

# If using screen/nohup
tail -f logs.txt
```

---

## 🛠️ Troubleshooting

| Problem | Solution |
|---|---|
| Bot not responding | Check logs — likely wrong `BOT_TOKEN` |
| Links not working | Check `DOMAIN` value in `.env` |
| Port 8080 refused | Open firewall: `sudo ufw allow 8080` |
| SSL certificate error | Run `sudo certbot --nginx -d yourdomain` |
| Out of disk space | Clean old files or upgrade VPS storage |
| Container crash loop | Run `docker-compose logs` to see error |

---

<div align="center">

**Need Help?**  
💬 [Support Group](https://t.me/Team_x_og) · 🔔 [Updates Channel](https://t.me/CRIMEZONE_UPDATE) · 👨‍💻 [Developer](https://t.me/MR_ARMAN_08)

**Made with ❤️ by [TEAMDEV](https://t.me/Team_x_og)**

</div>
