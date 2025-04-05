from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, Filters, CallbackContext
from buttons import register_buttons
from admin import register_admin_buttons
from database import init_db, get_channels, add_channel
import config

def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Kodu Aktif Et", callback_data="activate_code")],
        [InlineKeyboardButton("Kanal Ekle", callback_data="add_channel")],
        [InlineKeyboardButton("Ekli Kanallar", callback_data="list_channels")],
        [InlineKeyboardButton("Bakiyemi Kontrol Et", callback_data="check_balance")],
        [InlineKeyboardButton("İstatistikler", callback_data="stats")],
        [InlineKeyboardButton("Kullanım Kılavuzu", callback_data="help")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Bot'a hoş geldiniz!", reply_markup=reply_markup)

def handle_message(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    state = context.user_data.get('state')
    text = update.message.text

    if state == 'add_channel':
        channel_id = text
        try:
            context.bot.get_chat(channel_id)  # Botun kanala erişimi var mı kontrol et
            add_channel(user_id, channel_id, {'source': '', 'frequency': 'daily', 'type': 'text'})  # Varsayılan ayarlar
            keyboard = [[InlineKeyboardButton("Ayarları Yap", callback_data=f"set_channel_{channel_id}")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(f"{channel_id} eklendi. Ayarları yapabilirsiniz:", reply_markup=reply_markup)
            context.user_data['state'] = None
        except Exception as e:
            update.message.reply_text(f"Hata: {str(e)}. Lütfen botu kanala admin olarak ekleyin ve tekrar deneyin.")

    elif state == 'set_source':
        channel_id = context.user_data['current_channel']
        channels = get_channels(user_id)
        if channel_id in channels:
            channels[channel_id]['source'] = text
            add_channel(user_id, channel_id, channels[channel_id])  # Veritabanını güncelle
            keyboard = [[InlineKeyboardButton("Geri", callback_data=f"set_channel_{channel_id}")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(f"{channel_id} için kaynak '{text}' olarak ayarlandı.", reply_markup=reply_markup)
            context.user_data['state'] = None

    elif state == 'edit_channel':
        channel_id = text
        channels = get_channels(user_id)
        if channel_id in channels:
            keyboard = [
                [InlineKeyboardButton("Kaynak Değiştir", callback_data=f"source_{channel_id}")],
                [InlineKeyboardButton("Sıklık Değiştir", callback_data=f"frequency_{channel_id}")],
                [InlineKeyboardButton("Tür Değiştir", callback_data=f"type_{channel_id}")],
                [InlineKeyboardButton("Geri", callback_data="list_channels")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(f"{channel_id} için düzenleme seçenekleri:", reply_markup=reply_markup)
        else:
            update.message.reply_text("Bu kanal ekli değil.")
        context.user_data['state'] = None

def main():
    init_db()  # Veritabanını başlat
    app = Application.builder().token(config.BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    register_buttons(app)
    register_admin_buttons(app)

    app.run_polling()

if __name__ == "__main__":
    main()
