# telegram/bot.py
from telegram.ext import Updater
from config import TOKEN
from commands import register_commands
from buttons import register_buttons
from messages import register_messages
from admin import register_admin_buttons

from commands import register_commands  # Komutları kaydetmek için

def start_bot(dispatcher): 
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    register_commands(dp)
    register_buttons(dp)
    register_messages(dp)
    register_admin_buttons(dp)
    updater.start_polling()
    updater.idle()
