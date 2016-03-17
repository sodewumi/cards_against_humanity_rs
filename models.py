from Crypto.Hash import SHA256
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from flask import Flask

import os

db = SQLAlchemy()


# game_player = db.Table('game_player',
#                        db.Column('game_id', db.Integer, db.ForeignKey('game.id')),
#                        db.Column('player_id', db.Integer, db.ForeignKey('player.id'))
#                        )


# class GamePlayer(db.Model):
#     """Specifies which game a player belongs to"""
#
#     __tablename__ = "game_player"
#
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     game_id = db.Column(db.Integer, db.ForeignKey("player.id"))
#     player_id = db.Column(db.Integer, db.ForeignKey("player.id"))
#
#     def __repr__(self):
#         return "<GamePlayer: id=%d, game_id=%d, player_id=%d>" % (
#             self.id,
#             self.game_id,
#             self.player_id,
#         )


# round_player = db.Table('round_player',
#                         db.Column('round_id', db.Integer, db.ForeignKey('round.id')),
#                         db.Column('player_id', db.Integer, db.ForeignKey('player.id'))
#                         )


# class RoundPlayer(db.Model):
#     """Specifies which round a player belongs to"""
#
#     __tablename__ = "round_player"
#
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     round_id = db.Column(db.Integer, db.ForeignKey("round.id"), primary_key=True)
#     player_id = db.Column(db.Integer, db.ForeignKey("player.id"), primary_key=True)
#
#     def __repr__(self):
#         return "<RoundPlayer: id=%d, round_id=%d, player_id=%d>" % (
#             self.id,
#             self.round_id,
#             self.player_id,
#         )


# player_hand = db.Table('player_hand',
#                        db.Column('hand_id', db.Integer, db.ForeignKey('hand.id')),
#                        db.Column('player_id', db.Integer, db.ForeignKey('player.id'))
#                        )


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(15), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def check_password(self, password):
        return SHA256.new(password.encode('utf-8')).hexdigest() == self.password

    def __repr__(self):
        return "<User: id=%d, email=%s, password=%s, username=%s>" % (
            self.id,
            self.email,
            self.password,
            self.username,
        )


class RoomUser(db.Model):
    __tablename__ = 'room_user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Room(db.Model):
    __tablename__ = "room"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    users = db.relationship('User',
                            secondary='room_user',
                            backref='room',
                            # backref=db.backref('recipes', lazy='dynamic'))
                            lazy='dynamic')

    def __repr__(self):
        return "<Room: id=%d, name=%s>" % (
            self.id,
            self.name,
        )


class BlackMasterCard(db.Model):
    __tablename__ = "black_master_card"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    pick_number = db.Column(db.Integer)

    def __repr__(self):
        return "<PlayerCard: id=%d, text=%s, pick_number=%d>" % (
            self.id,
            self.text,
            self.pick_number,
        )


class BlackGameCard(db.Model):
    __tablename__ = "black_game_card"
    __table_args__ = (
        db.PrimaryKeyConstraint('game_id', 'card_id'),
    )

    # id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    card_id = db.Column(db.Integer, db.ForeignKey('black_master_card.id'))

    # def __repr__(self):
    #     return "<PlayerCard: id=%d, game_id=%d, card_id=%d>" % (
    #         self.id,
    #         self.game_id,
    #         self.card_id,
    #     )


class WhiteMasterCard(db.Model):
    __tablename__ = "white_master_card"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))

    def __repr__(self):
        return "<WhiteMasterCard: id=%d, text=%s>" % (
            self.id,
            self.text,
        )


class WhiteGameCard(db.Model):
    __tablename__ = "white_game_card"
    __table_args__ = (
        db.PrimaryKeyConstraint('game_id', 'card_id'),
    )

    # id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    card_id = db.Column(db.Integer, db.ForeignKey('white_master_card.id'))

    # def __repr__(self):
    #     return "<WhiteGameCard: id=%d, game_id=%d, card_id=%d>" % (
    #         self.id,
    #         self.game_id,
    #         self.card_id,
    #     )


class Game(db.Model):
    __tablename__ = "game"

    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    players = db.relationship("Player",
                              backref="game",
                              cascade="all, delete, delete-orphan",
                              single_parent=True,
                              lazy='dynamic')

    @property
    def max_num_of_players(self):
        return 8

    def __repr__(self):
        return "<Game: id=%d, room_id=%d>" % (
            self.id,
            self.room_id or 0,
        )

    def add_player(self, player):
        if not self.players.filter(Player.user_id == player.user_id).count() == 0:
            raise Exception('User is already in game')
        elif self.players.count() == self.max_num_of_players:
            raise Exception('Max number of players for game reached.')
        self.players.append(player)
        print('Player added.' + '{0} player(s) total.'.format(self.players.count()))

        return self


class Round(db.Model):
    __tablename__ = "round"
    __table_args__ = (
        UniqueConstraint('id', 'game_id', 'round_number'),
    )

    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    round_number = db.Column(db.Integer)
    black_card_id = db.Column(db.Integer, db.ForeignKey('black_master_card.id'))
    judge_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    winner_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    black_card = db.relationship(
        "BlackMasterCard", backref=db.backref("round", uselist=False)
    )
    white_cards = db.relationship("RoundWhiteCard", backref="round")
    # players = db.relationship('Player',
    #                           secondary='round_player',
    #                           backref='round',
    #                           # backref=db.backref('recipes', lazy='dynamic'))
    #                           lazy='dynamic')

    # def __repr__(self):
    #     return """<User: id=%d, game_id=%d, round_number=%d, black_card_id=%d,
    #         judge_id=%d, winner_id=%s>""" % (
    #         self.id,
    #         self.game_id,
    #         self.round_number,
    #         self.black_card_id,
    #         self.judge_id,
    #         self.winner_id or 'No Winner',
    #     )


class Player(db.Model):
    __tablename__ = "player"
    # __table_args__ = (
    #     db.UniqueConstraint('id', 'game_id', 'user_id', 'player_no'),
    # )

    id = db.Column(db.Integer, primary_key=True)
    player_no = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey("game.id"), nullable=False)
    cards = db.relationship("PlayerCard",
                            backref="player",
                            cascade="all, delete, delete-orphan",
                            single_parent=True,
                            lazy='dynamic')

    def __repr__(self):
        return "<Player: id=%d, user_id=%d, name=%s, game_id=%d>" % (
            self.id,
            self.user_id,
            self.name,
            self.game_id,
        )


class PlayerCard(db.Model):
    """Specifies which hand a player has"""

    __tablename__ = "player_card"
    __table_args__ = (
        db.PrimaryKeyConstraint('game_id', 'player_id', 'card_id'),
    )

    # id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey("game.id"))
    player_id = db.Column(db.Integer, db.ForeignKey("player.id"))
    card_id = db.Column(db.Integer, db.ForeignKey("white_master_card.id"))

    def __repr__(self):
        return "<PlayerCard: game_id=%d, card_id=%d, player_id=%d>" % (
            self.game_id,
            self.card_id,
            self.player_id,
        )


class RoundWhiteCard(db.Model):
    __tablename__ = "round_white_card"
    __table_args__ = (
        db.PrimaryKeyConstraint('game_id', 'round_id', 'player_id', 'white_card_id'),
    )

    # id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer)
    round_id = db.Column(db.Integer, db.ForeignKey(Round.id))
    player_id = db.Column(db.Integer, db.ForeignKey(Player.id))
    white_card_id = db.Column(db.Integer, db.ForeignKey(WhiteMasterCard.id))
    pick_num = db.Column(db.Integer)

    # round = db.relationship(
    #     "Round", backref=db.backref("round_white_card")
    # )

    def __repr__(self):
        return """<Game: id=%d, Round: round_id=%d, Player: player_id=%d, Card: white_card_id=%d,
            Pick: pick_num=%d>""" % (
            self.game_id,
            self.round_id,
            self.player_id,
            self.white_card_id,
            self.pick_num
        )


# class Hand(db.Model):
#     __tablename__ = "hand"
#     __table_args__ = (
#         db.ForeignKeyConstraint(
#             ['player_id', 'game_id'],
#             [Player.id, Player.game_id],
#         ),
#     )
#
#     id = db.Column(db.Integer, primary_key=True)
#     player_id = db.Column(db.Integer, db.ForeignKey('player.id'), primary_key=True)
#     game_id = db.Column(db.Integer, db.ForeignKey('player.game_id'), primary_key=True)
#     card_id = db.Column(db.Integer, db.ForeignKey("white_master_card.id"), primary_key=True)
#
#     def __repr__(self):
#         return "<Hand: id=%d, player_id=%d, game_id=%d>, card_id=%d>" % (
#             self.id,
#             self.player_id,
#             self.game_id,
#             self.card_id
#         )


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
