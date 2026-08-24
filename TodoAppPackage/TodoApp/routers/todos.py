from pydantic import BaseModel, Field
from starlette import status

from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path, APIRouter
from fastapi.dependencies.models import Dependant
from models import  Todos
from routers.dependencies import db_dependency, get_db

"""
1. uvicorn main:app --reload
        ↓
2. Запустился Python код в main.py
        ↓
3. models.Base.metadata.create_all(bind=engine)
        ↓
4. SQLAlchemy подключился к 'sqlite:///./todos.db'
        ↓
5. Проверила: есть ли уже БД с таким именем в текущей папке?
        ↓
6. НЕТ → создалась новая БД (файл todos.db)
        ↓
7. Создалась таблица "todos" на основе модели Todos
        ↓
8. ✅ todos.db появился в папке с main.py
"""

router = APIRouter()

class TodoRequest(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    completed: bool

@router.get('/', status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(Todos).all()


@router.get('/todo/{todo_id}', status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    if todo_model is not None:
        return todo_model

    raise HTTPException(status_code=404, detail='Todo not found')


@router.post('/todo', status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo_request: TodoRequest):
    todo_model = Todos(**todo_request.model_dump())
    db.add(todo_model)
    db.commit()


@router.put('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
        db: db_dependency,
        todo_request: TodoRequest,
        todo_id: int = Path(gt=0)):

    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    if todo_model is not None:
        todo_model.title = todo_request.title
        todo_model.description = todo_request.description
        todo_model.priority = todo_request.priority
        todo_model.completed = todo_request.completed

        # db.add(todo_model)
        db.commit()

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Todo not found')



@router.delete('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    if todo_model is not None:
        db.delete(todo_model)
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail='Todo not found')



























