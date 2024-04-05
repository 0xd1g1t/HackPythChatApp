from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://chatadm:Heute0000@localhost/chatdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '9aofijr33m83oeinrgbo3nem0gnoea8rg'

db = SQLAlchemy(app)

from chat import routes