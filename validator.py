"""Модуль проверки владельца бота."""
import os

from dotenv import load_dotenv

load_dotenv()

ORACLE_ID = os.getenv('ORACLE_ID')


def check_is_not_oracle(chat_id):
    """Асинхронный метод проверки, является ли пользователь не владельцем."""
    return str(chat_id) != ORACLE_ID


def stop_if_not_oracle(chat_id, context):
    """Асинхронный метод проверки, является ли пользователь не владельцем."""
    if check_is_not_oracle(chat_id):
        message = (
            'Только истинный [оракул](https://t.me/Poznakharev) '
            'может взывать к мемному богу!'
        )
        context.bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode='Markdown'
        )
        return True
