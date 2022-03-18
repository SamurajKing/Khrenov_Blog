# coding=utf-8
from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
socket_io = SocketIO(app, cors_allowed_origins='*')
db = SQLAlchemy(app)
login_manager = LoginManager(app)

from app import routes, models 
