
from enum import IntEnum

from pydantic import BaseModel, Field


class SearchTypeEnum(IntEnum):
    ACTOR_OFENDIDO = 1
    DEMANDADO_PROCESADO = 2


class GetCauseListModel(BaseModel):
    identification: str = Field(max_length=15)
    search_type: SearchTypeEnum
