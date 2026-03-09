"""
             Project By - @TEAM_X_OG Known As TEAMDEV
      
      Developer - @MR_ARMAN_08

This Is Open-source You Can Modify It And Use As You Want
butt Removing Credits It's Not Allowed.

GitHub - https://github.com/TeamDev-07/FileToLink-TeamDev

"""


import asyncio, logging, datetime, os, shutil, hmac, hashlib
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from config.config import (
    BOT_TOKEN, API_ID, API_HASH, LOG_CHANNEL, ADMINS,
    DOMAIN, MAX_FILE_SIZE, SUPPORT_LINK, UPDATE_LINK, DEV_LINK, DEV_USERNAME,
    COMMAND_RATE_LIMIT, FILES_DIR, MIN_FREE_BYTES, UPI_ID, UPI_NAME,
    PREMIUM_PLANS, DOWNLOAD_SECRET, BOT_USERNAME, BOT_NAME, OWNER_NAME,
)
from bot.database import (
    register_user, get_user, ban_user, unban_user, set_user_limit,
    get_user_limit, save_file, get_file_by_hash, set_file_ready, set_file_error,
    delete_file_by_hash, get_user_files, check_rate_limit, get_all_users,
    get_user_count, get_file_count, is_premium, grant_premium, revoke_premium,
    create_payment, submit_utr, get_pending_payments, verify_payment,
    reject_payment, get_payment_by_id, get_all_files_ordered, get_total_storage_used,
)
from bot.utils import generate_hash, human_size, parse_size_arg, is_streamable

log = logging.getLogger(__name__)
os.makedirs(FILES_DIR, exist_ok=True)

app = Client("streambot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

_utr_state: dict = {}

BOT_TITLE   = "𝙵𝚒𝚕𝚎𝚃𝚘𝙻𝚒𝚗𝚔𝚅𝟹"
OWNER_TITLE = "ᴍʀ. ᴅ [ᴛᴇᴀᴍᴅᴇᴠ]"

def fmt_name(s: str) -> str:
    """Convert plain ASCII to small-caps Unicode."""
    _MAP = str.maketrans(
        "abcdefghijklmnopqrstuvwxyz",
        "ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘQʀꜱᴛᴜᴠᴡxʏᴢ"
    )
    return s.upper().translate(_MAP)

def make_dl_token(file_hash: str) -> str:
    return hmac.new(DOWNLOAD_SECRET.encode(), file_hash.encode(), hashlib.sha256).hexdigest()[:32]

def stream_url(fh):       return f"https://{DOMAIN}/watch/teamdev/{fh}"
def download_url(fh, tok): return f"https://{DOMAIN}/dl/{fh}/{tok}"
def is_admin(uid):         return uid in ADMINS

def disk_has_space():
    try:    return shutil.disk_usage(FILES_DIR).free >= MIN_FREE_BYTES
    except: return True

def rate_limited(func):
    async def wrapper(client, message):
        ok, reason = check_rate_limit(message.from_user.id, COMMAND_RATE_LIMIT)
        if not ok: await message.reply(reason); return
        return await func(client, message)
    wrapper.__name__ = func.__name__
    return wrapper

async def log_event(action: str, user, extra: str = "", file_rec: dict = None):
    uname = f"@{user.username}" if user.username else "ɴᴏ ᴜꜱᴇʀɴᴀᴍᴇ"
    lines = [
        f"━━━━━━━━━━━━━━━━━━━━━━",
        f"📋 **{action}**",
        f"━━━━━━━━━━━━━━━━━━━━━━",
        f"👤 **ᴜꜱᴇʀ:** [{user.first_name}](tg://user?id={user.id})",
        f"🔖 **ᴜꜱᴇʀɴᴀᴍᴇ:** {uname}",
        f"🆔 **ᴜꜱᴇʀ ɪᴅ:** `{user.id}`",
        f"💎 **ᴘʀᴇᴍɪᴜᴍ:** {'ʏᴇꜱ ✅' if is_premium(user.id) else 'ɴᴏ ❌'}",
        f"🕐 **ᴛɪᴍᴇ:** `{datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC`",
    ]
    if file_rec:
        lines += [
            f"━━━━━━━━━━━━━━━━━━━━━━",
            f"📄 **ꜰɪʟᴇ:** `{file_rec.get('file_name','?')}`",
            f"📦 **ꜱɪᴢᴇ:** `{human_size(file_rec.get('file_size',0))}`",
            f"🎞️ **ᴛʏᴘᴇ:** `{file_rec.get('mime_type','?')}`",
            f"🗂️ **ᴄᴀᴛᴇɢᴏʀʏ:** `{file_rec.get('file_type','?').capitalize()}`",
            f"🔑 **ʜᴀꜱʜ:** `{file_rec.get('file_hash','?')}`",
        ]
    if extra:
        lines += [f"━━━━━━━━━━━━━━━━━━━━━━", f"ℹ️ {extra}"]
    try:
        await app.send_message(LOG_CHANNEL, "\n".join(lines))
    except Exception as e:
        log.warning(f"Log failed: {e}")

@app.on_message(filters.command("start") & filters.private)
@rate_limited
async def start_cmd(client, message: Message):
    user = message.from_user
    register_user(user.id, user.username, user.first_name)
    db_user = get_user(user.id)
    if db_user and db_user["is_banned"]:
        await message.reply(
            "╔══════════════════════╗\n"
            "║    🚫  𝙱𝙰𝙽𝙽𝙴𝙳  🚫    ║\n"
            "╚══════════════════════╝\n\n"
            "ʏᴏᴜ ᴀʀᴇ ʙᴀɴɴᴇᴅ ꜰʀᴏᴍ ᴜꜱɪɴɢ ᴛʜɪꜱ ʙᴏᴛ.\n"
            f"ᴄᴏɴᴛᴀᴄᴛ {DEV_USERNAME} ᴛᴏ ᴀᴘᴘᴇᴀʟ.")
        return

    prem  = is_premium(user.id)
    crown = "👑 " if prem else ""

    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 𝚄𝚙𝚍𝚊𝚝𝚎𝚜", url=UPDATE_LINK),
         InlineKeyboardButton("💬 𝚂𝚞𝚙𝚙𝚘𝚛𝚝", url=SUPPORT_LINK)],
        [InlineKeyboardButton("💎 ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴꜱ", callback_data="premium_menu"),
         InlineKeyboardButton("👨‍💻 𝙳𝚎𝚟𝚎𝚕𝚘𝚙𝚎𝚛", url=DEV_LINK)],
        [InlineKeyboardButton("📂 ᴍʏ ꜰɪʟᴇꜱ", callback_data="my_files"),
         InlineKeyboardButton("📊 ᴍʏ ꜱᴛᴀᴛꜱ",  callback_data="my_stats")],
    ])

    tier = "**👑 ᴘʀᴇᴍɪᴜᴍ ᴍᴇᴍʙᴇʀ**\n" if prem else ""
    await message.reply(
        f"╔══════════════════════════╗\n"
        f"║  𝙵𝚒𝚕𝚎𝚃𝚘𝙻𝚒𝚗𝚔𝚅𝟹 ▶️  ║\n"
        f"╚══════════════════════════╝\n\n"
        f"{tier}"
        f"👋 ᴡᴇʟᴄᴏᴍᴇ, **{crown}{user.first_name}**!\n\n"
        f"🎬 ᴜᴘʟᴏᴀᴅ ᴀɴʏ ꜰɪʟᴇ → ɢᴇᴛ ɪɴꜱᴛᴀɴᴛ **𝚜𝚝𝚛𝚎𝚊𝚖** ᴀɴᴅ **𝚍𝚘𝚠𝚗𝚕𝚘𝚊𝚍** ʟɪɴᴋꜱ.\n"
        f"🔒 𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍 ʟɪɴᴋꜱ ᴀʀᴇ **ᴘʀɪᴠᴀᴛᴇ** — ᴏɴʟʏ ʏᴏᴜ ᴄᴀɴ ᴀᴄᴄᴇꜱꜱ ᴛʜᴇᴍ.\n"
        f"🌐 𝚂𝚝𝚛𝚎𝚊𝚖 ʟɪɴᴋꜱ ᴀʀᴇ **ꜱʜᴀʀᴇᴀʙʟᴇ** — ᴀɴʏᴏɴᴇ ᴄᴀɴ ᴡᴀᴛᴄʜ!\n\n"
        f"📦 **ʏᴏᴜʀ ʟɪᴍɪᴛ:** `{human_size(get_user_limit(user.id))}`\n\n"
        f"⬇️ ᴊᴜꜱᴛ ꜱᴇɴᴅ ᴍᴇ ᴀ ꜰɪʟᴇ ᴛᴏ ɢᴇᴛ ꜱᴛᴀʀᴛᴇᴅ!\n\n"
        f"👑 𝙾𝚠𝚗𝚎𝚛: **{OWNER_TITLE}**",
        reply_markup=markup)

    await log_event("ꜱᴛᴀʀᴛ / ʙᴏᴛ ᴏᴘᴇɴᴇᴅ", user)

@app.on_message(filters.command("help") & filters.private)
@rate_limited
async def help_cmd(client, message: Message):
    uid = message.from_user.id
    text = (
        f"📖 **{BOT_TITLE} ʜᴇʟᴘ**\n\n"
        "**ᴜꜱᴇʀ ᴄᴏᴍᴍᴀɴᴅꜱ**\n"
        "╔══════════════════════╗\n"
        "║ /start   – ᴍᴀɪɴ ᴍᴇɴᴜ ║\n"
        "║ /help    – ᴛʜɪꜱ ᴍᴇɴᴜ ║\n"
        "║ /myfiles – ʏᴏᴜʀ ꜰɪʟᴇꜱ║\n"
        "║ /stats   – ʏᴏᴜʀ ꜱᴛᴀᴛꜱ║\n"
        "║ /premium – ʙᴜʏ ᴘʟᴀɴ  ║\n"
        "╚══════════════════════╝\n\n"
        "**🎬 𝙷𝚘𝚠 𝙸𝚝 𝚆𝚘𝚛𝚔𝚜**\n"
        "1️⃣ ꜱᴇɴᴅ ᴀɴʏ ꜰɪʟᴇ ᴛᴏ ᴛʜᴇ ʙᴏᴛ\n"
        "2️⃣ ʙᴏᴛ ᴅᴏᴡɴʟᴏᴀᴅꜱ ɪᴛ ᴛᴏ ꜱᴇʀᴠᴇʀ\n"
        "3️⃣ ʏᴏᴜ ɢᴇᴛ ꜱᴛʀᴇᴀᴍ + ᴘʀɪᴠᴀᴛᴇ ᴅᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ\n"
        "4️⃣ ʟɪɴᴋꜱ ɴᴇᴠᴇʀ ᴇxᴘɪʀᴇ ♾️\n\n"
        "**✨ ᴘʟᴀʏᴇʀ ꜰᴇᴀᴛᴜʀᴇꜱ**\n"
        "🎵 ᴍᴜʟᴛɪᴘʟᴇ ᴀᴜᴅɪᴏ ᴛʀᴀᴄᴋꜱ (ʟɪᴋᴇ ᴍx ᴘʟᴀʏᴇʀ)\n"
        "📝 ᴍᴜʟᴛɪᴘʟᴇ ꜱᴜʙᴛɪᴛʟᴇ ᴛʀᴀᴄᴋꜱ\n"
        "📺 ᴍᴜʟᴛɪᴘʟᴇ Qᴜᴀʟɪᴛʏ ʟᴇᴠᴇʟꜱ\n\n"
        "🔒 𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍 ʟɪɴᴋꜱ ᴀʀᴇ ʜᴍᴀᴄ-ꜱᴇᴄᴜʀᴇᴅ — ᴏɴʟʏ ʏᴏᴜ ᴄᴀɴ ᴜꜱᴇ ᴛʜᴇᴍ.\n"
        "🌐 ꜱᴛʀᴇᴀᴍ ʟɪɴᴋꜱ ᴡᴏʀᴋ ꜰᴏʀ ᴀɴʏᴏɴᴇ."
    )
    if is_admin(uid):
        text += (
            "\n\n**⚙️ ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅꜱ**\n"
            "╔══════════════════════════╗\n"
            "║ /ban [uid]               ║\n"
            "║ /unban [uid]             ║\n"
            "║ /delfile [hash]          ║\n"
            "║ /limit [uid] [size]mb/gb ║\n"
            "║ /broadcast [text]        ║\n"
            "║ /storage                 ║\n"
            "║ /users                   ║\n"
            "║ /payments                ║\n"
            "║ /grantpremium [uid][days]║\n"
            "║ /revokepremium [uid]     ║\n"
            "║ /userinfo [uid]          ║\n"
            "║ /filestats               ║\n"
            "╚══════════════════════════╝"
        )
    await message.reply(text)

@app.on_callback_query(filters.regex("^my_files$"))
async def cb_my_files(client, cb: CallbackQuery):
    await cb.answer()
    await _show_myfiles(cb.message, cb.from_user.id)

@app.on_callback_query(filters.regex("^my_stats$"))
async def cb_my_stats(client, cb: CallbackQuery):
    await cb.answer()
    await _show_stats(cb.message, cb.from_user)

@app.on_message(filters.command("myfiles") & filters.private)
@rate_limited
async def myfiles_cmd(client, message: Message):
    await _show_myfiles(message, message.from_user.id)

@app.on_message(filters.command("stats") & filters.private)
@rate_limited
async def stats_cmd(client, message: Message):
    await _show_stats(message, message.from_user)

async def _show_myfiles(dest, uid):
    files = get_user_files(uid)
    if not files:
        await dest.reply("📂 ʏᴏᴜ ʜᴀᴠᴇɴ'ᴛ ᴜᴘʟᴏᴀᴅᴇᴅ ᴀɴʏ ꜰɪʟᴇꜱ ʏᴇᴛ.\n\nꜱᴇɴᴅ ᴍᴇ ᴀ ꜰɪʟᴇ ᴛᴏ ɢᴇᴛ ꜱᴛᴀʀᴛᴇᴅ!"); return
    text = f"📂 **ʏᴏᴜʀ ꜰɪʟᴇꜱ** — {len(files)} ᴛᴏᴛᴀʟ\n\n"
    for i, f in enumerate(files[:15], 1):
        icon = "✅" if f.get("status")=="ready" else "⏳" if f.get("status")=="pending" else "❌"
        text += f"{i}. {icon} [{f['file_name']}]({stream_url(f['file_hash'])}) `{human_size(f['file_size'])}`\n"
    if len(files) > 15:
        text += f"\n_...ᴀɴᴅ {len(files)-15} ᴍᴏʀᴇ ꜰɪʟᴇꜱ_"
    await dest.reply(text, disable_web_page_preview=True)

async def _show_stats(dest, user):
    db    = get_user(user.id)
    if not db: await dest.reply("ꜱᴇɴᴅ /start ꜰɪʀꜱᴛ."); return
    files = get_user_files(user.id)
    prem  = is_premium(user.id)
    until = (db.get("premium_until") or "")[:10] or "—"
    ready = sum(1 for f in files if f.get("status")=="ready")
    total_size = sum(f["file_size"] for f in files)
    uname = f"@{user.username}" if user.username else "—"
    await dest.reply(
        f"╔══════════════════════╗\n"
        f"║   📊  ʏᴏᴜʀ ꜱᴛᴀᴛꜱ    ║\n"
        f"╚══════════════════════╝\n\n"
        f"👤 **ɴᴀᴍᴇ:** {user.first_name}\n"
        f"🔖 **ᴜꜱᴇʀɴᴀᴍᴇ:** {uname}\n"
        f"🆔 **ɪᴅ:** `{user.id}`\n"
        f"{'👑 **ᴘʀᴇᴍɪᴜᴍ** ᴜɴᴛɪʟ: '+until if prem else '⭐ **ᴘʟᴀɴ:** ꜰʀᴇᴇ'}\n\n"
        f"📁 **ꜰɪʟᴇꜱ:** {len(files)} ({ready} ʀᴇᴀᴅʏ)\n"
        f"💾 **ᴜꜱᴇᴅ:** {human_size(total_size)}\n"
        f"📦 **ʟɪᴍɪᴛ:** {human_size(get_user_limit(user.id))}\n"
        f"📅 **ᴊᴏɪɴᴇᴅ:** {db['joined_at'][:10]}")

@app.on_message(filters.command("premium") & filters.private)
@rate_limited
async def premium_cmd(client, message: Message):
    await show_premium_menu(message, message.from_user.id)

@app.on_callback_query(filters.regex("^premium_menu$"))
async def cb_premium_menu(client, cb: CallbackQuery):
    await cb.answer()
    await show_premium_menu(cb.message, cb.from_user.id)

async def show_premium_menu(dest, uid):
    prem  = is_premium(uid)
    db    = get_user(uid)
    until = (db.get("premium_until") or "")[:10] if db else ""
    status_line = f"👑 **ᴀᴄᴛɪᴠᴇ ᴘʀᴇᴍɪᴜᴍ** (ᴇxᴘɪʀᴇꜱ {until})\n\n" if prem else "⭐ **ꜰʀᴇᴇ ᴘʟᴀɴ**\n\n"

    buttons = []
    plan_lines = []
    for key, plan in PREMIUM_PLANS.items():
        plan_lines.append(f"  • **{plan['label']}** — ₹{plan['price']}")
        buttons.append([InlineKeyboardButton(
            f"💳 {plan['label']} – ₹{plan['price']}", callback_data=f"buy_{key}")])
    buttons.append([InlineKeyboardButton("🏠 ʙᴀᴄᴋ ᴛᴏ ᴍᴇɴᴜ", callback_data="back_start")])

    await dest.reply(
        f"╔══════════════════════╗\n"
        f"║   💎  ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴꜱ ║\n"
        f"╚══════════════════════╝\n\n"
        f"{status_line}"
        f"**ᴀᴠᴀɪʟᴀʙʟᴇ ᴘʟᴀɴꜱ:**\n" + "\n".join(plan_lines) + "\n\n"
        f"**✨ ᴘʀᴇᴍɪᴜᴍ ʙᴇɴᴇꜰɪᴛꜱ:**\n"
        f"  🔓 ʜɪɢʜᴇʀ ᴜᴘʟᴏᴀᴅ ʟɪᴍɪᴛꜱ\n"
        f"  ⚡ ᴘʀɪᴏʀɪᴛʏ ᴘʀᴏᴄᴇꜱꜱɪɴɢ\n"
        f"  🎯 ᴘʀɪᴏʀɪᴛʏ ꜱᴜᴘᴘᴏʀᴛ\n"
        f"  ♾️ ᴜɴʟɪᴍɪᴛᴇᴅ ʟɪɴᴋꜱ\n"
        f"  🚀 ᴇᴀʀʟʏ ᴀᴄᴄᴇꜱꜱ ᴛᴏ ꜰᴇᴀᴛᴜʀᴇꜱ\n\n"
        f"💳 **ᴘᴀʏᴍᴇɴᴛ ᴠɪᴀ ᴜᴘɪ** (ꜰᴀᴍᴘᴀʏ, ɢᴘᴀʏ, ᴘʜᴏɴᴇᴘᴇ, ᴘᴀʏᴛᴍ)",
        reply_markup=InlineKeyboardMarkup(buttons))

@app.on_callback_query(filters.regex("^back_start$"))
async def cb_back_start(client, cb: CallbackQuery):
    await cb.answer()
    user = cb.from_user
    register_user(user.id, user.username, user.first_name)
    db_user = get_user(user.id)
    if db_user and db_user["is_banned"]:
        await cb.message.reply("🚫 ʏᴏᴜ ᴀʀᴇ ʙᴀɴɴᴇᴅ.")
        return
    prem  = is_premium(user.id)
    crown = "👑 " if prem else ""
    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 𝚄𝚙𝚍𝚊𝚝𝚎𝚜", url=UPDATE_LINK),
         InlineKeyboardButton("💬 𝚂𝚞𝚙𝚙𝚘𝚛𝚝", url=SUPPORT_LINK)],
        [InlineKeyboardButton("💎 ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴꜱ", callback_data="premium_menu"),
         InlineKeyboardButton("👨‍💻 𝙳𝚎𝚟𝚎𝚕𝚘𝚙𝚎𝚛", url=DEV_LINK)],
        [InlineKeyboardButton("📂 ᴍʏ ꜰɪʟᴇꜱ", callback_data="my_files"),
         InlineKeyboardButton("📊 ᴍʏ ꜱᴛᴀᴛꜱ",  callback_data="my_stats")],
    ])
    tier = "**👑 ᴘʀᴇᴍɪᴜᴍ ᴍᴇᴍʙᴇʀ**\n" if prem else ""
    await cb.message.reply(
        f"╔══════════════════════════╗\n"
        f"║  𝙵𝚒𝚕𝚎𝚃𝚘𝙻𝚒𝚗𝚔𝚅𝟹 ▶️  ║\n"
        f"╚══════════════════════════╝\n\n"
        f"{tier}"
        f"👋 ᴡᴇʟᴄᴏᴍᴇ, **{crown}{user.first_name}**!\n\n"
        f"🎬 ᴜᴘʟᴏᴀᴅ ᴀɴʏ ꜰɪʟᴇ → ɪɴꜱᴛᴀɴᴛ **𝚜𝚝𝚛𝚎𝚊𝚖** ᴀɴᴅ **𝚍𝚘𝚠𝚗𝚕𝚘𝚊𝚍** ʟɪɴᴋꜱ.\n"
        f"📦 **ʏᴏᴜʀ ʟɪᴍɪᴛ:** `{human_size(get_user_limit(user.id))}`\n\n"
        f"👑 𝙾𝚠𝚗𝚎𝚛: **{OWNER_TITLE}**",
        reply_markup=markup)

@app.on_callback_query(filters.regex(r"^buy_(\w+)$"))
async def cb_buy_plan(client, cb: CallbackQuery):
    await cb.answer()
    key  = cb.matches[0].group(1)
    plan = PREMIUM_PLANS.get(key)
    if not plan: return

    uid    = cb.from_user.id
    pay_id = create_payment(uid, key, plan["price"])

    upi_url = (f"https://t.me/Pay_To_TeamDev/2")

    await cb.message.reply(
        f"╔══════════════════════╗\n"
        f"║  💳  ᴜᴘɪ ᴘᴀʏᴍᴇɴᴛ   ║\n"
        f"╚══════════════════════╝\n\n"
        f"📦 **ᴘʟᴀɴ:** {plan['label']} — ₹{plan['price']}\n"
        f"🆔 **ᴘᴀʏᴍᴇɴᴛ ɪᴅ:** `{pay_id}`\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"**ꜱᴛᴇᴘ 1** — ᴘᴀʏ ₹{plan['price']} ᴛᴏ:\n"
        f"  💳 ᴜᴘɪ ɪᴅ: `{UPI_ID}`\n\n"
        f"**ꜱᴛᴇᴘ 2** — ᴛᴀᴘ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ\n\n"
        f"**ꜱᴛᴇᴘ 3** — ᴄᴏᴍᴇ ʙᴀᴄᴋ ᴀɴᴅ ᴛᴀᴘ\n"
        f"  **✅ ɪ'ᴠᴇ ᴘᴀɪᴅ** ᴀɴᴅ ᴇɴᴛᴇʀ ʏᴏᴜʀ ᴜᴛʀ ɴᴜᴍʙᴇʀ.\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"⏱️ _ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ᴡɪᴛʜɪɴ 1–2 ʜᴏᴜʀꜱ_",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📱 𝙾𝚙𝚎𝚗 𝚄𝙿𝙸 𝙰𝚙𝚙 𝚝𝚘 𝙿𝚊𝚢", url=upi_url)],
            [InlineKeyboardButton("✅ ɪ'ᴠᴇ ᴘᴀɪᴅ — ᴇɴᴛᴇʀ ᴜᴛʀ", callback_data=f"enter_utr_{pay_id}")],
            [InlineKeyboardButton("❌ ᴄᴀɴᴄᴇʟ", callback_data="premium_menu")],
        ]))

@app.on_callback_query(filters.regex(r"^enter_utr_(\d+)$"))
async def cb_enter_utr(client, cb: CallbackQuery):
    await cb.answer()
    pay_id = int(cb.matches[0].group(1))
    _utr_state[cb.from_user.id] = pay_id
    await cb.message.reply(
        f"📝 **ᴇɴᴛᴇʀ ᴜᴛʀ / ᴛʀᴀɴꜱᴀᴄᴛɪᴏɴ ɪᴅ**\n\n"
        f"ᴘᴀʏᴍᴇɴᴛ ɪᴅ: `{pay_id}`\n\n"
        f"ᴘʟᴇᴀꜱᴇ ᴛʏᴘᴇ ʏᴏᴜʀ **ᴜᴛʀ ɴᴜᴍʙᴇʀ** (ᴛʜᴇ 12-ᴅɪɢɪᴛ ᴛʀᴀɴꜱᴀᴄᴛɪᴏɴ ʀᴇꜰᴇʀᴇɴᴄᴇ "
        f"ꜱʜᴏᴡɴ ɪɴ ʏᴏᴜʀ ᴜᴘɪ ᴀᴘᴘ ᴀꜰᴛᴇʀ ᴘᴀʏᴍᴇɴᴛ).\n\n"
        f"_ᴇxᴀᴍᴘʟᴇ: `324812938471`_",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("❌ ᴄᴀɴᴄᴇʟ", callback_data="cancel_utr")]]))

@app.on_callback_query(filters.regex("^cancel_utr$"))
async def cb_cancel_utr(client, cb: CallbackQuery):
    await cb.answer("Cancelled ✓")
    _utr_state.pop(cb.from_user.id, None)
    await cb.message.reply("ᴘᴀʏᴍᴇɴᴛ ᴄᴀɴᴄᴇʟʟᴇᴅ. ʏᴏᴜ ᴄᴀɴ ᴛʀʏ ᴀɢᴀɪɴ ᴀɴʏᴛɪᴍᴇ ᴡɪᴛʜ /premium.")

@app.on_message(filters.private & filters.text & ~filters.command(["start","help","myfiles","stats","premium",
    "ban","unban","delfile","limit","broadcast","storage","users","payments","grantpremium","revokepremium","userinfo","filestats"]))
async def text_handler(client, message: Message):
    uid = message.from_user.id
    if uid not in _utr_state:
        return

    pay_id = _utr_state.pop(uid)
    utr    = message.text.strip()

    if not utr.isdigit() or not (8 <= len(utr) <= 20):
        await message.reply(
            "❌ **ɪɴᴠᴀʟɪᴅ ᴜᴛʀ**\n\n"
            "ᴜᴛʀ ᴍᴜꜱᴛ ʙᴇ ᴀ ɴᴜᴍʙᴇʀ, 8–20 ᴅɪɢɪᴛꜱ ʟᴏɴɢ.\n"
            "ᴘʟᴇᴀꜱᴇ ᴛʀʏ ᴀɢᴀɪɴ: ᴊᴜꜱᴛ ᴛʏᴘᴇ ᴛʜᴇ ɴᴜᴍʙᴇʀ.")
        _utr_state[uid] = pay_id
        return

    submit_utr(pay_id, utr)
    rec = get_payment_by_id(pay_id)

    await message.reply(
        f"✅ **ᴜᴛʀ ꜱᴜʙᴍɪᴛᴛᴇᴅ!**\n\n"
        f"🔑 ᴜᴛʀ: `{utr}`\n"
        f"🆔 ᴘᴀʏᴍᴇɴᴛ ɪᴅ: `{pay_id}`\n\n"
        f"ᴀᴅᴍɪɴ ᴡɪʟʟ ᴠᴇʀɪꜰʏ ᴀɴᴅ ᴀᴄᴛɪᴠᴀᴛᴇ ʏᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ ᴡɪᴛʜɪɴ **1–2 ʜᴏᴜʀꜱ**.\n"
        f"ʏᴏᴜ'ʟʟ ʀᴇᴄᴇɪᴠᴇ ᴀ ᴄᴏɴꜰɪʀᴍᴀᴛɪᴏɴ ᴍᴇꜱꜱᴀɢᴇ ʜᴇʀᴇ ᴏɴᴄᴇ ᴀᴘᴘʀᴏᴠᴇᴅ.\n\n"
        f"📞 ꜱᴜᴘᴘᴏʀᴛ: {DEV_USERNAME}")

    for admin_id in ADMINS:
        try:
            plan = PREMIUM_PLANS.get(rec.get("plan",""), {})
            await app.send_message(admin_id,
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"💰 **ɴᴇᴡ ᴘᴀʏᴍᴇɴᴛ — ᴀᴄᴛɪᴏɴ ʀᴇQᴜɪʀᴇᴅ**\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"👤 [{message.from_user.first_name}](tg://user?id={uid})\n"
                f"🔖 @{message.from_user.username or 'no_username'}\n"
                f"🆔 ᴜɪᴅ: `{uid}`\n"
                f"📦 ᴘʟᴀɴ: **{plan.get('label','?')}** — ₹{rec.get('amount','?')}\n"
                f"🔑 ᴜᴛʀ: `{utr}`\n"
                f"🆔 ᴘᴀʏᴍᴇɴᴛ ɪᴅ: `{pay_id}`",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("✅ ᴠᴇʀɪꜰʏ & ɢʀᴀɴᴛ", callback_data=f"verifypay_{pay_id}"),
                    InlineKeyboardButton("❌ ʀᴇᴊᴇᴄᴛ",          callback_data=f"rejectpay_{pay_id}"),
                ]]))
        except Exception as e:
            log.warning(f"Admin notify failed: {e}")

@app.on_callback_query(filters.regex(r"^verifypay_(\d+)$"))
async def cb_verify_pay(client, cb: CallbackQuery):
    if not is_admin(cb.from_user.id): await cb.answer("❌ ɴᴏᴛ ᴀᴅᴍɪɴ"); return
    pay_id = int(cb.matches[0].group(1))
    rec    = verify_payment(pay_id)
    if not rec: await cb.answer("ᴘᴀʏᴍᴇɴᴛ ɴᴏᴛ ꜰᴏᴜɴᴅ"); return

    plan = PREMIUM_PLANS.get(rec["plan"], {})
    grant_premium(rec["user_id"], plan.get("days", 30))
    await cb.answer("✅ ᴘʀᴇᴍɪᴜᴍ ɢʀᴀɴᴛᴇᴅ!")
    await cb.message.edit_text(
        f"✅ **ᴠᴇʀɪꜰɪᴇᴅ** — ᴘᴀʏᴍᴇɴᴛ `{pay_id}`\n"
        f"👤 ᴜɪᴅ: `{rec['user_id']}`\n"
        f"📦 ᴘʟᴀɴ: {plan.get('label','?')}\n"
        f"🔑 ᴜᴛʀ: `{rec.get('utr','?')}`\n"
        f"⚙️ ᴠᴇʀɪꜰɪᴇᴅ ʙʏ: @{cb.from_user.username}")
    try:
        await app.send_message(rec["user_id"],
            f"🎉 **ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴛɪᴠᴀᴛᴇᴅ!**\n\n"
            f"👑 **{plan.get('label','')} ᴘʟᴀɴ** ɪꜱ ɴᴏᴡ ᴀᴄᴛɪᴠᴇ!\n\n"
            f"ᴇɴᴊᴏʏ {BOT_TITLE} ᴘʀᴇᴍɪᴜᴍ! 🚀\n\n"
            f"ᴛʜᴀɴᴋꜱ ꜰᴏʀ ꜱᴜᴘᴘᴏʀᴛɪɴɢ ᴜꜱ! ❤️")
    except: pass

@app.on_callback_query(filters.regex(r"^rejectpay_(\d+)$"))
async def cb_reject_pay(client, cb: CallbackQuery):
    if not is_admin(cb.from_user.id): await cb.answer("❌ ɴᴏᴛ ᴀᴅᴍɪɴ"); return
    pay_id = int(cb.matches[0].group(1))
    rec    = get_payment_by_id(pay_id)
    reject_payment(pay_id)
    await cb.answer("❌ ʀᴇᴊᴇᴄᴛᴇᴅ")
    await cb.message.edit_text(
        f"❌ **ʀᴇᴊᴇᴄᴛᴇᴅ** — ᴘᴀʏᴍᴇɴᴛ `{pay_id}`\n"
        f"⚙️ ʀᴇᴊᴇᴄᴛᴇᴅ ʙʏ: @{cb.from_user.username}")
    if rec:
        try:
            await app.send_message(rec["user_id"],
                f"❌ **ᴘᴀʏᴍᴇɴᴛ ʀᴇᴊᴇᴄᴛᴇᴅ**\n\n"
                f"ᴘᴀʏᴍᴇɴᴛ `{pay_id}` (ᴜᴛʀ: `{rec.get('utr','?')}`) ᴄᴏᴜʟᴅ ɴᴏᴛ ʙᴇ ᴠᴇʀɪꜰɪᴇᴅ.\n\n"
                f"ɪꜰ ʏᴏᴜ ʙᴇʟɪᴇᴠᴇ ᴛʜɪꜱ ɪꜱ ᴀɴ ᴇʀʀᴏʀ, ᴄᴏɴᴛᴀᴄᴛ {DEV_USERNAME}.")
        except: pass

@app.on_message(filters.command("payments") & filters.private)
async def payments_cmd(client, message: Message):
    if not is_admin(message.from_user.id): return
    pending = get_pending_payments()
    if not pending:
        await message.reply("✅ ɴᴏ ᴘᴇɴᴅɪɴɢ ᴘᴀʏᴍᴇɴᴛꜱ."); return
    for p in pending[:10]:
        plan = PREMIUM_PLANS.get(p["plan"],{})
        await message.reply(
            f"💰 **ᴘᴀʏᴍᴇɴᴛ `{p['id']}`**\n"
            f"👤 ᴜɪᴅ: `{p['user_id']}`\n"
            f"📦 {plan.get('label','?')} — ₹{p['amount']}\n"
            f"🔑 ᴜᴛʀ: `{p['utr']}`\n"
            f"📅 {p['created_at'][:16]}",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("✅ ᴠᴇʀɪꜰʏ", callback_data=f"verifypay_{p['id']}"),
                InlineKeyboardButton("❌ ʀᴇᴊᴇᴄᴛ", callback_data=f"rejectpay_{p['id']}"),
            ]]))

@app.on_message(filters.command("grantpremium") & filters.private)
async def grant_cmd(client, message: Message):
    if not is_admin(message.from_user.id): return
    args = message.text.split()
    if len(args) < 3: await message.reply("ᴜꜱᴀɢᴇ: /grantpremium [uid] [days]"); return
    uid, days = int(args[1]), int(args[2])
    grant_premium(uid, days)
    await message.reply(f"✅ ᴘʀᴇᴍɪᴜᴍ ɢʀᴀɴᴛᴇᴅ ᴛᴏ `{uid}` ꜰᴏʀ **{days} ᴅᴀʏꜱ**.")
    try: await app.send_message(uid, f"🎉 ᴀᴅᴍɪɴ ɢʀᴀɴᴛᴇᴅ ʏᴏᴜ **{days} ᴅᴀʏꜱ ᴘʀᴇᴍɪᴜᴍ**!\n\nᴇɴᴊᴏʏ {BOT_TITLE}! 🚀")
    except: pass
    await log_event("ᴀᴅᴍɪɴ: ɢʀᴀɴᴛ ᴘʀᴇᴍɪᴜᴍ", message.from_user, f"ᴛᴀʀɢᴇᴛ ᴜɪᴅ: {uid}, ᴅᴀʏꜱ: {days}")

@app.on_message(filters.command("revokepremium") & filters.private)
async def revoke_cmd(client, message: Message):
    if not is_admin(message.from_user.id): return
    args = message.text.split()
    if len(args) < 2: await message.reply("ᴜꜱᴀɢᴇ: /revokepremium [uid]"); return
    revoke_premium(int(args[1]))
    await message.reply(f"✅ ᴘʀᴇᴍɪᴜᴍ ʀᴇᴠᴏᴋᴇᴅ ꜰᴏʀ `{args[1]}`.")

@app.on_message(filters.command("userinfo") & filters.private)
async def userinfo_cmd(client, message: Message):
    if not is_admin(message.from_user.id): return
    args = message.text.split()
    if len(args) < 2: await message.reply("ᴜꜱᴀɢᴇ: /userinfo [uid]"); return
    uid = int(args[1]); db = get_user(uid)
    if not db: await message.reply(f"ᴜꜱᴇʀ `{uid}` ɴᴏᴛ ꜰᴏᴜɴᴅ."); return
    files = get_user_files(uid)
    prem  = is_premium(uid)
    until = (db.get("premium_until") or "")[:10] or "—"
    await message.reply(
        f"╔══════════════════════╗\n"
        f"║   👤  ᴜꜱᴇʀ ɪɴꜰᴏ    ║\n"
        f"╚══════════════════════╝\n\n"
        f"**ɴᴀᴍᴇ:** {db['first_name']}\n"
        f"**ᴜꜱᴇʀɴᴀᴍᴇ:** @{db.get('username') or 'none'}\n"
        f"**ᴜɪᴅ:** `{uid}`\n"
        f"**ᴊᴏɪɴᴇᴅ:** {db['joined_at'][:10]}\n"
        f"**ʙᴀɴɴᴇᴅ:** {'🔴 ʏᴇꜱ' if db['is_banned'] else '🟢 ɴᴏ'}\n"
        f"**ᴘʀᴇᴍɪᴜᴍ:** {'👑 ʏᴇꜱ (ᴜɴᴛɪʟ '+until+')' if prem else '❌ ɴᴏ'}\n"
        f"**ʟɪᴍɪᴛ:** {human_size(get_user_limit(uid))}\n"
        f"**ꜰɪʟᴇꜱ:** {len(files)}\n"
        f"**ᴛᴏᴛᴀʟ ꜱɪᴢᴇ:** {human_size(sum(f['file_size'] for f in files))}")

@app.on_message(filters.command("users") & filters.private)
async def users_cmd(client, message: Message):
    if not is_admin(message.from_user.id): return
    count = get_user_count()
    await message.reply(f"👥 **ᴛᴏᴛᴀʟ ᴜꜱᴇʀꜱ:** `{count}`")

@app.on_message(filters.command("filestats") & filters.private)
async def filestats_cmd(client, message: Message):
    if not is_admin(message.from_user.id): return
    total_files = get_file_count()
    total_size  = get_total_storage_used()
    await message.reply(
        f"📁 **ꜰɪʟᴇ ꜱᴛᴀᴛɪꜱᴛɪᴄꜱ**\n\n"
        f"ᴛᴏᴛᴀʟ ꜰɪʟᴇꜱ: `{total_files}`\n"
        f"ᴛᴏᴛᴀʟ ꜱᴛᴏʀᴇᴅ: `{human_size(total_size)}`")

@app.on_message(filters.command("storage") & filters.private)
async def storage_cmd(client, message: Message):
    if not is_admin(message.from_user.id): return
    disk = shutil.disk_usage(FILES_DIR)
    used = get_total_storage_used()
    low  = disk.free < MIN_FREE_BYTES
    await message.reply(
        f"╔══════════════════════╗\n"
        f"║   💾  ᴅɪꜱᴋ ꜱᴛᴏʀᴀɢᴇ  ║\n"
        f"╚══════════════════════╝\n\n"
        f"📁 ꜰɪʟᴇꜱ ꜱᴛᴏʀᴇᴅ: `{get_file_count()}`\n"
        f"📦 ʙᴏᴛ ᴅᴀᴛᴀ: `{human_size(used)}`\n\n"
        f"🖥️ ᴅɪꜱᴋ ᴛᴏᴛᴀʟ: `{human_size(disk.total)}`\n"
        f"📊 ᴅɪꜱᴋ ᴜꜱᴇᴅ: `{human_size(disk.used)}`\n"
        f"✅ ᴅɪꜱᴋ ꜰʀᴇᴇ: `{human_size(disk.free)}`\n"
        f"⚠️ ᴍɪɴ ʀᴇQᴜɪʀᴇᴅ: `{human_size(MIN_FREE_BYTES)}`\n\n"
        f"{'🔴 **ᴡᴀʀɴɪɴɢ: ʟᴏᴡ ᴅɪꜱᴋ ꜱᴘᴀᴄᴇ!**' if low else '🟢 ꜱᴛᴏʀᴀɢᴇ ᴏᴋ'}")

@app.on_message(filters.private & (
    filters.video | filters.audio | filters.document |
    filters.voice | filters.video_note | filters.animation
))
async def file_handler(client, message: Message):
    user = message.from_user
    db   = get_user(user.id)
    if not db:
        register_user(user.id, user.username, user.first_name)
        db = get_user(user.id)
    if db["is_banned"]:
        await message.reply("🚫 ʏᴏᴜ ᴀʀᴇ ʙᴀɴɴᴇᴅ ꜰʀᴏᴍ ᴜꜱɪɴɢ ᴛʜɪꜱ ʙᴏᴛ."); return
    ok, reason = check_rate_limit(user.id)
    if not ok: await message.reply(reason); return

    media = (message.video or message.audio or message.document or
             message.voice or message.video_note or message.animation)
    if not media: await message.reply("❌ ᴜɴꜱᴜᴘᴘᴏʀᴛᴇᴅ ꜰɪʟᴇ ᴛʏᴘᴇ."); return

    file_size  = media.file_size or 0
    user_limit = get_user_limit(user.id)
    if file_size > user_limit:
        await message.reply(
            f"❌ **ꜰɪʟᴇ ᴛᴏᴏ ʟᴀʀɢᴇ**\n\n"
            f"📦 ꜰɪʟᴇ: `{human_size(file_size)}`\n"
            f"📏 ʏᴏᴜʀ ʟɪᴍɪᴛ: `{human_size(user_limit)}`\n\n"
            f"ᴄᴏɴᴛᴀᴄᴛ {DEV_USERNAME} ᴛᴏ ɪɴᴄʀᴇᴀꜱᴇ ʏᴏᴜʀ ʟɪᴍɪᴛ."); return

    if not disk_has_space():
        await message.reply(
            "⚠️ **ꜱᴇʀᴠᴇʀ ꜱᴛᴏʀᴀɢᴇ ꜰᴜʟʟ**\n\n"
            "ᴛʜᴇ ꜱᴇʀᴠᴇʀ ɪꜱ ᴀʟᴍᴏꜱᴛ ᴏᴜᴛ ᴏꜰ ᴅɪꜱᴋ ꜱᴘᴀᴄᴇ.\n"
            f"ᴄᴏɴᴛᴀᴄᴛ {DEV_USERNAME}."); return

    proc = await message.reply(
        "📥 **𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍𝚒𝚗𝚐 𝚝𝚘 𝚜𝚎𝚛𝚟𝚎𝚛…**\n\n"
        "`░░░░░░░░░░` 0%")

    file_hash = None
    try:
        file_id        = media.file_id
        file_unique_id = media.file_unique_id
        file_hash      = generate_hash(file_unique_id)
        mime_type      = getattr(media, "mime_type", None) or ""
        file_name      = getattr(media, "file_name", None) or f"file_{file_unique_id}"
        file_type      = ("video"    if (message.video or message.video_note or message.animation)
                          else "audio" if (message.audio or message.voice) else "document")

        existing = get_file_by_hash(file_hash)
        if (existing and existing.get("status") == "ready"
                and existing.get("local_path")
                and os.path.exists(existing.get("local_path",""))):
            dl_tok = existing.get("dl_token") or make_dl_token(file_hash)
            await _send_ready_msg(proc, existing, stream_url(file_hash),
                                  download_url(file_hash, dl_tok),
                                  is_streamable(mime_type) or file_type in ("video","audio"),
                                  cached=True)
            await log_event("ꜰɪʟᴇ ᴜᴘʟᴏᴀᴅᴇᴅ (ᴄᴀᴄʜᴇᴅ)", user, "ꜰɪʟᴇ ᴀʟʀᴇᴀᴅʏ ᴏɴ ᴅɪꜱᴋ.", existing)
            return

        dl_tok = make_dl_token(file_hash)
        if not existing:
            save_file(file_id, file_hash, user.id, file_name, file_type,
                      file_size, mime_type, dl_token=dl_tok)

        dest_dir  = os.path.join(FILES_DIR, file_hash[:2])
        os.makedirs(dest_dir, exist_ok=True)
        dest_path = os.path.join(dest_dir, file_name)

        last_pct = [0]
        async def progress(current, total):
            pct = int(current * 100 / total) if total else 0
            if pct - last_pct[0] >= 5:
                last_pct[0] = pct
                filled = pct // 10; empty = 10 - filled
                bar = "█"*filled + "░"*empty
                try:
                    await proc.edit(
                        f"📥 **𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍𝚒𝚗𝚐 𝚝𝚘 𝚜𝚎𝚛𝚟𝚎𝚛…**\n\n"
                        f"`{bar}` **{pct}%**\n"
                        f"`{human_size(current)}` / `{human_size(total)}`")
                except: pass

        path = await client.download_media(message, file_name=dest_path, progress=progress)
        if not path or not os.path.exists(path):
            raise Exception("ᴅᴏᴡɴʟᴏᴀᴅ ꜰᴀɪʟᴇᴅ — ꜰɪʟᴇ ᴍɪꜱꜱɪɴɢ ᴀꜰᴛᴇʀ ᴅᴏᴡɴʟᴏᴀᴅ.")

        set_file_ready(file_hash, path, dl_tok)
        rec = get_file_by_hash(file_hash)
        streamable = is_streamable(mime_type) or file_type in ("video","audio")
        await _send_ready_msg(proc, rec, stream_url(file_hash),
                              download_url(file_hash, dl_tok), streamable)
        await log_event("ꜰɪʟᴇ ᴜᴘʟᴏᴀᴅᴇᴅ", user, f"ᴘᴀᴛʜ: {path}", rec)

    except Exception as e:
        log.error(f"File handler error: {e}", exc_info=True)
        if file_hash:
            try: set_file_error(file_hash)
            except: pass
        await proc.edit(
            f"❌ **𝚄𝚙𝚕𝚘𝚊𝚍 𝙵𝚊𝚒𝚕𝚎𝚍**\n\n"
            f"`{str(e)[:200]}`\n\n"
            f"ᴘʟᴇᴀꜱᴇ ᴛʀʏ ᴀɢᴀɪɴ ᴏʀ ᴄᴏɴᴛᴀᴄᴛ {DEV_USERNAME}")

async def _send_ready_msg(msg, rec, s_url, d_url, streamable, cached=False):
    fn = rec["file_name"]; fs = rec["file_size"]; ft = rec["file_type"]
    cache_note = "\n♻️ _ꜱᴇʀᴠᴇᴅ ꜰʀᴏᴍ ᴄᴀᴄʜᴇ_" if cached else ""
    if streamable:
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("▶️ 𝚂𝚝𝚛𝚎𝚊𝚖 𝙽𝚘𝚠", url=s_url),
             InlineKeyboardButton("⬇️ ᴍʏ ᴅᴏᴡɴʟᴏᴀᴅ", url=d_url)],
            [InlineKeyboardButton("📂 ᴍʏ ꜰɪʟᴇꜱ", callback_data="my_files")],
        ])
        text = (
            f"╔══════════════════════╗\n"
            f"║   ✅  𝙵𝙸𝙻𝙴 𝚁𝙴𝙰𝙳𝚈!  ║\n"
            f"╚══════════════════════╝\n\n"
            f"📄 **{fn}**\n"
            f"📦 ꜱɪᴢᴇ: `{human_size(fs)}`\n"
            f"🎞️ ᴛʏᴘᴇ: `{ft.capitalize()}`{cache_note}\n\n"
            f"🌐 **𝚂𝚝𝚛𝚎𝚊𝚖 𝙻𝚒𝚗𝚔** _(ꜱʜᴀʀᴇᴀʙʟᴇ)_\n"
            f"`{s_url}`\n\n"
            f"🔒 **𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍 𝙻𝚒𝚗𝚔** _(ᴘʀɪᴠᴀᴛᴇ — ᴏɴʟʏ ʏᴏᴜ)_\n"
            f"`{d_url}`\n\n"
            f"✨ ᴍᴜʟᴛɪ-ᴀᴜᴅɪᴏ · ᴍᴜʟᴛɪ-ꜱᴜʙ · ᴍᴜʟᴛɪ-Qᴜᴀʟɪᴛʏ ᴘʟᴀʏᴇʀ\n"
            f"♾️ ʟɪɴᴋꜱ ɴᴇᴠᴇʀ ᴇxᴘɪʀᴇ!")
    else:
        markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("⬇️ ᴍʏ ᴅᴏᴡɴʟᴏᴀᴅ", url=d_url)],
            [InlineKeyboardButton("📂 ᴍʏ ꜰɪʟᴇꜱ", callback_data="my_files")],
        ])
        text = (
            f"╔══════════════════════╗\n"
            f"║   ✅  𝙵𝙸𝙻𝙴 𝚁𝙴𝙰𝙳𝚈!  ║\n"
            f"╚══════════════════════╝\n\n"
            f"📄 **{fn}**\n"
            f"📦 ꜱɪᴢᴇ: `{human_size(fs)}`{cache_note}\n\n"
            f"🔒 **𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍 𝙻𝚒𝚗𝚔** _(ᴘʀɪᴠᴀᴛᴇ — ᴏɴʟʏ ʏᴏᴜ)_\n"
            f"`{d_url}`\n\n"
            f"♾️ ʟɪɴᴋ ɴᴇᴠᴇʀ ᴇxᴘɪʀᴇꜱ!")
    await msg.edit(text, reply_markup=markup)

@app.on_message(filters.command("ban") & filters.private)
async def ban_cmd(client, message: Message):
    if not is_admin(message.from_user.id): return
    args = message.text.split()
    if len(args)<2: await message.reply("ᴜꜱᴀɢᴇ: /ban [uid]"); return
    uid = int(args[1]); ban_user(uid)
    await message.reply(f"✅ ᴜꜱᴇʀ `{uid}` ʙᴀɴɴᴇᴅ.")
    try: await app.send_message(uid, f"🚫 ʏᴏᴜ ʜᴀᴠᴇ ʙᴇᴇɴ **ʙᴀɴɴᴇᴅ**.\nᴄᴏɴᴛᴀᴄᴛ {DEV_USERNAME} ᴛᴏ ᴀᴘᴘᴇᴀʟ.")
    except: pass
    await log_event("ᴀᴅᴍɪɴ: ʙᴀɴ ᴜꜱᴇʀ", message.from_user, f"ʙᴀɴɴᴇᴅ ᴜɪᴅ: {uid}")

@app.on_message(filters.command("unban") & filters.private)
async def unban_cmd(client, message: Message):
    if not is_admin(message.from_user.id): return
    args = message.text.split()
    if len(args)<2: await message.reply("ᴜꜱᴀɢᴇ: /unban [uid]"); return
    uid = int(args[1]); unban_user(uid)
    await message.reply(f"✅ ᴜꜱᴇʀ `{uid}` ᴜɴʙᴀɴɴᴇᴅ.")
    try: await app.send_message(uid, "✅ ʏᴏᴜ ʜᴀᴠᴇ ʙᴇᴇɴ **ᴜɴʙᴀɴɴᴇᴅ**! ᴡᴇʟᴄᴏᴍᴇ ʙᴀᴄᴋ.")
    except: pass

@app.on_message(filters.command("delfile") & filters.private)
async def delfile_cmd(client, message: Message):
    if not is_admin(message.from_user.id): return
    args = message.text.split()
    if len(args)<2: await message.reply("ᴜꜱᴀɢᴇ: /delfile [file_hash]"); return
    fh = args[1]; rec = get_file_by_hash(fh)
    if rec and rec.get("local_path") and os.path.exists(rec["local_path"]):
        os.remove(rec["local_path"])
    if rec: delete_file_by_hash(fh)
    await message.reply(f"🗑️ ꜰɪʟᴇ `{fh}` ᴅᴇʟᴇᴛᴇᴅ ꜰʀᴏᴍ ᴅɪꜱᴋ ᴀɴᴅ ᴅᴀᴛᴀʙᴀꜱᴇ.")

@app.on_message(filters.command("limit") & filters.private)
async def limit_cmd(client, message: Message):
    if not is_admin(message.from_user.id): return
    args = message.text.split()
    if len(args)<3: await message.reply("ᴜꜱᴀɢᴇ: /limit [uid] [size]gb/mb"); return
    uid = int(args[1]); sz = parse_size_arg(args[2])
    set_user_limit(uid, sz)
    await message.reply(f"✅ ᴜᴘʟᴏᴀᴅ ʟɪᴍɪᴛ ꜰᴏʀ `{uid}` ꜱᴇᴛ ᴛᴏ `{human_size(sz)}`.")
    try: await app.send_message(uid, f"📦 ʏᴏᴜʀ ᴜᴘʟᴏᴀᴅ ʟɪᴍɪᴛ ᴡᴀꜱ ᴜᴘᴅᴀᴛᴇᴅ ᴛᴏ **{human_size(sz)}**.")
    except: pass

@app.on_message(filters.command("broadcast") & filters.private)
async def broadcast_cmd(client, message: Message):
    if not is_admin(message.from_user.id): return
    parts = message.text.split(None, 1)
    if len(parts)<2: await message.reply("ᴜꜱᴀɢᴇ: /broadcast [text]"); return
    users = get_all_users(); sent = failed = 0
    sm    = await message.reply(f"📢 𝙱𝚛𝚘𝚊𝚍𝚌𝚊𝚜𝚝𝚒𝚗𝚐 ᴛᴏ **{len(users)}** ᴜꜱᴇʀꜱ…")
    for uid in users:
        try: await app.send_message(uid, parts[1]); sent+=1
        except: failed+=1
        await asyncio.sleep(0.05)
    await sm.edit(f"📢 **𝙱𝚛𝚘𝚊𝚍𝚌𝚊𝚜𝚝 𝙲𝚘𝚖𝚙𝚕𝚎𝚝𝚎!**\n\n✅ ꜱᴇɴᴛ: `{sent}`\n❌ ꜰᴀɪʟᴇᴅ: `{failed}`")
