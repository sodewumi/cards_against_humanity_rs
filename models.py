from flask_sqlalchemy import SQLAlchemy
from flask import Flask

import os

db = SQLAlchemy()

# game_player = db.Table('game_player',
#                        db.Column('game_id', db.Integer, db.ForeignKey('game.id')),
#                        db.Column('player_id', db.Integer, db.ForeignKey('player.id'))
#                        )


class GamePlayer(db.Model):
    """Specifies which game a player belongs to"""

    __tablename__ = "game_player"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    game_id = db.Column(db.Integer, db.ForeignKey("player.id"))
    player_id = db.Column(db.Integer, db.ForeignKey("player.id"))


# round_player = db.Table('round_player',
#                         db.Column('round_id', db.Integer, db.ForeignKey('round.id')),
#                         db.Column('player_id', db.Integer, db.ForeignKey('player.id'))
#                         )


class RoundPlayer(db.Model):
    """Specifies which round a player belongs to"""

    __tablename__ = "round_player"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    round_id = db.Column(db.Integer, db.ForeignKey("round.id"))
    player_id = db.Column(db.Integer, db.ForeignKey("player.id"))

# player_hand = db.Table('player_hand',
#                        db.Column('hand_id', db.Integer, db.ForeignKey('hand.id')),
#                        db.Column('player_id', db.Integer, db.ForeignKey('player.id'))
#                        )


class PlayerHand(db.Model):
    """Specifies which hand a player has"""

    __tablename__ = "player_hand"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    card_id = db.Column(db.Integer, db.ForeignKey("white_master_deck.id"))
    player_id = db.Column(db.Integer, db.ForeignKey("player.id"))


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(15), nullable=False)
    username = db.Column(db.String(15), nullable=False, unique=True)

    @classmethod
    def create_new_user(cls, email, password, username):
        new_user = cls(email=email, password=password, username=username)
        db.session.add(new_user)
        db.session.commit()


class Room(db.Model):
    __tablename__ = "room"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))


class Game(db.Model):
    __tablename__ = "game"

    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))


class Round(db.Model):
    __tablename__ = "round"

    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    round_number = db.Column(db.Integer)
    black_card_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    judge_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    winner_id = db.Column(db.Integer, db.ForeignKey('player.id'))


class Player(db.Model):
    __tablename__ = "player"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(20))
    game_id = db.Column(db.Integer, db.ForeignKey('room.id'))


class Hand(db.Model):
    __tablename__ = "hand"

    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    card_id = db.Column(db.Integer, db.ForeignKey("white_master_deck.id"))


class BlackMasterCard(db.Model):
    __tablename__ = "black_master_deck"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    pick_number = db.Column(db.Integer)


class BlackGameCard(db.Model):
    __tablename__ = "black_game_deck"

    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    card_id = db.Column(db.Integer, db.ForeignKey('black_master_deck.id'))


class WhiteMasterCard(db.Model):
    __tablename__ = "white_master_deck"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))


class WhiteGameCard(db.Model):
    __tablename__ = "white_game_deck"

    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    card_id = db.Column(db.Integer, db.ForeignKey('white_master_deck.id'))


def connect_to_db(app):
    """Connect the database to our Flask app."""
    if os.environ.get('DATABSE_URL') is None:
        SQLALCHEMY_DATABASE_URI = os.environ['LOCAL_DATABASE_URI']
    else:
        SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)
    db.create_all()


if __name__ == "__main__":
    from app import app
    connect_to_db(app)