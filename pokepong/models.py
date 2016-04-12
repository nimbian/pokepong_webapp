from __future__ import absolute_import, print_function
from math import floor
import random
from datetime import datetime
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
import bcrypt

class LearnableHm(Base):
    '''Simple Class to map all the learnable hms and the pokemon that can learn them'''
    __tablename__ = 'learnablehm'
    id = Column(Integer, primary_key=True)
    pokemon_id = Column(Integer, ForeignKey('pokemon.id'), nullable=False)
    pokemon = relationship('Pokemon', backref='learnablehms')
    tmhm_id = Column(Integer, ForeignKey('tmhm.id'), nullable=False)
    hm = relationship('TmHm')

class LearnableTm(Base):
    '''Simple Class to map all the learnable tms and the pokemon that can learn them'''
    __tablename__ = 'learnabletm'
    id = Column(Integer, primary_key=True)
    pokemon_id = Column(Integer, ForeignKey('pokemon.id'), nullable=False)
    pokemon = relationship('Pokemon', backref='learnabletms')
    tmhm_id = Column(Integer, ForeignKey('tmhm.id'), nullable=False)
    tm = relationship('TmHm')

class TmHm(Base):
    '''Simple Class to map all the learnable tm/hms and thier move'''
    __tablename__ = 'tmhm'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    move_id = Column(Integer, ForeignKey('move.id'), nullable=False)
    move = relationship('Move', backref=backref('TmHm', uselist=False))

class Type(Base):
    '''Lookup class the defines all the pokemon and move types'''
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
    '''Lookup class that defines all of the pokedex entries'''
    __tablename__ = 'pokedex'
    id = Column(Integer, primary_key=True)
    pokemon_id = Column(Integer, ForeignKey('pokemon.id'), nullable=False)
    pokemon = relationship('Pokemon', backref=backref('pokedex', uselist=False))
    height = Column(String, nullable=False)
    weight = Column(String, nullable=False)
    entry = Column(String, nullable=False)

class LearnableMove(Base):
    '''Lookup class that maps the a pokemon to a move and the level they learn it at'''
    __tablename__ = 'learnablemove'
    id = Column(Integer, primary_key=True)
    pokemon_id = Column(Integer, ForeignKey('pokemon.id'), nullable=False)
    pokemon = relationship('Pokemon', backref='learns')
    move_id = Column(Integer, ForeignKey('move.id'), nullable=False)
    move = relationship('Move')
    learnedat = Column(Integer, nullable=False)

class Move(Base):
    '''Class defining every possible move and its stats'''
    __tablename__ = 'move'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type_id = Column(String, ForeignKey('type.id'), nullable=False)
    type_ = relationship('Type', backref='moves')
    maxpp = Column(Integer, nullable=False)
    power = Column(Integer)
    acc = Column(Integer)

class Trainer(Base, UserMixin):
    '''Every registered trainer'''
    __tablename__ = 'trainer'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    password = Column(String)
    admin = Column(Boolean)
    created = Column(DateTime)
    money = Column(Integer, default=1500)

    def __init__(self, name, password, admin=False):
        self.name = name
        self.set_password(password)
        self.admin = admin
        self.created = datetime.now()

    #TODO: Maybe use sqlalchemy hybrid atribute? Seems like overkill tho.....
    def set_password(self, password):
        '''Uses bcrypt to hash the password before setting it to the pasword field'''
        self.password = bcrypt.hashpw(password.encode('utf-8'),
                                      bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        '''Uses bcrypt to compare password to given string'''
        return bcrypt.hashpw(password.encode('utf-8'),
                             self.password.encode('utf-8')) == self.password.encode('utf-8')

class Pokemon(Base):
    '''Lookup class that has the base stats of all the pokemon types'''
    __tablename__ = 'pokemon'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    hp = Column(Integer)
    attack = Column(Integer)
    defense = Column(Integer)
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
    basecatch = Column(Integer)

class Owned(Base):
    '''Class that holds a captured pokemon mapped to the owning trainer'''
    __tablename__ = 'owned'
    id = Column(Integer, primary_key=True)
    trainer_id = Column(Integer, ForeignKey('trainer.id'))
    owner = relationship('Trainer', backref=backref('pokemon',
                                                    order_by='Owned.id'))
    base_id = Column(Integer, ForeignKey('pokemon.id'))
    base = relationship('Pokemon')
    name = Column(String)
    move1_id = Column(Integer, ForeignKey('move.id'))
    move1 = relationship('Move', foreign_keys='Owned.move1_id')
    move2_id = Column(Integer, ForeignKey('move.id'))
    move2 = relationship('Move', foreign_keys='Owned.move2_id')
    move3_id = Column(Integer, ForeignKey('move.id'))
    move3 = relationship('Move', foreign_keys='Owned.move3_id')
    move4_id = Column(Integer, ForeignKey('move.id'))
    move4 = relationship('Move', foreign_keys='Owned.move4_id')
    lvl = Column(Integer, nullable=False)
    hpev = Column(Integer, default=0)
    attackev = Column(Integer, default=0)
    defenseev = Column(Integer, default=0)
    speedev = Column(Integer, default=0)
    specialev = Column(Integer, default=0)
    attackiv = Column(Integer, default=random.randint(0, 15))
    defenseiv = Column(Integer, default=random.randint(0, 15))
    speediv = Column(Integer, default=random.randint(0, 15))
    specialiv = Column(Integer, default=random.randint(0, 15))
    exp = Column(Integer, default=0)
    pp1 = Column(Integer, default=0)
    pp2 = Column(Integer, default=0)
    pp3 = Column(Integer, default=0)
    pp4 = Column(Integer, default=0)

    def __init__(self, base_id, lvl=5):
        self.base_id = base_id
        self.lvl = lvl
        x = LearnableMove.query.filter(
            LearnableMove.learnedat <= self.lvl) .filter(
                LearnableMove.pokemon_id == self.base_id).all()
        tmp = []
        for i in x[-4:]:
            tmp.append(Move.query.filter(Move.id==i.move_id).one())
        self.move1, self.move2, self.move3, self.move4 = (tmp+([None] * 4))[:4]
        self.exp = {'f': int(4 * self.lvl ** 3 / 5.),
                    'mf': self.lvl ** 3,
                    'ms': int(6/5. * self.lvl ** 3 - 15 * self.lvl ** 2 + 100 * self.lvl - 140),
                    's': int(5 * self.lvl ** 3 / 4.)}[self.base.lvlspeed]

    @property
    def maxhp(self):
        I = [0, 8][self.attackiv % 2] + [0, 4][self.defenseiv % 2] +\
            [0, 2][self.speediv % 2] + [0, 1][self.specialiv % 2]
        E = min(63, int(floor(floor((max(0, self.hpev-1)**.5)+1)/4.)))
        stat = floor((2 * self.base.hp + I + E) * self.lvl / 100. + 5)
        return stat

class OwnedItem(Base):
    __tablename__ = 'owneditem'
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('items.id'))
    trainer_id = Column(Integer, ForeignKey('trainer.id'))
    owner = relationship('Trainer', backref='items')
    count = Column(Integer)

class Items(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    battle = Column(Integer)
    buyable = Column(Integer)
    buyprice = Column(Integer)
    sellprice = Column(Integer)
