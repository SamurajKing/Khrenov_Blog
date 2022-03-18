# coding=utf-8
from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.Integer, default=0)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)  
    posts = db.relationship('Post', backref='author', lazy='dynamic') 
    roleColor = db.Column(db.String(64), default="orange")
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    messages = db.relationship('Message', backref='author', lazy='dynamic')

    def set_password(self, password):  
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User %r>" % self.id


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)  
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    user_id = db.Column(db.Integer, ForeignKey(User.id))
    is_pinned = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return "<Post %r>" % self.id


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)
    post_id = db.Column(db.Integer, ForeignKey(Post.id))
    user_id = db.Column(db.Integer, ForeignKey(User.id))

    def __repr__(self):
        return "<Comment %r>" % self.id


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False) 
    user_id = db.Column(db.Integer, ForeignKey(User.id))
