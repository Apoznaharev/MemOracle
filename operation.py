"""Модуль основных операций с мемами."""
import os
import random

from telegram import Update
from telegram.ext import CallbackContext

import constants
from validator import stop_if_not_oracle

photo_list: list = []


def load_photo_list():
    """Загрузка мемов из папки."""
    global photo_list
    photo_list = os.listdir(constants.PHOTOS_DIRECTORY)


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
    random_number = random.randint(1, len(photo_list) - 1)
    try:
        random_photo_path = os.path.join(
            constants.PHOTOS_DIRECTORY,
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
    update.message.reply_text(f'Моему взору доступно {mems_count} мемов.')


def send_photo(update: Update, context: CallbackContext):
    """Запрос мема по индексу или имени файла."""
    if stop_if_not_oracle(update.effective_chat.id, context):
        return

    try:
        photo_number = int(update.message.text)
        if 1 <= photo_number <= len(photo_list):
            photo_path = os.path.join(
                constants.PHOTOS_DIRECTORY,
                photo_list[photo_number - 1]
            )
            update.message.reply_photo(photo=open(photo_path, 'rb'))
            return
        else:
            update.message.reply_text(
                f'Нужно выбрать число от 1 до {len(photo_list)}.'
            )
    except ValueError:
        pass

    try:
        photo_name = update.message.text
        photo_path = os.path.join(
            constants.PHOTOS_DIRECTORY,
            photo_name
        )

        if os.path.exists(photo_path):
            update.message.reply_photo(photo=open(photo_path, 'rb'))
        else:
            update.message.reply_text(
                "Извини, такого мема не найдено."
            )
    except ValueError:
        update.message.reply_text(
            "Отправь имя файла или цифру для получения фотографии."
        )
