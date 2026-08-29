from .models import Base
from .database import engine
from fastapi import FastAPI
from .routers import auth, todos, admin, users

app = FastAPI()

Base.metadata.create_all(bind=engine)

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


@app.get('/healthy')
def health_check():
    return {'status': 'HEALTHY!'}


# check JWT tokens
# https://jwt.io