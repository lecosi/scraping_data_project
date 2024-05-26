import logging

from fastapi import FastAPI, Depends, Response, status, HTTPException, Request
from jwt import InvalidTokenError, ExpiredSignatureError
from sqlalchemy.orm import Session

from app.authentication.authenticator import JWTAuthenticator
from app.authentication.services import (
    UserSignUp,
    UserTokenService,
    RefreshTokenService
)
from app.db.connection import get_database_session
from app.integrations.funcion_judicial.controllers.cause_controller import \
    CauseController
from app.integrations.funcion_judicial.services import JudicialFunctionService
from app.schemas.auth_user_schema import InputSigUpModel, InputTokenModel, \
    InputRefreshModel
from app.schemas.cause_schema import GetCauseListModel
from app.utils.rest_api_client_async import RestAPIClient

logger = logging.getLogger(__name__)

app = FastAPI()


@app.get('/')
def home():
    return {"message": "Hello World"}


@app.post('/search', tags=['Search'])
async def search_information_list(
    request: Request,
    cause_data: GetCauseListModel,
    session_db: Session = Depends(get_database_session)
):
    try:
        jwt_auth = JWTAuthenticator(session=session_db)
        user, _ = jwt_auth.authenticate(request=request)
        api_rest_client = RestAPIClient()
        judicial_service = JudicialFunctionService(
            api_rest_client=api_rest_client
        )
        cause_controller = CauseController(judicial_service=judicial_service)
        return await cause_controller.get_process_information(
            cause_data=cause_data
        )
    except (IndexError, ValueError) as e:
        logger.error(f'search_information_list :: {e}')
        msg = 'Header malformed'
        return HTTPException(status.HTTP_400_BAD_REQUEST, msg)

    except (ExpiredSignatureError, InvalidTokenError) as e:
        logger.error(f'search_information_list :: {e}')
        return HTTPException(status.HTTP_401_UNAUTHORIZED, e.args[0])

    except Exception as e:
        logger.error(f'search_information_list :: {e}')
        msg = 'there is a problem when sent request, try again later'
        return HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, msg)


@app.post('/signup', tags=['Auth'])
def signup(
    user_data: InputSigUpModel,
    session_db: Session = Depends(get_database_session)
):
    try:
        signup_service = UserSignUp(session=session_db)
        signup_service.validate_and_create_user(
            username=user_data.username,
            password=user_data.password
        )
    except Exception as e:
        logger.error(f'signup :: {e}')
        return HTTPException(status.HTTP_400_BAD_REQUEST, e.args[0])
    return Response(status_code=status.HTTP_201_CREATED)


@app.post('/login', tags=['Auth'])
def login(
    user_data: InputTokenModel,
    session_db: Session = Depends(get_database_session)
):
    try:
        signup_service = UserTokenService(session=session_db)
        token_data = signup_service.get_token(token_data=user_data)

    except Exception as e:
        logger.error(f'login :: {e}')
        return HTTPException(status.HTTP_400_BAD_REQUEST, e.args[0])

    return token_data


@app.post('/refresh-token', tags=['Auth'])
def get_refresh_token(
    request: Request,
    token_input_data: InputRefreshModel,
    session_db: Session = Depends(get_database_session)
):
    try:
        jwt_auth = JWTAuthenticator(session=session_db)
        user, _ = jwt_auth.authenticate(request=request)
        signup_service = RefreshTokenService(session=session_db)
        token_data = signup_service.validate_and_refresh_token(
            user=user,
            token_data=token_input_data
        )

    except (IndexError, ValueError) as e:
        logger.error(f'get_refresh_token :: {e}')
        msg = 'Header malformed'
        return HTTPException(status.HTTP_400_BAD_REQUEST, msg)

    except (ExpiredSignatureError, InvalidTokenError) as e:
        logger.error(f'get_refresh_token :: {e}')
        return HTTPException(status.HTTP_401_UNAUTHORIZED, e.args[0])

    except Exception as e:
        logger.error(f'get_refresh_token :: {e}')
        msg = 'there is a problem when sent request, try again later'
        return HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, msg)

    return token_data
