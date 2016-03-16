from flask.ext.wtf import Form
from wtforms import StringField, TextField, PasswordField, BooleanField
from wtforms.validators import DataRequired
from models import User
from logic import create_new_user, get_user_by_username, get_user_by_email

class LoginForm(Form):
    username = TextField('username',  validators=[DataRequired()])
    password = PasswordField('password',  validators=[DataRequired()])

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

        # if not user.check_password(self.password.data):
        #     self.password.errors.append('Invalid password')
        #     return False

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

    # user = User.query.filter_by(
    #     username=self.username.data).first()

    # if user is None:
    #     self.username.errors.append('Unknown username')
    #     return False

    # if user is None:
    #     self.username.errors.append('Unknown username')
    #     return False

    # if not user.check_password(self.password.data):
    #     self.password.errors.append('Invalid password')
    #     return False

    # self.user = user
    # return True