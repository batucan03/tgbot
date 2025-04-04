# telegram/messages.py
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import MessageHandler, Filters, CallbackContext
from config import MAX_PROMPT_LENGTH, NO_CHANNEL_MESSAGE, POST_SENT_MESSAGE, BALANCE_EXPIRED_MESSAGE, APPROVE_MESSAGE
from database import activate_code, add_channel, add_prompt, get_channels, decrease_balance, get_settings, update_settings
from content import generate_content
from image import fetch_image
import os

def message_handler(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    text = update.message.text
    state = context.user_data.get('state', '')

    if state == 'activate_code':
        result = activate_code(user_id, text)
        context.bot_data['user_settings'][user_id] = get_settings(user_id)
        keyboard = [[InlineKeyboardButton("Ana Menü", callback_data="back")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(result, reply_markup=reply_markup)
        context.user_data['state'] = ''

    elif state == 'add_source':
        result = add_channel(user_id, text)
        keyboard = [[InlineKeyboardButton("Geri", callback_data="rss_mode")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(result, reply_markup=reply_markup)
        context.user_data['state'] = ''

    elif state == 'single_prompt':
        if len(text) > MAX_PROMPT_LENGTH:
            update.message.reply_text(f"Prompt {MAX_PROMPT_LENGTH} karakterden uzun olamaz!")
            return
        add_prompt(user_id, text)
        if not decrease_balance(user_id):
            update.message.reply_text(BALANCE_EXPIRED_MESSAGE)
            return
        content = generate_content(text)
        channels = get_channels(user_id)
        if not channels:
            update.message.reply_text(NO_CHANNEL_MESSAGE)
            return
        channel_id = channels[0]
        settings = context.bot_data['user_settings'][user_id]
        if settings['approval']:
            post_id = len(context.bot_data.get('pending_posts', {}))
            context.bot_data.setdefault('pending_posts', {})[post_id] = {
                'user_id': user_id,
                'channel_id': channel_id,
                'content': content
            }
            keyboard = [
                [InlineKeyboardButton("Onayla", callback_data=f"approve_{post_id}")],
                [InlineKeyboardButton("Reddet", callback_data=f"reject_{post_id}")],
                [InlineKeyboardButton("Onay Bekleyenleri Gör", callback_data="list_pending")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(APPROVE_MESSAGE.format(content=content), reply_markup=reply_markup)
        else:
            if settings['images']:
                image_path = fetch_image(text)
                if image_path:
                    with open(image_path, 'rb') as photo:
                        context.bot.send_photo(chat_id=channel_id, photo=photo, caption=content)
                    os.remove(image_path)
                else:
                    context.bot.send_message(chat_id=channel_id, text=content)
            else:
                context.bot.send_message(chat_id=channel_id, text=content)
            update.message.reply_text(POST_SENT_MESSAGE)
        context.user_data['state'] = ''

    elif state == 'set_concept':
        settings = context.bot_data['user_settings'][user_id]
        settings['concept'] = text
        update_settings(user_id, settings)
        keyboard = [[InlineKeyboardButton("Geri", callback_data="ai_mode")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(f"Kanal konsepti ayarlandı: {text}", reply_markup=reply_markup)
        context.user_data['state'] = ''

def register_messages(dp):
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, message_handler))
