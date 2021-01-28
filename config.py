import os
basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
SECRET_KEY = 'SuperSecretString'

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'site.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

POSTS_PER_PAGE = 6

PRODUCTS_PICS_DIR = '/static/products_pics'
USERS_PICS_DIR = '/static/profile_pics'

##### EMAIL CONF
DEBUG = True
TESTING = False
MAIL_SERVER = 'localhost'
MAIL_PORT = 8080
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'andrymyzik@i.ua'
MAIL_PASSWORD = 'some pass'
MAIL_DEFAULT_SENDER = 'andrymyzik@i.ua'
MAIL_MAX_EMAILS = None
#MAIL_SUPPRESS_SEND = False
MAIL_ASCII_ATTACHMENTS = False