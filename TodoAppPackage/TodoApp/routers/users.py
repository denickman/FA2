from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter, Path
from starlette import status
from database import SessionLocal
from passlib.context import CryptContext

from .auth import get_current_user
from routers.dependencies import db_dependency, get_db
from models import Todos, Users


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
user_dependency = Annotated[dict, Depends(get_current_user)]

class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)


class MessageResponse(BaseModel):
    message: str






router = APIRouter(
    prefix="/user",
    tags=["user"],
)

@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db.query(Users).filter(Users.id == user.get("user_id")).first()




@router.put('/password', status_code=status.HTTP_200_OK, response_model=MessageResponse)
async def change_password(user: user_dependency, db: db_dependency, user_verification: UserVerification):

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user_model = db.query(Users).filter(Users.id == user.get("user_id")).first()

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Error on password verification")


    user_model.hashed_password = bcrypt_context.encrypt(user_verification.new_password)

    db.add(user_model)
    db.commit()

    return {"message": "Password changed successfully"}








