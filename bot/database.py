"""
             Project By - @TEAM_X_OG Known As TEAMDEV
      
      Developer - @MR_ARMAN_08

This Is Open-source You Can Modify It And Use As You Want
butt Removing Credits It's Not Allowed.

GitHub - https://github.com/TeamDev-07/FileToLink-TeamDev

"""


import sqlite3, os, json, time, datetime
from config.config import DB_PATH, MAX_FILE_SIZE

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False, timeout=30)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    return conn

def init_db():
    conn = get_conn(); c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            user_id       INTEGER PRIMARY KEY,
            username      TEXT,
            first_name    TEXT,
            joined_at     TEXT DEFAULT (datetime('now')),
            is_banned     INTEGER DEFAULT 0,
            max_limit     INTEGER DEFAULT 0,
            is_premium    INTEGER DEFAULT 0,
            premium_until TEXT DEFAULT NULL
        );
        CREATE TABLE IF NOT EXISTS files (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            file_id      TEXT UNIQUE,
            file_hash    TEXT UNIQUE,
            user_id      INTEGER,
            file_name    TEXT,
            file_type    TEXT,
            file_size    INTEGER,
            mime_type    TEXT,
            local_path   TEXT DEFAULT '',
            status       TEXT DEFAULT 'pending',
            dl_token     TEXT DEFAULT '',
            uploaded_at  TEXT DEFAULT (datetime('now')),
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        );
        CREATE TABLE IF NOT EXISTS rate_limits (
            user_id   INTEGER PRIMARY KEY,
            last_cmd  REAL DEFAULT 0,
            msg_times TEXT DEFAULT '[]'
        );
        CREATE TABLE IF NOT EXISTS premium_payments (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER,
            plan        TEXT,
            amount      INTEGER,
            utr         TEXT DEFAULT '',
            status      TEXT DEFAULT 'pending',
            created_at  TEXT DEFAULT (datetime('now')),
            verified_at TEXT DEFAULT NULL
        );
    """)

    for table, col, defn in [
        ("files",  "local_path",   "TEXT DEFAULT ''"),
        ("files",  "status",       "TEXT DEFAULT 'pending'"),
        ("files",  "dl_token",     "TEXT DEFAULT ''"),
        ("users",  "is_premium",   "INTEGER DEFAULT 0"),
        ("users",  "premium_until","TEXT DEFAULT NULL"),
    ]:
        existing = [r[1] for r in c.execute(f"PRAGMA table_info({table})").fetchall()]
        if col not in existing:
            c.execute(f"ALTER TABLE {table} ADD COLUMN {col} {defn}")
    conn.commit(); conn.close()

def register_user(uid, username, first_name):
    conn = get_conn()
    conn.execute("""INSERT INTO users(user_id,username,first_name) VALUES(?,?,?)
        ON CONFLICT(user_id) DO UPDATE SET username=excluded.username,first_name=excluded.first_name""",
        (uid, username, first_name))
    conn.commit(); conn.close()

def get_user(uid):
    conn = get_conn()
    row = conn.execute("SELECT * FROM users WHERE user_id=?", (uid,)).fetchone()
    conn.close(); return dict(row) if row else None

def ban_user(uid):
    conn=get_conn(); conn.execute("UPDATE users SET is_banned=1 WHERE user_id=?",(uid,)); conn.commit(); conn.close()

def unban_user(uid):
    conn=get_conn(); conn.execute("UPDATE users SET is_banned=0 WHERE user_id=?",(uid,)); conn.commit(); conn.close()

def set_user_limit(uid, size):
    conn=get_conn(); conn.execute("UPDATE users SET max_limit=? WHERE user_id=?",(size,uid)); conn.commit(); conn.close()

def get_user_limit(uid):
    conn=get_conn(); row=conn.execute("SELECT max_limit FROM users WHERE user_id=?",(uid,)).fetchone(); conn.close()
    return row[0] if row and row[0] > 0 else MAX_FILE_SIZE

def get_all_users():
    conn=get_conn(); rows=conn.execute("SELECT user_id FROM users WHERE is_banned=0").fetchall(); conn.close()
    return [r[0] for r in rows]

def get_user_count():
    conn=get_conn(); row=conn.execute("SELECT COUNT(*) FROM users").fetchone(); conn.close(); return row[0]

def is_premium(uid):
    conn=get_conn(); row=conn.execute("SELECT is_premium,premium_until FROM users WHERE user_id=?",(uid,)).fetchone(); conn.close()
    if not row or not row["is_premium"]: return False
    if row["premium_until"]:
        until = datetime.datetime.fromisoformat(row["premium_until"])
        if datetime.datetime.utcnow() > until:
            conn2=get_conn(); conn2.execute("UPDATE users SET is_premium=0 WHERE user_id=?",(uid,)); conn2.commit(); conn2.close()
            return False
    return True

def grant_premium(uid, days):
    until = (datetime.datetime.utcnow() + datetime.timedelta(days=days)).isoformat()
    conn=get_conn(); conn.execute("UPDATE users SET is_premium=1,premium_until=? WHERE user_id=?",(until,uid)); conn.commit(); conn.close()

def revoke_premium(uid):
    conn=get_conn(); conn.execute("UPDATE users SET is_premium=0,premium_until=NULL WHERE user_id=?",(uid,)); conn.commit(); conn.close()

def save_file(file_id, file_hash, user_id, file_name, file_type, file_size, mime_type, local_path="", status="pending", dl_token=""):
    conn=get_conn()
    conn.execute("""INSERT OR IGNORE INTO files
        (file_id,file_hash,user_id,file_name,file_type,file_size,mime_type,local_path,status,dl_token)
        VALUES(?,?,?,?,?,?,?,?,?,?)""",
        (file_id,file_hash,user_id,file_name,file_type,file_size,mime_type,local_path,status,dl_token))
    conn.commit(); conn.close()

def set_file_ready(file_hash, local_path, dl_token):
    conn=get_conn(); conn.execute("UPDATE files SET local_path=?,status='ready',dl_token=? WHERE file_hash=?",(local_path,dl_token,file_hash)); conn.commit(); conn.close()

def set_file_error(file_hash):
    conn=get_conn(); conn.execute("UPDATE files SET status='error' WHERE file_hash=?",(file_hash,)); conn.commit(); conn.close()

def get_file_by_hash(fh):
    conn=get_conn(); row=conn.execute("SELECT * FROM files WHERE file_hash=?",(fh,)).fetchone(); conn.close()
    return dict(row) if row else None

def get_file_by_id(fid):
    conn=get_conn(); row=conn.execute("SELECT * FROM files WHERE file_id=?",(fid,)).fetchone(); conn.close()
    return dict(row) if row else None

def delete_file_by_hash(fh):
    conn=get_conn(); conn.execute("DELETE FROM files WHERE file_hash=?",(fh,)); conn.commit(); conn.close()

def get_user_files(uid):
    conn=get_conn(); rows=conn.execute("SELECT * FROM files WHERE user_id=? ORDER BY uploaded_at DESC",(uid,)).fetchall(); conn.close()
    return [dict(r) for r in rows]

def get_all_files_ordered():
    conn=get_conn(); rows=conn.execute("SELECT * FROM files WHERE status='ready' ORDER BY uploaded_at ASC").fetchall(); conn.close()
    return [dict(r) for r in rows]

def get_total_storage_used():
    conn=get_conn(); row=conn.execute("SELECT SUM(file_size) FROM files WHERE status='ready'").fetchone(); conn.close()
    return row[0] or 0

def get_file_count():
    conn=get_conn(); row=conn.execute("SELECT COUNT(*) FROM files WHERE status='ready'").fetchone(); conn.close(); return row[0]

def scan_and_recover():
    """
    On startup: scan FILES_DIR for files that exist on disk but are marked
    'pending' or 'error' in DB (e.g. bot crashed mid-download).
    Re-verify and mark them 'ready' so links keep working after restart.
    """
    from config.config import FILES_DIR
    conn = get_conn()
    rows = conn.execute("SELECT * FROM files WHERE status IN ('ready','pending','error')").fetchall()
    recovered = 0
    for row in rows:
        rec = dict(row)
        lp  = rec.get("local_path","")
        if lp and os.path.exists(lp) and os.path.getsize(lp) > 0:
            if rec["status"] != "ready":
                conn.execute("UPDATE files SET status='ready' WHERE file_hash=?", (rec["file_hash"],))
                recovered += 1
        elif rec["status"] == "ready" and (not lp or not os.path.exists(lp)):
            
            conn.execute("UPDATE files SET status='error' WHERE file_hash=?", (rec["file_hash"],))
    conn.commit(); conn.close()
    return recovered

def create_payment(uid, plan, amount):
    conn=get_conn(); conn.execute("INSERT INTO premium_payments(user_id,plan,amount) VALUES(?,?,?)",(uid,plan,amount)); conn.commit()
    rid=conn.execute("SELECT last_insert_rowid()").fetchone()[0]; conn.close(); return rid

def submit_utr(pay_id, utr):
    conn=get_conn(); conn.execute("UPDATE premium_payments SET utr=? WHERE id=?",(utr,pay_id)); conn.commit(); conn.close()

def get_pending_payments():
    conn=get_conn(); rows=conn.execute("SELECT * FROM premium_payments WHERE status='pending' AND utr!='' ORDER BY created_at DESC").fetchall(); conn.close()
    return [dict(r) for r in rows]

def verify_payment(pay_id):
    conn=get_conn()
    row=conn.execute("SELECT * FROM premium_payments WHERE id=?",(pay_id,)).fetchone()
    if row: conn.execute("UPDATE premium_payments SET status='verified',verified_at=datetime('now') WHERE id=?",(pay_id,))
    conn.commit(); conn.close(); return dict(row) if row else None

def reject_payment(pay_id):
    conn=get_conn(); conn.execute("UPDATE premium_payments SET status='rejected' WHERE id=?",(pay_id,)); conn.commit(); conn.close()

def get_payment_by_id(pay_id):
    conn=get_conn(); row=conn.execute("SELECT * FROM premium_payments WHERE id=?",(pay_id,)).fetchone(); conn.close()
    return dict(row) if row else None

def check_rate_limit(uid, command_gap=5, flood_limit=10, flood_window=10):
    conn=get_conn(); row=conn.execute("SELECT * FROM rate_limits WHERE user_id=?",(uid,)).fetchone(); now=time.time()
    last_cmd=row["last_cmd"] if row else 0; msg_times=json.loads(row["msg_times"]) if row else []
    if now-last_cmd < command_gap: conn.close(); return False, f"⏳ Please wait {command_gap-int(now-last_cmd)}s."
    msg_times=[t for t in msg_times if now-t < flood_window]
    if len(msg_times) >= flood_limit: conn.close(); return False, "🚫 Slow down!"
    msg_times.append(now)
    conn.execute("INSERT INTO rate_limits(user_id,last_cmd,msg_times) VALUES(?,?,?) ON CONFLICT(user_id) DO UPDATE SET last_cmd=excluded.last_cmd,msg_times=excluded.msg_times",
        (uid,now,json.dumps(msg_times)))
    conn.commit(); conn.close(); return True, None
