# main.py
from telegram.ext import Updater
from database import init_db
from bot import start_bot
from scheduler import start_scheduler
import threading

def main():
    init_db()
    updater = Updater("your-telegram-bot-token", use_context=True)
    dp = updater.dispatcher
    bot_thread = threading.Thread(target=start_bot)
    scheduler_thread = threading.Thread(target=start_scheduler, args=(dp.context,))
    bot_thread.start()
    scheduler_thread.start()
    bot_thread.join()
    scheduler_thread.join()

if __name__ == "__main__":
    main()
