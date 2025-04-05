# telegram/admin.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
from database import add_activation_code, list_activation_codes, get_user_info
import time

def admin_button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    data = query.data

    if data == "admin_generate_code":
        keyboard = [
            [InlineKeyboardButton("100 Paylaşım", callback_data="code_100")],
            [InlineKeyboardButton("500 Paylaşım", callback_data="code_500")],
            [InlineKeyboardButton("Özel Miktar", callback_data="code_custom")],
            [InlineKeyboardButton("Geri", callback_data="admin_back")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Kod oluşturma seçenekleri:", reply_markup=reply_markup)

    elif data == "code_100":
        code = f"USER-{int(time.time())}"
        add_activation_code(code, 100)
        keyboard = [[InlineKeyboardButton("Geri", callback_data="admin_generate_code")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(f"Yeni kod oluşturuldu: {code} (100 paylaşım)", reply_markup=reply_markup)

    elif data == "code_500":
        code = f"USER-{int(time.time())}"
        add_activation_code(code, 500)
        keyboard = [[InlineKeyboardButton("Geri", callback_data="admin_generate_code")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(f"Yeni kod oluşturuldu: {code} (500 paylaşım)", reply_markup=reply_markup)

    elif data == "admin_list_codes":
        codes = list_activation_codes()
        message = "\n".join([f"{c['code']} - {c['count']} paylaşım" for c in codes]) or "Hiç kod yok."
        keyboard = [[InlineKeyboardButton("Geri", callback_data="admin_back")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(f"Oluşturulmuş Kodlar:\n{message}", reply_markup=reply_markup)

    elif data == "admin_view_user":
        query.message.reply_text("Lütfen kullanıcı ID'sini gönderin:")
        context.user_data["admin_state"] = "waiting_for_user_id"

    elif data == "admin_exit":
        query.message.reply_text("Admin panelinden çıkış yapıldı.")

    elif data == "admin_back":
        keyboard = [
            [InlineKeyboardButton("Kod Oluştur", callback_data="admin_generate_code")],
            [InlineKeyboardButton("Kodları Listele", callback_data="admin_list_codes")],
            [InlineKeyboardButton("Kullanıcıyı Görüntüle", callback_data="admin_view_user")],
            [InlineKeyboardButton("Çıkış", callback_data="admin_exit")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Admin Paneline Hoş Geldiniz.", reply_markup=reply_markup)
