import sqlite3
import json
from datetime import datetime
from config import DB_PATH
import os

# ─── Init ──────────────────────────────────────────────────────────────────────
def init_db():
    os.makedirs("database", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS saved_looks (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id  TEXT,
            occasion    TEXT,
            season      TEXT,
            budget      TEXT,
            style_pref  TEXT,
            face_shape  TEXT,
            gender      TEXT,
            outfit_rec  TEXT,
            hair_rec    TEXT,
            makeup_rec  TEXT,
            accessory_rec TEXT,
            color_palette TEXT,
            fashion_score TEXT,
            full_report TEXT,
            created_at  TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id  TEXT,
            role        TEXT,
            message     TEXT,
            created_at  TEXT
        )
    """)

    conn.commit()
    conn.close()

# ─── Save Look ─────────────────────────────────────────────────────────────────
def save_look(session_id, data: dict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO saved_looks
        (session_id, occasion, season, budget, style_pref, face_shape, gender,
         outfit_rec, hair_rec, makeup_rec, accessory_rec, color_palette,
         fashion_score, full_report, created_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        session_id,
        data.get("occasion", ""),
        data.get("season", ""),
        data.get("budget", ""),
        data.get("style_pref", ""),
        data.get("face_shape", ""),
        data.get("gender", ""),
        data.get("outfit_rec", ""),
        data.get("hair_rec", ""),
        data.get("makeup_rec", ""),
        data.get("accessory_rec", ""),
        json.dumps(data.get("color_palette", [])),
        data.get("fashion_score", ""),
        data.get("full_report", ""),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    conn.commit()
    conn.close()

# ─── Get Saved Looks ───────────────────────────────────────────────────────────
def get_saved_looks(session_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT id, occasion, season, budget, style_pref, face_shape,
               gender, outfit_rec, hair_rec, makeup_rec, accessory_rec,
               color_palette, fashion_score, full_report, created_at
        FROM saved_looks WHERE session_id=? ORDER BY id DESC
    """, (session_id,))
    rows = c.fetchall()
    conn.close()
    return rows

# ─── Delete Look ───────────────────────────────────────────────────────────────
def delete_look(look_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM saved_looks WHERE id=?", (look_id,))
    conn.commit()
    conn.close()

# ─── Chat History ──────────────────────────────────────────────────────────────
def save_chat_message(session_id, role, message):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO chat_history (session_id, role, message, created_at)
        VALUES (?,?,?,?)
    """, (session_id, role, message, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def get_chat_history(session_id, limit=50):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT role, message FROM chat_history
        WHERE session_id=? ORDER BY id DESC LIMIT ?
    """, (session_id, limit))
    rows = c.fetchall()
    conn.close()
    return list(reversed(rows))
