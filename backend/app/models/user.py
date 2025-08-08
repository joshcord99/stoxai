from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class Watchlist(db.Model):
    __tablename__ = 'watchlists'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    ticker = db.Column(db.String(20), nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', back_populates='watchlist_items')
    
    __table_args__ = (db.UniqueConstraint('user_id', 'ticker', name='_user_ticker_uc'),)

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    watchlist_items = db.relationship('Watchlist', back_populates='user', cascade='all, delete-orphan')
    
    def __init__(self, email, password, first_name, last_name):
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.first_name = first_name
        self.last_name = last_name
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    def get_watchlist(self):
        return [item.ticker for item in self.watchlist_items]
    
    def add_to_watchlist(self, ticker):
        if not any(item.ticker == ticker.upper() for item in self.watchlist_items):
            watchlist_item = Watchlist(user_id=self.id, ticker=ticker.upper())
            db.session.add(watchlist_item)
            db.session.commit()
    
    def remove_from_watchlist(self, ticker):
        item = Watchlist.query.filter_by(user_id=self.id, ticker=ticker.upper()).first()
        if item:
            db.session.delete(item)
            db.session.commit()
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.get_full_name(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_active': self.is_active,
            'watchlist': self.get_watchlist()
        }
    
    def __repr__(self):
        return f'<User {self.get_full_name()}>'
