import sqlite3
from config import DB_PATH

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, balance INTEGER DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS channels (
        user_id INTEGER, channel_id TEXT, settings TEXT,
        PRIMARY KEY (user_id, channel_id)
    )''')
    conn.commit()
    conn.close()

def add_channel(user_id, channel_id, settings):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    import json
    settings_json = json.dumps(settings)
    c.execute("INSERT OR REPLACE INTO channels (user_id, channel_id, settings) VALUES (?, ?, ?)",
              (user_id, channel_id, settings_json))
    conn.commit()
    conn.close()

def get_channels(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT channel_id, settings FROM channels WHERE user_id = ?", (user_id,))
    rows = c.fetchall()
    conn.close()
    import json
    return {row[0]: json.loads(row[1]) for row in rows}

def get_balance(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else 0

def get_stats(user_id):
    # Örnek istatistik fonksiyonu, gerekirse güncelle
    return {'total_posts': 0, 'channel_counts': {}}
