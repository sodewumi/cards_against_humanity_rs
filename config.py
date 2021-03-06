import os

basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = False

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = os.environ['LOCAL_DATABASE_URI']
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')