from pokepong.app import app
from pokepong.config import _cfg, _cfgi
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import bcrypt

app.config['SQLALCHEMY_DATABASE_URI'] = _cfg('connection-string')
db = SQLAlchemy(app)

class Trainer(db.model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, Nullable=False)
    password = db.Column(db.String)
    admin = Column(db.Boolean)
    created = Column(db.DateTime)

    def __init__(self, username, password, admin=False):
        self.username = username
        self.set_password(password)
        self.admin = admin
        self.created = datetime.now()

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'),
                                      bcrypt.gensalt()).decode('utf-8')

class Pokemon(db.model):
    #likely need at least a name, level and associated trainer
    pass

class Item(db.model):
    #likely just link item id in complete item db to trainer(2 relationships)
    pass
