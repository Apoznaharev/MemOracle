"""Константы и переменные."""
import os

from dotenv import load_dotenv

load_dotenv()

ORACLE_ID = os.getenv('ORACLE_ID')
TOKEN = os.getenv('TOKEN')
PHOTOS_DIRECTORY = 'mems_actual'
