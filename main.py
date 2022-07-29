import logging
from aiogram import types
from aiogram.utils.executor import start_webhook
from aiogram.utils.deep_linking import get_start_link, decode_payload
from config import bot, dp, WEBHOOK_URL, WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT
import button as nav
import test_req as req
import m_db
import pytz
import datetime
import threading
from time import sleep
from threading import Thread

region = 'None'
step = 0
proporsal = False
username_t = ''
text_gr = ''
def ping_timer():
    sleep(60)
    time_now_zone = datetime.datetime.now(pytz.timezone("Europe/Kiev"))
    while True:
        req.get_request_simple('https://wotblitztelegramm.herokuapp.com/')
        print('Herok wake up!')
        print(int(str(time_now_zone.hour) + str(time_now_zone.minute)))
        sleep((60*15))
        time_now_zone = datetime.datetime.now(pytz.timezone("Europe/Kiev"))
    print('Heroku sleep!')
    
th = Thread(target=ping_timer)
th.start()

async def on_startup(dispatcher):
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)

async def on_shutdown(dispatcher):
    await bot.delete_webhook()

@dp.callback_query_handler(text = "move_back")
async def share_punkt(call: types.CallbackQuery):
    #await call.answer(message.from_user.id, "/start",reply_markup = nav.mainmenu)
    await call.message.answer(text = '/start',reply_markup = nav.mainmenu)
    step = 0
    await call.answer(text="Понравился бот? Не забудь поделиться с другом!\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t😉", show_alert=True)
    
@dp.message_handler(commands = ['start'])
async def command_start(msg: types.Message):
    await bot.send_message(msg.from_user.id, "Данный бот создан для анализа статистики игрока WoT Blitz.Давайте начнём!".format(msg.from_user),reply_markup = nav.mainmenu)
    m_db.users_list(msg.chat.id)
    args = msg.get_args()
    reference = decode_payload(args)
    if reference != '':
        print(reference)
        print(type(reference))
        m_db.update_referal(int(reference),msg.from_user.id)
    step = 0
 
@dp.message_handler(commands = ['refers'])
async def command_referals(msg: types.Message):
    if '-' not in str(msg.chat.id):
        ref_link = await get_start_link(str(msg.from_user.id), encode=True)
        await bot.send_message(msg.from_user.id,f'Ваша реферальная ссылка: {ref_link}')
        m_db.add_referal(msg.from_user.id,msg.from_user.first_name,msg.from_user.username)

@dp.message_handler(commands = ['count'])
async def noun_referal(msg: types.Message):
    if '-' not in str(msg.chat.id):
        await bot.send_message(msg.from_user.id,f'Количество ваших рефералов: {m_db.ref_count(msg.from_user.id)}')

@dp.message_handler(commands = ['fit4a'])
async def command_start(msg: types.Message):
    m_db.get_user_l()
    for us_l in m_db.user_list:
        try:
            await bot.send_message(us_l,msg.text[msg.text.find(' '):])
        except:
            pass
@dp.message_handler(commands = ['help'])
async def command_help(msg: types.Message):
    await bot.send_message(msg.from_user.id,'Вместо того, чтобы прокалазывать по кнопкам, можно ввести такую команду:')

@dp.message_handler(commands = ['statist'])
async def command_send_group(msg: types.Message):
    global region,proporsal,username_t,text_gr
    text_gr = msg.text.replace('/statist ','')
    text_gr = text_gr.split(' ')
    if len(text_gr) == 2:
        req.get_id_wot(text_gr[0],text_gr[1])
        nav.share_stat_b(req.text_teleg[1],req.player_name,req.player_region)
        await msg.reply(req.text_teleg[1])
        username_t = f"<{msg.from_user.username}>_<{msg.from_user.id}>_<{msg.from_user.first_name}>_<{msg.from_user.last_name}>"
        m_db.check_in(req.text_teleg[0],msg.text,region,username_t)
    else:
        await msg.reply('Неправильно заполнена форма')
    m_db.users_list(msg.chat.id)
@dp.message_handler()
async def bot_mes(msg: types.Message):
    global step,region,proporsal,username_t
    if "-" not in str(msg.chat.id):
        if msg.text == 'Обо мне':
            await bot.send_message(msg.from_user.id,nav.about,reply_markup = nav.share_menu)
        elif msg.text == 'Предложить':
            await bot.send_message(msg.from_user.id,'Напишите сюда ос своём предложении и я его рассмотрю:', reply_markup = nav.back_menu_inline)
            step = 4
        elif step == 4 and msg.text != 'Статистика':
            step = 0
            username_t = f"<{msg.from_user.username}>_<{msg.from_user.id}>_<{msg.from_user.first_name}>_<{msg.from_user.last_name}>"
            m_db.prop(msg.text,username_t)
            await bot.send_message(msg.from_user.id,'Спасибо за предложение!', reply_markup = nav.mainmenu)
        elif msg.text == 'Статистика':
            await bot.send_message(msg.from_user.id, "Выберете регион сервера, на котором зарегистрирован аккаунт".format(msg.from_user),reply_markup = nav.region)
            step = 2
        elif msg.text == 'RUS 🇷🇺' and step == 2:
            region = 'ru'
            print(region)
            await bot.send_message(msg.from_user.id,'Введите свой ник:', reply_markup = nav.ReplyKeyboardRemove())
            step = 3
        elif msg.text == 'EU 🇪🇺' and step == 2:
            region = 'eu'
            print(region)
            await bot.send_message(msg.from_user.id,'Введите свой ник:', reply_markup = nav.ReplyKeyboardRemove())
            step = 3
        elif step == 3:
            await bot.send_message(msg.from_user.id,'Подождите...')
            req.get_id_wot(msg.text,region)
            nav.share_stat_b(req.text_teleg[1],req.player_name,req.player_region)
            await bot.send_message(msg.from_user.id,req.text_teleg[1],reply_markup = nav.back_menu)
            username_t = f"<{msg.from_user.username}>_<{msg.from_user.id}>_<{msg.from_user.first_name}>_<{msg.from_user.last_name}>"
            m_db.check_in(req.text_teleg[0],msg.text,region,username_t)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
    
