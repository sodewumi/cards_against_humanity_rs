from flask_sqlalchemy import SQLAlchemy
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
from models import Round_White_Card
# from models import RoundPlayer
from models import User
from models import WhiteMasterCard
from models import WhiteGameCard
from seed import connect_to_db
from app import app

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

def get_user_by_username(username):
    return User.query.filter(
        User.username == username
    ).first()

def get_user_by_email(email):
    return User.query.filter(
        User.email == email
    ).first()


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
    # all cards in common game deck
    sq1 = db.session.query(WhiteGameCard.card_id)
    # all cards currently in a pending round
    sq2 = db.session.query(Round_White_Card.white_card_id).join(Round).filter(Round.winner_id is None)
    # all cards currently in a player's hand
    sq3 = db.session.query(PlayerCard.card_id)

    q = db.session.query(WhiteMasterCard) \
        .filter(and_(~WhiteMasterCard.id.in_(sq1), ~WhiteMasterCard.id.in_(sq2), ~WhiteMasterCard.id.in_(sq3)))
    return q


def get_in_play_white_cards():
    sq = db.session.query(WhiteMasterCard.id) \
        .join(WhiteGameCard) \
        .join(PlayerCard) \
        .filter(or_(WhiteMasterCard.id == PlayerCard.card_id, WhiteMasterCard.id == WhiteGameCard.card_id))
    return sq


def get_in_play_black_cards_():
    sq = db.session.query(BlackMasterCard.id) \
        .join(BlackGameCard) \
        .join(PlayerCard) \
        .filter(or_(BlackMasterCard.id == PlayerCard.card_id, BlackMasterCard.id == BlackGameCard.card_id))
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
        round_num,
        winner_id
):
    round = Round.query.filter(Round.game_id == game_id, Round.round_number == round_num).one()

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


def initialize_black_game_deck(game_id):
    """Initializes new white card deck for a game."""
    black_cards = BlackMasterCard.query.all()
    for black_card in black_cards:
        db.session.add(
            BlackGameCard(game_id=game_id, card_id=black_card.card_id)
        )

    db.session.commit()


def play_white_card(
        game_id,
        round_id,
        player_id,
        card_id,
        pick_num
):
    """Check if card is already in play for this round."""
    rwp = Round_White_Card.query.filter(
        Round_White_Card.game_id == game_id,
        Round_White_Card.round_id == round_id,
        Round_White_Card.player_id == player_id,
        Round_White_Card.white_card_id == card_id,
        Round_White_Card.pick_num == pick_num
    ).first()

    """If card is in play throw exception."""
    if rwp is not None:
        print(rwp)
        raise Exception()

    round = Round.query.filter(Round.game_id == game_id, Round.id == round_id)

    """Else play the card for this round."""
    rwp = Round_White_Card(
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

