"""Модуль добавление и удаления файлов из папки."""
from telegram import Update
from telegram.ext import CallbackContext


def photo_handler(update: Update, context: CallbackContext) -> None:
    """Метод сохранения фотографий."""
    chat_id = update.message.chat_id
    if update.message.photo:
        photo = update.message.photo[-1]
        file_id = photo.file_id
        file = context.bot.get_file(file_id)
        file_extension = file.file_path.split('.')[-1]
        file_name = (
            f"mem_{update.message.message_id}.{file_extension}"
        )
        file.download(f"mems_actual/{file_name}")

        context.bot.send_message(
            chat_id=chat_id,
            text="Фотография успешно сохранена!"
        )
    else:
        context.bot.send_message(
            chat_id=chat_id,
            text="Пожалуйста, отправьте фотографию."
        )
