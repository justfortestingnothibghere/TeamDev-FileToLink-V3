<div align="center">

# 🚂 Railway Hosting Guide

### _Deploy FileToLink V3 on Railway — Fast, Modern, Developer-Friendly_

[![Support](https://img.shields.io/badge/Support-Team__x__og-green?logo=telegram&style=for-the-badge)](https://t.me/Team_x_og)
[![Updates](https://img.shields.io/badge/Updates-CRIMEZONE-red?logo=telegram&style=for-the-badge)](https://t.me/CRIMEZONE_UPDATE)
[![Developer](https://img.shields.io/badge/Dev-MR__ARMAN__08-purple?logo=telegram&style=for-the-badge)](https://t.me/MR_ARMAN_08)

</div>

---

> **Best for:** Fast deploys · Great developer experience · Generous free tier · Easy volumes for persistent storage

---

## 📋 What You Need

- ✅ A [Railway](https://railway.app) account (sign up with GitHub)
- ✅ A [GitHub](https://github.com) account
- ✅ Your bot credentials (Token, API ID, API Hash)
- ✅ A forked copy of this repo on your GitHub

---

## 🍴 Step 1 — Fork the Repository

1. Go to [github.com/TeamDev-07/FileToLink-TeamDev](https://github.com/TeamDev-07/FileToLink-TeamDev)
2. Click **Fork** → **Create Fork**
3. Your fork: `github.com/YourUsername/FileToLink-TeamDev`

---

## 🚀 Step 2 — Create a New Project on Railway

1. Go to [railway.app](https://railway.app) → **New Project**
2. Select **Deploy from GitHub repo**
3. Connect your GitHub account if prompted
4. Select your forked `FileToLink-TeamDev` repo
5. Click **Deploy Now**

Railway will auto-detect the `Dockerfile` and start building. ⚡

---

## ⚙️ Step 3 — Set Environment Variables

1. Click your service in the Railway dashboard
2. Go to **Variables** tab
3. Add each variable using **+ New Variable**:

| Key | Value |
|---|---|
| `BOT_TOKEN` | Your bot token |
| `API_ID` | Your API ID |
| `API_HASH` | Your API hash |
| `BOT_USERNAME` | Your bot's username |
| `LOG_CHANNEL` | Your log channel ID (e.g. `-1003580719468`) |
| `ADMINS` | Your Telegram user ID |
| `PORT` | `8080` |
| `DOMAIN` | _(see Step 4 below)_ |
| `DOWNLOAD_SECRET` | Any long random string |

After adding variables, Railway will automatically redeploy. ✅

---

## 🌐 Step 4 — Domain Setup

### ✅ If You Have a Domain

1. In your Railway service, go to **Settings** → **Networking**
2. Click **+ Custom Domain**
3. Enter your domain, e.g. `watch.yourdomain.com`
4. Railway will show you a **CNAME target** like `your-project.up.railway.app`

**Add this at your domain registrar (e.g. Cloudflare, Namecheap):**

| Type | Name | Value |
|---|---|---|
| CNAME | watch | `your-project.up.railway.app` |

5. DNS propagates in 5–30 minutes
6. Railway auto-provisions SSL for your custom domain 🎉
7. Set `DOMAIN=watch.yourdomain.com` in **Variables**

---

### ❌ If You Don't Have a Domain

No problem! Railway provides a **free public subdomain**:

1. In your service, go to **Settings** → **Networking**
2. Click **Generate Domain**
3. Railway creates a URL like:
   ```
   https://filetolink-production-xxxx.up.railway.app
   ```
4. Set this as your `DOMAIN` variable:
   ```
   DOMAIN=filetolink-production-xxxx.up.railway.app
   ```

Your bot will generate links like:
```
https://filetolink-production-xxxx.up.railway.app/watch/...
```

HTTPS is included automatically — no setup needed! ✅

> 💡 This free Railway subdomain is permanent and works great without a custom domain.

---

## 💾 Step 5 — Add Persistent Storage (Volume)

By default, Railway containers are stateless — files in `data/` will be lost on redeploy. Add a volume to persist your data:

1. In your project, click **+ New** → **Volume**
2. Set **Mount Path** to `/app/data`
3. Click **Add**

Railway attaches the volume to your service. Your database and uploaded files now survive restarts and redeployments! ✅

---

## ▶️ Step 6 — Verify Deployment

Click **Deployments** → latest deployment → **View Logs**.

Look for:
```
Database initialized.
Bot started.
Web server started on port 8080.
FileToLinkV3 is running.
```

Your bot is live! 🎉

---

## 🔄 Auto-Deploy on Push

Railway auto-deploys whenever you push to the connected GitHub branch. To trigger a manual redeploy:

**Deployments** → **Redeploy** (on any previous deployment)

---

## 📦 Free Tier Info

Railway's Hobby plan offers:

| Feature | Details |
|---|---|
| Free trial credits | $5 one-time credit for new accounts |
| Hobby plan | $5/month — includes 500 hours, 1 GB RAM, 1 GB volume |
| No sleep | Services stay awake (unlike Render free tier) |
| Build minutes | 500 free build minutes/month |

> 💡 Railway's Hobby plan is very affordable and services **don't sleep** — great for bots that need to be always online.

---

## 📊 Viewing Logs

1. Click your service in Railway dashboard
2. Click **Deployments** → latest → **View Logs**
3. Or use the **Logs** tab for live streaming

---

## 🛠️ Troubleshooting

| Problem | Solution |
|---|---|
| Build failed | Check `Dockerfile` is in repo root |
| Bot not starting | Check env vars — especially `BOT_TOKEN` |
| Links broken | Verify `DOMAIN` var matches your Railway URL (no `https://`) |
| Files disappear | Add a Volume mounted at `/app/data` |
| Port error | Ensure `PORT=8080` is set in variables |
| SSL not working | Wait 5–10 min after adding custom domain |
| Out of free credits | Upgrade to Hobby plan ($5/month) |

---

## 🆚 Railway vs Render vs VPS

| Feature | Railway | Render | VPS |
|---|---|---|---|
| Free tier | ✅ $5 credit | ✅ Free tier | ❌ Paid |
| Always on | ✅ Yes | ❌ Sleeps (free) | ✅ Yes |
| Persistent storage | ✅ Volumes | ✅ Paid disks | ✅ Full disk |
| Custom domain | ✅ Free CNAME | ✅ Free CNAME | ✅ Manual |
| Auto SSL | ✅ Yes | ✅ Yes | ⚙️ Manual |
| Setup difficulty | ⭐ Easy | ⭐ Easy | ⭐⭐⭐ Hard |

---

<div align="center">

**Need Help?**  
💬 [Support Group](https://t.me/Team_x_og) · 🔔 [Updates Channel](https://t.me/CRIMEZONE_UPDATE) · 👨‍💻 [Developer](https://t.me/MR_ARMAN_08)

**Made with ❤️ by [TEAMDEV](https://t.me/Team_x_og)**

</div>
