from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from passlib.hash import sha256_crypt

import random
import json
import time
import copy

db_connection = 'postgresql://postgres:postgres@127.0.0.1:5432/timemeout-db'
engine = create_engine(db_connection)

app = Flask(__name__)
CORS(app)


# Test
@app.route("/", methods=["GET"])
def get_example():
    """GET in server"""
    response = jsonify(message="Simple server is running")
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response


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
@app.route('/register_user', methods=['POST'])
def register_user():
    if request.method == 'POST':
        data = request.json

        username = ''' '{0}' '''.format(str(data['username']))
        password = ''' '{0}' '''.format(sha256_crypt.hash(str(data['password'])))

        with engine.connect() as connection:
            unique_user_query = connection.execute(text('''SELECT username FROM player WHERE username = {0};'''.format(username)))
            player_id = ''

            if unique_user_query.fetchall():
                response = jsonify({'registration': 0, 'player_id': player_id})
                response.headers.add("Access-Control-Allow-Origin", "*")
                return response

            create_user_query = connection.execute(text('''INSERT INTO player (username, user_password, score) VALUES ({0}, {1}, 100);'''.format(username, password)))
            select_user_id = connection.execute(text('''SELECT player_id FROM player WHERE username = {0};'''.format(username)))
            player_id = select_user_id.fetchone()[0]
            response = jsonify({'registration': 1, 'player_id': player_id})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response


# User login authentication
@app.route('/login_user', methods=['POST'])
def login_user():
    if request.method == 'POST':
        data = request.json

        username = ''' '{0}' '''.format(str(data['username']))

        with engine.connect() as connection:
            find_user_query = connection.execute(text('''SELECT user_password FROM player WHERE username = {0};'''.format(username)))

            player_id = ''
            user_data = find_user_query.fetchone()
            if not user_data:
                response = jsonify({'login': 0, 'player_id': player_id})
                response.headers.add("Access-Control-Allow-Origin", "*")
                return response

            if sha256_crypt.verify(str(data['password']), user_data[0]):
                select_user_id = connection.execute(text('''SELECT player_id FROM player WHERE username = {0};'''.format(username)))
                player_id = select_user_id.fetchone()[0]
                response = jsonify({'login': 1, 'player_id': player_id})
                response.headers.add("Access-Control-Allow-Origin", "*")
                return response
            else:
                response = jsonify({'login': 0, 'player_id': player_id})
                response.headers.add("Access-Control-Allow-Origin", "*")
                return response


# Create game
# Creates game and adds it to the db
# {'host_id': 'host_id', 'field_size': 'field_size', 'time_limit': 'time_limit'}
@app.route('/create_game', methods=['POST'])
def create_game():
    if request.method == 'POST':
        data = request.json

        host_id = data['host_id']
        field_size = data['field_size']
        time_limit = data['time_limit']

        current_time = round(time.time())
        file_name_db = "'" + '{0}{1}.json'.format(host_id, current_time) + "'"
        file_name = '{0}{1}.json'.format(host_id, current_time)

        room_id = ''

        # Create room
        with engine.connect() as connection:
            create_room_query = connection.execute(text('''INSERT INTO room (host_id, field_size, time_limit, json_name) VALUES ({0}, {1}, {2}, {3});'''.format(host_id, field_size, time_limit, file_name_db)))

            data_room_query = connection.execute(text('''SELECT * FROM room WHERE host_id = {0} AND json_name = {1} AND finished = '0';'''.format(host_id, file_name_db)))

            data_room_db = data_room_query.fetchone()
            if not data_room_db:
                response = jsonify({'game_creation': 0, 'room_data_json': '', 'room_id': ''})
                response.headers.add("Access-Control-Allow-Origin", "*")
                return response

            room_id = data_room_db['room_id']

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
        'player_host': { 'board': cards_first_player, 'time_left': data_room_db['time_limit'], 'player_score': player_host_score, 'game_score': 0, 'attacks': 0 },
        'player_guest': { 'board': cards_second_player, 'time_left': data_room_db['time_limit'], 'player_score': player_guest_score, 'game_score': 0, 'attacks': 0 }, 'result': { 'game_result': 'None', 'points_host': 0, 'points_guest': 0 }}

        with open('./rooms_json/' + file_name, 'w', encoding='utf-8') as json_file:
            json.dump(data_json, json_file, ensure_ascii=False, indent=4)

        response = jsonify({'game_creation': 1, 'room_data_json': data_json, 'room_id': room_id})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response


# List available games
@app.route('/list_games', methods=['GET'])
def list_games():
    if request.method == 'GET':
        with engine.connect() as connection:
            rooms_list_query = connection.execute(text('''SELECT * FROM room WHERE finished = '0' AND guest_id is NULL;'''))

            rooms = rooms_list_query.fetchall()
            rooms_list = []
            for row in rooms:
                rooms_list.append(row[0])

            if not rooms_list_query.fetchall():
                response = jsonify({'rooms_list': ''})
                response.headers.add("Access-Control-Allow-Origin", "*")

                return response

            response = jsonify({'rooms_list': rooms_list})
            response.headers.add("Access-Control-Allow-Origin", "*")

            return response


# Connect to given game
# Input: {'guest_id': 'guest_id', 'room_id': 'room_id'}
# Output: {'room_data_json': 'room_data'} and {'room_data_json': ''} if room not available
# Returns room information
@app.route('/connect_to_game', methods=['POST'])
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
                response = jsonify({'room_data_json': ''})
                response.headers.add("Access-Control-Allow-Origin", "*")
                return response

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

            response = jsonify({'room_data_json': json_data})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response

# Displays final result message
# Ends the game
# Input: {'room_id': 'room_id', 'winner': 'host/guest/draw', 'player_id': id, 'player_role': 'host/guest', 'player_game_score': 'game_score'}
@app.route('/end_game', methods=['POST'])
def end_game():
    # Check if winner and player_role are the same if they are continue
    # else return response for losing the game

    if request.method == 'POST':
        data = request.json
        room_id = data['room_id']
        game_result = data['winner']
        player_id = data['player_id']
        player_role = data['player_role']
        player_game_score = data['player_game_score']

        if game_result.lower() == 'draw':
            with engine.connect() as connection:
                finish_game_query = connection.execute(text('''UPDATE room SET Finished = {0} WHERE room_id = {1};'''.format(True, room_id)))
            response = jsonify({'result': game_result})
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response
        elif game_result.lower() == 'host':
            with engine.connect() as connection:
                rooms_json_query = connection.execute(text('''SELECT json_name FROM room WHERE room_id = {0};'''.format(room_id)))

                room = rooms_json_query.fetchone()
                player_score_query = connection.execute(text('''SELECT Score FROM Player WHERE Player_id = {0};'''.format(player_id)))
                pl_score = player_score_query.fetchone()

                if room is not None and pl_score is not None:
                    file_name = room[0]
                    finish_game_query = connection.execute(text('''UPDATE room SET Finished = {0}, Game_result = {1} WHERE room_id = {2};'''.format(True, "'WIN'", room_id)))

                    json_data = {}
                    with open('./rooms_json/' + file_name, 'r', encoding='utf-8') as json_file:
                        json_data = json.load(json_file)

                    score = pl_score[0]
                    # 1. Add query for guest score
                    # 2. Add 10% of the score to the host's score + 6% of his game score
                    # 3. Remove 10% of the guest's score
                    if player_role == 'host':
                        score += int(0.10 * score + 0.06 * player_game_score)
                        json_data["player_host"]["player_score"] = score
                        json_data["player_host"]["game_score"] = player_game_score

                    # If guest do nothing - the scores are already updated in the db
                    if player_role == 'guest':
                        score -= int(0.10 * score)
                        json_data["player_guest"]["player_score"] = score
                        json_data["player_guest"]["game_score"] = player_game_score
                    player_score_query = connection.execute(text('''UPDATE Player SET Score = {0} WHERE Player_id = {1};'''.format(score, player_id)))

                    with open('./rooms_json/' + file_name, 'w', encoding='utf-8') as json_file:
                        json.dump(json_data, json_file, ensure_ascii=False, indent=4)

        elif game_result.lower() == 'guest':
            with engine.connect() as connection:
                rooms_json_query = connection.execute(text('''SELECT json_name FROM room WHERE room_id = {0};'''.format(room_id)))

                room = rooms_json_query.fetchone()
                player_score_query = connection.execute(text('''SELECT Score FROM Player WHERE Player_id = {0};'''.format(player_id)))
                pl_score = player_score_query.fetchone()

                if room is not None and pl_score is not None:
                    file_name = room[0]
                    finish_game_query = connection.execute(text('''UPDATE room SET Finished = {0}, Game_result = {1} WHERE room_id = {2};'''.format(True, "'LOST'", room_id)))

                    json_data = {}
                    with open('./rooms_json/' + file_name, 'r', encoding='utf-8') as json_file:
                        json_data = json.load(json_file)

                    score = pl_score[0]
                    if player_role == 'host':
                        score -= int(0.10 * score)
                        json_data["player_host"]["player_score"] = score
                        json_data["player_host"]["game_score"] = player_game_score
                    if player_role == 'guest':
                        score += int(0.10 * score + 0.06 * player_game_score)
                        json_data["player_guest"]["player_score"] = score
                        json_data["player_guest"]["game_score"] = player_game_score
                    player_score_query = connection.execute(text('''UPDATE Player SET Score = {0} WHERE Player_id = {1};'''.format(score, player_id)))

                    with open('./rooms_json/' + file_name, 'w', encoding='utf-8') as json_file:
                        json.dump(json_data, json_file, ensure_ascii=False, indent=4)

        response = jsonify({'result': game_result})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response


# @app.route('/attack', methods = ['POST'])
# def attack():
# Attack on player
# Input: {'attack_type': 0/1/2, 'player_id': 'player_id', 'player_role': 'host/guest', 'room_id': 'room_id'}
# Output: {'attack_type': 0/1/2, 'player_id': 'player_id', 'player_role': 'host/guest', 'room_id': 'room_id'}
@app.route('/attack', methods=['POST'])
def attack():
    if request.method == 'POST':
        data = request.json
        attack_type = data['attack_type']
        player_id = data['player_id']
        player_role = data['player_role']
        room_id = data['room_id']

        if attack_type == 0:
            with engine.connect() as connection:
                rooms_json_query = connection.execute(text('''SELECT json_name FROM room WHERE room_id = {0};'''.format(room_id)))

                room = rooms_json_query.fetchone()
                if room is not None:
                    file_name = room[0]
                    json_data = {}
                    with open('./rooms_json/' + file_name, 'r', encoding='utf-8') as json_file:
                        json_data = json.load(json_file)
                    host_id = json_data['host_id']
                    guest_id = json_data['guest_id']

                    attack = 0
                    oponent_id = 0
                    oponent_role = ''
                    if player_role.lower() == 'host':
                        attack = json_data['player_guest']['attacks']  # the attack from pl2 to pl1
                        json_data['player_guest']['attacks'] = 0
                        oponent_id = guest_id
                        oponent_role = 'guest'

                    else:
                        attack = json_data['player_host']['attacks']  # the attack from pl1 to pl2
                        json_data['player_host']['attacks'] = 0
                        oponent_id = host_id
                        oponent_role = 'host'

                    with open('./rooms_json/' + file_name, 'w', encoding='utf-8') as json_file:
                        json.dump(json_data, json_file, ensure_ascii=False, indent=4)

                    response = jsonify({'attack_type': attack, 'player_id': oponent_id, 'player_role': oponent_role, 'room_id': room_id})
                    response.headers.add("Access-Control-Allow-Origin", "*")
                    return response

        else:
            with engine.connect() as connection:
                rooms_json_query = connection.execute(text('''SELECT json_name FROM room WHERE room_id = {0};'''.format(room_id)))

                room = rooms_json_query.fetchone()
                if room is not None:
                    file_name = room[0]
                    json_data = {}
                    with open('./rooms_json/' + file_name, 'r', encoding='utf-8') as json_file:
                        json_data = json.load(json_file)
                    host_id = json_data['host_id']
                    guest_id = json_data['guest_id']

                    attack = 0
                    oponent_id = 0
                    if player_role.lower() == 'host':
                        # attack = json_data['player_guest']['attacks']  # the attack from pl2 to pl1
                        json_data['player_host']['attacks'] = attack_type
                        oponent_id = guest_id
                        oponent_role = 'guest'

                    else:
                        # attack = json_data['player_host']['attacks']  # the attack from pl1 to pl2
                        json_data['player_guest']['attacks'] = attack_type
                        oponent_id = host_id
                        oponent_role = 'host'

                    with open('./rooms_json/' + file_name, 'w', encoding='utf-8') as json_file:
                        json.dump(json_data, json_file, ensure_ascii=False, indent=4)

                    response = jsonify({'attack_type': attack, 'player_id': oponent_id, 'player_role': oponent_role, 'room_id': room_id})
                    response.headers.add("Access-Control-Allow-Origin", "*")
                    return response


if __name__ == '__main__':
    app.run(debug=True)
