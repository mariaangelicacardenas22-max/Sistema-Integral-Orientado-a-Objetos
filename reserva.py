"Clase Reserva integra cliente, servicio, duracion y estado"
from cliente import Cliente
from entidad import EntidadBase
from excepciones import (ErrorSoftwareFJ, OperacionNoPermitidaError,
                          ReservaInvalidaError, ServicioNoDisponibleError)
from logger import log
from servicios import Servicio


class Reserva(EntidadBase):
    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    CANCELADA = "CANCELADA"
    PROCESADA = "PROCESADA"

    def __init__(self, cliente=None, servicio=None, horas=None):
        super().__init__()
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva requiere un cliente valido")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva requiere un servicio valido")
        if not servicio.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{servicio.nombre}' no esta disponible")
        try:
            servicio.validar_parametros(horas)
        except ErrorSoftwareFJ as error:
            raise ReservaInvalidaError("No se pudo crear la reserva. Duracion invalida") from error
        self._cliente = cliente
        self._servicio = servicio
        self._horas = horas
        self._estado = self.PENDIENTE

    @property
    def estado(self):
        return self._estado

    def confirmar(self):
        if self._estado != self.PENDIENTE:
            raise OperacionNoPermitidaError(
                f"Solo se confirma una reserva PENDIENTE (actual: {self._estado}).")
        if not self._servicio.disponible:
            raise ServicioNoDisponibleError("El servicio dejo de estar disponible")
        self._estado = self.CONFIRMADA

    def cancelar(self):
        if self._estado in (self.CANCELADA, self.PROCESADA):
            raise OperacionNoPermitidaError(
                f"No se puede cancelar una reserva {self._estado}.")
        self._estado = self.CANCELADA

    def calcular_total(self, impuesto=None, descuento=0.0):
        "Variantes: calcular_total(), calcular_total(0.19), calcular_total(0.19, 0.1)"
        return self._servicio.calcular_costo_total(self._horas, impuesto, descuento)

    def procesar(self, descuento=0.0):
        "Procesa la reserva"
        total = None
        try:
            if self._estado != self.CONFIRMADA:
                raise OperacionNoPermitidaError(
                    f"Solo se procesa una reserva CONFIRMADA (actual: {self._estado}).")
            total = self.calcular_total(descuento=descuento)
        except ErrorSoftwareFJ as error:
            log.error("Reserva #%s no procesada: %s", self.id, error)
            raise
        else:
            self._estado = self.PROCESADA
            log.info("Reserva #%s procesada. Total: $%s", self.id, f"{total:,.2f}")
            return total
        finally:
            log.info("Intento de procesamiento finalizado para reserva #%s", self.id)

    def describir(self):
        return (f"Reserva #{self.id} | {self._cliente.nombre} | {self._servicio.nombre} | "
                f"{self._horas}h | {self._estado}")
