from typing import Tuple
from fastapi import Request
from jwt.exceptions import InvalidTokenError
from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from .constants import TokenTypes
from .pyjwt import JWTHandler
from .selectors import get_user_by_id
from ..db.models import User


class BaseAuthenticator(ABC):

    @abstractmethod
    def authenticate(self, request):
        """Authenticate a user based on request information,
        in order to use with DRF method should return a tuple
        with an authenticated user and its token
        :returns (None, None)
        """


class JWTAuthenticator(BaseAuthenticator):

    def __init__(self, session: Session):
        self.token_handler = JWTHandler()
        self._db_connection = session

    def authenticate(self, request: Request, **kwargs):
        token = request.headers.get('authorization')
        if not token:
            raise InvalidTokenError({
                'component': 'Authentication',
                'msg': 'No token provided'
            })

        token = token.split(' ')[1]
        user, token = self.authenticate_credentials(token)
        return user, token

    def authenticate_credentials(self, token) -> Tuple[User, str]:
        payload = self.token_handler.decode(token=token)
        if payload.get('token_type') != TokenTypes.ACCESS.name:
            raise InvalidTokenError({
                'component': 'Authentication',
                'msg': 'Not access token provided'
            })
        user_id = payload.get('user_id')
        if user_id is None:
            raise InvalidTokenError({
                'component': 'Authentication',
                'msg': 'Token malformed or not found'
            })

        user = get_user_by_id(
            user_id=user_id,
            session_db=self._db_connection
        )
        if not user:
            raise InvalidTokenError({
                'component': 'Authentication',
                'msg': 'User does not exists'
            })

        if not user.is_active:
            raise InvalidTokenError({
                'component': 'Authentication',
                'msg': 'User is inactive'
            })

        return user, token
