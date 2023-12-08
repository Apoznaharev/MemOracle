"""Главный модуль бота."""
import logging
import os

from dotenv import load_dotenv
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from operation import (how_many_mems, load_photo_list, random_photo,
                       send_photo, shufle)
from save import photo_handler, delete_photo_by_command
from start import start

load_dotenv()

ORACLE_ID = os.getenv('ORACLE_ID')
TOKEN = os.getenv('TOKEN')
PHOTOS_DIRECTORY = 'mems_actual'

def handle_delete_or_send_photo(update, context):
    """Обработчик для удаления или отправки фотографии."""
    text = update.message.text

    if text.startswith('delete__'):
        # Если сообщение начинается с /delete_, обработать удаление
        delete_photo_by_command(update, context)
    else:
        # Иначе обработать отправку фотографии
        send_photo(update, context)

def main():
    """Основная логика бота."""
    logging.basicConfig(
        filename='my_log_file.log',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    load_photo_list()

    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('order', load_photo_list))

    dispatcher.add_handler(CommandHandler('random', random_photo))
    dispatcher.add_handler(CommandHandler('how_many', how_many_mems))
    dispatcher.add_handler(CommandHandler('shufle', shufle))

    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, handle_delete_or_send_photo)
    )
    dispatcher.add_handler(MessageHandler(Filters.photo, photo_handler))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
