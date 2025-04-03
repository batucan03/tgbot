# database.py
import sqlite3
import json
from datetime import datetime
from config import MAX_CHANNELS

def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        balance INTEGER DEFAULT 0,
        channels TEXT DEFAULT '[]',
        stats TEXT DEFAULT '{}',
        is_admin INTEGER DEFAULT 0,
        settings TEXT DEFAULT '{}',
        prompts TEXT DEFAULT '[]'
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS activation_codes (
        code TEXT PRIMARY KEY,
        balance INTEGER,
        used INTEGER DEFAULT 0,
        user_id INTEGER
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS posts (
        post_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        channel_id TEXT,
        content TEXT,
        timestamp TEXT
    )''')
    conn.commit()
    conn.close()

def activate_code(user_id, code):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT balance, used FROM activation_codes WHERE code = ?", (code,))
    result = c.fetchone()
    if not result:
        return "Geçersiz kod!"
    balance, used = result
    if used:
        return "Bu kod zaten kullanılmış!"
    
    c.execute("SELECT balance, settings FROM users WHERE user_id = ?", (user_id,))
    user = c.fetchone()
    if user:
        current_balance, settings = user
        new_balance = current_balance + balance
        c.execute("UPDATE users SET balance = ? WHERE user_id = ?", (new_balance, user_id))
    else:
        new_balance = balance
        settings = json.dumps({'approval': False, 'images': False, 'template': '{title}\n{summary}\nKaynak: {link}', 'concept': ''})
        c.execute("INSERT INTO users (user_id, balance, settings) VALUES (?, ?, ?)", (user_id, new_balance, settings))
    
    c.execute("UPDATE activation_codes SET used = 1, user_id = ? WHERE code = ?", (user_id, code))
    conn.commit()
    conn.close()
    return f"Kod aktif edildi! Yeni bakiyeniz: {new_balance} paylaşım"

def add_activation_code(code, balance):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("INSERT INTO activation_codes (code, balance, used, user_id) VALUES (?, ?, 0, NULL)", (code, balance))
    conn.commit()
    conn.close()

def get_balance(user_id):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else 0

def decrease_balance(user_id):
    balance = get_balance(user_id)
    if balance <= 0:
        return False
    new_balance = balance - 1
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("UPDATE users SET balance = ? WHERE user_id = ?", (new_balance, user_id))
    conn.commit()
    conn.close()
    return True

def add_channel(user_id, channel_id):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT channels FROM users WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    if not result:
        return "Önce bir kod aktif edin!"
    channels = json.loads(result[0])
    if channel_id in channels:
        return "Bu kanal zaten ekli!"
    if len(channels) >= MAX_CHANNELS:
        return f"Maksimum kanal sayısına ulaştınız ({MAX_CHANNELS})!"
    channels.append(channel_id)
    c.execute("UPDATE users SET channels = ? WHERE user_id = ?", (json.dumps(channels), user_id))
    conn.commit()
    conn.close()
    return "Kanal başarıyla eklendi!"

def get_channels(user_id):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT channels FROM users WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    conn.close()
    return json.loads(result[0]) if result else []

def log_post(user_id, channel_id, content):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    timestamp = datetime.now().isoformat()
    c.execute("INSERT INTO posts (user_id, channel_id, content, timestamp) VALUES (?, ?, ?, ?)",
              (user_id, channel_id, content, timestamp))
    conn.commit()
    conn.close()

def get_stats(user_id):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT channel_id, content FROM posts WHERE user_id = ?", (user_id,))
    posts = c.fetchall()
    total_posts = len(posts)
    channel_counts = {}
    for post in posts:
        channel_id = post[0]
        channel_counts[channel_id] = channel_counts.get(channel_id, 0) + 1
    conn.close()
    return {"total_posts": total_posts, "channel_counts": channel_counts}

def get_settings(user_id):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT settings FROM users WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    conn.close()
    return json.loads(result[0]) if result else {'approval': False, 'images': False, 'template': '{title}\n{summary}\nKaynak: {link}', 'concept': ''}

def update_settings(user_id, settings):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("UPDATE users SET settings = ? WHERE user_id = ?", (json.dumps(settings), user_id))
    conn.commit()
    conn.close()

def add_prompt(user_id, prompt):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT prompts FROM users WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    if not result:
        prompts = []
    else:
        prompts = json.loads(result[0])
    prompts.append(prompt)
    c.execute("UPDATE users SET prompts = ? WHERE user_id = ?", (json.dumps(prompts), user_id))
    conn.commit()
    conn.close()

def get_prompts(user_id):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT prompts FROM users WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    conn.close()
    return json.loads(result[0]) if result else []
