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
url = 'register_user'
user_one = {'username': 'luntropy', 'password': 'luntropy'}
user_two = {'username': 'lunt', 'password': 'lunt'}
x = requests.post(BASE + url, json=user_one)
x = requests.post(BASE + url, json=user_two)

# Test user login
url = 'login_user'
user = {'username': 'luntropy', 'password': 'luntropy'}
x = requests.post(BASE + url, json=user)

# Test games creation
url = 'create_game'
x = requests.post(BASE + url, json={'host_id': 5, 'field_size': 20, 'time_limit': 30})

# Test games listing
url = 'list_games'
x = requests.get(BASE + url)

# Test connection to a game
data = {'guest_id': 6, 'room_id': 62}

url = 'connect_to_game'
x = requests.post(BASE + url, json=data)

# test end of the game
data = {'room_id': 62, 'winner': 'host', 'player_id': 5, 'player_role': 'guest', 'player_game_score': 10}

url = 'end_game'
x = requests.post(BASE + url, json=data)

# data = {'attack_type': 1, 'player_id': 5, 'player_role': 'host', 'room_id': 51}
# url = 'attack'
# x = requests.post(BASE + url, json=data)

print(x.json)
