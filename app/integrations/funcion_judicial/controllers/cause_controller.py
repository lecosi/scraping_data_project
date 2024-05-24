from typing import List

from app.integrations.funcion_judicial.services import JudicialFunctionService
from app.schemas.cause_schema import CauseModel, GetCauseListModel


class CauseController:

    @staticmethod
    def get_information(
        *,
        cause_data: GetCauseListModel,
        judicial_service: JudicialFunctionService
    ) -> List[CauseModel]:

        headers = {
            'Accept': 'application/json, text/plain,  */*',
            'Accept-Language': 'es-419,es;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Origin': 'https://procesosjudiciales.funcionjudicial.gob.ec',
            'Referer': 'https://procesosjudiciales.funcionjudicial.gob.ec/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        }
        response = judicial_service.request_causes(
            cause_data=cause_data,
            total_records=140,
            headers=headers
        )

        return response
