# from sqlalchemy import create_engine
#
# db_connection = 'postgresql://postgres:postgres@127.0.0.1:5432/timemeout-db'
# engine = create_engine(db_connection)
#
# with engine.connect() as connection:
#     unique_user = connection.execute('''SELECT username FROM player;''')
#
#     if not unique_user.fetchall():
#         print('Empty')

import requests
import urllib.request, json

BASE = 'http://127.0.0.1:5000/'

# Test user creation
postdata = {'username':'asd', 'password': 'asdasd123'}
url = 'register_user'
x = requests.post(BASE + url, json = {'username':'luntropy', 'password': 'luntropy'})

url = 'list_games'
x = requests.get(BASE + url)

url = 'create_game'
x = requests.post(BASE + url, json = {'host_id': 1, 'field_size': 20, 'time_limit': 30})

print(x.json)
