

import pytest


from fastapi.testclient import TestClient

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from ..database import  Base
from ..main import app

from ..models import Todos




SQLALCHEMY_DATABASE_URI = 'sqlite:///./testdb.db'


engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)



def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db

    finally:
        db.close()


def override_get_current_user():
    return {
        "user_id": 1,
        "username": "den",
        "user_role": "admin"
    }



client = TestClient(app)

@pytest.fixture
def test_todo():
    todo = Todos(
        title="Learn the code",
        description="Every day",
        priority=5,
        completed=False,
        owner_id=1,
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text('DELETE FROM todos;'))
        connection.commit()

