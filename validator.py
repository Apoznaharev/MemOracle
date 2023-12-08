"""Модуль проверки владельца бота."""
import constants


def check_is_not_oracle(chat_id):
    """Асинхронный метод проверки, является ли пользователь не владельцем."""
    return str(chat_id) != constants.ORACLE_ID


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
