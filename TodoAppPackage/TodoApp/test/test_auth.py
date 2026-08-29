from passlib.hosts import netbsd_context

from .utils import *
from ..routers.auth import get_db, authenticate_user


app.dependency_overrides[get_db] = override_get_db

def test_authenticate_user(test_user):
    db = TestingSessionLocal()

    authenticated_user = authenticate_user(db, test_user.username, 'password')
    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username

    non_existent_user = authenticate_user(db, 'Wrong username', 'password')
    assert non_existent_user is None


    wrong_password_user = authenticate_user(db, 'Wrong password', '')
    assert wrong_password_user is None
