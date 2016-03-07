import flask.ext.login as flask_login

from flask.ext.login import LoginManager, UserMixin, current_user, login_user, logout_user

login_manager = flask_login.LoginManager()
login_manager.init_app(app)
users = {'foo@bar.tld': {'pw': 'secret'}}

class User(flask_login.UserMixin):
    def __init__(self, username):
            self.id = username

def check_auth():
    user_object = users.get('foo@bar.tld')

    if user_object:
        if user_object['pw'] == password:
            return True
        else:
            return False
    return False


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    return User(username)


# @login_manager.request_loader
# def request_loader(request):
#     email = request.form.get('email')
#     if email not in users:
#         return

#     user = User()
#     user.id = email

#     # DO NOT ever store passwords in plaintext and always compare password
#     # hashes using constant-time comparison!
#     user.is_authenticated = request.form['pw'] == users[email]['pw']

#     return user