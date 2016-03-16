from app import app
from flask import Flask, render_template, url_for, request
from helpers import forms

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = forms.LoginForm()
    register_form = forms.RegisterForm()
    return render_template(
        'login.html',
       title='Sign In',
       login_form=login_form,
       register_form=register_form
    )