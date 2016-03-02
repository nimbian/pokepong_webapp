from sqlalchemy import Column, Integer, String, Unicode, Boolean, DateTime, ForeignKey, Table, UnicodeText, Text, text
from sqlalchemy.orm import relationship, backref
from .database import Base
from datetime import datetime
import bcrypt

class Trainer(Base):
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

