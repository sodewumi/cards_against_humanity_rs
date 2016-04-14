from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import and_, or_
import os

from models import BlackGameCard
from models import BlackMasterCard
from models import Game
# from models import GamePlayer
from models import PlayerCard
from models import Player
# from models import PlayerHand
from models import Room
from models import Round
from models import RoundWhiteCard
# from models import RoundPlayer
from models import User
from models import WhiteMasterCard
from models import WhiteGameCard
from models import GameSchema, PlayerSchema, RoomSchema, RoundSchema, WhiteMasterCard, BlackCardSchema, UserSchema
from seed import connect_to_db
from app import app

db = SQLAlchemy()
ma = Marshmallow()


# CREATE
def create_new_user(
        email,
        password,
        username,
):
    new_user = User(
        email=email,
        password=password,
        username=username
    )

    db.session.add(new_user)
    db.session.commit()


def get_user_by_username(user_name):
    user_schema = UserSchema()
    user = User.query.filter(User.username == user_name).one()
    return user_schema.dump(user).data


def get_user_by_email(email):
    user_schema = UserSchema()
    user = User.query.filter(User.email == email).one()
    return user_schema.dump(user).data


def get_user_by_id(_id):
    user_schema = UserSchema()
    user = User.query.filter(User.id == _id).one()
    return user_schema.dump(user).data


def get_users():
    users_schema = UserSchema(many=True)
    users = Game.query.all()
    return users_schema.dump(users).data


def create_new_room(
        name,
):
    new_room = Room(name=name, )

    db.session.add(new_room)
    db.session.commit()


def create_new_game(
        room_id,
):
    new_game = Game(
        room_id=room_id,
    )

    db.session.add(new_game)
    db.session.commit()


def create_new_player(
        user_id, name, game_id
):
    game = Game.query.filter(Game.id == game_id).one()
    if game is None:
        raise Exception('Game {0} does not exist.'.format(game_id))
    new_player = Player(user_id=user_id, name=name)
    g = game.add_player(new_player);
    db.session.commit()

    db.session.add(new_player)
    db.session.commit()


def create_new_round(
        game_id,
        judge_id
):
    black_card_id = BlackGameCard.query.first().card_id

    new_round = Round(
        game_id=game_id,
        black_card_id=black_card_id,
        judge_id=judge_id
    )

    db.session.add(new_round)
    db.session.commit()

    return new_round.round_number


# GET
def get_rooms():
    rooms_schema = RoomSchema(many=True)
    rooms = Room.query.all()
    return rooms_schema.dump(rooms).data


def get_room(room_id):
    room_schema = RoomSchema()
    room = Room.query.filter(Room.id == room_id).first()
    return room_schema.dump(room).data


def get_games():
    games_schema = GameSchema(many=True)
    games = Game.query.all()
    return games_schema.dump(games).data


def get_game(game_id):
    game_schema = GameSchema()
    game = Game.query.filter(Game.id == game_id).one()
    return game_schema.dump(game).data


def get_game_players(game_id):
    players_schema = PlayerSchema(many=True)
    players = Player.query.filter(Player.game_id == game_id).all()
    return players_schema.dump(players).data


def get_round(game_id, round_number):
    # return Round.query.filter(Round.game_id == game_id, Round.round_number == round_number).one()
    round_schema = RoundSchema()
    round = Round.query.filter(Round.game_id == game_id, Round.round_number==round_number).one()
    return round_schema.dump(round).data


def get_players(game_id):
    players_schema = PlayerSchema(many=True)
    players = Player.query.filter(Player.game_id == game_id).all()
    return players_schema.dump(players).data


def get_player(game_id, player_id):
    player_schema = PlayerSchema()
    player = Player.query.filter(Player.game_id == game_id, Player.id == player_id).one()
    return player_schema.dump(player).data


def get_hand(game_id, player_id):
    return Player.query.filter(Player.game_id == game_id, Player.id == player_id).first().cards.all()


def get_discarded_white_cards(game_id):
    """

    :return:
    """
    # all cards in common game deck
    sq1 = db.session.query(WhiteGameCard.card_id).filter(WhiteGameCard.game_id == game_id)
    # all cards currently in a pending round
    sq2 = db.session.query(RoundWhiteCard.white_card_id) \
        .join(Round) \
        .filter(Round.judge_id is None) \
        .filter(RoundWhiteCard.game_id == game_id)
    # all cards currently in a player's hand
    sq3 = db.session.query(PlayerCard.card_id).filter(PlayerCard.game_id == game_id)

    q = db.session.query(WhiteMasterCard) \
        .filter(and_(~WhiteMasterCard.id.in_(sq1), ~WhiteMasterCard.id.in_(sq2), ~WhiteMasterCard.id.in_(sq3)))
    return q


def get_in_play_white_cards(game_id):
    sq = db.session.query(WhiteMasterCard.id) \
        .join(WhiteGameCard) \
        .join(PlayerCard) \
        .filter(or_(and_(WhiteMasterCard.id == PlayerCard.card_id, PlayerCard.game_id == game_id),
                    and_(WhiteMasterCard.id == WhiteGameCard.card_id, WhiteGameCard.game_id == game_id),
                    and_(WhiteMasterCard.id == RoundWhiteCard.white_card_id, RoundWhiteCard.game_id == game_id)))
    return sq


def get_in_play_black_cards_(game_id):
    sq = db.session.query(BlackMasterCard.id) \
        .join(BlackGameCard) \
        .join(PlayerCard) \
        .filter(or_(and_(BlackMasterCard.id == PlayerCard.card_id, PlayerCard.game_id == game_id),
                    and_(BlackMasterCard.id == BlackGameCard.card_id), BlackGameCard.game_id == game_id))
    return sq


# MISC
def deal_white_cards(
        player_id,
        game_id,
        number_of_cards
):
    objects = []
    white_cards = WhiteGameCard.query.limit(number_of_cards)
    for white_card in white_cards:
        objects.append(PlayerCard(player_id=player_id, game_id=game_id, card_id=white_card.card_id))
    db.session.bulk_save_objects(objects)
    db.session.commit()

    for obj in objects:
        db.session.query(WhiteGameCard).filter(WhiteGameCard.card_id == obj.card_id).delete()
    db.session.commit()


def declare_round_winner(
        game_id,
        round_number,
        winner_id
):
    round = Round.query.filter(Round.game_id == game_id, Round.round_number == round_number).one()

    if round.judge_id == winner_id:
        raise Exception('Round judge cannot be winner.')

    round.winner_id = winner_id

    db.session.commit()


def initialize_black_game_deck(game_id):
    """Initializes new black card deck for a game."""

    cards = []
    black_cards = BlackMasterCard.query.all()
    for black_card in black_cards:
        cards.append(BlackGameCard(game_id=game_id, card_id=black_card.card_id))

    db.session.bulk_save_objects(cards)
    db.session.commit()


def initialize_white_game_deck(game_id):
    """Initializes new white card deck for a game."""

    cards = []
    white_cards = WhiteMasterCard.query.all()
    for white_card in white_cards:
        cards.append(WhiteGameCard(game_id=game_id, card_id=white_card.card_id))

    db.session.bulk_save_objects(cards)
    db.session.commit()


def replenish_white_deck(game_id):
    """"""

    cards = []
    discarded_cards = get_discarded_white_cards().all()
    for discarded_card in discarded_cards:
        cards.append(WhiteGameCard(game_id=game_id, card_id=discarded_card.id))

    db.session.bulk_save_objects(cards)
    db.session.commit()


def replenish_black_deck(game_id):
    """

    :return:
    """

    cards = []
    discarded_cards = BlackMasterCard.query.filter(~BlackMasterCard.id.in_(BlackGameCard.query.all()))
    for discarded_card in discarded_cards:
        cards.append(BlackGameCard(game_id=game_id, card_id=discarded_card.id))

    db.session.bulk_save_objects(cards)
    db.session.commit()


# def initialize_black_game_deck(game_id):
#     """Initializes new white card deck for a game."""
#     black_cards = BlackMasterCard.query.all()
#     for black_card in black_cards:
#         db.session.add(
#             BlackGameCard(game_id=game_id, card_id=black_card.card_id)
#         )
#
#     db.session.commit()


def play_white_card(
        game_id,
        round_id,
        player_id,
        card_id,
        pick_num
):
    """Check if card is already in play for this round."""
    rwp = RoundWhiteCard.query.filter(
        RoundWhiteCard.game_id == game_id,
        RoundWhiteCard.round_id == round_id,
        RoundWhiteCard.player_id == player_id,
        RoundWhiteCard.white_card_id == card_id,
        RoundWhiteCard.pick_num == pick_num
    ).first()

    """If card is in play throw exception."""
    if rwp is not None:
        print(rwp)
        raise Exception()

    round = Round.query.filter(Round.game_id == game_id, Round.id == round_id)

    """Else play the card for this round."""
    rwp = RoundWhiteCard(
        game_id=game_id,
        round_id=round_id,
        player_id=player_id,
        white_card_id=card_id,
        pick_num=pick_num)

    db.session.add(rwp)
    db.session.commit()

    """Remove played card from player's hand"""
    db.session.query(PlayerCard).filter(
        PlayerCard.game_id == game_id,
        PlayerCard.player_id == player_id,
        PlayerCard.card_id == card_id
    ).delete()
    p = db.session.query(Player).filter(Player.id == player_id).one().cards
    db.session.commit()


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
