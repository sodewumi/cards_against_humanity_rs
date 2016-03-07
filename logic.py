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


# GET
def get_game_players(
        game_id
):
    return Player.query.filter(Player.game_id == game_id).all()
