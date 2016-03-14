from sqlalchemy import Column, Integer, String, Unicode, Boolean, DateTime, ForeignKey, Table, UnicodeText, Text, text
from sqlalchemy.orm import relationship, backref
from flask.ext.login import UserMixin
from .database import Base
from datetime import datetime
import bcrypt

class Trainer(Base, UserMixin):
    __tablename__ = 'trainer'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String)
    admin = Column(Boolean)
    created = Column(DateTime)

    def __init__(self, username, password, admin=False):
        self.username = username
        self.set_password(password)
        self.admin = admin
        self.created = datetime.now()

    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'),
                                      bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'),
                             self.password.encode('utf-8')) == self.password.encode('utf-8')

class Pokemon(Base):
    __tablename__ = 'pokemon'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    hp = Column(Integer)
    attack = Column(Integer)
    defence = Column(Integer)
    speed = Column(Integer)
    special = Column(Integer)
    exp = Column(Integer)
    type1 = Column(String)
    type2 = Column(String)

class Owned(Base):
    __tablename__ = 'owned'
    id = Column(Integer, primary_key=True)
    trainer_id = Column(Integer, ForeignKey('trainer.id'))
    owner = relationship('Trainer',
                         backref=backref('pokemon', lazy='dynamic'))
    base_id = Column(Integer, ForeignKey('pokemon.id'))
    base = relationship('Pokemon')
    name = Column(String)
    move1 =Column(String)
    move2 =Column(String)
    move3 =Column(String)
    move4 =Column(String)
    lvl = Column(Integer, nullable=False)
    hpev = Column(Integer)
    attackev = Column(Integer)
    defenseev = Column(Integer)
    speedev = Column(Integer)
    specialev = Column(Integer)
    attackiv = Column(Integer)
    defenseiv = Column(Integer)
    speediv = Column(Integer)
    specialiv = Column(Integer)
    exp = Column(Integer)
    pp1 = Column(Integer)
    pp2 = Column(Integer)
    pp3 = Column(Integer)
    pp4 = Column(Integer)

class Item(Base):
    __tablename__ = 'item'
    #likely just link item id in complete item db to trainer(2 relationships)
    id = Column(Integer, primary_key=True)
