"""Метод фильтрации текстовых сообщений в боте."""
from operation import send_photo
from save import delete_photo_by_command


def handle_delete_or_send_photo(update, context):
    """Обработчик для удаления или отправки фотографии."""
    text = update.message.text

    if text.startswith('delete__'):
        delete_photo_by_command(update, context)
    else:
        send_photo(update, context)
