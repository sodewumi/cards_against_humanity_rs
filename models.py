import json
from Crypto.Hash import SHA256
from sqlalchemy import UniqueConstraint
from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import ModelSchema, field_for
from flask_marshmallow.sqla import HyperlinkRelated
from app import app

import os
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_utils.operators import func
from sqlalchemy.sql.expression import select

db = SQLAlchemy()
ma = Marshmallow()


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(15), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)

    @property
    def url(self):
        return url_for('user', id=self.id)

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
    __table_args__ = (
        db.PrimaryKeyConstraint('room_id', 'user_id'),
    )

    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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

    @property
    def url(self):
        return url_for('room', id=self.id)

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

    @property
    def url(self):
        return url_for('black_master_card', id=self.id)

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

    def __repr__(self):
        return "<PlayerCard: game_id=%d, card_id=%d>" % (
            self.game_id,
            self.card_id,
        )


class WhiteMasterCard(db.Model):
    __tablename__ = "white_master_card"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))

    @property
    def url(self):
        return url_for('white_master_card', id=self.id)

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

    rounds = db.relationship("Round",
                             backref="game",
                             cascade="all, delete, delete-orphan",
                             single_parent=True,
                             lazy='dynamic')

    @property
    def url(self):
        return url_for('game', id=self.id)

    @property
    def max_num_of_players(self):
        return 8

    @property
    def player_slot_available(self):
        return self.max_num_of_players - self.players.count()

    # @property
    # def json(self):
    #     print (to_json(self, self.__class__))
    #     return to_json(self, self.__class__)

    # @property
    # def url(self):
    #     return url_for('game', id=self.id)

    # def __repr__(self):
    #     return "<Game: id=%d, room_id=%r>" % (
    #         self.id,
    #         self.room_id,
    #     )

    def add_player(self, player):

        if not self.players.filter(Player.user_id == player.user_id).count() == 0:
            raise Exception('User is already in game')
        elif not self.player_slot_available:
            raise Exception('Max number of players for game reached.')

        player.player_no = self.players.count() + 1
        self.players.append(player)

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
    # winner = db.relationship("Player")
    black_card = db.relationship(
        "BlackMasterCard", backref=db.backref("round", uselist=False)
    )
    white_cards = db.relationship("RoundWhiteCard", backref="round")

    @property
    def url(self):
        return url_for('round', id=self.id)

    def __repr__(self):
        return """<Round: id=%d, game_id=%d, round_number=%d, black_card_id=%d,
            judge_id=%d, winner_id=%r>""" % (
            self.id,
            self.game_id,
            self.round_number,
            self.black_card_id,
            self.judge_id,
            self.winner_id,
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
    cards = db.relationship('WhiteMasterCard',
                            secondary='player_card',
                            backref="player",
                            cascade="all, delete, delete-orphan",
                            single_parent=True,
                            lazy='dynamic')

    # rounds = db.relationship('Round',
    #                          primaryjoin="and_(Player.game_id==Round.game_id, Player.id==Round.winner_id)",
    #                          lazy='dynamic')

    rounds = db.relationship('Round',
                             primaryjoin="and_(Player.game_id==Round.game_id, Player.id==Round.winner_id)")

    @property
    def score(self):
        db.session.query(Round).filter(Round.game_id == self.game_id)

    @property
    def url(self):
        return url_for('player', id=self.id)

    @property
    def hand(self):
        return self.cards.all()

    @hybrid_property
    def score(self):
        # return sum(rnd.balance for rnd in self.rounds)
        return self.rounds.count()

    @score.expression
    def score(cls):
        return select([func.count(Round.id)]).where(Round.game_id == cls.game_id,
                                                    Round.winner_id == cls.winner_id).label("score")

    def __repr__(self):
        return "<Player: id=%d, user_id=%d, name=%s, game_id=%d>" % (
            self.id,
            self.user_id,
            self.name,
            self.game_id,
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

    white_card = db.relationship(
        "WhiteMasterCard", backref=db.backref("round", uselist=False)
    )

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


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
        fields = ("id", "email", "username", '_links')
        exclude = ("password",)

    # Smart hyperlinking
    _links = ma.Hyperlinks({
        # 'self': ma.URLFor('_get_user', user_name='<username>'),
        'collection': ma.URLFor('_get_users')
    })


class RoomSchema(ma.ModelSchema):
    class Meta:
        model = Room

    # Smart hyperlinking
    _links = ma.Hyperlinks({
        'self': ma.URLFor('_get_room', room_id='<id>'),
        'collection': ma.URLFor('_get_rooms')
    })


class RoomUserSchema(ma.ModelSchema):
    class Meta:
        model = RoomUser


class WhiteMasterCardSchema(ma.ModelSchema):
    class Meta:
        model = WhiteMasterCard
        only = ('id', 'text')
        exclude = ('player', 'round')

    # Smart hyperlinking
    _links = ma.Hyperlinks({
        'self': ma.URLFor('_get_white_master_card', id='<id>'),
        'collection': ma.URLFor('_get_white_master_cards')
    })


class BlackMasterCardSchema(ma.ModelSchema):
    class Meta:
        model = BlackMasterCard

    # Smart hyperlinking
    _links = ma.Hyperlinks({
        'self': ma.URLFor('_get_black_master_card', id='<id>'),
        'collection': ma.URLFor('_get_black_master_cards')
    })


class PlayerCardSchema(ma.ModelSchema):
    class Meta:
        model = PlayerCard
        fields = ('game_id', 'player_id', 'card_id',)

    # Smart hyperlinking
    _links = ma.Hyperlinks({
        'self': ma.URLFor('_get_player', game_id='<game_id>', player_id='<player_id>'),
        'collection': ma.URLFor('_get_game_players', player_id='<game_id>')
    })


class PlayerSchema(ma.ModelSchema):
    class Meta:
        model = Player

    # Smart hyperlinking
    _links = ma.Hyperlinks({
        'self': ma.URLFor('_get_player', game_id='<game_id>', player_id='<id>'),
        'collection': ma.URLFor('_get_game_players', id='<id>')
    })

    cards = ma.Nested(WhiteMasterCardSchema, many=True)
    # cards = ma.Nested(PlayerCardSchema, many=True)

    # date_created = field_for(Player, 'score', dump_only=True)


class RoundWhiteCardSchema(ma.ModelSchema):
    class Meta:
        fields = ('player_id', 'white_card_id', 'pick_num',)
        model = RoundWhiteCard

    # Smart hyperlinking
    _links = ma.Hyperlinks({
        # 'self': ma.URLFor('_get_round_white_card', game_id='<game_id>', round_number='<round_number>'),
        'collection': ma.URLFor('_get_round_white_cards', game_id='<game_id>', round_number='<round_number>')
    })


class RoundSchema(ma.ModelSchema):
    class Meta:
        model = Round
        fields = ('id', 'round_number', 'winner_id', '_links', 'black_card', 'white_cards')
        ordered = True

    # Smart hyperlinking
    _links = ma.Hyperlinks({
        'self': ma.URLFor('_get_round', game_id='<game_id>', round_number='<round_number>'),
        'collection': ma.URLFor('_get_rounds', id='<id>')
    })

    black_card = ma.Nested(BlackMasterCardSchema)
    white_cards = ma.Nested(RoundWhiteCardSchema, many=True)


class GameSchema(ma.ModelSchema):
    class Meta:
        model = Game

    # Smart hyperlinking
    _links = ma.Hyperlinks({
        'self': ma.URLFor('_get_games', id='<id>'),
        'collection': ma.URLFor('_get_games')
    })

    players = ma.Nested(PlayerSchema, many=True)
    rounds = ma.Nested(RoundSchema, many=True)
    # players = ma.List(HyperlinkRelated(
    #     '_get_game_players',
    #     url_kwargs={'game_id': '<game_id>', 'player_id': '<player_id>'},
    #     # Include resource linkage
    #     many=True, include_data=True,
    #     type_='players'
    # ))
    #
    # rounds = ma.List(HyperlinkRelated(
    #     '_get_rounds',
    #     url_kwargs={'id': '<id>'},
    #     # Include resource linkage
    #     many=True, include_data=True,
    #     type_='rounds'
    # ))


class BlackCardSchema(ma.ModelSchema):
    class Meta:
        model = BlackGameCard

    # Smart hyperlinking
    _links = ma.Hyperlinks({
        # 'self': ma.URLFor('_get_black_game_card', game_id='<game_id>'),
        'collection': ma.URLFor('_get_black_game_cards', game_id='<game_id>')
    })


def connect_to_db(app):
    """Connect the database to our Flask app."""
    if os.environ.get('DATABASE_URL') is None:
        SQLALCHEMY_DATABASE_URI = os.environ['LOCAL_DATABASE_URI']
    else:
        SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    ma.app = app
    db.init_app(app)
    db.create_all()


if __name__ == "__main__":
    from app import app

    connect_to_db(app)
