"""Главный модуль бота."""
import logging
import os

from dotenv import load_dotenv
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from operation import (how_many_mems, load_photo_list, random_photo,
                       send_photo_by_number, shufle)
from save import photo_handler
from start import start

load_dotenv()

ORACLE_ID = os.getenv('ORACLE_ID')
TOKEN = os.getenv('TOKEN')
PHOTOS_DIRECTORY = 'mems_actual'
photo_list = []


def main():
    """Основная логика бота."""
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    load_photo_list()

    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('random', random_photo))
    dispatcher.add_handler(CommandHandler('how_many', how_many_mems))
    dispatcher.add_handler(CommandHandler('shufle', shufle))
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, send_photo_by_number)
    )
    dispatcher.add_handler(MessageHandler(Filters.photo, photo_handler))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
