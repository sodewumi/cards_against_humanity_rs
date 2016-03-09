from models import BlackGameDeck
from models import BlackMasterDeck
from models import Game
from models import GamePlayer
from models import Hand
from models import Player
from models import PlayerHand
from models import Room
from models import Round
from models import RoundPlayer
from models import User
from models import WhiteMasterDeck
from models import WhiteGameDeck
from models import db


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
		room_id = room_id,
	)

	db.session.add(new_game)
	db.session.commit()

def create_new_hand(
	player_id,
	game_id,
):

def get_player_hand():

def initialize_white_game_deck():
    white_cards = WhiteMasterCard.query.all()
    for white_card in white_cards:
        db.session.add(WhiteGameCard(card_id=white_card.id))

    db.session.commit()

def initalize_black_game_deck():
    black_cards = BlackMasterCard.query.all()
    for black_card in black_cards:
        db.session.add(BlackGameCard(card_id=black_card.id))

    db.session.commit()
