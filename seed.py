import os
import json

from flask_sqlalchemy import SQLAlchemy
from flask import Flask

from models import *


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
    db.drop_all()


def seed_card_data():
    """

    :return:
    """

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
    """seed initial database records for testing"""
    p1 = Player(name='Randall')
    db.session.add(p1)
    p2 = Player(name='Stella')
    db.session.add(p1)
    p2 = Player(name='Robot1')
    db.session.add(p3)
    p2 = Player(name='Robot2')
    db.session.add(p4)

    h1 = Hand()
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