from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent

player_region = ''
player_name = ''
text_teleg = []
categ_win = []
session = requests.Session()
link = 'https://wblitz.net/accounts/x_search_autocomplete'
ua = UserAgent()

def get_request_simple(bot_link):
    global head_s
    head_s = {'User-Agent': ua.random}
    requests.get(bot_link, headers=head_s)

def new(user_id,user_reg): 
    global text_teleg
    text_teleg.clear()
    link = f'https://wblitz.net/accounts/profile/{user_id}/1/{user_reg}'
    contents = requests.get(link).text
    soup = BeautifulSoup(contents, 'lxml')
    block = soup.find('div',class_ = 'row content-area')
    wg_id = block.find('div', class_ = 'text-center')
    wg_id = wg_id.find('strong').text
    text_teleg.append(wg_id)
    block_2 = block.find('div', class_ = 'row') 
    battle_noun = block_2.find_all('h2')[0].text
    win_rate = block_2.find_all('h2')[1].text
    vzvod = block_2.find_all('h2')[2].text
    damage = block_2.find_all('h2')[3].text
     
    #---------------first_colum---------------------
    more_stat = soup.find('div',id = 'fullStatDiv')
    more_stat = more_stat.find('div',class_ = 'col-xs-6 col-sm-5 col-sm-offset-1 col-md-3 col-md-offset-3')
    tank_level = more_stat.find_all('td')[22].text
    mid_exp = more_stat.find_all('td')[20].text
    veh_noun = more_stat.find_all('td')[23].text
    reg_day = more_stat.find_all('td')[0].text
    wins = more_stat.find_all('td')[6].text
    alive = more_stat.find_all('td')[15].text
    #---------------------second_colum------------------
    more_stat = soup.find('div', id = "fullStatDiv")
    more_stat = more_stat.find('div', class_ = 'col-xs-6 col-sm-5 col-md-3')
    hit = more_stat.find_all('td')[9].text
    shot = more_stat.find_all('td')[7].text
    master = more_stat.find_all('td')[20].text
    first_degree = more_stat.find_all('td')[21].text
    #-------------------type_taks--------------------
    more_stat = soup.find('div', id = 'fullStatDiv')
    more_stat = more_stat.find_all('div', class_ = 'col-xs-12 col-sm-10 col-sm-offset-1 col-md-6 col-md-offset-3')[1]
    exp_veh = more_stat.find_all('div',class_ = 'progress-bar')[0].text
    prem_veh = more_stat.find_all('div',class_ = 'progress-bar')[1].text
    b = exp_veh.split()
    exp_veh = ''.join(b)
    b = prem_veh.split()
    prem_veh = ''.join(b)
    exp_veh = exp_veh.replace('из',' из ')
    prem_veh = prem_veh.replace('из',' из ')
    #------------------categories-------------------
    categ = block.find('div', class_ = 'by-categs')

    table_win = categ.find_all('table')[0]
    table_win_noun = table_win.find_all('span')[0].text
    table_win_pecent = table_win.find_all('td')[0].text
    a = 0
    categ_win.clear()
    for i in range(10):
    	categ_win.append(table_win.find_all('span')[a].text)
    	a += 1
    #--------------medals------------------------
    medals_l = []
    for i in range(5):
        medals = soup.find_all('div',class_='caption')[i].text
        if i == 2:
            medals_l.append((''.join(i for i in ''.join(medals.split()) if not i.isalpha())).split('/')[0].lstrip().replace('-',''))
        else:
            medals_l.append((''.join(i for i in ''.join(medals.split()) if not i.isalpha())).split('/')[0].lstrip())
    #print(medals_l)
    #-------------tanks_10-------------
    content_tank = requests.get(f'https://wblitz.net/accounts/x_vehicles/{user_id}/1/{user_reg}#').text
    bet_soup = BeautifulSoup(content_tank,'lxml')
    tank_model = len(bet_soup.find_all(attrs={"data-tier": '10'}))
    tank_model_n = []
    for i in range((len(bet_soup.find_all(attrs={"data-tier": '10'})))):
        tank_model = bet_soup.find_all(attrs={"data-tier": '10'})[(i)]
        tank_model_n.append(tank_model.find_all('a')[1].text)
    
    tank_model_other = len(bet_soup.find_all(attrs={"data-nation": 'other'}))
    tank_model_other_n = []
    for i in range((len(bet_soup.find_all(attrs={"data-nation": 'other'})))):
        tank_model = bet_soup.find_all(attrs={"data-nation": 'other'})[(i)]
        tank_model_other_n.append(tank_model.find_all('a')[1].text)
    
    #----------------------------------
    #print(categ_win)
    #print(max(categ_win, key=int))
    #print(categ_win.index((max(categ_win, key=int))) + 1 )
    #--------------conclusion------------------------
    #print(f'Количество боёв: {battle_noun}\nПроцент побед: {win_rate}\nБитв взводом: {vzvod}\nСредний урон: {damage}')
    text_teleg.append(f'---------------Статистика---------------\n🟢Дата регистрации: {reg_day}\n⚙️Количество техники: {veh_noun}\n🔷Исследуемой: {exp_veh}\n🔶Премиумной и колл-ой: {prem_veh}\n🆙Средний уровень: {tank_level}\n⚔️Количество боёв: {battle_noun}\n🛡️Количество побед: {wins}\n🛡️Процент побед: {win_rate}\
        \n🍃Выживаний: {alive}\n⚔️Битв взводом: {vzvod}\n💥Средний урон: {damage}\n✨Средний опыт: {mid_exp}\n🔫В среднем попаданий: {hit}\n🔫В среднем выстрелов: {shot}\n---------------Медали---------------\nⓂ️Мастеров: {master}\n🥇Первая степень: {first_degree}\n🥇Медаль героев Расейняя: {medals_l[0]}\nМедаль Пула: {medals_l[1]}\nРэдли-Уолтерса: {medals_l[2]}\nВоин: {medals_l[3]}\nМедаль Колобанова: {medals_l[4]}\n⚔️Больше всего боёв на {categ_win.index((max(categ_win, key=int))) + 1 } уровне - {max(categ_win, key=int)}!\nНа аккаунте были/есть танки 10 уровня: {tank_model_n}\n\nНа аккаунте были/есть танки сборной нации: {tank_model_other_n}')
    categ_win.clear()
    tank_model_n.clear()
    tank_model_other_n.clear()
    print(text_teleg)

def get_id_wot(login,server):
    global link,player_name, player_region
    data = {
    'query':login,
    'server':server
    }
    player_name = login
    player_region = server
    response = session.post(link,data=data).text
    response = response.split(''',''')
    response = response[0]
    response = str(response).split('''"''')
    try:
        new(response[1],server) 
    except IndexError:
        print(f'''Пользователь {data['query']} не найден в регионе {data['server']}''')
        text_teleg.clear()
        text_teleg.append('None correct value')
        text_teleg.append(f'''Пользователь {data['query']} не найден в регионе {data['server']}''')
    
    
#get_id_wot('Andrey_05','eu')
