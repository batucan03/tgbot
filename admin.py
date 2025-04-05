# telegram/admin.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler, CallbackContext
from database import add_activation_code
import time  # time modülünü ekledim

def admin_button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    data = query.data
    user_id = query.from_user.id

    # Admin paneline erişim kontrolü (örnek bir kontrol, kendi mantığına göre düzenleyebilirsin)
    if user_id not in context.bot_data.get('admins', []):  # Admin listesi kontrolü
        query.edit_message_text("Bu panele erişim yetkiniz yok.")
        return

    if data == "admin_generate_code":
        keyboard = [
            [InlineKeyboardButton("100 Paylaşım", callback_data="code_100")],
            [InlineKeyboardButton("500 Paylaşım", callback_data="code_500")],
            [InlineKeyboardButton("Özel Miktar", callback_data="code_custom")],
            [InlineKeyboardButton("Geri", callback_data="admin_back")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text("Kod oluşturma seçenekleri:", reply_markup=reply_markup)

    elif data == "code_100":
        code = f"USER-{int(time.time())}"
        add_activation_code(code, 100)
        keyboard = [[InlineKeyboardButton("Geri", callback_data="admin_generate_code")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(f"Yeni kod oluşturuldu: {code} (100 paylaşım)", reply_markup=reply_markup)

    elif data == "code_500":
        code = f"USER-{int(time.time())}"
        add_activation_code(code, 500)
        keyboard = [[InlineKeyboardButton("Geri", callback_data="admin_generate_code")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(f"Yeni kod oluşturuldu: {code} (500 paylaşım)", reply_markup=reply_markup)

    elif data == "code_custom":
        context.user_data['state'] = 'custom_code'
        keyboard = [[InlineKeyboardButton("İptal", callback_data="admin_generate_code")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text("Lütfen özel paylaşım miktarını girin:", reply_markup=reply_markup)

    elif data == "admin_list_codes":
        # Örnek: Kod listeleme (veritabanından çekmen gerek)
        codes = context.bot_data.get('activation_codes', {})
        if not codes:
            text = "Henüz oluşturulmuş kod yok."
        else:
            text = "Oluşturulan kodlar:\n" + "\n".join([f"{code}: {amount} paylaşım" for code, amount in codes.items()])
        keyboard = [[InlineKeyboardButton("Geri", callback_data="admin_back")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text, reply_markup=reply_markup)

    elif data == "admin_view_user":
        context.user_data['state'] = 'view_user'
        keyboard = [[InlineKeyboardButton("İptal", callback_data="admin_back")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text("Görüntülemek istediğiniz kullanıcının ID'sini girin:", reply_markup=reply_markup)

    elif data == "admin_exit":
        query.edit_message_text("Admin panelinden çıktınız.")

    elif data == "admin_back":
        keyboard = [
            [InlineKeyboardButton("Kod Oluştur", callback_data="admin_generate_code")],
            [InlineKeyboardButton("Kodları Listele", callback_data="admin_list_codes")],
            [InlineKeyboardButton("Kullanıcıyı Görüntüle", callback_data="admin_view_user")],
            [InlineKeyboardButton("Çıkış", callback_data="admin_exit")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text("Yönetici paneline hoş geldiniz!", reply_markup=reply_markup)

def register_admin_buttons(dp):
    dp.add_handler(CallbackQueryHandler(admin_button_handler, pattern="^(admin_generate_code|code_100|code_500|code_custom|admin_list_codes|admin_view_user|admin_exit|admin_back)$"))
