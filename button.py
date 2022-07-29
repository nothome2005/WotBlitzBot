from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

btnmain= KeyboardButton('Начальное меню')


#--------Start Menu-------
button_about = KeyboardButton('Обо мне')
profile = KeyboardButton('Предложить')
get_gold = KeyboardButton('Статистика')
mainmenu = ReplyKeyboardMarkup(resize_keyboard = True,row_width = 2).add(button_about,profile,get_gold)

#----------region------------
rus = KeyboardButton('RUS 🇷🇺')
eu = KeyboardButton('EU 🇪🇺')
region = ReplyKeyboardMarkup(resize_keyboard = True,one_time_keyboard = True).add(rus,eu)

#-----------share-----------
share_menu = InlineKeyboardMarkup(row_width = 2)
back_btn = InlineKeyboardButton(text = "<<Назад",callback_data="move_back")
share_btn = InlineKeyboardButton(text = "Поделиться",switch_inline_query = 'Бот для анализа статистики WoT Blitz!')
share_menu.insert(back_btn)
share_menu.insert(share_btn)
def share_stat_b(stat_mes,name,region_pl):
  global back_menu, share_stat, back_menu
  back_menu = InlineKeyboardMarkup()
  share_stat = InlineKeyboardButton(text = 'Поделиться', switch_inline_query = f"Вот  статистика игрока {name}({region_pl}):\n {stat_mes}")
  back_menu.insert(back_btn)
  back_menu.insert(share_stat)
#----------inline_button-----------
back_menu_inline = InlineKeyboardMarkup()
back_menu_inline.insert(back_btn)
#-----------Text-----------
about = 'Я создал бота, способного получать статистику с аккаунта WoT Blitz. Разработкой данного проекта занимался один человек, бот без рекламы, и я не являюсь партнёром или сотрудником компании Wargaming. Я буду благодарен если вы поделитесь этим ботом со своимми друзьями. Спасибо за использование! По вопросам сотрудничества писать сюда: @mislov_2005'

