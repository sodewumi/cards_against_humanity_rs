# # from flask_wtf import Form
# from wtforms import Form
# from wtforms import StringField, PasswordField, TextField, validators


# class LoginForm(Form):
#     username = TextField('Username', [validators.input_required()])
#     password = PasswordField('Password', [validators.input_required()])


# class RegisterForm(Form):
#     username = StringField(
#         'Username',
#         [validators.Length(min=4, max=25)]
#     )
#     email = StringField(
#         'Email Address',
#         [validators.Length(min=6, max=35)]
#     )
#     password = PasswordField(
#         'Password',
#         [validators.input_required()]
#     )

from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)