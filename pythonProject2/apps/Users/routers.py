from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from apps.Users.schemas import UserRegistrationRequestSchema, UserLoginRequestSchema, UserResponseSchema
from apps.Users.services import UserServices
from apps.database import get_db
from apps.utils import get_current_active_user

user_api_router = APIRouter(
    tags=["users"],
    prefix="/user",
)


@user_api_router.get("/secure-data/", status_code=200)
def get_secure_data(current_user: UserResponseSchema = Depends(get_current_active_user)):
    return UserServices.test_api(current_user)


@user_api_router.post("/register", status_code=201)
def register_user(request: UserRegistrationRequestSchema, db: Session = Depends(get_db)):
    return UserServices.register(request=request, db_session=db)


@user_api_router.post("/token", status_code=200)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return UserServices.get_token(form_data=form_data, db_session=db)


@user_api_router.post("/login", status_code=200)
def login_user(request: UserLoginRequestSchema, db: Session = Depends(get_db)):
    return UserServices.login(request=request, db_session=db)
