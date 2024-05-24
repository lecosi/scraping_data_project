import logging
from fastapi import FastAPI, Depends, Response
from sqlalchemy.orm import Session

from app.db.connection import get_database_session
from app.integrations.funcion_judicial.controllers.cause_controller import \
    CauseController
from app.integrations.funcion_judicial.services import JudicialFunctionService
from app.schemas.cause_schema import GetCauseListModel
from app.utils.rest_api_client import RestAPIClient

logger = logging.getLogger(__name__)

app = FastAPI()


@app.get('/')
def home():
    return {"message": "Hello World"}


@app.post('/search', tags=['Search'])
def search_information_list(cause_data: GetCauseListModel):
    api_rest_client = RestAPIClient()
    judicial_service = JudicialFunctionService(api_rest_client=api_rest_client)
    cause_controller = CauseController()
    return cause_controller.get_information(
        cause_data=cause_data,
        judicial_service=judicial_service
    )


@app.post('/get-legal_information', tags=['Search'])
def search_information_list(
    cause_data: GetCauseListModel,
    response: Response,
    session_db: Session = Depends(get_database_session)
):
    pass


