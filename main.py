# main.py
from database import init_db
from scheduler import start_scheduler
from bot import start_bot
from config import TOKEN
from telegram.ext import Updater  # Updater sınıfını içe aktar

def main():
    # Veritabanını başlat
    init_db()

    # Botu başlat
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Komutları ve zamanlayıcıyı başlat
    start_bot(dispatcher)
    start_scheduler(dispatcher)

    # Botu çalıştır
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
