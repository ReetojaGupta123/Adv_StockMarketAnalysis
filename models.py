from . import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    cash_balance = db.Column(db.Numeric(12, 2), default=10000)

class Holding(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    symbol = db.Column(db.String(10), nullable=False)
    quantity = db.Column(db.Numeric(12, 4), nullable=False)
    avg_price = db.Column(db.Numeric(12, 4), nullable=False)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    symbol = db.Column(db.String(10), nullable=False)
    side = db.Column(db.String(4), nullable=False)  # BUY/SELL
    quantity = db.Column(db.Numeric(12, 4), nullable=False)
    price = db.Column(db.Numeric(12, 4), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
