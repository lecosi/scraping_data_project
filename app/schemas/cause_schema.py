
from enum import IntEnum

from pydantic import BaseModel, Field


class SearchTypeEnum(IntEnum):
    ACTOR_OFENDIDO = 1
    DEMANDADO_PROCESADO = 2


class GetCauseListModel(BaseModel):
    identification: str = Field(max_length=15)
    search_type: SearchTypeEnum


class CauseModel(BaseModel):
    id: int
    id_juicio: str
    estado_actual: str
    id_materia: int
    id_provincia: int = None
    id_canton: int = None
    id_judicatura: int = None
    nombre_delito: str = None
    fecha_ingreso: str = None
    nombre: str = None
    cedula: str = None
    id_estado_juicio: int = None
    nombre_materia: str = None
    nombre_estado_juicio: str = None
    nombre_judicatura: str = None
    nombre_tipo_resolucion: str = None
    nombre_tipo_accion: str = None
    fecha_providencia: str = None
    nombre_providencia: str = None
    nombre_provincia: str = None
    iedocumento_adjunto: str = None
