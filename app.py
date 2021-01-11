from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text

import random
import json
import time
import copy

db_connection = 'postgresql://postgres:postgres@127.0.0.1:5432/timemeout'  # timemeout-db
engine = create_engine(db_connection)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = db_connection
db = SQLAlchemy(app)

# Functions
def generate_cards(field_size):
    # 4x5 = 20, 10 unique
    # 4x4 = 16, 8 unique
    # 3x4 = 12, 6 unique

    count_unique_cards = int(field_size / 2)
    list_card_ids = list(range(0, 21))

    random.shuffle(list_card_ids)
    cards = list_card_ids[:count_unique_cards]
    duplicates = copy.copy(cards)

    deck = cards + duplicates
    random.shuffle(deck)

    deck_dictionary = {}
    for card in deck:
        card = str(card)

        if card in deck_dictionary.keys():
            card = card + '-2'

        deck_dictionary[card] = 0

    return deck_dictionary

# User registration
# Needed information:
# Username, password in format: {'username': 'username', 'password': 'hashed_password'}
# Tokens
@app.route('/register_user', methods = ['POST'])
def register_user():
    if request.method == 'POST':
        data = request.json

        username = str(data['username'])
        password = str(data['password'])
        username = ''' '{0}' '''.format(username)
        password = ''' '{0}' '''.format(password)

        with engine.connect() as connection:
            unique_user_query = connection.execute(text('''SELECT username FROM player WHERE username = {0};'''.format(username)))

            if unique_user_query.fetchall():
                return {'registration': 'unsuccessful'}

            create_user_query = connection.execute(text('''INSERT INTO player (username, user_password, score) VALUES ({0}, {1}, 100);'''.format(username, password)))

        return {'registration': 'successful'}

# User login authentication
# @app.route('/login_user', methods = ['POST'])
# def login_user():
#     if request.method == 'POST':
#         data = request.json

# Create game
# Creates game and adds it to the db
# {'host_id': 'host_id', 'field_size': 'field_size', 'time_limit': 'time_limit'}
@app.route('/create_game', methods = ['POST'])
def create_game():
    if request.method == 'POST':
        data = request.json

        host_id = data['host_id']
        field_size = data['field_size']
        time_limit = data['time_limit']

        current_time = round(time.time())
        file_name_db = "'" + '{0}{1}.json'.format(host_id, current_time) + "'"
        file_name = '{0}{1}.json'.format(host_id, current_time)

        # Create room
        with engine.connect() as connection:
            create_room_query = connection.execute(text('''INSERT INTO room (host_id, field_size, time_limit, json_name) VALUES ({0}, {1}, {2}, {3});'''.format(host_id, field_size, time_limit, file_name_db)))

            data_room_query = connection.execute(text('''SELECT * FROM room WHERE host_id = {0} AND json_name = {1} AND finished = '0';'''.format(host_id, file_name_db)))

            data_room_db = data_room_query.fetchone()
            if not data_room_db:
                return {'game_creation': 'unsuccessful', 'room_data_json': 'None'}

            player_host_score_query = connection.execute(text('''SELECT score FROM player WHERE player_id = {0};'''.format(host_id)))
            player_host_score = player_host_score_query.fetchone()
            for r in player_host_score:
                player_host_score = r

            player_guest_score = 0

        # Generate json file for the room configuration
        cards_first_player = generate_cards(field_size)
        cards_second_player = generate_cards(field_size)

        data_json = {'room_id': data_room_db['room_id'],
        'host_id': data_room_db['host_id'],
        'guest_id': data_room_db['guest_id'],
        'settings': { 'field_size': data_room_db['field_size'], 'time_limit': data_room_db['time_limit'] },
        'player_host': { 'board': cards_first_player, 'time_left': data_room_db['time_limit'], 'player_score': player_host_score, 'game_score': 0, 'attacks': {} },
        'player_guest': { 'board': cards_second_player, 'time_left': data_room_db['time_limit'], 'player_score': player_guest_score, 'game_score': 0, 'attacks': {} }, 'result': { 'game_result': 'None', 'points_host': 0, 'points_guest': 0 }}

        print(type(data_json))
        with open('./rooms_json/' + file_name, 'w', encoding='utf-8') as json_file:
            json.dump(data_json, json_file, ensure_ascii=False, indent=4)

        return {'game_creation': 'unsuccessful', 'room_data_json': file_name_db}

# List available games
@app.route('/list_games', methods = ['GET'])
def list_games():
    if request.method == 'GET':
        with engine.connect() as connection:
            rooms_list_query = connection.execute(text('''SELECT * FROM room WHERE finished = '0' AND guest_id is NULL;'''))

            rooms = rooms_list_query.fetchall()
            rooms_list = []
            for row in rooms:
                rooms_list.append(row[0])

            if not rooms_list_query.fetchall():
                return {'rooms_list': 'None'}

            return {'rooms_list': rooms_list}

# Connect to given game
# Input: {'guest_id': 'guest_id', 'room_id': 'room_id'}
# Output: {'room_data_json': 'room_data_json.json'}
# Returns room information
# @app.route('/connect_to_game', methods = ['POST'])
# def connect_to_game():
@app.route('/connect_to_game', methods = ['POST'])
def connect_to_game():
    # Updates in the db:
    # host_id
    # Updates the json file:
    # Guest_id
    # player_guest_score
    if request.method == 'POST':
        data = request.json
        guest_id = data['guest_id']
        room_id = data['room_id']
        with engine.connect as connection:
            connect_to_game_query = connection.execute('''UPDATE room SET guest_id = {0} WHERE room_id = {1}'''.format(guest_id, room_id))
            rooms_json_query = connection.execute(text('''SELECT json_name FROM room WHERE room_id = {0};'''.format(room_id)))

            room = rooms_json_query.fetchone()
            file_name = room[0]
            json_data = {}
            with open('./rooms_json/' + file_name, 'r', encoding='utf-8') as json_file:
                json_data = json.load(json_file)
            json_data['guest_id'] = guest_id
            with open('./rooms_json/' + file_name, 'w', encoding='utf-8') as json_file:
                json.dump(json_data, json_file, ensure_ascii=False, indent=4)
            # returns dic but can be changed
            return {'room_data_json': json_data}

# Displays final result message
# Ends the game
# Input: {'winner': 'host/guest/draw'}
# Output: json file updated 'result' with final points gained or lost by the players {'json': 'updated'} or {'json': 'None'}
# @app.route('/end_game', methods = ['POST'])
# def end_game():
@app.route('/end_game', methods = ['POST'])
def end_game():
    # Updates the db with the final result
    # Updates:
    # finished = 1
    # game_result win/ lose/ draw - host perspective
    # host_score = the score the host gained when playing - different from player score
    # guest_schore = the score the guest gained when playing - different from player score
    if request.method == 'POST':
        data = request.jsons
        game_result = data['winner']
        # ??????? we need room_id at least, not only the reuslt... also the score......

    # Updates the players' score:
    # 1. From the json file get player score (or db)
    # 2. From the json file get points gained for the host and the guest - player score in player_host and player_guest
    # 3. Formula: P1 - won P1 score = P1 score + 10% * P2 score + 6% P1 game_score_p1
    # if P2 lost and P2 score = 0 then formula: P1 score = P1 score + 5 + 6% P1 game_score_p1
    # Formula: P2 - lost P2 score = P2 score - 10% P2 score
    # If draw no one gains or loses points

# @app.route('/attack', methods = ['POST'])
# def attack():
# Attack on player

if __name__ == '__main__':
    app.run(debug=True)
