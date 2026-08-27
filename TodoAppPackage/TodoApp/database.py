from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# for local sqlite DB
# SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'



# for Postgres SQL
# name of DB should be the same as you set it in pgAdmin4 programm
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:qwerty@localhost/ToDoAppDatabase'
# postgresql://postgres:qwerty@localhost/ToDoAppDatabase
#     ↓           ↓       ↓        ↓            ↓
#   драйвер    юзер    пароль    хост       имя базы данных



# for local sqlite DB
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})


# for Postgres SQL
engine = create_engine(SQLALCHEMY_DATABASE_URL)



SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()




