import asyncio
import logging
from typing import List, Dict, Any, Optional, Union

import pandas as pd

from app.integrations.funcion_judicial.services import JudicialFunctionService
from app.schemas.cause_schema import GetCauseListModel

logger = logging.getLogger(__name__)


class CauseController:

    def __init__(self, judicial_service: JudicialFunctionService):
        self.judicial_service = judicial_service

    async def get_process_information(
        self,
        *,
        cause_data: GetCauseListModel
    ) -> Optional[List[Dict[str, Any]]]:

        total_records = await self.judicial_service.request_get_total_causes(
            cause_data=cause_data
        )
        causes_lst = await self.judicial_service.request_causes(
            cause_data=cause_data,
            total_records=total_records
        )
        tasks = []
        result = []
        for cause in causes_lst:
            tasks.append(self.run_process(cause=cause, result=result))

        await asyncio.gather(*tasks)

        df = pd.DataFrame(result)
        csv_file = 'output.csv'
        df.to_csv(csv_file, index=False)

        return causes_lst

    async def run_process(
        self,
        cause: Dict[str, Union[int, str]],
        result: List
    ):
        judgment_id = cause['idJuicio']
        detail_data = await self.get_cause_detail_by_judgment_id(
            judgment_id=judgment_id
        )

        if not detail_data:
            cause['detalleProceso'] = {}
            return

        incident = detail_data.get('lstIncidenteJudicatura')
        if not incident:
            return

        judicial_data = await self.get_judicial_process_lst(
            judgment_id=judgment_id,
            judiciary_id=detail_data['idJudicatura'],
            incident_judgment_id=incident[0]['idIncidenteJudicatura'],
            incident_judgment_movement_id=incident[0][
                'idMovimientoJuicioIncidente']
        )
        if not judicial_data:
            cause['detalleProceso'] = detail_data
            return

        detail_data['actuacionesJudiciales'] = judicial_data
        cause['detalleProceso'] = detail_data

        result.append(cause)

    async def get_cause_detail_by_judgment_id(
        self,
        judgment_id: str
    ) -> Optional[Dict[str, Any]]:
        try:
            response_detail = \
                await self.judicial_service.request_detail_process(
                    judgment_id=judgment_id
                )
            judgment_data = response_detail[0]
            if not judgment_data:
                return {}

            return judgment_data
        except Exception as e:
            logger.error(f'get_cause_detail_by_judgment_id :: {e}')
            return {}

    async def get_judicial_process_lst(
        self,
        *,
        judgment_id: str,
        judiciary_id: str,
        incident_judgment_id: int,
        incident_judgment_movement_id: int
    ) -> Optional[List[Dict[str, Any]]]:
        try:
            judicial_proceeding_lst = \
                await self.judicial_service.request_judicial_proceedings(
                    judgment_id=judgment_id,
                    judiciary_id=judiciary_id,
                    incident_judgment_id=incident_judgment_id,
                    incident_judgment_movement_id=incident_judgment_movement_id
                )

            return judicial_proceeding_lst

        except Exception as e:
            logger.error(e)
            return []
