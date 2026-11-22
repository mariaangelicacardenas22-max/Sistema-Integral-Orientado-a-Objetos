"Excepciones personalizadas del sistema"


class ErrorSoftwareFJ(Exception):
    "Excepcion base todaslas demas heredan de ella"


class ClienteInvalidoError(ErrorSoftwareFJ):
    "Datos de cliente invalidos"


class ServicioInvalidoError(ErrorSoftwareFJ):
    "Parametros de servicio invalidos"


class ServicioNoDisponibleError(ErrorSoftwareFJ):
    "El servicio no esta disponible para reservar"


class ParametroFaltanteError(ErrorSoftwareFJ):
    "Falta un parametro obligatorio"


class ReservaInvalidaError(ErrorSoftwareFJ):
    "Intento de reserva incorrecto"


class OperacionNoPermitidaError(ErrorSoftwareFJ):
    "Operacion no permitida por el estado actual"


class CalculoInconsistenteError(ErrorSoftwareFJ):
    "Calculo de costos con resultados inconsistentes"
