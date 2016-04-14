import os
import json

from flask_sqlalchemy import SQLAlchemy
from flask import Flask

from models import *
from sqlalchemy import and_, or_


db = SQLAlchemy()

def drop_db():
    """Connect the database to our Flask app."""
    from app import app
    if os.environ.get('DATABASE_URL') is None:
        SQLALCHEMY_DATABASE_URI = os.environ['LOCAL_DATABASE_URI']
    else:
        SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)
    # db.drop_all()
    db.engine.execute("drop schema if exists public cascade")
    db.engine.execute("create schema public")


def seed_card_data():
    """
    Seeds master decks for all games
    :return:
    """

    with open('static/js/cards.json') as data_file:
        try:
            game = json.load(data_file)
            for black_card in game['blackCards']:
                bmc = BlackMasterCard(text=black_card['text'], pick_number=int(black_card['pick']))
                db.session.add(bmc)

            for white_card in game['whiteCards']:
                wmc = WhiteMasterCard(text=white_card)
                db.session.add(wmc)

            db.session.commit()

        except Exception as e:
            raise Exception("Invalid JSON format.")


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
    discarded_cards = get_discarded_white_cards().all()
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


def seed_game_data():
    game = Game()
    db.session.add(game)
    db.session.commit()


def seed_player_hands():
    g = Game.query.first()

    p1 = Player.query.filter(Player.name == 'Randall').one()
    p2 = Player.query.filter(Player.name == 'Stella').one()
    p3 = Player.query.filter(Player.name == 'Robot1').one()
    p4 = Player.query.filter(Player.name == 'Robot2').one()

    h1 = PlayerCard(player_id=p1.id, game_id=g.id)
    db.session.add(h1)
    h2 = PlayerCard(player_id=p2.id, game_id=g.id)
    db.session.add(h2)
    h3 = PlayerCard(player_id=p3.id, game_id=g.id)
    db.session.add(h3)
    h4 = PlayerCard(player_id=p4.id, game_id=g.id)
    db.session.add(h4)
    db.session.commit()


def seed_players():
    """seed dummy players for testing"""
    g = db.session.query(Game).first()

    # p1 = Player(name='Randall', user_id=1, game_id=g.id, player_no=1)
    # db.session.add(p1)
    # p2 = Player(name='Stella', user_id=2, game_id=g.id, player_no=2)
    # db.session.add(p2)
    # p3 = Player(name='Robot1', user_id=3, game_id=g.id, player_no=3)
    # db.session.add(p3)
    # p4 = Player(name='Robot2', user_id=4, game_id=g.id, player_no=4)
    # db.session.add(p4)

    p1 = Player(name='Randall', user_id=1, player_no=1)
    p2 = Player(name='Stella', user_id=2, player_no=2)
    p3 = Player(name='Robot1', user_id=3, player_no=3)
    p4 = Player(name='Robot2', user_id=4, player_no=4)

    g = g.add_player(p1)
    g = g.add_player(p2)
    g = g.add_player(p3)
    g = g.add_player(p4)

    db.session.commit()


def seed_round(
):
    """Seed a new round for testing purposes"""

    new_round = Round(
        game_id=Game.query.first().id,
        round_number=1,
        black_card_id=BlackGameCard.query.first().card_id,
        judge_id=Player.query.first().id
    )

    db.session.add(new_round)
    db.session.commit()


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


def seed_user_data():
    u1 = User(
        email='randall@you.com',
        username='randall',
        password=SHA256.new('12345'.encode('utf-8')).hexdigest(),
    )
    db.session.add(u1)
    u2 = User(
        email='stella@you.com',
        username='stella',
        password=SHA256.new('12345'.encode('utf-8')).hexdigest(),
    )
    db.session.add(u2)
    u3 =  User(
        email='robo1@you.com',
        username='robo1',
        password=SHA256.new('12345'.encode('utf-8')).hexdigest(),
    )
    db.session.add(u3)
    u4 = User(
        email='robo2@you.com',
        username='robo2',
        password=SHA256.new('12345'.encode('utf-8')).hexdigest(),
    )
    db.session.add(u4)
    db.session.commit()


def setup_for_testing():
    """Run this first to set up everything for testing"""

    seed_user_data()
    seed_game_data()
    seed_card_data()
    initialize_black_game_deck(game_id=1)
    initialize_white_game_deck(game_id=1)
    seed_players()
    seed_round()


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
        .join(RoundWhiteCard) \
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
                    and_(BlackMasterCard.id == BlackGameCard.card_id, BlackGameCard.game_id == game_id)))
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


def connect_to_db(app):
    """Connect the database to our Flask app."""
    if os.environ.get('DATABASE_URL') is None:
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
    from models import *
    connect_to_db(app)
