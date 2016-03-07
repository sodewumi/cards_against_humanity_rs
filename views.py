from app import app
from flask import Flask, render_template, url_for, request
from helpers.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', 
                           title='Sign In',
                           form=form)