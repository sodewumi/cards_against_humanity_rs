from Crypto.Hash import SHA256
from flask import Flask, flash, jsonify, redirect, render_template, url_for, request, session

from app import app, requires_login
from helpers import forms
from logic import create_new_user, get_all_usernames, get_user_by_username, get_user_by_email
from logic import create_new_room, create_new_game, create_new_player, get_user_id_by_username

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
@requires_login
def create_room():

    create_room_form = forms.CreateRoomForm()

    return render_template(
        'create_room.html',
        create_room_form=create_room_form,
    )

@app.route('/create_room', methods=['Post'])
def create_room_post():
    room_name = request.form['room_name']
    players = request.form['players'].split(',')

    room_id = create_new_room(room_name)
    game_id = create_new_game(room_id)

    for player in players:
        create_new_player(
            user_id=get_user_id_by_username(player),
            name=player,
            game_id=game_id,
        )

    return "Hello World"

@app.route('/player_list', methods=['Get'])
def get_player_list():
    player_list = []
    for player in get_all_usernames():
        player_list.append({'value': player[0]})

    return jsonify({'foo': player_list})
