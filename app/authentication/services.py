import time
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Union
from jwt import exceptions
from sqlalchemy.orm import Session

from . import selectors as auth_sel
from .constants import TokenTypes
from .pyjwt import JWTHandler
from ..db.models import User
from ..schemas.auth_user_schema import CreateUserModel, InputTokenModel, \
    InputRefreshModel


class BaseAuthServices(ABC):

    @abstractmethod
    def create_token(self, customer_external_id):
        """Create an access authentication token
        it can be use by any encryption service, from a user.
        """

    @abstractmethod
    def validate_token(self, user: User, token: str):
        """This is a specific validation method for
        refresh access process, Validates an Invalid or
        Expire Signature of a token"""


class JWTAuthService(BaseAuthServices):

    def __init__(self, token_handler: JWTHandler, session_db: Session):
        self.token_handler = token_handler
        self._db_connection = session_db

    def validate_user_can_get_token(
        self,
        *,
        username: str,
        password: str
    ) -> Optional[User]:

        user = auth_sel.get_user_by_username(
            username=username,
            session_db=self._db_connection
        )

        if user is None:
            raise ValueError({
                'component': 'Authentication',
                'msg': 'username or password is incorrect'
            })

        if not user.is_active:
            raise ValueError({
                'component': 'Authentication',
                'msg': 'user is inactive'
            })

        is_password = user.verify_password(password)
        if not is_password:
            raise ValueError({
                'component': 'Authentication',
                'msg': 'username or password is incorrect'
            })
        return user

    @staticmethod
    def get_expires_timestamp(
        *,
        minutes: int
    ) -> int:
        date = datetime.now()
        expires = date + timedelta(minutes=minutes)
        return int(time.mktime(expires.timetuple()))

    def create_token(
        self,
        *,
        user_id: int
    ) -> Dict[str, Any]:
        response = self._handle_tokens_creation(
            user_id=user_id
        )
        response['expires'] = self.get_expires_timestamp(
            minutes=TokenTypes.ACCESS.value
        )
        return response

    def validate_token(
        self,
        *,
        user: User,
        token: str
    ) -> Union[None]:
        payload = self.token_handler.decode(token=token)
        if user.id != payload.get('user_id'):
            raise ValueError({
                'component': 'Authentication',
                'msg': 'refresh token is invalid'
            })
        if payload.get('token_type') == TokenTypes.ACCESS.name:
            raise ValueError({
                'component': 'Authentication',
                'msg': 'Not a refresh token'
            })

    def _handle_tokens_creation(self, user_id: int):
        response = {}
        self._validate_user_exists(user_id=user_id)

        token_lst = [
            {'token_type': 'ACCESS', 'name': 'access_token'},
            {'token_type': 'REFRESH', 'name': 'refresh_token'}
        ]

        for token_data in token_lst:
            params = {
                'user_id': user_id,
                'expires': self.get_expires_timestamp(
                    minutes=TokenTypes.ACCESS.value
                ),
                'token_type': token_data['token_type']
            }
            token = self.token_handler.encode(**params)
            response[token_data['name']] = token

        return response

    def _validate_user_exists(self, *, user_id: int) -> bool:
        user = auth_sel.filter_user_active(
            user_id=user_id, session_db=self._db_connection
        )
        if not user:
            dict_response = dict(
                component='Authentication',
                msg='user not found',
            )
            raise exceptions.InvalidKeyError(dict_response)
        return True


class UserSignUp:
    def __init__(self, session: Session):
        self._db_connection = session

    def validate_and_create_user(
        self,
        *,
        username: str,
        password: str
    ):
        user = auth_sel.get_user_by_username(
            username=username,
            session_db=self._db_connection
        )

        if user is not None:
            raise ValueError({
                'component': 'SignUp',
                'msg': 'username already exists'
            })

        return self.create_user(
            user=CreateUserModel(username=username, password=password)
        )

    def create_user(self, user: CreateUserModel) -> User:
        hashed_password = user.get_password_hash()
        new_user = User(
            username=user.username,
            password=hashed_password
        )
        self._db_connection.add(new_user)
        self._db_connection.commit()
        self._db_connection.refresh(new_user)
        return new_user


class UserTokenService:
    def __init__(self, session: Session):
        self._db_connection = session

    def get_token(self, token_data: InputTokenModel):
        auth_service = JWTAuthService(
            token_handler=JWTHandler(),
            session_db=self._db_connection
        )

        user = auth_service.validate_user_can_get_token(
            username=token_data.username,
            password=token_data.password
        )
        return auth_service.create_token(user_id=user.id)


class RefreshTokenService:
    def __init__(self, session: Session):
        self._db_connection = session

    def validate_and_refresh_token(
        self,
        user: User,
        token_data: InputRefreshModel
    ):
        auth_services = JWTAuthService(
            token_handler=JWTHandler(),
            session_db=self._db_connection
        )

        auth_services.validate_token(
            user=user,
            token=token_data.refresh_token
        )
        return auth_services.create_token(user_id=user.id)
