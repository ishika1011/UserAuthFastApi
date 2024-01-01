from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

import config

current_config_object = config.get_current_server_config()
engine = create_engine(current_config_object.SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()
