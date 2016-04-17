from app import app
from app.helpers import forms
from flask import abort
from flask import flash, jsonify, redirect, render_template, url_for, request, session
from flask import make_response
from logic import create_new_round
from logic import get_game, get_games, get_round, get_player, get_rounds
from logic import get_game_players, get_black_game_cards, get_black_master_cards, get_black_master_card, \
    get_player_cards, get_rooms, get_room, get_white_master_cards, get_white_master_card
from logic import get_users, get_user_by_id
from logic import play_white_card, declare_round_winner, replenish_white_deck, replenish_black_deck
from models import *
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.wrappers import Response


@app.route('/cah/api/v1.0/users', methods=['GET'])
def _get_users():
    try:
        users = get_users()
    except NoResultFound:
        abort(404)
    return jsonify({'users': users})


@app.route('/cah/api/v1.0/users/<int:_id>', methods=['GET'])
def _get_user_by_id(_id):
    try:
        user = get_user_by_id(_id=_id)
    except NoResultFound:
        abort(404)

    return jsonify({'user': user})


@app.route('/cah/api/v1.0/rooms', methods=['GET'])
def _get_rooms():
    try:
        rooms = get_rooms()
    except NoResultFound:
        abort(404)

    return jsonify({'rooms': rooms})


@app.route('/cah/api/v1.0/rooms/<int:room_id>', methods=['GET'])
def _get_room(room_id):
    try:
        room = get_room(room_id=room_id)
    except NoResultFound:
        abort(404)

    return jsonify({'room': room})


@app.route('/cah/api/v1.0/users/<string:user_name>', methods=['GET'])
def _get_user(user_name):
    try:
        user = get_user_by_username(user_name=user_name)
    except NoResultFound:
        abort(404)

    return jsonify({'user': user})


@app.route('/cah/api/v1.0/users/<string:email>', methods=['GET'])
def _get_user_by_email(email):
    try:
        user = get_user_by_email(email=email)
    except NoResultFound:
        abort(404)

    return jsonify({'user': user})


@app.route('/cah/api/v1.0/games', methods=['GET'])
def _get_games():
    try:
        games = get_games()
    except NoResultFound:
        abort(404)

    return jsonify({'games': games}), 201, {'Content-Type': 'application/json'}


@app.route('/cah/api/v1.0/games/<int:game_id>', methods=['GET'])
def _get_game(game_id):
    try:
        game = get_game(game_id)
    except NoResultFound:
        abort(404)

    return jsonify({'game': game})


@app.route('/cah/api/v1.0/games/<int:game_id>/rounds/<int:round_number>', methods=['GET'])
def _get_round(game_id, round_number):
    try:
        round = get_round(game_id, round_number)
    except NoResultFound:
        abort(404)
    return jsonify({'round': round})


@app.route('/cah/api/v1.0/games/<int:id>/rounds', methods=['GET'])
def _get_rounds(id):
    try:
        rounds = get_rounds(id)
    except NoResultFound:
        abort(404)
    return jsonify({'rounds': rounds})


@app.route('/cah/api/v1.0/games/<int:id>/players', methods=['GET'])
def _get_game_players(id):
    try:
        players = get_game_players(id)
    except NoResultFound:
        abort(404)

    return jsonify({'players': players})


@app.route('/cah/api/v1.0/games/<int:game_id>/players/<int:player_id>', methods=['GET'])
def _get_player(game_id, player_id):
    try:
        player = get_player(game_id, player_id)
    except NoResultFound:
        abort(404)

    return jsonify({'player': player}), 201, {'Content-Type': 'application/json'}


@app.route('/cah/api/v1.0/games/<int:game_id>/players/<int:player_id>/cards', methods=['GET'])
def _get_player_cards(game_id, player_id):
    try:
        cards = get_player_cards(game_id, player_id)
    except NoResultFound:
        abort(404)

    return jsonify({'cards': cards}), 201, {'Content-Type': 'application/json'}


@app.route('/cah/api/v1.0/black_master_cards', methods=['GET'])
def _get_black_master_cards():
    try:
        black_master_cards = get_black_master_cards()
    except NoResultFound:
        abort(404)

    return jsonify({'black_master_cards': black_master_cards})


@app.route('/cah/api/v1.0/black_master_card/<int:id>', methods=['GET'])
def _get_black_master_card(id):
    try:
        black_master_card = get_black_master_card(id)
    except NoResultFound:
        abort(404)

    return jsonify({'black_master_card': black_master_card})


@app.route('/cah/api/v1.0/white_master_cards', methods=['GET'])
def _get_white_master_cards():
    try:
        white_master_cards = get_white_master_cards()
    except NoResultFound:
        abort(404)

    return jsonify({'white_master_cards': white_master_cards})


@app.route('/cah/api/v1.0/white_master_card/<int:id>', methods=['GET'])
def _get_white_master_card(id):
    try:
        white_master_card = get_white_master_card(id)
    except NoResultFound:
        abort(404)

    return jsonify({'white_master_card': white_master_card})


@app.route('/cah/api/v1.0/games/<int:game_id>/black_game_cards', methods=['GET'])
def _get_black_game_cards(game_id):
    try:
        black_cards = get_black_game_cards(game_id)
    except NoResultFound:
        abort(404)

    return jsonify({'black_cards': black_cards})


class MyResponse(Response):
    @classmethod
    def force_type(cls, rv, environ=None):
        if isinstance(rv, dict):
            rv = jsonify(rv)
        return super(MyResponse, cls).force_type(rv, environ)


@app.route('/cah/api/v1.0/rooms/<string:name>/create', methods=['POST'])
def _create_room(name):
    room_id = create_new_room(name=name)
    room = get_room(room_id=room_id)
    if room is None:
        abort(404)
    return jsonify({'room': room})


@app.route('/cah/api/v1.0/rooms/<int:room_id>/games/create', methods=['POST'])
def _create_game(room_id):
    if not request.json or not 'title' in request.json:
        abort(400)
    game_id = create_new_game(room_id=room_id)
    game = get_game(game_id=game_id)
    if game is None:
        abort(404)
    return jsonify({'game': game}), 201


@app.route('/cah/api/v1.0/games/<int:game_id>/users/<int:user_id>/players/<string:name>/create', methods=['POST'])
def _create_player(user_id, name, game_id):
    player_id = create_new_player(user_id=user_id, name=name, game_id=game_id)
    player = get_player(game_id=game_id)
    if player is None:
        abort(404)
    return jsonify({'player': player})


@app.route('/cah/api/v1.0/games/<int:game_id>/judge/<int:judge_id>/create', methods=['POST'])
def _create_round(game_id, judge_id):
    round_number = create_new_round(game_id=game_id, judge_id=judge_id)
    _round = get_round(game_id=game_id, round_number=round_number)
    if round is None:
        abort(404)
    return jsonify({'round': _round})


@app.route('/cah/api/v1.0/games/<int:game_id>/rounds/<int:round_number>/players/'
           '<int:player_id>/card/<int:card_id>/pick_num/<int:pick_num>/play',
           methods=['POST', 'PUT'])
def _play_card(game_id, round_number, player_id, card_id, pick_num):
    try:
        play_white_card(game_id, round_number, player_id, card_id, pick_num)
    except:
        abort(404)

    _round = get_round(game_id=game_id, round_number=round_number)
    return jsonify({'round': _round})


@app.route('/cah/api/v1.0/games/<int:game_id>/players/<int:player_id>/number_of_cards/<int:number_of_cards>/deal',
           methods=['POST', 'PUT'])
def _deal_white_cards(game_id, player_id, number_of_cards):
    try:
        deal_white_cards(player_id=player_id, game_id=game_id, number_of_cards=number_of_cards)
    except:
        abort(404)

    hand = get_player_cards(game_id=game_id, player_no=player_id)
    return jsonify({'hand': hand})


@app.route(
    '/cah/api/v1.0/games/<int:game_id>/rounds/<int:round_number>/winner/<int:winner_id>',
    methods=['POST', 'PUT'])
def _declare_round_winner(game_id, round_number, winner_id):
    try:
        declare_round_winner(game_id=game_id, round_number=round_number, winner_id=winner_id)
    except:
        abort(404)

    round = get_round(game_id=game_id, round_number=round_number)
    return jsonify({'round': round})


@app.route(
    '/cah/api/v1.0/games/<int:game_id>/replenish_white_deck',
    methods=['POST', 'PUT'])
def _replenish_white_deck(game_id):
    try:
        replenish_white_deck(game_id=game_id)
    except:
        abort(404)

    white_game_cards = get_white_game_cards(game_id=game_id)
    return jsonify({'round': round})


@app.route(
    '/cah/api/v1.0/games/<int:game_id>/replenish_black_deck',
    methods=['POST', 'PUT'])
def _replenish_black_deck(game_id):
    try:
        replenish_black_deck(game_id=game_id)
    except:
        abort(404)

    black_game_cards = get_black_game_cards(game_id=game_id)
    return jsonify({'black_game_cards': black_game_cards})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


from logic import create_new_user, get_all_usernames, get_user_by_username, get_user_by_email
from logic import create_new_room, create_new_game, create_new_player
from logic import deal_white_cards


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['Get', 'Post'])
def login():
    login_form = forms.LoginForm()

    if login_form.validate_on_submit():
        flash(u'Successfully logged in as %s' % login_form.user.username)
        session['user_id'] = login_form.user.id
        return redirect(url_for('create_room'))
    return render_template(
        'login.html',
        login_form=login_form,
    )


@app.route('/register', methods=['Get'])
def register():
    """Registers User"""

    register_form = forms.RegisterForm()

    return render_template(
        'register.html',
        register_form=register_form,
    )


@app.route('/register', methods=['Post'])
def register_post():
    register_form = forms.RegisterForm()

    if register_form.validate_on_submit():
        register_email = request.form['email']
        register_password = request.form['password']
        register_username = request.form['username']

        register_password_hashed = SHA256.new(register_password.encode('utf-8')).hexdigest()

        create_new_user(
            email=register_email,
            password=register_password_hashed,
            username=register_username,
        )
        flash('Thanks for creating an account! Please sign in')
        return redirect('/login')
    else:
        return render_template(
            'register.html',
            register_form=register_form,
        )


@app.route('/logout')
def logout_user():
    """Remove login information from session"""
    session.pop('user_id')
    flash("You've successfully logged out. Goodbye.")
    return redirect("/")


@app.route('/create_room', methods=['Get'])
# @requires_login
def create_room():
    create_room_form = forms.CreateRoomForm()

    return render_template(
        'create_room.html',
        create_room_form=create_room_form,
    )


@app.route('/player_list', methods=['Get'])
def get_player_list():
    player_list = []
    for player in get_all_usernames():
        player_list.append({'value': player[0]})

    return jsonify({'foo': player_list})


@app.route('/create_room', methods=['Post'])
def create_room_post():
    # room_name = request.form['room_name']
    # players = request.form['players'].split(',')

    # room_id = create_new_room(room_name)
    # game_id = create_new_game(room_id)

    # for player in players:
    #     create_new_player(
    #         user_id=get_user_id_by_username(player),
    #         name=player,
    #         game_id=game_id,
    #     )

    # remove later
    from models import Player
    player1 = Player.query.filter(Player.id == 1).one()
    player2 = Player.query.filter(Player.id == 2).one()
    player3 = Player.query.filter(Player.id == 3).one()
    player4 = Player.query.filter(Player.id == 4).one()

    players = [player1, player2, player3, player4]

    deal_white_cards(player1.id, 1, 10)
    deal_white_cards(player2.id, 1, 10)
    deal_white_cards(player3.id, 1, 10)
    deal_white_cards(player4.id, 1, 10)

    # session['player_data'] = {}
    # for i, player in enumerate(players):
    #     print(session, "############")
    #     session['player_data'][player.name] = session['player_data'].get(player.id, player.cards.all())

    return redirect(url_for('game_room'))


def enabled_categories():
    from models import PlayerCard
    print(PlayerCard.query.filter(PlayerCard.card_id < 11).all(), "####################")
    return PlayerCard.query.filter(PlayerCard.card_id < 11).all()


@app.route('/game_room')
def game_room():
    from models import Player
    player1 = Player.query.filter(Player.id == 1).one()
    player2 = Player.query.filter(Player.id == 2).one()
    player3 = Player.query.filter(Player.id == 3).one()
    player4 = Player.query.filter(Player.id == 4).one()

    players = [player1, player2, player3, player4]

    players_card_choice_form = forms.PlayersCardChoiceForm(obj=player1)
    # players_card_choice_form.my_field.choices = enabled_categories()

    return render_template(
        "game.html",
        players=players,
        players_card_choice_form=players_card_choice_form,
    )


@app.route('/play_hand', methods=['Post'])
def play_hand():
    pass
