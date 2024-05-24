class JudicialFunctionConnectionError(Exception):
    pass


class JudicialFunctionServerError(Exception):
    pass


class JudicialFunctionCauseConnectionError(JudicialFunctionConnectionError):
    pass


class JudicialFunctionCauseServerError(JudicialFunctionServerError):
    pass


class JudicialFunctionCountConnectionError(JudicialFunctionConnectionError):
    pass


class JudicialFunctionCountServerError(JudicialFunctionServerError):
    pass


class JudicialFunctionDetailConnectionError(JudicialFunctionConnectionError):
    pass


class JudicialFunctionDetailServerError(JudicialFunctionServerError):
    pass


class JudicialFunctionProceedingConnectionError(JudicialFunctionConnectionError):
    pass


class JudicialFunctionProceedingServerError(JudicialFunctionServerError):
    pass
