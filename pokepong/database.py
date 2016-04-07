from flask import current_app
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from flask import current_app
engine = create_engine(current_app.config['CONNECTION_STRING'])
db = scoped_session(sessionmaker(autocommit=False,
                                 autoflush=False,
                                 bind=engine))

Base = declarative_base()
Base.query = db.query_property()

def init_db():
    import pokepong.models
    Base.metadata.create_all(bind=engine)
    with engine.begin() as conn:
        result = conn.execute("SELECT id FROM pokemon")
        if result.first() is None:
            with open('pokepong/pokemon.sql', 'r') as file_:
                for line in file_:
                    conn.execute(line)
