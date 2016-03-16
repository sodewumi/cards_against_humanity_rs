from flask.ext.wtf import Form
from wtforms import StringField, TextField, PasswordField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(Form):
    username = TextField('username',  validators=[DataRequired()])
    password = PasswordField('password',  validators=[DataRequired()])

class RegisterForm(Form):
    username = StringField(
        'username',
        validators=[DataRequired()],
    )
    email = StringField(
        'email_address',
        validators=[DataRequired()],
    )
    password = PasswordField(
        'password',
        validators=[DataRequired()],
    )
