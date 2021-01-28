from . import db
from datetime import datetime as dt
from flask_login import UserMixin, current_user
from app import login
from app import bcrypt
from app import ma


@login.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(70), nullable=False)
    about_me = db.Column(db.Text, default='Hi everyone!')
    last_seen = db.Column(db.DateTime, default=dt.utcnow)
    products = db.relationship('Product', backref='seller', lazy=True)
    admin = db.Column(db.Boolean, default=0, nullable=False)

    def is_admin(self):
        return self.admin

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.hash_password(password)
    
    def hash_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, candidate):
        return bcrypt.check_password_hash(self.password, candidate)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=dt.utcnow)
    description = db.Column(db.Text, nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, default=0)
    views = db.Column(db.Integer, default=0)

    def __init__(self, title, description, user_id, price, quantity):
        self.title = title
        self.description = description
        self.seller_id = user_id
        self.price = price
        self.quantity = quantity
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def __repr__(self):
        return f"Product('{self.title}', '{self.content}', '{self.seller_id}', '{self.date_posted}')"

