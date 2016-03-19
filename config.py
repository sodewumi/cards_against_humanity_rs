import os


WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

if os.environ.get('DATABSE_URL') is None:
    SQLALCHEMY_DATABASE_URI = os.environ['LOCAL_DATABASE_URI']
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')