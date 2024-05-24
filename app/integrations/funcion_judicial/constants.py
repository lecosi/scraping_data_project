from enum import Enum


JUDICIAL_FUNCTION_URL = 'https://api.funcionjudicial.gob.ec'


class JudicialFunctionAPI(Enum):
    EXPEL_API = 'EXPEL-CONSULTA-CAUSAS-SERVICE/api/'
    EXPEL_CLEX_API = 'EXPEL-CONSULTA-CAUSAS-CLEX-SERVICE/api/'


class JudicialFunctionURL(Enum):
    SEARCH_CAUSES = 'consulta-causas/informacion/buscarCausas'
    COUNT_CAUSES = 'consulta-causas/informacion/contarCausas'
    PROCESS_DETAIL = 'consulta-causas-clex/informacion/getIncidenteJudicatura/'
    JUDICIAL_PROCEEDINGS = 'consulta-causas/informacion/actuacionesJudiciales'
