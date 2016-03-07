from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from models import *

import os

db = SQLAlchemy()


def drop_db():
    """Connect the database to our Flask app."""
    from app import app
    if os.environ.get('DATABSE_URL') is None:
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

    :return:
    """
    import os, json
    with open('static/cards.json') as data_file:
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


def initialize_game_decks():
    black_cards = BlackMasterCard.query.all()
    for black_card in black_cards:
        db.session.add(BlackGameCard(card_id=black_card.id))

    white_cards = WhiteMasterCard.query.all()
    for white_card in white_cards:
        db.session.add(WhiteGameCard(card_id=white_card.id))

    db.session.commit()


def seed_db_data():
    game = Game()
    db.session.add(game)
    db.session.commit()

    g = Game.query.first()

    """seed initial database records for testing"""
    p1 = Player(name='Randall', game_id=g.id)
    db.session.add(p1)
    p2 = Player(name='Stella', game_id=g.id)
    db.session.add(p2)
    p3 = Player(name='Robot1', game_id=g.id)
    db.session.add(p3)
    p4 = Player(name='Robot2', game_id=g.id)
    db.session.add(p4)
    db.session.commit()

    p1 = Player.query.filter(Player.name == 'Randall').one()
    p2 = Player.query.filter(Player.name == 'Stella').one()
    p3 = Player.query.filter(Player.name == 'Robot1').one()
    p4 = Player.query.filter(Player.name == 'Robot2').one()

    h1 = Hand(player_id=p1.id, game_id=game.id)
    db.session.add(h1)
    h2 = Hand(player_id=p2.id, game_id=game.id)
    db.session.add(h2)
    h3 = Hand(player_id=p3.id, game_id=game.id)
    db.session.add(h3)
    h4 = Hand(player_id=p4.id, game_id=game.id)
    db.session.add(h4)
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
