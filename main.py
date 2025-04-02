import feedparser
import requests
import schedule
import time
import json
import os
import random
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

TOKEN = os.environ.get("TOKEN")
BASE_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
ADMIN_CHAT_ID = "6120131340"  # Kendi admin kanalını yaz

settings = [
    {
        "rss_url": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
        "chat_id": "@globalhabers",  # Kendi kanalını yaz
        "frequency": 3600,  # 1 saat
        "max_length": 200,
        "format": "{title}\n{summary}\nKaynak: {link}"
    }
]

LAST_POST_FILE = "last_posts.json"

def summarize_text(text, max_length):
    try:
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, 2)
        return " ".join([str(sentence) for sentence in summary])[:max_length]
    except:
        return text[:max_length]

def send_to_telegram(chat_id, text):
    payload = {"chat_id": chat_id, "text": text}
    response = requests.post(BASE_URL, data=payload)
    if not response.ok:
        send_to_telegram(ADMIN_CHAT_ID, f"Hata: {chat_id} kanalına mesaj gönderilemedi")

def get_shared_posts(rss_url):
    try:
        with open(LAST_POST_FILE, "r") as f:
            data = json.load(f)
            return data.get(rss_url, [])
    except:
        return []

def update_shared_posts(rss_url, post_id):
    try:
        with open(LAST_POST_FILE, "r") as f:
            data = json.load(f)
    except:
        data = {}
    if rss_url not in data:
        data[rss_url] = []
    data[rss_url].append(post_id)
    with open(LAST_POST_FILE, "w") as f:
        json.dump(data, f)

def process_feed(setting):
    feed = feedparser.parse(setting["rss_url"])
    if not feed.entries:
        send_to_telegram(ADMIN_CHAT_ID, f"Hata: {setting['rss_url']} çalışmıyor")
