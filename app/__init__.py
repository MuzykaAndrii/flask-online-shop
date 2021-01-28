from flask import Flask, Markup
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_ckeditor import CKEditor, CKEditorField
from flask_marshmallow import Marshmallow
from wtforms import PasswordField
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object('config')
app.jinja_env.filters['markup'] = Markup
db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
mail = Mail(app)

login = LoginManager(app)
login.login_view = 'login'
login.sesion_protection = 'strong'
login.login_message_category = 'info'

from app.products.blueprint import products
app.register_blueprint(products, url_prefix='/shop')

from app.auth.blueprint import auth
app.register_blueprint(auth, url_prefix='/auth')

from app import views
from app.models import *

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_admin()

class ProductsModelView(ModelView):
    form_excluded_columns = ('date_posted', 'views')

    def is_accessible(self):
        return current_user.is_admin()

class UserModelView(ModelView):

    #exclude pass field and other
    form_excluded_columns = ('password', 'image_file', 'last_seen')

    #add additionally pass field
    form_extra_fields = {
        'password2': PasswordField('Password')
    }

    #IMPORTANT! 2 rules under just rearrange fields in forms, not exclude him
    form_create_rules = ['username', 'email', 'password2', 'about_me', 'admin', 'products']
    form_edit_rules  = ['username', 'email', 'password2', 'about_me', 'admin', 'products']


    def on_model_change(self, form, model, is_created):
        if form.password2.data:
            model.hash_password(form.password2.data)
        return super(UserModelView, self).on_model_change(form, model, is_created)
    
    
    def is_accessible(self):
        return current_user.is_admin()


admin = Admin(app, index_view=MyAdminIndexView())
admin.add_view(UserModelView(User, db.session))
admin.add_view(ProductsModelView(Product, db.session))

