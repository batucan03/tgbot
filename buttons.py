# telegram/buttons.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler, CallbackContext
from config import (
    SELECT_MODE_MESSAGE, RSS_MODE_MESSAGE, ADD_SOURCE_MESSAGE, SET_TEMPLATE_MESSAGE,
    TEMPLATE_1_MESSAGE, TEMPLATE_2_MESSAGE, AI_MODE_MESSAGE, SINGLE_PROMPT_MESSAGE,
    CONCEPT_MODE_MESSAGE, NO_PROMPTS_MESSAGE, SETTINGS_MESSAGE, APPROVAL_TOGGLED_MESSAGE,
    IMAGES_TOGGLED_MESSAGE, APPROVE_MESSAGE, APPROVED_MESSAGE, REJECTED_MESSAGE,
    NO_PENDING_MESSAGE, STATS_MESSAGE, HELP_MESSAGE, HELP_MODES_MESSAGE,
    HELP_APPROVAL_MESSAGE, HELP_IMAGES_MESSAGE, HELP_COMMANDS_MESSAGE, BALANCE_MESSAGE
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

    elif data == "select_mode":
        keyboard = [
            [InlineKeyboardButton("RSS ile İçerik Çekme", callback_data="rss_mode")],
            [InlineKeyboardButton("Yapay Zeka ile İçerik Üretme", callback_data="ai_mode")],
            [InlineKeyboardButton("Geri", callback_data="back")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(SELECT_MODE_MESSAGE, reply_markup=reply_markup)

    elif data == "rss_mode":
        context.user_data['state'] = 'rss_mode'
        keyboard = [
            [InlineKeyboardButton("Kaynak Ekle", callback_data="add_source")],
            [InlineKeyboardButton("Şablon Seç", callback_data="set_template")],
            [InlineKeyboardButton("Geri", callback_data="select_mode")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(RSS_MODE_MESSAGE, reply_markup=reply_markup)

    elif data == "add_source":
        context.user_data['state'] = 'add_source'
        keyboard = [[InlineKeyboardButton("İptal", callback_data="rss_mode")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(ADD_SOURCE_MESSAGE, reply_markup=reply_markup)

    elif data == "set_template":
        keyboard = [
            [InlineKeyboardButton("Başlık + Özet + Kaynak", callback_data="template_1")],
            [InlineKeyboardButton("Başlık + 100 Karakter Özet", callback_data="template_2")],
            [InlineKeyboardButton("Geri", callback_data="rss_mode")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(SET_TEMPLATE_MESSAGE, reply_markup=reply_markup)

    elif data == "template_1":
        settings = context.bot_data['user_settings'][user_id]
        settings['template'] = '{title}\n{summary}\nKaynak: {link}'
        update_settings(user_id, settings)
        keyboard = [[InlineKeyboardButton("Geri", callback_data="rss_mode")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(TEMPLATE_1_MESSAGE, reply_markup=reply_markup)

    elif data == "template_2":
        settings = context.bot_data['user_settings'][user_id]
        settings['template'] = '{title}\n{summary}'
        update_settings(user_id, settings)
        keyboard = [[InlineKeyboardButton("Geri", callback_data="rss_mode")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(TEMPLATE_2_MESSAGE, reply_markup=reply_markup)

    elif data == "ai_mode":
        context.user_data['state'] = 'ai_mode'
        keyboard = [
            [InlineKeyboardButton("Tek Seferlik Prompt", callback_data="single_prompt")],
            [InlineKeyboardButton("Kanal Konsepti Modu", callback_data="concept_mode")],
            [InlineKeyboardButton("Prompt’larımı Gör", callback_data="list_prompts")],
            [InlineKeyboardButton("Geri", callback_data="select_mode")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(AI_MODE_MESSAGE, reply_markup=reply_markup)

    elif data == "single_prompt":
        context.user_data['state'] = 'single_prompt'
        keyboard = [[InlineKeyboardButton("İptal", callback_data="ai_mode")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(SINGLE_PROMPT_MESSAGE, reply_markup=reply_markup)

    elif data == "concept_mode":
        context.user_data['state'] = 'set_concept'
        keyboard = [[InlineKeyboardButton("İptal", callback_data="ai_mode")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(CONCEPT_MODE_MESSAGE, reply_markup=reply_markup)

    elif data == "list_prompts":
        prompts = get_prompts(user_id)
        if not prompts:
            text = NO_PROMPTS_MESSAGE
        else:
            text = "Yazdığınız prompt’lar:\n" + "\n".join([f"{i+1}. {prompt}" for i, prompt in enumerate(prompts)])
        keyboard = [[InlineKeyboardButton("Geri", callback_data="ai_mode")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(text, reply_markup=reply_markup)

    elif data == "settings":
        settings = context.bot_data['user_settings'][user_id]
        approval = "Açık" if settings['approval'] else "Kapalı"
        images = "Açık" if settings['images'] else "Kapalı"
        text = SETTINGS_MESSAGE.format(approval=approval, images=images)
        keyboard = [
            [InlineKeyboardButton("Onay Özelliğini Aç/Kapat", callback_data="toggle_approval")],
            [InlineKeyboardButton("Görsel Ekleme Aç/Kapat", callback_data="toggle_images")],
            [InlineKeyboardButton("Geri", callback_data="back")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(text, reply_markup=reply_markup)

    elif data == "toggle_approval":
        settings = context.bot_data['user_settings'][user_id]
        settings['approval'] = not settings['approval']
        update_settings(user_id, settings)
        status = "Açık" if settings['approval'] else "Kapalı"
        text = APPROVAL_TOGGLED_MESSAGE.format(status=status)
        keyboard = [[InlineKeyboardButton("Geri", callback_data="settings")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(text, reply_markup=reply_markup)

    elif data == "toggle_images":
        settings = context.bot_data['user_settings'][user_id]
        settings['images'] = not settings['images']
        update_settings(user_id, settings)
        status = "Açık" if settings['images'] else "Kapalı"
        text = IMAGES_TOGGLED_MESSAGE.format(status=status)
        keyboard = [[InlineKeyboardButton("Geri", callback_data="settings")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text(text, reply_markup=reply_markup)

    elif data.startswith("approve_"):
        post_id = int(data.split("_")[1])
        if post_id in context.bot_data.get('pending_posts', {}):
            post = context.bot_data['pending_posts'].pop(post_id)
            user_id = post['user_id']
            channel_id = post['channel_id']
            content = post['content']
            settings = context.bot_data['user_settings'][user_id]
            if settings['images']:
                image_path = fetch_image("news" if settings['template'] else settings['concept'])
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
            [InlineKeyboardButton("Paylaşım Türünü Seç", callback_data="select_mode")],
            [InlineKeyboardButton("Ayarlar", callback_data="settings")],
            [InlineKeyboardButton("Bakiyemi Kontrol Et", callback_data="check_balance")],
            [InlineKeyboardButton("İstatistikler", callback_data="stats")],
            [InlineKeyboardButton("Kullanım Kılavuzu", callback_data="help")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.message.reply_text("Ana menüye döndünüz:", reply_markup=reply_markup)

def register_buttons(dp):
    dp.add_handler(CallbackQueryHandler(button_handler))
