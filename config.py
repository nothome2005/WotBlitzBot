from aiogram.dispatcher import Dispatcher
from aiogram import Bot
import os

TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')

# webhook settings
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT', default=8000)


# transkation ru-en
language = {
  'Enjoy':['Понравился бот? Не забудь поделиться с другом!\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t😉',''],
  'on_start':['Данный бот создан для анализа статистики игрока WoT Blitz.Давайте начнём!',''],
  'help_chat':['Введите команду:/statist <Nickname> <Region>. Где Nickname - это имя игрового аккаунта, а Region - соотвественно регион сервера. Важно использовать сокращение такого вида: ru, eu, na, asia',''],
  'form_error':['Неправильно заполнена форма',''],
  'proposite':['Напишите сюда ос своём предложении и я его рассмотрю:',''],
  'thank':['Спасибо за предложение!',''],
  'rg_choser':['Выберете регион сервера, на котором зарегистрирован аккаунт','']
}
