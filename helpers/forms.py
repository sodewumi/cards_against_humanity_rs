from flask.ext.wtf import Form
from wtforms import StringField, TextField, PasswordField, BooleanField
from wtforms.validators import DataRequired
from models import User
from logic import create_new_user, get_user_by_username, get_user_by_email

class LoginForm(Form):
    username = TextField(
        'username',
        validators=[DataRequired()],
    )

    password = PasswordField(
        'password',
        validators=[DataRequired()],
    )

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = User.query.filter_by(
            username=self.username.data).first()
        if user is None:
            self.username.errors.append('Unknown username')
            return False

        if not user.check_password(self.password.data):
            self.password.errors.append('Invalid password')
            return False

        self.user = user
        return True

class RegisterForm(Form):
    username = StringField(
        'username',
        validators=[DataRequired()],
    )

    email = StringField(
        'email',
        validators=[DataRequired()],
    )

    password = PasswordField(
        'password',
        validators=[DataRequired()],
    )

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        if get_user_by_username(self.username.data):
            self.username.errors.append('Username taken')
            return False

        if get_user_by_email(self.email.data):
            self.email.errors.append('Email Taken')
            return False

        return True

class CreateRoomForm(Form):
    room_name = StringField(
        'room_name',
        validators=[DataRequired()],
    )

    players = StringField(
        'players',
        validators=[DataRequired()],
    )


    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        if self.room_name.data is None:
            self.room_name.errors.append('PLease enter room name')
            return False

        if len(self.players.data.split(',')) < 3:

            self.players.errors.append('Please enter more than two players')
            return False

        return True

