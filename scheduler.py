# scheduler.py
import schedule
import time
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from config import SCHEDULE_INTERVAL_MINUTES, BALANCE_EXPIRED_MESSAGE, APPROVE_MESSAGE
from database import get_channels, decrease_balance, log_post, get_settings
from content import process_rss_content, generate_content
from image import fetch_image
import sqlite3
import os

def schedule_posts(context: CallbackContext):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT user_id FROM users")
    users = c.fetchall()
    conn.close()

    for user in users:
        user_id = user[0]
        settings = get_settings(user_id)
        channels = get_channels(user_id)

        if not channels:
            continue

        if not decrease_balance(user_id):
            for channel_id in channels:
                context.bot.send_message(chat_id=channel_id, text=BALANCE_EXPIRED_MESSAGE)
            continue

        if settings['template']:
            content = process_rss_content(settings['template'])
            if content:
                for channel_id in channels:
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
                        context.bot.send_message(chat_id=user_id, text=APPROVE_MESSAGE.format(content=content), reply_markup=reply_markup)
                    else:
                        if settings['images']:
                            image_path = fetch_image("news")
                            if image_path:
                                with open(image_path, 'rb') as photo:
                                    context.bot.send_photo(chat_id=channel_id, photo=photo, caption=content)
                                os.remove(image_path)
                            else:
                                context.bot.send_message(chat_id=channel_id, text=content)
                        else:
                            context.bot.send_message(chat_id=channel_id, text=content)
                        log_post(user_id, channel_id, content)

        if settings['concept']:
            content = generate_content(settings['concept'])
            for channel_id in channels:
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
                    context.bot.send_message(chat_id=user_id, text=APPROVE_MESSAGE.format(content=content), reply_markup=reply_markup)
                else:
                    if settings['images']:
                        image_path = fetch_image(settings['concept'])
                        if image_path:
                            with open(image_path, 'rb') as photo:
                                context.bot.send_photo(chat_id=channel_id, photo=photo, caption=content)
                            os.remove(image_path)
                        else:
                            context.bot.send_message(chat_id=channel_id, text=content)
                    else:
                        context.bot.send_message(chat_id=channel_id, text=content)
                    log_post(user_id, channel_id, content)

def start_scheduler(context: CallbackContext):
    schedule.every(SCHEDULE_INTERVAL_MINUTES).minutes.do(schedule_posts, context=context)
    while True:
        schedule.run_pending()
        time.sleep(60)
