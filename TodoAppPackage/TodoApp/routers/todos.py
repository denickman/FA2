from typing import Annotated

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path, Request
from starlette import status

from ..database import SessionLocal
from ..models import Todos
from .dependencies import db_dependency, get_db
from .auth import get_current_user
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="TodoApp/templates")

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

router = APIRouter(
    prefix='/todo',
    tags=['todos'],
)

user_dependency = Annotated[dict, Depends(get_current_user)]


class TodoRequest(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    completed: bool



def redirect_to_login():
    redirect_response =  RedirectResponse(url='/auth/login-page', status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key='access-token')
    return redirect_response



### PAGES ###

@router.get('/todo-page', status_code=status.HTTP_200_OK)
async def render_todo_page(request: Request, db: db_dependency):
    try:
        user = await get_current_user(request.cookies.get('access_token'))
        if user is None:
            return redirect_to_login()

        todos = db.query(Todos).filter(Todos.owner_id == user.get('user_id')).all()
        return templates.TemplateResponse(request, "todo.html", {"todos": todos, "user": user})

    except Exception as e:
        print(f"ERROR in render_todo_page: {e}")
        return redirect_to_login()


@router.get('/add-todo-page', status_code=status.HTTP_200_OK)
async def render_add_todo_page(request: Request):
    try:
        user = await get_current_user(request.cookies.get('access_token'))
        if user is None:
            return redirect_to_login()

        return templates.TemplateResponse(request, 'add-todo.html', {"user": user})

    except Exception as e:
        print(f"ERROR in render_add_todo_page: {e}")
        return redirect_to_login()


### Endpoint ###

@router.get('', status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Auth failed')

    return db.query(Todos).filter(Todos.owner_id == user.get('user_id')).all()


@router.get('/{todo_id}', status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Auth failed')

    todo_model = (db.query(Todos)
                  .filter(Todos.id == todo_id)
                  .filter(Todos.owner_id == user.get('user_id'))
                  .first())

    if todo_model is not None:
        return todo_model

    raise HTTPException(status_code=404, detail='Todo not found')


@router.post('', status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest):

    if user is None:
        raise HTTPException(status_code=401, detail='Auth failed')

    todo_model = Todos(**todo_request.model_dump(), owner_id=user.get('user_id'))
    db.add(todo_model)
    db.commit()


@router.put('/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
        user: user_dependency,
        db: db_dependency,
        todo_request: TodoRequest,
        todo_id: int = Path(gt=0)):

    if user is None:
        raise HTTPException(status_code=401, detail='Auth failed')

    todo_model = ((db.query(Todos)
                  .filter(Todos.id == todo_id))
                  .filter(Todos.owner_id == user.get('user_id')).first())

    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found')

    if todo_model is not None:
        todo_model.title = todo_request.title
        todo_model.description = todo_request.description
        todo_model.priority = todo_request.priority
        todo_model.completed = todo_request.completed

        # db.add(todo_model)
        db.commit()

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Todo not found')


@router.delete('/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
        user: user_dependency,
        db: db_dependency,
        todo_id: int = Path(gt=0)):

    if user is None:
        raise HTTPException(status_code=401, detail='Auth failed')

    todo_model = (db.query(Todos)
                  .filter(Todos.id == todo_id)
                  .filter(Todos.owner_id == user.get('user_id'))
                  .first())

    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found')

    if todo_model is not None:
        db.delete(todo_model)
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail='Todo not found')