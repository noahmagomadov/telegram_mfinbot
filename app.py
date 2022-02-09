''' Telegram bot pour calculer budget'''
import logging
import os

from aiogram import Bot, Dispatcher, executor, types

import httplib2
from google.oauth2.credentials import Credentials
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

import expenses


logging.basicConfig(level=logging.INFO)


''' gogle sheets API parti '''

CREDENTIALS_FILE = os.environ.get('token_file.json')
spreadsheet_id = os.environ.get('spreadsheet_id')

scores = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE, scores)

httpAuth = credentials.authorize(httplib2.Http())
service = discovery.build('sheets', 'v4', http=httpAuth)


def add_to_googlesheets(data):
    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range='expenses!A3:C3',
        valueInputOption='USER_ENTERED',
        insertDataOption='OVERWRITE',
        body={'values': data}
    ).execute()


def read_case(range_read_all):
    values_read = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=range_read_all,
        majorDimension='ROWS'
    ).execute()
    return values_read


''' Telegram bot parti '''


API_TOKEN = os.environ.get('TELEGRAM_API_TOKEN')
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler(commands=['month'])
async def month_statistics(message: types.Message):
    """Get somme of month"""
    answer_message = 'Hier will expenses by month'
    await message.answer(answer_message)


@dp.message_handler()
async def add_expense(message: types.Message):
    """Add new expense"""
    try:
        data = expenses.add_expense(message.text)
        add_to_googlesheets(data)
    except Exception as e:
        await message.answer(str(e))
        return
    answer_message = ("Added expense Entry\n\n")
    await message.answer(answer_message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
