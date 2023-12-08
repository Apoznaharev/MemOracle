"""Главный модуль бота."""
import logging
import sys

from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

import constants
from operation import how_many_mems, load_photo_list, random_photo, shufle
from save import save_foto
from start import start
from text_filter import handle_delete_or_send_photo


def log_exception(exc_type, exc_value, exc_traceback):
    """Обработчик необработанных исключений для логгирования."""
    logging.error(
        "Uncaught exception",
        exc_info=(exc_type, exc_value, exc_traceback)
    )


def main():
    """Основная логика бота."""
    logging.basicConfig(filename='my_log_file.log', level=logging.INFO)

    # Регистрация обработчика необработанных исключений
    sys.excepthook = log_exception

    load_photo_list()

    updater = Updater(token=constants.TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('order', load_photo_list))
    dispatcher.add_handler(CommandHandler('random', random_photo))
    dispatcher.add_handler(CommandHandler('how_many', how_many_mems))
    dispatcher.add_handler(CommandHandler('shufle', shufle))

    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command,
        handle_delete_or_send_photo
    ))
    dispatcher.add_handler(MessageHandler(Filters.photo, save_foto))
    logging.info(f"Bot started with token: {constants.TOKEN}")
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
