from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path, APIRouter
from starlette import status
from models import Todos
from database import SessionLocal
from .auth import get_current_user
from routers.dependencies import db_dependency, get_db


router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)


user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get('/todo', status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return db.query(Todos).all()


@router.delete('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, user: user_dependency, todo_id: int = Path(gt=0)):

    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return db.query(Todos).filter(Todos.todo_id == todo_id).delete()