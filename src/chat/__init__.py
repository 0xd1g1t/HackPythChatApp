from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

UPLOAD_PATH = '/srv/uploads'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://chatdbuser:Heute0000@db/chatdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'b9399f21060d4b5fcb6d3cf5fea8de'
app.config['UPLOAD_PATH'] = '/srv/uploads'
app.config['SESSION_COOKIE_HTTPONLY'] = False

db = SQLAlchemy(app)

from chat import routes