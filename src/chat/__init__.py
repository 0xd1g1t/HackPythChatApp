from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

UPLOAD_PATH = '/srv/uploads'

app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["10 per minute"]
)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://chatdbuser:Heute0000@db/chatdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'b9399f21060d4b5fcb6d3cf5fea8de'
app.config['UPLOAD_PATH'] = '/srv/uploads'
app.config['SESSION_COOKIE_HTTPONLY'] = False

db = SQLAlchemy(app)

from chat import routes