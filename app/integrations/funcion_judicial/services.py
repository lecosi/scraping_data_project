import json
from typing import Optional, Dict, Any, Union

from app.integrations.funcion_judicial.constants import JudicialFunctionAPI, \
    JudicialFunctionURL, JUDICIAL_FUNCTION_URL
from app.integrations.funcion_judicial.exceptions import \
    JudicialFunctionCauseServerError, JudicialFunctionCauseConnectionError
from app.schemas.cause_schema import GetCauseListModel, SearchTypeEnum
from app.utils.rest_api_client import RestAPIClient


class JudicialFunctionService:

    def __init__(
        self,
        api_rest_client: RestAPIClient
    ):
        self.rest_client = api_rest_client

    def request_causes(
        self,
        *,
        cause_data: GetCauseListModel,
        total_records: int,
        headers: Dict[str, Union[int, str]]
    ) -> Optional[Dict[str, Any]]:

        endpoint = JudicialFunctionURL.SEARCH_CAUSES.value
        api_version = JudicialFunctionAPI.EXPEL_API.value

        url = f'{JUDICIAL_FUNCTION_URL}/{api_version}/{endpoint}' \
              f'?page=1&size={total_records}'

        data = {
            "numeroCausa": "",
            "actor": {
                "cedulaActor": "",
                "nombreActor": ""
            },
            "demandado": {
                "cedulaDemandado": "",
                "nombreDemandado": ""
            },
            "provincia": "",
            "numeroFiscalia": "",
            "recaptcha": "verdad",
            "first": "1",
            "pageSize": "10"
        }
        if cause_data.search_type == SearchTypeEnum.ACTOR_OFENDIDO.value:
            data['actor']['cedulaActor'] = cause_data.identification
        else:
            data['cedulaDemandado']['cedulaDemandado'] = \
                cause_data.identification

        import pdb; pdb.set_trace()

        response = self.rest_client.request_post(
            url=url,
            headers=headers,
            data=data
        )

        if 300 <= response.status_code <= 499:
            raise JudicialFunctionCauseConnectionError({
                'code': 'AH001',
                'message': 'Error Connection with funcion judicial'
            })

        if response.status_code >= 500:
            raise JudicialFunctionCauseServerError({
                'code': 'AH002',
                'message': 'Error Server of funcion judicial'
            })

        response_data = json.loads(response.text)

        return response_data

