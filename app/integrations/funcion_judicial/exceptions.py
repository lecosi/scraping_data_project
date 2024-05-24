class JudicialFunctionConnectionError(Exception):
    pass


class JudicialFunctionServerError(Exception):
    pass


class JudicialFunctionCauseConnectionError(JudicialFunctionConnectionError):
    pass


class JudicialFunctionCauseServerError(JudicialFunctionServerError):
    pass
