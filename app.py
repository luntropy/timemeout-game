from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from passlib.hash import sha256_crypt

import random
import json
import time
import copy

@app.route("/", methods=["GET"])
def get_example():
    """GET in server"""
    response = jsonify(message="Simple server is running")
    return response
    
db_connection = 'postgresql://postgres:postgres@127.0.0.1:5432/timemeout-db'
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
    list_card_ids = list(range(1, 21))

    random.shuffle(list_card_ids)
    cards = list_card_ids[:count_unique_cards]
    duplicates = copy.copy(cards)

    deck = cards + duplicates
    random.shuffle(deck)

    deck_list = []
    for card in deck:
        deck_list.append(str(card))

    return deck_list

# User registration
# Needed information:
# Username, password in format: {'username': 'username', 'password': 'hashed_password'}
@app.route('/register_user', methods = ['POST'])
def register_user():
    if request.method == 'POST':
        data = request.json

        username = ''' '{0}' '''.format(str(data['username']))
        password = ''' '{0}' '''.format(sha256_crypt.hash(str(data['password'])))

        with engine.connect() as connection:
            unique_user_query = connection.execute(text('''SELECT username FROM player WHERE username = {0};'''.format(username)))

            if unique_user_query.fetchall():
                return {'registration': 0}

            create_user_query = connection.execute(text('''INSERT INTO player (username, user_password, score) VALUES ({0}, {1}, 100);'''.format(username, password)))

        return {'registration': 1}

# User login authentication
@app.route('/login_user', methods = ['POST'])
def login_user():
    if request.method == 'POST':
        data = request.json

        username = ''' '{0}' '''.format(str(data['username']))

        with engine.connect() as connection:
            find_user_query = connection.execute(text('''SELECT user_password FROM player WHERE username = {0};'''.format(username)))

            user_data = find_user_query.fetchone()
            if not user_data:
                return {'login': 0}

            if sha256_crypt.verify(str(data['password']), user_data[0]):
                return {'login': 1}
            else:
                return {'login': 0}

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
                return {'game_creation': 0, 'room_data_json': ''}

            player_host_score_query = connection.execute(text('''SELECT score FROM player WHERE player_id = {0};'''.format(host_id)))
            player_host_score = player_host_score_query.fetchone()
            for r in player_host_score:
                player_host_score = r

            player_guest_score = 0

        # Generate json file with the room configuration
        cards_first_player = generate_cards(field_size)
        cards_second_player = generate_cards(field_size)

        data_json = {'room_id': data_room_db['room_id'],
        'host_id': data_room_db['host_id'],
        'guest_id': data_room_db['guest_id'],
        'settings': { 'field_size': data_room_db['field_size'], 'time_limit': data_room_db['time_limit'] },
        'player_host': { 'board': cards_first_player, 'time_left': data_room_db['time_limit'], 'player_score': player_host_score, 'game_score': 0, 'attacks': {} },
        'player_guest': { 'board': cards_second_player, 'time_left': data_room_db['time_limit'], 'player_score': player_guest_score, 'game_score': 0, 'attacks': {} }, 'result': { 'game_result': 'None', 'points_host': 0, 'points_guest': 0 }}

        with open('./rooms_json/' + file_name, 'w', encoding='utf-8') as json_file:
            json.dump(data_json, json_file, ensure_ascii=False, indent=4)

        return {'game_creation': 1, 'room_data_json': data_json}

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
                return {'rooms_list': ''}

            return {'rooms_list': rooms_list}

# Connect to given game
# Input: {'guest_id': 'guest_id', 'room_id': 'room_id'}
# Output: {'room_data_json': 'room_data'} and {'room_data_json': ''} if room not available
# Returns room information
@app.route('/connect_to_game', methods = ['POST'])
def connect_to_game():
    # Updates in the db:
    # host_id
    # Updates the json file:
    # Guest_id
    # player_guest_score
    if request.method == 'POST':
        data = request.json
        room_id = data['room_id']
        guest_id = data['guest_id']

        with engine.connect() as connection:
            # Check if the requested game is available
            check_if_available_query = connection.execute(text('''SELECT * FROM room WHERE room_id = {0} AND guest_id is NULL;'''.format(room_id)))

            if not check_if_available_query.fetchone():
                return {'room_data_json': ''}

            connect_to_game_query = connection.execute(text('''UPDATE room SET guest_id = {0} WHERE room_id = {1};'''.format(guest_id, room_id)))
            rooms_json_query = connection.execute(text('''SELECT json_name FROM room WHERE room_id = {0};'''.format(room_id)))

            room = rooms_json_query.fetchone()
            file_name = room[0]

            json_data = {}
            with open('./rooms_json/' + file_name, 'r', encoding='utf-8') as json_file:
                json_data = json.load(json_file)
            json_data['guest_id'] = guest_id
            with open('./rooms_json/' + file_name, 'w', encoding='utf-8') as json_file:
                json.dump(json_data, json_file, ensure_ascii=False, indent=4)

            return {'room_data_json': json_data}

# Displays final result message
# Ends the game
# Input: {'room_id': 'room_id', 'winner': 'host/guest/draw'}
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
