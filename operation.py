"""Модуль основных операций с мемами."""
import os
import random

from telegram import Update
from telegram.ext import CallbackContext

from validator import stop_if_not_oracle

PHOTOS_DIRECTORY = 'mems_actual'
photo_list: list = []


def load_photo_list():
    """Загрузка мемов из папки."""
    global photo_list
    photo_list = os.listdir(PHOTOS_DIRECTORY)


def shufle(update: Update, context: CallbackContext):
    """Перемешать мемы."""
    chat_id = update.message.chat_id
    if stop_if_not_oracle(chat_id, context):
        return
    global photo_list
    if not photo_list:
        context.bot.send_message(
            chat_id=chat_id,
            text="Папка с мемами пуста."
        )
        return
    try:
        random.shuffle(photo_list)
        context.bot.send_message(
            chat_id=chat_id,
            text="Мемы перемешаны."
        )
    except Exception as e:
        print(f"Error: {e}")
        context.bot.send_message(
            chat_id=chat_id,
            text="Что-то пошло не так."
        )


def random_photo(update: Update, context: CallbackContext):
    """Запрос рандомного фото."""
    global photo_list
    if not photo_list:
        update.message.reply_text("Папка с мемами пуста.")
        return
    random_number = random.randint(1, len(photo_list)-1)
    try:
        random_photo_path = os.path.join(
            PHOTOS_DIRECTORY,
            photo_list[random_number]
        )
        update.message.reply_photo(photo=open(random_photo_path, 'rb'))
    except Exception as e:
        print(f"Error: {e}")
        update.message.reply_text(
            "Произошла ошибка при загрузке случайной фотографии."
        )


def how_many_mems(update: Update, context: CallbackContext):
    """Узнать, сколько мемов."""
    mems_count = len(photo_list)
    update.message.reply_text(f'В моей базе ровно {mems_count} мемов.')


def send_photo_by_number(update: Update, context: CallbackContext):
    """Запрос мема по индексу."""
    if stop_if_not_oracle(update.effective_chat.id, context):
        return
    try:
        photo_number = int(update.message.text)
        if 1 <= photo_number <= len(photo_list):
            photo_path = os.path.join(
                PHOTOS_DIRECTORY,
                photo_list[photo_number - 1]
            )
            update.message.reply_photo(photo=open(photo_path, 'rb'))
        else:
            update.message.reply_text(
                "Извини, у меня не так много мемов."
            )
    except ValueError:
        update.message.reply_text(
            "Пожалуйста, отправь цифру, чтобы получить фотографию."
        )
