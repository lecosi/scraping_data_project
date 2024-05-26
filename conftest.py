from typing import Tuple

import pytest
import faker
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from app.authentication.pyjwt import JWTHandler
from app.authentication.services import JWTAuthService, UserSignUp
from app.db.connection import get_database_session
from app.db.models import User, Base
from app.schemas.auth_user_schema import CreateUserModel
from main import app

fake = faker.Faker()

SQLALCHEMY_DATABASE_URL = "postgresql://leonardocollazos:123456@localhost:5432/test_datos_co_db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_database_session():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_database_session] = override_get_database_session()


@pytest.fixture
def user_initial() -> User:
    user_ser = UserSignUp(session=get_database_session())
    user = user_ser.create_user(
        user=CreateUserModel(
            username=f'{fake.first_name()}_{fake.last_name()}',
            password='123456',
        )
    )
    return user


@pytest.fixture
def user_with_api_authenticated(user_initial) -> Tuple[TestClient, User, str]:

    jwr_handler = JWTHandler()
    jwt_auth_service = JWTAuthService(
        token_handler=jwr_handler,
        session_db=get_database_session()
    )
    tokens = jwt_auth_service.create_token(
        user_id=user_initial.id
    )
    access_token = tokens['access_token']
    refresh_token = tokens['refresh_token']

    client = TestClient(
        app,
        headers=dict(
            Accept='application/json, text/plain,  */*',
            Authorization=f'Token: {access_token}'
        )
    )
    return client, user_initial, refresh_token
