import json
from typing import Optional, Dict, Any, List

from app.integrations.funcion_judicial.constants import JudicialFunctionAPI, \
    JudicialFunctionURL, JUDICIAL_FUNCTION_URL
from app.integrations.funcion_judicial.exceptions import \
    JudicialFunctionCauseServerError, JudicialFunctionCauseConnectionError, \
    JudicialFunctionCountConnectionError, JudicialFunctionCountServerError, \
    JudicialFunctionDetailConnectionError, JudicialFunctionDetailServerError, \
    JudicialFunctionProceedingConnectionError, \
    JudicialFunctionProceedingServerError
from app.schemas.cause_schema import GetCauseListModel, SearchTypeEnum
from app.utils.rest_api_client_async import RestAPIClient
from app.utils.scraping_utils import generate_user_agent


class JudicialFunctionService:

    HEADERS = {
        'Accept': 'application/json, text/plain,  */*',
        'Accept-Language': 'es-419,es;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://procesosjudiciales.funcionjudicial.gob.ec',
        'Referer': 'https://procesosjudiciales.funcionjudicial.gob.ec/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': generate_user_agent()
    }

    def __init__(
        self,
        api_rest_client: RestAPIClient
    ):
        self.rest_client = api_rest_client

    async def request_get_total_causes(
        self,
        *,
        cause_data: GetCauseListModel
    ) -> Optional[int]:

        api_version = JudicialFunctionAPI.EXPEL_API.value
        endpoint = JudicialFunctionURL.COUNT_CAUSES.value

        url = f'{JUDICIAL_FUNCTION_URL}/{api_version}/{endpoint}'

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
            "recaptcha": "verdad"
        }

        if cause_data.search_type == SearchTypeEnum.ACTOR_OFENDIDO.value:
            data['actor']['cedulaActor'] = cause_data.identification

        else:
            data['cedulaDemandado']['cedulaDemandado'] = \
                cause_data.identification

        response = await self.rest_client.request_post(
            url=url,
            headers=self.HEADERS,
            data=data
        )

        if 300 <= response.status_code <= 499:
            raise JudicialFunctionCountConnectionError({
                'code': 'JF001',
                'message': 'Error Connection with funcion judicial'
            })

        if response.status_code >= 500:
            raise JudicialFunctionCountServerError({
                'code': 'JF002',
                'message': 'Error Server of funcion judicial'
            })

        response_data = json.loads(response.text)

        return response_data

    async def request_causes(
        self,
        *,
        cause_data: GetCauseListModel,
        total_records: int
    ) -> Optional[List[Dict[str, Any]]]:

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

        response = await self.rest_client.request_post(
            url=url,
            headers=self.HEADERS,
            data=data
        )

        if 300 <= response.status_code <= 499:
            raise JudicialFunctionCauseConnectionError({
                'code': 'JF003',
                'message': 'Error Connection with funcion judicial'
            })

        if response.status_code >= 500:
            raise JudicialFunctionCauseServerError({
                'code': 'JF004',
                'message': 'Error Server of funcion judicial'
            })

        response_data = json.loads(response.text)

        return response_data

    async def request_detail_process(
        self,
        *,
        judgment_id: str,
    ) -> Optional[List[Dict[str, Any]]]:

        endpoint = JudicialFunctionURL.PROCESS_DETAIL.value
        api_version = JudicialFunctionAPI.EXPEL_CLEX_API.value

        url = f'{JUDICIAL_FUNCTION_URL}/{api_version}/{endpoint}/{judgment_id}'

        response = await self.rest_client.request_get(
            url=url,
            headers=self.HEADERS
        )

        if 300 <= response.status_code <= 499:
            raise JudicialFunctionDetailConnectionError({
                'code': 'JF005',
                'message': 'Error Connection with funcion judicial'
            })

        if response.status_code >= 500:
            raise JudicialFunctionDetailServerError({
                'code': 'JF006',
                'message': 'Error Server of funcion judicial'
            })

        response_data = json.loads(response.text)

        return response_data

    async def request_judicial_proceedings(
        self,
        *,
        judgment_id: str,
        judiciary_id: str,
        incident_judgment_id: int,
        incident_judgment_movement_id: int
    ) -> Optional[List[Dict[str, Any]]]:

        api_version = JudicialFunctionAPI.EXPEL_API.value
        endpoint = JudicialFunctionURL.JUDICIAL_PROCEEDINGS.value

        url = f'{JUDICIAL_FUNCTION_URL}/{api_version}/{endpoint}'

        data = {
            "idMovimientoJuicioIncidente": incident_judgment_movement_id,
            "idJuicio": judgment_id,
            "idJudicatura": judiciary_id,
            "idIncidenteJudicatura": incident_judgment_id,
            "aplicativo": "web",
            "incidente": 1
        }

        response = await self.rest_client.request_post(
            url=url,
            headers=self.HEADERS,
            data=data
        )

        if 300 <= response.status_code <= 499:
            raise JudicialFunctionProceedingConnectionError({
                'code': 'JF007',
                'message': 'Error Connection with funcion judicial'
            })

        if response.status_code >= 500:
            raise JudicialFunctionProceedingServerError({
                'code': 'JF008',
                'message': 'Error Server of funcion judicial'
            })

        response_data = json.loads(response.text)

        return response_data
