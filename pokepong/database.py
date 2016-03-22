from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from .config import _cfg
engine = create_engine(_cfg('connection-string'))
db = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db.query_property()

def init_db():
    import pokepong.models
    Base.metadata.create_all(bind=engine)
    with engine.begin() as conn:
        with open('pokepong/pokemon.sql', 'r') as file_:
            for line in file_:
                conn.execute(line)
