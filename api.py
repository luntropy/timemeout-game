from flask import Flask, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@127.0.0.1:5432/timemeout-db'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique = True)

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return self.username

class Room(Resource):
    def post(self, host_id, field_size, time_limit):
        return {'host_id': host_id, 'field_size': field_size, 'time_limit': time_limit}

    def get(self, room_id):
        return {'room_id': room_id}


api.add_resource(Room, '/room/<int:host_id>/<string:field_size>/<int:time_limit>')

if __name__ == '__main__':
    app.run(debug=True)
