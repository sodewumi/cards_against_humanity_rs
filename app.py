from flask import Flask
from flask.ext.login import LoginManager, UserMixin, current_user, login_user, logout_user

from models import connect_to_db

app = Flask(__name__)
app.secret_key = "public for now"

connect_to_db(app)

login_manager = LoginManager()
login_manager.init_app(app)