"""Модуль добавление и удаления файлов из папки."""
import os

from telegram import Update
from telegram.ext import CallbackContext

import constants
from operation import load_photo_list
from validator import stop_if_not_oracle


def save_foto(update: Update, context: CallbackContext) -> None:
    """Метод сохранения фотографий."""
    message = update.message
    chat_id = message.chat_id
    if stop_if_not_oracle(chat_id, context):
        return
    if message.photo:
        photo = message.photo[-1]
        file_id = photo.file_id
        file = context.bot.get_file(file_id)
        file_extension = file.file_path.split('.')[-1]
        file_name = (
            f"mem_{message.date.strftime('%Y.%m.%d')}_{message.message_id}"
            f".{file_extension}"
        )
        file.download(f"mems_actual/{file_name}")
        load_photo_list()
        context.bot.send_message(
            chat_id=chat_id,
            text="Фотография успешно сохранена!"
        )
    else:
        context.bot.send_message(
            chat_id=chat_id,
            text="Пожалуйста, отправьте фотографию."
        )


def delete_photo_by_command(update: Update, context: CallbackContext):
    """Удаление мема по команде /delete__'имя_файла'."""
    if stop_if_not_oracle(update.effective_chat.id, context):
        return
    try:
        command_parts = update.message.text.split('__')
        if len(command_parts) == 2:
            photo_name = command_parts[1]
            photo_path = os.path.join(
                constants.PHOTOS_DIRECTORY,
                photo_name
            )
            if os.path.exists(photo_path):
                os.remove(photo_path)
                update.message.reply_text(
                    f"Фотография {photo_name} успешно удалена."
                )
            else:
                update.message.reply_text(
                    "Извини, такого мема не найдено."
                )
        else:
            update.message.reply_text(
                "Неправильный формат команды. Используйте /delete_'имя_файла'."
            )
    except Exception as e:
        update.message.reply_text(
            f"Произошла ошибка при удалении фотографии: {str(e)}"
        )
