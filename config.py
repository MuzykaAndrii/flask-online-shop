import os
basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
SECRET_KEY = 'SuperSecretString'

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'site.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

POSTS_PER_PAGE = 5

USERS_PICS_DIR = '/static/products_pics'