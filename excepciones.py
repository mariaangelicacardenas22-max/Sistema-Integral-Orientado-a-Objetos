"Excepciones personalizadas del sistema"

"Tipos de error para que cada problema tenga un nombre claro"


class ErrorSoftwareFJ(Exception):
    "Todos los demás errores del sistema heredan de este"


class ClienteInvalidoError(ErrorSoftwareFJ):
    "Los datos del cliente no son válidos"


class ServicioInvalidoError(ErrorSoftwareFJ):
    "Los datos del servicio no son válidos"


class ServicioNoDisponibleError(ErrorSoftwareFJ):
    "El servicio existe, pero no se puede reservar en este momento"


class ParametroFaltanteError(ErrorSoftwareFJ):
    "Falta un dato obligatorio"


class ReservaInvalidaError(ErrorSoftwareFJ):
    "Se intentó crear o usar una reserva de forma incorrecta"


class OperacionNoPermitidaError(ErrorSoftwareFJ):
    "La operación no se puede hacer en el estado actual o el dato ya existe"


class CalculoInconsistenteError(ErrorSoftwareFJ):
    "El cálculo del costo dio un resultado que no tiene sentido"
