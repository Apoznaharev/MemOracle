"""Модуль функции start меморакула."""
import os

from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup
from validator import check_is_not_oracle

load_dotenv()

ORACLE_ID = os.getenv('ORACLE_ID')


def start(update, context):
    """Функция запуска бота."""
    chat_id = update.effective_chat.id
    buttons = [['/random'], ['/how_many']]
    if not check_is_not_oracle(chat_id):
        buttons.append(['/shufle'])
        buttons.append(['/order'])
    context.bot.send_message(
        chat_id=chat_id,
        text=(
            'Этот мемный оракул! Чтобы узнать своё будущее, подпишись на канал'
            ' https://t.me/metpoz, и каждый понедельник у тебя будет шанс '
            'узнать свою судьбу. А сейчас ты можешь получить случайный мем '
            'нажав кнопку внизу, или отправив команду /random .'),
        reply_markup=ReplyKeyboardMarkup(
            buttons,
            resize_keyboard=True
        )
    )
