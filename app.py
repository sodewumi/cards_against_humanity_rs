from flask import Flask
from flask.ext.login import LoginManager, UserMixin, current_user, login_user, logout_user

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

