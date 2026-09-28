import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Берём DATABASE_URL из переменной окружения (её задаёт docker-compose.yml для Postgres).
# Если переменной нет — используем локальный SQLite, как раньше, чтобы uvicorn
# без Docker продолжал работать точно так же, как и до этого.
SQLALCHEMY_DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./todosapp.db')

# Этот параметр нужен только для SQLite (он по умолчанию разрешает только один поток).
# Postgres и MySQL его не понимают и выдадут ошибку, если передать.
connect_args = (
    {"check_same_thread": False}
    if SQLALCHEMY_DATABASE_URL.startswith('sqlite')
    else {}
)

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)





SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()




