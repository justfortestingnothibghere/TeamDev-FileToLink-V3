<div align="center">

# 🟣 Render Hosting Guide

### _Deploy FileToLink V3 on Render — Free & Easy_

[![Support](https://img.shields.io/badge/Support-Team__x__og-green?logo=telegram&style=for-the-badge)](https://t.me/Team_x_og)
[![Updates](https://img.shields.io/badge/Updates-CRIMEZONE-red?logo=telegram&style=for-the-badge)](https://t.me/CRIMEZONE_UPDATE)
[![Developer](https://img.shields.io/badge/Dev-MR__ARMAN__08-purple?logo=telegram&style=for-the-badge)](https://t.me/MR_ARMAN_08)

</div>

---

> **Best for:** Quick deployment · No server management · Free tier available · Auto-SSL included

> ⚠️ **Important Note:** Render's free tier has ephemeral storage — uploaded files are **deleted on restart/redeploy**. For persistent file storage, use a paid plan with a Persistent Disk or switch to [VPS Hosting](VPS_HOSTING.md).

---

## 📋 What You Need

- ✅ A [Render](https://render.com) account (free)
- ✅ A [GitHub](https://github.com) account
- ✅ Your bot credentials (Token, API ID, API Hash)
- ✅ A forked copy of this repo on your GitHub

---

## 🍴 Step 1 — Fork the Repository

1. Go to [github.com/TeamDev-07/FileToLink-TeamDev](https://github.com/TeamDev-07/FileToLink-TeamDev)
2. Click **Fork** → **Create Fork**
3. Your fork will be at `github.com/YourUsername/FileToLink-TeamDev`

---

## 🚀 Step 2 — Create a New Web Service on Render

1. Go to [render.com](https://render.com) → **Dashboard** → **New +** → **Web Service**
2. Connect your GitHub account if not already
3. Select your forked repo `FileToLink-TeamDev`
4. Click **Connect**

---

## ⚙️ Step 3 — Configure the Service

Fill in these settings:

| Field | Value |
|---|---|
| **Name** | `filetolink` (or anything you like) |
| **Region** | Choose nearest to your users |
| **Branch** | `main` |
| **Runtime** | `Docker` |
| **Instance Type** | Free (or paid for persistent disk) |

Render will auto-detect the `Dockerfile` in your repo.

---

## 🔐 Step 4 — Set Environment Variables

In the **Environment** section, add these variables one by one:

| Key | Value |
|---|---|
| `BOT_TOKEN` | Your bot token |
| `API_ID` | Your API ID |
| `API_HASH` | Your API hash |
| `BOT_USERNAME` | Your bot's username |
| `LOG_CHANNEL` | Your log channel ID (e.g. `-1003580719468`) |
| `ADMINS` | Your Telegram user ID |
| `PORT` | `8080` |
| `DOMAIN` | _(see Step 5 below)_ |
| `DOWNLOAD_SECRET` | Any long random string |

---

## 🌐 Step 5 — Domain Setup

### ✅ If You Have a Domain

1. After creating the service, go to **Settings** → **Custom Domains**
2. Click **Add Custom Domain**
3. Enter your domain, e.g. `watch.yourdomain.com`
4. Render will show you a **CNAME record** to add

**Add this DNS record at your domain registrar:**

| Type | Name | Value |
|---|---|---|
| CNAME | watch | `your-service.onrender.com` |

5. Wait for DNS propagation (usually 5–30 minutes)
6. Render automatically provisions SSL — no extra steps needed! 🎉
7. Set `DOMAIN=watch.yourdomain.com` in your environment variables

---

### ❌ If You Don't Have a Domain

No worries! Render gives you a **free subdomain automatically**:

```
https://your-service-name.onrender.com
```

Just set:
```
DOMAIN=your-service-name.onrender.com
```

in your environment variables. The bot will generate links like:
```
https://your-service-name.onrender.com/watch/...
```

SSL is included automatically — it's HTTPS by default! ✅

> 💡 The free subdomain is permanent as long as your service exists. You don't need to buy a domain to run this bot.

---

## ▶️ Step 6 — Deploy

1. Click **Create Web Service**
2. Render will build your Docker image and deploy it
3. Watch the **Deploy Logs** — look for:
   ```
   Bot started.
   Web server started on port 8080.
   FileToLinkV3 is running.
   ```
4. Your bot is live! 🎉

---

## 💾 Persistent Storage (Paid Plans)

On the free tier, files stored in `data/` are **lost on restart**. To keep files:

1. Upgrade to a paid instance on Render
2. Go to **Disks** → **Add Disk**
3. Set mount path to `/app/data`
4. Set size (e.g. 10 GB)

This ensures your uploaded files survive restarts and redeployments.

---

## 🔄 Auto-Deploy on Code Push

By default, Render auto-deploys whenever you push to your GitHub repo. To disable:

**Settings** → **Build & Deploy** → Toggle off **Auto-Deploy**

To manually deploy: **Dashboard** → **Manual Deploy** → **Deploy latest commit**

---

## ⏰ Free Tier Limitations

| Limitation | Details |
|---|---|
| Sleep on inactivity | Service sleeps after 15 min of no requests |
| Spin-up delay | ~30 seconds to wake from sleep |
| 750 free hours/month | Enough for ~1 service running all month |
| Ephemeral disk | Files deleted on restart |

> 💡 **Tip:** To prevent sleep, use a service like [UptimeRobot](https://uptimerobot.com) to ping your service every 10 minutes for free.

---

## 📊 Viewing Logs

1. Go to your service on Render dashboard
2. Click **Logs** tab
3. Live logs stream in real-time

---

## 🛠️ Troubleshooting

| Problem | Solution |
|---|---|
| Build failed | Check `Dockerfile` — ensure it's in repo root |
| Bot not responding | Check env vars — especially `BOT_TOKEN` |
| Links return 404 | Check `DOMAIN` env var matches your Render URL |
| Service keeps sleeping | Use UptimeRobot to ping every 10 minutes |
| Files disappear | Expected on free tier — upgrade for persistent disk |
| SSL error | Wait 5–10 min after custom domain setup |

---

<div align="center">

**Need Help?**  
💬 [Support Group](https://t.me/Team_x_og) · 🔔 [Updates Channel](https://t.me/CRIMEZONE_UPDATE) · 👨‍💻 [Developer](https://t.me/MR_ARMAN_08)

**Made with ❤️ by [TEAMDEV](https://t.me/Team_x_og)**

</div>
