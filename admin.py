# telegram/admin.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler, CallbackContext
from database import add_activation_code

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

    elif data == "admin_back":
        keyboard = [
            [InlineKeyboardButton("Kod Oluştur", callback_data="admin_generate_code")],
            [InlineKeyboardButton("Kodları Listele", callback_data="admin_list_codes")],
            [InlineKeyboardButton("Kullanıcıyı Görüntüle", callback_data="admin_view_user")],
            [InlineKeyboardButton("Çıkış", callback_data="admin_exit")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Yönetici paneline hoş geldiniz!", reply_markup=reply_markup)

def register_admin_buttons(dp):
    dp.add_handler(CallbackQueryHandler(admin_button_handler, pattern="^(admin_generate_code|code_100|code_500|admin_back)$"))
