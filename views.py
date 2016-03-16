from flask import Flask, flash, redirect, render_template, url_for, request, session

from app import app
from helpers import forms
from logic import create_new_user, get_user_by_username, get_user_by_email

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/login', methods=['Get', 'Post'])
def login():
    login_form = forms.LoginForm()
    # register_form = forms.RegisterForm()

    if login_form.validate_on_submit():
        flash(u'Successfully logged in as %s' % login_form.user.username)
        session['user_id'] = login_form.user.id
        return redirect(url_for('index'))
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

        if get_user_by_email(register_email):
            flash('A person has already registered with the email')
            return redirect('/')
        elif get_user_by_username(register_username):
            flash('A person has already taken that username')
            return redirect('/')
        else:
            if register_email and register_password and register_username:
                create_new_user(
                    email=register_email,
                    password=register_password,
                    username=register_username,
                )
                flash('Thanks for creating an account with Gutenberg Translate! Please sign in')
                return redirect('/')
    else:
        return render_template(
            'register.html',
            register_form=register_form,
        )

