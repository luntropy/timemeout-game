from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

import time

db_connection = 'postgresql://postgres:postgres@127.0.0.1:5432/timemeout-db'
engine = create_engine(db_connection)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = db_connection
db = SQLAlchemy(app)

# @app.route('/register_user', methods = ['POST'])
# def register_user():
# User registration
#     # if request.method == 'POST':
#     #     data = request.get_json()
#     #
#     #     with engine.connect() as connection:
#     #         result = connection.execute('''INSERT INTO player (username, user_password, score) VALUES ('llunts', 'llunts', 100);''')
#     #
#     # return {'registration': 'successful'}

# @app.route('/login_user', methods = ['POST'])
# def login_user():
# User login authentication

# @app.route('/list_games', methods = ['POST'])
# def list_games():
# List available games

# @app.route('/connect_to_game', methods = ['POST'])
# def connect_to_game():
# Connect to given game
# Connects user to the choosen game - returns json with room info

# @app.route('/create_game', methods = ['POST'])
# def create_game():
# Create game
# Creates game and adds it to the db

# @app.route('/exit_game', methods = ['POST'])
# def exit_game():
# Exit game
# Updates the db with the final result and returns the player to main menu

# @app.route('/abandon_game', methods = ['POST'])
# def abandon_game():
# Updates the db with the result and returns the player to main menu

# @app.route('/attack', methods = ['POST'])
# def attack():
# Attack on player

# Tests:
# @app.route('/display')
# def display():
    # with engine.connect() as connection:
    #     result = connection.execute('''SELECT username FROM player;''')
    #
    # return jsonify({'result': [dict(row) for row in result]})

if __name__ == '__main__':
    app.run(debug=True)
