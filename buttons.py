# telegram/buttons.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler, CallbackContext
from config import (
    BALANCE_MESSAGE, STATS_MESSAGE, HELP_MESSAGE, HELP_MODES_MESSAGE,
    HELP_APPROVAL_MESSAGE, HELP_IMAGES_MESSAGE, HELP_COMMANDS_MESSAGE,
    NO_PENDING_MESSAGE, APPROVED_MESSAGE, REJECTED_MESSAGE
)
from database import get_balance, get_prompts, update_settings, get_stats
from image import fetch_image
import os

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    user_id = query.from_user.id
    data = query.data

    if data == "activate_code":
        context.user_data['state'] = 'activate_code'
        keyboard = [[InlineKeyboardButton("İptal", callback_data="back")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Lütfen erişim kodunuzu girin (örneğin: USER-ABC123).", reply_markup=reply_markup)

    elif data == "check_balance":
        balance = get_balance(user_id)
        keyboard = [[InlineKeyboardButton("Ana Menü", callback_data="back")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(BALANCE_MESSAGE.format(balance=balance), reply_markup=reply_markup)

    elif data == "add_channel":
        context.user_data['state'] = 'add_channel'
        keyboard = [[InlineKeyboardButton("İptal", callback_data="back")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Lütfen kanal ID'sini girin (örneğin: @KanalAdi veya -100123456789):", reply_markup=reply_markup)

    elif data.startswith("set_channel_"):
        channel_id = data.split("_")[2]
        context.user_data['current_channel'] = channel_id
        keyboard = [
            [InlineKeyboardButton("Kaynak Ekle (RSS)", callback_data=f"source_{channel_id}")],
            [InlineKeyboardButton("Paylaşım Sıklığı", callback_data=f"frequency_{channel_id}")],
            [InlineKeyboardButton("Paylaşım Türü", callback_data=f"type_{channel_id}")],
            [InlineKeyboardButton("Geri", callback_data="back")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(f"{channel_id} için ayarları yapın:", reply_markup=reply_markup)

    elif data.startswith("source_"):
        channel_id = data.split("_")[1]
        context.user_data['state'] = 'set_source'
        keyboard = [[InlineKeyboardButton("İptal", callback_data=f"set_channel_{channel_id}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text("Lütfen RSS kaynak URL'sini girin:", reply_markup=reply_markup)

    elif data.startswith("frequency_"):
        channel_id = data.split("_")[1]
        keyboard = [
            [InlineKeyboardButton("Her Saat", callback_data=f"freq_{channel_id}_hourly")],
            [InlineKeyboardButton("Günlük", callback_data=f"freq_{channel_id}_daily")],
            [InlineKeyboardButton("Haftalık", callback_data=f"freq_{channel_id}_weekly")],
            [InlineKeyboardButton("Geri", callback_data=f"set_channel_{channel_id}")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text("Paylaşım sıklığını seçin:", reply_markup=reply_markup)

    elif data.startswith("type_"):
        channel_id = data.split("_")[1]
        keyboard = [
            [InlineKeyboardButton("Metin", callback_data=f"type_{channel_id}_text")],
            [InlineKeyboardButton("Medya", callback_data=f"type_{channel_id}_media")],
            [InlineKeyboardButton("Geri", callback_data=f"set_channel_{channel_id}")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text("Paylaşım türünü seçin:", reply_markup=reply_markup)

    elif data.startswith("freq_"):
        channel_id, freq = data.split("_")[1], data.split("_")[2]
        if 'channels' not in context.bot_data:
            context.bot_data['channels'] = {}
        if channel_id not in context.bot_data['channels']:
            context.bot_data['channels'][channel_id] = {}
        context.bot_data['channels'][channel_id]['frequency'] = freq
        keyboard = [[InlineKeyboardButton("Geri", callback_data=f"set_channel_{channel_id}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(f"{channel_id} için sıklık '{freq}' olarak ayarlandı.", reply_markup=reply_markup)

    elif data.startswith("type_"):
        channel_id, share_type = data.split("_")[1], data.split("_")[2]
        if 'channels' not in context.bot_data:
            context.bot_data['channels'] = {}
        if channel_id not in context.bot_data['channels']:
            context.bot_data['channels'][channel_id] = {}
        context.bot_data['channels'][channel_id]['type'] = share_type
        keyboard = [[InlineKeyboardButton("Geri", callback_data=f"set_channel_{channel_id}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(f"{channel_id} için paylaşım türü '{share_type}' olarak ayarlandı.", reply_markup=reply_markup)

    elif data == "list_channels":
        channels = context.bot_data.get('channels', {})
        if not channels:
            text = "Henüz eklenmiş kanal yok."
        else:
            text = "Ekli Kanallar:\n"
            for channel_id, settings in channels.items():
                source = settings.get('source', 'Belirtilmemiş')
                freq = settings.get('frequency', 'Belirtilmemiş')
                share_type = settings.get('type', 'Belirtilmemiş')
                text += f"{channel_id}:\n  Kaynak: {source}\n  Sıklık: {freq}\n  Tür: {share_type}\n"
        keyboard = [
            [InlineKeyboardButton("Kanal Düzenle", callback_data="edit_channel")],
            [InlineKeyboardButton("Geri", callback_data="back")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text, reply_markup=reply_markup)

    elif data == "edit_channel":
        context.user_data['state'] = 'edit_channel'
        keyboard = [[InlineKeyboardButton("İptal", callback_data="list_channels")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text("Düzenlemek istediğiniz kanalın ID'sini girin:", reply_markup=reply_markup)

    elif data == "list_pending":
        user_posts = {k: v for k, v in context.bot_data.get('pending_posts', {}).items() if v['user_id'] == user_id}
        if not user_posts:
            text = NO_PENDING_MESSAGE
        else:
            text = "Onay bekleyen paylaşımlar:\n" + "\n".join([f"ID: {k}\n{v['content']}" for k, v in user_posts.items()])
        keyboard = [[InlineKeyboardButton("Geri", callback_data="back")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(text, reply_markup=reply_markup)

    elif data == "stats":
        stats = get_stats(user_id)
        total_posts = stats['total_posts']
        channel_counts = stats['channel_counts']
        channels_text = "\n".join([f"{channel_id}: {count} paylaşım" for channel_id, count in channel_counts.items()])
        text = STATS_MESSAGE.format(total=total_posts, channels=channels_text)
        keyboard = [[InlineKeyboardButton("Ana Menü", callback_data="back")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(text, reply_markup=reply_markup)

    elif data == "help":
        keyboard = [
            [InlineKeyboardButton("Paylaşım Türleri", callback_data="help_modes")],
            [InlineKeyboardButton("Onay Özelliği", callback_data="help_approval")],
            [InlineKeyboardButton("Görsel Ekleme", callback_data="help_images")],
            [InlineKeyboardButton("Komutlar ve İpuçları", callback_data="help_commands")],
            [InlineKeyboardButton("Geri", callback_data="back")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(HELP_MESSAGE, reply_markup=reply_markup)

    elif data == "help_modes":
        keyboard = [[InlineKeyboardButton("Geri", callback_data="help")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(HELP_MODES_MESSAGE, reply_markup=reply_markup)

    elif data == "help_approval":
        keyboard = [[InlineKeyboardButton("Geri", callback_data="help")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(HELP_APPROVAL_MESSAGE, reply_markup=reply_markup)

    elif data == "help_images":
        keyboard = [[InlineKeyboardButton("Geri", callback_data="help")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(HELP_IMAGES_MESSAGE, reply_markup=reply_markup)

    elif data == "help_commands":
        keyboard = [[InlineKeyboardButton("Geri", callback_data="help")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(HELP_COMMANDS_MESSAGE, reply_markup=reply_markup)

    elif data == "back":
        keyboard = [
            [InlineKeyboardButton("Kodu Aktif Et", callback_data="activate_code")],
            [InlineKeyboardButton("Kanal Ekle", callback_data="add_channel")],
            [InlineKeyboardButton("Ekli Kanallar", callback_data="list_channels")],
            [InlineKeyboardButton("Bakiyemi Kontrol Et", callback_data="check_balance")],
            [InlineKeyboardButton("İstatistikler", callback_data="stats")],
            [InlineKeyboardButton("Kullanım Kılavuzu", callback_data="help")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Ana menüye döndünüz:", reply_markup=reply_markup)

    elif data.startswith("approve_"):
        post_id = int(data.split("_")[1])
        if post_id in context.bot_data.get('pending_posts', {}):
            post = context.bot_data['pending_posts'].pop(post_id)
            user_id = post['user_id']
            channel_id = post['channel_id']
            content = post['content']
            settings = context.bot_data['channels'].get(channel_id, {})
            if settings.get('type') == 'media':
                image_path = fetch_image("news")
                if image_path:
                    with open(image_path, 'rb') as photo:
                        context.bot.send_photo(chat_id=channel_id, photo=photo, caption=content)
                    os.remove(image_path)
                else:
                    context.bot.send_message(chat_id=channel_id, text=content)
            else:
                context.bot.send_message(chat_id=channel_id, text=content)
            query.message.reply_text(APPROVED_MESSAGE)
        else:
            query.message.reply_text("Bu paylaşım artık geçerli değil.")

    elif data.startswith("reject_"):
        post_id = int(data.split("_")[1])
        if post_id in context.bot_data.get('pending_posts', {}):
            context.bot_data['pending_posts'].pop(post_id)
            query.message.reply_text(REJECTED_MESSAGE)
        else:
            query.message.reply_text("Bu paylaşım artık geçerli değil.")

def register_buttons(dp):
    dp.add_handler(CallbackQueryHandler(button_handler))
