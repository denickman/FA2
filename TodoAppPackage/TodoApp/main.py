from .models import Base
from .database import engine
from fastapi import FastAPI, Request
from .routers import auth, todos, admin, users

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles






app = FastAPI()

Base.metadata.create_all(bind=engine)


templates = Jinja2Templates(directory='TodoApp/templates')

app.mount('/static', StaticFiles(directory='TodoApp/static'), name='static')



'''
app.dependency_overrides  # это просто словарь: {}
По умолчанию этот словарь пустой.

. У объекта app есть словарь dependency_overrides. Ключ — оригинальная функция-зависимость
 (та, что реально используется в роутах через Depends(...)), значение — функция-замена.

'''

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)


@app.get('/')
def test(request: Request):
    return templates.TemplateResponse(request, 'home.html', {})





@app.get('/healthy')
def health_check():
    return {'status': 'HEALTHY!'}


# check JWT tokens
# https://jwt.io