from datetime import datetime
from typing import Any

from sqlalchemy import String, Column, DateTime, Integer, Boolean
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from apps.database import Base
from apps.Users.hashing import Hasher


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, unique=True)
    user_name = Column(String(30), nullable=False, unique=True)
    password = Column(String(), nullable=False)
    email = Column(String(320), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.now())
    is_admin = Column(Boolean, default=False, nullable=False)
    disabled = Column(Boolean, default=False, nullable=False)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.user_name = kwargs.get("user_name")
        self.email = kwargs.get("email")
        self.password = Hasher.hash_password(kwargs.get("password"))

    @classmethod
    def save(cls, db_session, data):
        try:
            user = cls(**data)
            db_session.add(user)
            db_session.commit()
            db_session.refresh(user)
            return True, user
        except IntegrityError as e:
            error = e.orig.diag.message_detail[4:].split("=")
            return False, error[0] + error[1]
        except SQLAlchemyError as e:
            return False, e.__str__()

    @classmethod
    def get_user_by_email(cls, db_session: Any, email: str):
        return db_session.query(cls).filter(cls.email == email).first()

    @classmethod
    def get_user_by_username(cls, db_session: Any, user_name: str):
        return db_session.query(cls).filter(cls.user_name == user_name).first()

    @classmethod
    def get_user_by_user_id(cls, db_session: Any, user_id: int):
        return db_session.query(cls).filter(cls.user_id == user_id).first()

    def __repr__(self) -> str:
        return f"<User {self.user_id}>"
