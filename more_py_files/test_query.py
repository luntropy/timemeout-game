# from sqlalchemy import create_engine
#
# db_connection = 'postgresql://postgres:postgres@127.0.0.1:5432/timemeout-db'
# engine = create_engine(db_connection)
#
# with engine.connect() as connection:
#     unique_user = connection.execute('''SELECT username FROM player;''')
#
#     if not unique_user.fetchall():
#         print('aaa')

import requests
import urllib.request, json

# BASE = 'http://127.0.0.1:5000/'

# postdata = {'username':'asd', 'password': 'asdasd123'}
# url = 'http://127.0.0.1:5000/register_user'
# x = requests.post(url, json = {'username':'luntropy', 'password': 'luntropy'})

url = 'http://127.0.0.1:5000/list_games'
x = requests.get(url)

# url = 'http://127.0.0.1:5000/create_game'
# x = requests.post(url, json = {'host_id': 1, 'field_size': 20, 'time_limit': 30})

print(x.json)
