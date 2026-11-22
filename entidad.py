"Clase abstracta de las entidades generales del sistema"
from abc import ABC, abstractmethod


class EntidadBase(ABC):
    "Las entidades (Cliente, Servicio y Reserva) tienen un identificador y sus datos"

    _contador = 0

    def __init__(self):
        EntidadBase._contador += 1
        self._id = EntidadBase._contador

    @property
    def id(self):
        return self._id

    @abstractmethod
    def describir(self):
        "Verifican los datos y generan una excepción si hay errores"

    def __str__(self):
        return self.describir()
