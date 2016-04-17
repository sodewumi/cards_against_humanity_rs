from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import and_, or_
import os

# from models import BlackGameCard
# from models import BlackMasterCard
# from models import Game
# from models import GamePlayer
# from models import models.PlayerCard
# from models import Player
# from models import models.Room
# from models import Round
# from models import models.RoundWhiteCard
# from models import models.User
# from models import WhiteMasterCard
# from models import WhiteGameCard
# from models import GameSchema, PlayerSchema, RoomSchema, models.RoundSchema, WhiteMasterCard, BlackCardSchema, models.UserSchema,\
#     PlayerCardSchema
import models
# from seed import connect_to_db
# from app import app

db = SQLAlchemy()
ma = Marshmallow()


# CREATE
def create_new_user(
        email,
        password,
        username,
):
    new_user = models.User(
        email=email,
        password=password,
        username=username
    )

    db.session.add(new_user)
    db.session.commit()


def get_user_by_username(user_name):
    user_schema = models.UserSchema()
    user = models.User.query.filter(models.User.username == user_name).one()
    return user_schema.dump(user).data


def get_user_by_email(email):
    user_schema = models.UserSchema()
    user = models.User.query.filter(models.User.email == email).one()
    return user_schema.dump(user).data


def get_user_by_id(_id):
    user_schema = models.UserSchema()
    user = models.User.query.filter(models.User.id == _id).one()
    return user_schema.dump(user).data


def get_users():
    users_schema = models.UserSchema(many=True)
    users = models.User.query.all()
    return users_schema.dump(users).data


def create_new_room(
        name,
):
    new_room = models.Room(name=name, )

    db.session.add(new_room)
    db.session.commit()
    return new_room.id


def create_new_game(
        room_id,
):
    new_game = models.Game(
        room_id=room_id,
    )

    db.session.add(new_game)
    db.session.commit()

    return new_game.id


def get_user_id_by_username(username):
    user_schema = models.UserSchema()
    user = db.session.query(
        models.User.id
    ).filter(
        models.User.username == username
    ).one()
    return user_schema.dump(user).data


def create_new_player(
        user_id,
        name,
        game_id,
):
    game = models.Game.query.filter(models.Game.id == game_id).one()
    if game is None:
        raise Exception('Game {0} does not exist.'.format(game_id))
    new_player = models.Player(user_id=user_id, name=name)
    g = game.add_player(new_player);
    db.session.commit()

    # db.session.add(new_player)
    # db.session.commit()


def create_new_round(
        game_id,
        judge_id
):
    black_card_id = models.BlackGameCard.query.first().card_id

    new_round = models.Round(
        game_id=game_id,
        black_card_id=black_card_id,
        judge_id=judge_id
    )

    db.session.add(new_round)
    db.session.commit()

    return new_round.round_number


# GET
def get_rooms():
    rooms_schema = models.RoomSchema(many=True)
    rooms = models.Room.query.all()
    return rooms_schema.dump(rooms).data


def get_room(room_id):
    room_schema = models.RoomSchema()
    room = models.Room.query.filter(models.Room.id == room_id).one()
    print('HEYYYY: ', room)
    return room_schema.dump(room).data


def get_games():
    games_schema = models.GameSchema(many=True)
    games = models.Game.query.all()
    return games_schema.dump(games).data


def get_game(game_id):
    game_schema = models.GameSchema()
    game = models.Game.query.filter(models.Game.id == game_id).one()
    return game_schema.dump(game).data


def get_game_players(game_id):
    players_schema = models.PlayerSchema(many=True)
    players = models.Player.query.filter(models.Player.game_id == game_id).all()
    return players_schema.dump(players).data


def get_black_game_cards(game_id):
    black_cards_schema = models.BlackCardSchema(many=True)
    black_cards = models.BlackGameCard.query.filter(models.BlackGameCard.game_id == game_id).all()
    return black_cards_schema.dump(black_cards).data


def get_black_master_cards():
    black_master_card_schema = models.BlackMasterCardSchema(many=True)
    black_cards = models.BlackMasterCard.query.all()
    return black_master_card_schema.dump(black_cards).data


def get_black_master_card(id):
    black_master_card_schema = models.BlackMasterCardSchema()
    black_card = models.BlackMasterCard.query.filter(models.BlackMasterCard.id == id).one()
    return black_master_card_schema.dump(black_card).data


def get_white_master_cards():
    white_master_cards_schema = models.WhiteMasterCardSchema(many=True)
    white_cards = models.WhiteMasterCard.query.all()
    return white_master_cards_schema.dump(white_cards).data


def get_white_master_card(id):
    white_master_card_schema = models.WhiteMasterCardSchema()
    white_card = models.WhiteMasterCard.query.filter(models.WhiteMasterCard.id == id).one()
    return white_master_card_schema.dump(white_card).data


def get_round(game_id, round_number):
    # return models.Round.query.filter(models.Round.game_id == game_id, models.Round.round_number == round_number).one()
    round_schema = models.RoundSchema()
    round = models.Round.query.filter(models.Round.game_id == game_id, models.Round.round_number == round_number).one()
    return round_schema.dump(round).data


def get_rounds(id):
    rounds_schema = models.RoundSchema(many=True)
    rounds = models.Round.query.filter(models.Round.game_id == id).all()
    return rounds_schema.dump(rounds).data


def get_players(game_id):
    players_schema = models.PlayerSchema(many=True)
    players = models.Player.query.filter(models.Player.game_id == game_id).all()
    return players_schema.dump(players).data


def get_player(game_id, player_no):
    player_schema = models.PlayerSchema()
    player = models.Player.query.filter(models.Player.game_id == game_id, models.Player.player_no == player_no).one()
    return player_schema.dump(player).data


def get_player_cards(game_id, player_no):
    print('game_id:', game_id)
    print('player_no: ', player_no)
    player_cards_schema = models.PlayerCardSchema(many=True)
    cards = models.PlayerCard.query.filter(models.PlayerCard.game_id == game_id,
                                           models.PlayerCard.player_id == player_no).all()
    print('cards: ', cards)
    return player_cards_schema.dump(cards).data


def get_all_usernames():
    return db.session.query(
        models.User.username
    ).order_by(
        models.User.username
    ).all()


# GET
def get_game_players(
        game_id
):
    players_schema = models.PlayerSchema(many=True)
    players = models.Player.query.filter(models.Player.game_id == game_id).all()
    return players_schema.dump(players).data


def get_discarded_white_cards(game_id):
    """

    :return:
    """
    # all cards in common game deck
    sq1 = db.session.query(models.WhiteGameCard.card_id).filter(models.WhiteGameCard.game_id == game_id)
    # all cards currently in a pending round
    sq2 = db.session.query(models.RoundWhiteCard.white_card_id) \
        .join(models.Round) \
        .filter(models.Round.judge_id is None) \
        .filter(models.RoundWhiteCard.game_id == game_id)
    # all cards currently in a player's hand
    sq3 = db.session.query(models.PlayerCard.card_id).filter(models.PlayerCard.game_id == game_id)

    q = db.session.query(models.WhiteMasterCard) \
        .filter(and_(~models.WhiteMasterCard.id.in_(sq1), ~models.WhiteMasterCard.id.in_(sq2),
                     ~models.WhiteMasterCard.id.in_(sq3)))
    return q


def get_in_play_white_cards(game_id):
    sq = db.session.query(models.WhiteMasterCard.id) \
        .join(models.WhiteGameCard) \
        .join(models.PlayerCard) \
        .filter(or_(and_(models.WhiteMasterCard.id == models.PlayerCard.card_id, models.PlayerCard.game_id == game_id),
                    and_(models.WhiteMasterCard.id == models.WhiteGameCard.card_id,
                         models.WhiteGameCard.game_id == game_id),
                    and_(models.WhiteMasterCard.id == models.RoundWhiteCard.white_card_id,
                         models.RoundWhiteCard.game_id == game_id)))
    return sq


def get_in_play_black_cards_(game_id):
    sq = db.session.query(models.BlackMasterCard.id) \
        .join(models.BlackGameCard) \
        .join(models.PlayerCard) \
        .filter(or_(and_(models.BlackMasterCard.id == models.PlayerCard.card_id, models.PlayerCard.game_id == game_id),
                    and_(models.BlackMasterCard.id == models.BlackGameCard.card_id),
                    models.BlackGameCard.game_id == game_id))
    return sq


# MISC
def deal_white_cards(
        player_id,
        game_id,
        number_of_cards,
):
    objects = []
    white_cards = models.WhiteGameCard.query.limit(number_of_cards)
    for white_card in white_cards:
        objects.append(models.PlayerCard(player_id=player_id, game_id=game_id, card_id=white_card.card_id))
    db.session.bulk_save_objects(objects)
    db.session.commit()

    for obj in objects:
        db.session.query(models.WhiteGameCard).filter(models.WhiteGameCard.card_id == obj.card_id).delete()
    db.session.commit()


def declare_round_winner(
        game_id,
        round_number,
        winner_id,
):
    round = models.Round.query.filter(models.Round.game_id == game_id, models.Round.round_number == round_number).one()

    if round.judge_id == winner_id:
        raise Exception('Round judge cannot be winner.')

    round.winner_id = winner_id

    db.session.commit()


def initialize_black_game_deck(game_id):
    """Initializes new black card deck for a game."""

    cards = []
    black_cards = models.BlackMasterCard.query.all()
    for black_card in black_cards:
        cards.append(models.BlackGameCard(game_id=game_id, card_id=black_card.card_id))

    db.session.bulk_save_objects(cards)
    db.session.commit()


def initialize_white_game_deck(game_id):
    """Initializes new white card deck for a game."""

    cards = []
    white_cards = models.WhiteMasterCard.query.all()
    for white_card in white_cards:
        cards.append(models.WhiteGameCard(game_id=game_id, card_id=white_card.card_id))

    db.session.bulk_save_objects(cards)
    db.session.commit()


def replenish_white_deck(game_id):
    """"""

    cards = []
    discarded_cards = get_discarded_white_cards().all()
    for discarded_card in discarded_cards:
        cards.append(models.WhiteGameCard(game_id=game_id, card_id=discarded_card.id))

    db.session.bulk_save_objects(cards)
    db.session.commit()


def replenish_black_deck(game_id):
    """

    :return:
    """

    cards = []
    discarded_cards = models.BlackMasterCard.query.filter(
        ~models.BlackMasterCard.id.in_(models.BlackGameCard.query.all()))
    for discarded_card in discarded_cards:
        cards.append(models.BlackGameCard(game_id=game_id, card_id=discarded_card.id))

    db.session.bulk_save_objects(cards)
    db.session.commit()


# def initialize_black_game_deck(game_id):
#     """Initializes new white card deck for a game."""
#     black_cards = models.BlackMasterCard.query.all()
#     for black_card in black_cards:
#         db.session.add(
#             models.BlackGameCard(game_id=game_id, card_id=black_card.card_id)
#         )
#
#     db.session.commit()


def play_white_card(
        game_id,
        round_id,
        player_id,
        card_id,
        pick_num,
):
    """Check if card is already in play for this round."""
    rwp = db.session.query(models.RoundWhiteCard).filter(
        models.RoundWhiteCard.game_id == game_id,
        models.RoundWhiteCard.round_id == round_id,
        models.RoundWhiteCard.player_id == player_id,
        models.RoundWhiteCard.white_card_id == card_id,
        models.RoundWhiteCard.pick_num == pick_num
    ).first()

    """If card is in play throw exception."""
    if rwp is not None:
        print(rwp)
        raise Exception()

    # round = models.Round.query.filter(models.Round.game_id == game_id, models.Round.id == round_id)

    """Else play the card for this round."""
    rwp = models.RoundWhiteCard(
        game_id=game_id,
        round_id=round_id,
        player_id=player_id,
        white_card_id=card_id,
        pick_num=pick_num)

    db.session.add(rwp)
    db.session.commit()

    """Remove played card from player's hand"""
    db.session.query(models.PlayerCard).filter(
        models.PlayerCard.game_id == game_id,
        models.PlayerCard.player_id == player_id,
        models.PlayerCard.card_id == card_id
    ).delete()
    p = db.session.query(models.Player).filter(models.Player.id == player_id).one().cards
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
