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
