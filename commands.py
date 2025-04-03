# telegram/commands.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CommandHandler, CallbackContext
from config import WELCOME_MESSAGE, ADMIN_CODE
from database import get_settings

def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id not in context.bot_data.get('user_settings', {}):
        context.bot_data.setdefault('user_settings', {})[user_id] = get_settings(user_id)
    keyboard = [
        [InlineKeyboardButton("Kodu Aktif Et", callback_data="activate_code")],
        [InlineKeyboardButton("Paylaşım Türünü Seç", callback_data="select_mode")],
        [InlineKeyboardButton("Ayarlar", callback_data="settings")],
        [InlineKeyboardButton("Bakiyemi Kontrol Et", callback_data="check_balance")],
        [InlineKeyboardButton("İstatistikler", callback_data="stats")],
        [InlineKeyboardButton("Kullanım Kılavuzu", callback_data="help")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(WELCOME_MESSAGE, reply_markup=reply_markup)

def admin(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if len(context.args) != 1:
        update.message.reply_text("Lütfen yönetici kodunu girin: /admin <kod>")
        return
    code = context.args[0]
    if code != ADMIN_CODE:
        update.message.reply_text("Geçersiz yönetici kodu!")
        return
    keyboard = [
        [InlineKeyboardButton("Kod Oluştur", callback_data="admin_generate_code")],
        [InlineKeyboardButton("Kodları Listele", callback_data="admin_list_codes")],
        [InlineKeyboardButton("Kullanıcıyı Görüntüle", callback_data="admin_view_user")],
        [InlineKeyboardButton("Çıkış", callback_data="admin_exit")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Yönetici paneline hoş geldiniz!", reply_markup=reply_markup)

def register_commands(dp):
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("admin", admin))
