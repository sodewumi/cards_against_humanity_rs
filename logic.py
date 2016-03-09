from flask_sqlalchemy import SQLAlchemy

from models import BlackGameCard
from models import BlackMasterCard
from models import Game
from models import GamePlayer
from models import Hand
from models import Player
from models import PlayerHand
from models import Room
from models import Round
from models import RoundPlayer
from models import User
from models import WhiteMasterCard
from models import WhiteGameCard

db = SQLAlchemy()


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


def create_new_room(
        name,
):
    new_room = Room(
        name=name,
    )

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
    new_player = Player(user_id=user_id, name=name, game_id=game_id)

    db.session.add(new_player)
    db.session.commit()


def create_new_round(
        game_id,
        black_card_id,
        judge_id
):
    new_round = Round(
        game_id=game_id,
        black_card_id=black_card_id,
        judge_id=judge_id
    )

    db.session.add(new_round)
    db.session.commit()


# GET
def get_game_players(
        game_id
):
    return Player.query.filter(Player.game_id == game_id).all()


def get_discarded_white_cards():
    """

    :return:
    """
    q = db.session.query(WhiteMasterCard) \
        .filter(~WhiteMasterCard.id.in_(db.session.query(WhiteGameCard.card_id))) \
        .filter(~WhiteMasterCard.id.in_(db.session.query(Hand.card_id)))
    return q


def get_in_play_white_cards():
    sq = db.session.query(WhiteMasterCard.id) \
        .join(WhiteGameCard) \
        .join(Hand) \
        .filter(or_(WhiteMasterCard.id == Hand.card_id, WhiteMasterCard.id == WhiteGameCard.card_id))
    return sq


def get_in_play_black_cards_():
    sq = db.session.query(BlackMasterCard.id) \
        .join(BlackGameCard) \
        .join(Hand) \
        .filter(or_(BlackMasterCard.id == Hand.card_id, BlackMasterCard.id == BlackGameCard.card_id))
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
        objects.append(Hand(player_id=player_id, game_id=game_id, card_id=white_card.id))
    db.session.bulk_save_objects(objects)
    db.session.commit()

    for obj in objects:
        db.session.query(WhiteGameCard).filter(WhiteGameCard.id == obj.card_id).delete()
    db.session.commit()


def declare_round_winner(
        game_id,
        round_num,
        winner_id
):
    round = Round.query.filter(Round.game_id == game_id, Round.round_number == round_num)
    round.winner_id = winner_id

    db.session.commit()


def initialize_black_game_deck(game_id):
    """Initializes new black card deck for a game."""

    cards = []
    black_cards = BlackMasterCard.query.all()
    for black_card in black_cards:
        cards.append(BlackGameCard(game_id=game_id, card_id=black_card.id))

    db.session.bulk_save_objects(cards)
    db.session.commit()


def initialize_white_game_deck(game_id):
    """Initializes new white card deck for a game."""

    cards = []
    white_cards = WhiteMasterCard.query.all()
    for white_card in white_cards:
        cards.append(WhiteGameCard(game_id=game_id, card_id=white_card.id))

    db.session.bulk_save_objects(cards)
    db.session.commit()


def replenish_white_deck(game_id):
    """"""

    cards = []
    discarded_cards = WhiteMasterCard.query.filter(~WhiteMasterCard.id.in_(WhiteGameCard.query.all()))
    for discarded_card in discarded_cards:
        cards.append(WhiteGameCard(game_id=game_id, card_id=discarded_card.id))

    db.session.bulk_save_objects(cards)
    db.session.commit()


def replenish_black_deck(game_id):
    """"""

    cards = []
    discarded_cards = BlackMasterCard.query.filter(~BlackMasterCard.id.in_(BlackGameCard.query.all()))
    for discarded_card in discarded_cards:
        cards.append(BlackGameCard(game_id=game_id, card_id=discarded_card.id))

    db.session.bulk_save_objects(cards)
    db.session.commit()


def initialize_black_game_deck(game_id):
    """Initializes new white card deck for a game."""
    black_cards = BlackMasterCard.query.all()
    for black_card in black_cards:
        db.session.add(
            BlackGameCard(game_id=game_id, card_id=black_card.id)
        )

    db.session.commit()
