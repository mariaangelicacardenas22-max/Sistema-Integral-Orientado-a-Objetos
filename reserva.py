"Clase Reserva: integra cliente, servicio, duración y estado"

"Una reserva pasa por estados"
from cliente import Cliente
from entidad import EntidadBase
from excepciones import (ErrorSoftwareFJ, OperacionNoPermitidaError,
                         ReservaInvalidaError, ServicioNoDisponibleError)
from logger import log
from servicios import Servicio


class Reserva(EntidadBase):
    # Los estados posibles se guardan como constantes para no escribirlos mal
    Pendiente = "Pendiente"
    Confirmada = "Confirmada"
    Cancelada = "Cancelada"
    Procesada = "Procesada"

    def __init__(self, cliente=None, servicio=None, horas=None):
        # Se revisa que lo recibido sea realmente un Cliente y un Servicio
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva requiere un cliente valido")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva requiere un servicio valido")
        if not servicio.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{servicio.nombre}' no esta disponible")
        try:
            # Cada servicio revisa las horas con sus propias reglas
            servicio.validar_parametros(horas)
        except ErrorSoftwareFJ as error:
            # Cambiamos el mensaje, se conserva el motivo original
            raise ReservaInvalidaError("No se pudo crear la reserva. Duracion invalida") from error

        # Si todo está bien, se guardan los datos
        self._cliente = cliente
        self._servicio = servicio
        self._horas = horas
        self._estado = self.Pendiente # Toda reserva nueva empieza en pendiente 
        super().__init__("Reserva")    # El identificador se asigna al final

    @property
    def estado(self):
        return self._estado

    def confirmar(self):
        "Pendiente -> Confirmada"
        if self._estado != self.Pendiente:
            raise OperacionNoPermitidaError(
                f"Solo se confirma una reserva pendiente (actual: {self._estado}).")
        if not self._servicio.disponible:
            raise ServicioNoDisponibleError("El servicio dejo de estar disponible")
        self._estado = self.Confirmada

    def cancelar(self):
        "Cancela la reserva, a menos que este cancelada o procesada"
        if self._estado in (self.Cancelada, self.Procesada):
            raise OperacionNoPermitidaError(
                f"No se puede cancelar una reserva {self._estado}.")
        self._estado = self.Cancelada

    def calcular_total(self, impuesto=None, descuento=0.0):
        "Método sobrecargado con parámetros opcionales"
        return self._servicio.calcular_costo_total(self._horas, impuesto, descuento)

    def procesar(self, descuento=0.0):
        "Confirmada-> Procesada. Muestra el total a pagar"
        try:
            if self._estado != self.Confirmada:
                raise OperacionNoPermitidaError(
                    f"Solo se procesa una reserva Confirmada (actual: {self._estado}).")
            total = self.calcular_total(descuento=descuento)
        except ErrorSoftwareFJ as error:
            log.error("Reserva #%s no procesada: %s", self.id, error)
            raise  # Vuelve a dar error para que lo vea quien llamó al método
        else:
            # Si el try terminó sin errores
            self._estado = self.Procesada
            log.info("Reserva #%s procesada. Total: $%s", self.id, f"{total:,.2f}")
            return total
        finally:
            # Siempre se anota el intento en el log
            log.info("Intento de procesamiento finalizado para reserva #%s", self.id)

    def describir(self):
        return (f"Reserva #{self.id} | {self._cliente.nombre} | {self._servicio.nombre} | "
                f"{self._horas}h | {self._estado}")
