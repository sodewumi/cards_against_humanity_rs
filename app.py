from flask import Flask, flash, request, url_for, redirect, session
from flask.ext.login import LoginManager, UserMixin, login_user, logout_user
from functools import wraps

from models import connect_to_db, User

app = Flask(__name__)
app.secret_key = "public for now"
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

connect_to_db(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

def requires_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            flash('login required')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function
