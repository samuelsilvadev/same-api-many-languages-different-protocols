from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker as session_maker
from .config import config_instance

engine = create_engine(config_instance.DATABASE_URL)
Session = session_maker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_session():
    db = Session()

    try:
        return db
    finally:
        db.close()
