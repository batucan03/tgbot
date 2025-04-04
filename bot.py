# telegram/bot.py
from telegram.ext import Updater
from config import TOKEN
from commands import register_commands
from telegram.buttons import register_buttons
from telegram.messages import register_messages
from telegram.admin import register_admin_buttons

def start_bot():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    register_commands(dp)
    register_buttons(dp)
    register_messages(dp)
    register_admin_buttons(dp)
    updater.start_polling()
    updater.idle()
