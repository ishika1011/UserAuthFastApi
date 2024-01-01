from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from apps.Users.models import User
from apps.Users.schemas import UserResponseSchema
from apps.database import get_db
from config import JWTConfig

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token")

secret_key = JWTConfig().authjwt_secret_key
algorithm = JWTConfig().JWT_ALGORITHM


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = User.get_user_by_username(db_session=db, user_name=username)
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(current_user: UserResponseSchema = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
