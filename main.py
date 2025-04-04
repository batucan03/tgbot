# main.py
from database import init_db
from scheduler import start_scheduler
from bot import start_bot
from config import TOKEN
from telegram.ext import Updater
import http.server
import socketserver
import threading

def start_health_check_server():
    # 8000 portunda basit bir HTTP sunucusu başlat
    PORT = 8000
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Health check server running on port {PORT}")
        httpd.serve_forever()

def main():
    # Veritabanını başlat
    init_db()

    # Botu başlat
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Komutları ve zamanlayıcıyı başlat
    start_bot(dispatcher)
    start_scheduler(dispatcher)

    # Sağlık kontrolü sunucusunu ayrı bir thread'de başlat
    health_check_thread = threading.Thread(target=start_health_check_server, daemon=True)
    health_check_thread.start()

    # Botu çalıştır
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
