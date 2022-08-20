import pymongo
import datetime
import pytz

client = pymongo.MongoClient("mongodb+srv://Fit4a:S8Lqaagemi98rTt@cluster0.dzzqz.mongodb.net/Tele_db?retryWrites=true&w=majority")
db = client.Tele_db
coll = db.users
prop_doc = db.prop_coll
rf = db.referals
def check_in(user_id,nickname,region,username):
    query = {'_id': user_id}
    for value in coll.find(query):
        print(value)
    try:
        a = type(value)
    except UnboundLocalError:
        user = {
        '_id' : user_id,
        'name' : nickname,
        'region' : region,
        'telegram_user' : username,
        'date': datetime.datetime.now(pytz.timezone("Europe/Kiev"))
        }
        coll.insert_one(user)
def prop(text,username):
    if text != 'Статистика':
        for value in prop_doc.find({'_id': username}):
            print(value)
        try:
            prop_doc.insert_one({'_id':username,'Message': text})
        except:    
            prop_doc.update_one({'_id': username}, {'$set': {'Message': text}})
    #    prop_doc.deleteOne({'_id': username})
    #except:
    #    pass
    #prop_doc.insert_one({'_id':username,'Message': text})
def users_list(chat):
    #coll.insert_one({'_id': 1010101,'chat_list':[chat]})
    if chat in coll.find_one({'_id':1010101})['chat_list']:
        print(f'Element {chat} already in list')
    else:
        coll.update_one({'_id': 1010101}, {'$push': {'chat_list': chat}})
        print('Good!')
def get_user_l():
    global user_list
    user_list = coll.find_one({'_id':1010101})['chat_list']
def add_referal(user_id_party,f_name,s_name):
    query_r = {'_id': user_id_party}
    for value in rf.find(query_r):
        print(value)
    try:
        type(value)
    except UnboundLocalError:
        user_rf = {
        '_id' : user_id_party,
        'name' : f'{f_name}_{s_name}',
        'user_referals' : []
        }
        rf.insert_one(user_rf)

def update_referal(referal: int,partner: int):
    if partner not in rf.find_one({'_id':referal})['user_referals'] and partner != referal:
        rf.update_one({'_id': referal}, {'$push': {'user_referals': partner}})
def ref_count(id_ref_n):
    try:
        return len(rf.find_one({'_id':int(id_ref_n)})['user_referals'])
    except:
        return '0'
ref_count('rbgsbr')
