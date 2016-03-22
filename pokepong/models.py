from __future__ import absolute_import, print_function
from sqlalchemy import (Column,
                        Integer,
                        String,
                        Unicode,
                        Boolean,
                        DateTime,
                        ForeignKey,
                        Float)
from sqlalchemy.orm import relationship, backref
from flask.ext.login import UserMixin
from pokepong.database import Base
from datetime import datetime
import bcrypt

class LearnableHm(Base):
    __tablename__ = 'learnablehm'
    id = Column(Integer, primary_key=True)
    pokemon_id = Column(Integer, ForeignKey('pokemon.id'), nullable=False)
    pokemon = relationship('Pokemon', backref='learnablehms')
    tmhm_id = Column(Integer, ForeignKey('tmhm.id'), nullable=False)
    hm = relationship('TmHm')

class LearnableTm(Base):
    __tablename__ = 'learnabletm'
    id = Column(Integer, primary_key=True)
    pokemon_id = Column(Integer, ForeignKey('pokemon.id'), nullable=False)
    pokemon = relationship('Pokemon', backref='learnabletms')
    tmhm_id = Column(Integer, ForeignKey('tmhm.id'), nullable=False)
    tm = relationship('TmHm')

class TmHm(Base):
    __tablename__ = 'tmhm'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    move_id = Column(Integer, ForeignKey('move.id'), nullable=False)
    move = relationship('Move', backref=backref('TmHm', uselist=False))
    
class Type(Base):
    __tablename__ = 'type'
    id = Column(Integer, primary_key=True)
    type_ = Column(String, nullable=False)
    bug = Column(Float, nullable=False)
    dragon = Column(Float, nullable=False)
    electric = Column(Float, nullable=False)
    fighting = Column(Float, nullable=False)
    fire = Column(Float, nullable=False)
    flying = Column(Float, nullable=False)
    ghost = Column(Float, nullable=False)
    grass = Column(Float, nullable=False)
    ground = Column(Float, nullable=False)
    ice = Column(Float, nullable=False)
    normal = Column(Float, nullable=False)
    poison = Column(Float, nullable=False)
    psychic = Column(Float, nullable=False)
    rock = Column(Float, nullable=False)
    water = Column(Float, nullable=False)

class Pokedex(Base):
    __tablename__ = 'pokedex'
    id = Column(Integer, primary_key=True)
    pokemon_id = Column(Integer, ForeignKey('pokemon.id'), nullable=False)
    pokemon = relationship('Pokemon', backref=backref('pokedex', uselist=False))
    height = Column(String, nullable=False)
    weight = Column(String, nullable=False)
    entry = Column(String, nullable=False)

class LearnableMove(Base):
    __tablename__ = 'learnablemove'
    id = Column(Integer, primary_key=True)
    pokemon_id = Column(Integer, ForeignKey('pokemon.id'), nullable=False)
    pokemon = relationship('Pokemon', backref='learns')
    move_id = Column(Integer, ForeignKey('move.id'),  nullable=False)
    move = relationship('Move')
    learnedat = Column(Integer, nullable=False)

class Move(Base):
    __tablename__ = 'move'
    id = Column(Integer, primary_key=True)
    move = Column(String, nullable=False)
    type_id = Column(String, ForeignKey('type.id'), nullable=False)
    type_ = relationship('Type', backref='moves')
    pp = Column(Integer, nullable=False)
    power = Column(Integer)
    acc = Column(Integer)

class Trainer(Base, UserMixin):
    __tablename__ = 'trainer'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    password = Column(String)
    admin = Column(Boolean)
    created = Column(DateTime)

    def __init__(self, name, password, admin=False):
        self.name = name
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
    lvlspeed = Column(String, nullable=False)
    evolves_to_id = Column(Integer, ForeignKey('pokemon.id'))
    evolves_at = Column(Integer)
    evolves_to = relationship('Pokemon',
                              lazy='joined',
                              join_depth=1)

class Owned(Base):
    __tablename__ = 'owned'
    id = Column(Integer, primary_key=True)
    trainer_id = Column(Integer, ForeignKey('trainer.id'))
    owner = relationship('Trainer', backref='pokemon')
    base_id = Column(Integer, ForeignKey('pokemon.id'))
    base = relationship('Pokemon')
    name = Column(String)
    move1 = Column(String)
    move2 = Column(String)
    move3 = Column(String)
    move4 = Column(String)
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
