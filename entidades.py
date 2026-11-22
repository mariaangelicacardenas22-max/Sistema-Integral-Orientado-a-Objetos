"Clase abstracta de las entidades generales del sistema"
from abc import ABC, abstractmethod


class EntidadBase(ABC):
    "Las entidades (Cliente, Servicio, Reserva) tienen una identificacion"

    _contador = 0

    def __init__(self):
        EntidadBase._contador += 1
        self._id = EntidadBase._contador

    @property
    def id(self):
        return self._id

    @abstractmethod
    def describir(self):
        "Descripcion en texto de la entidad"

    def __str__(self):
        return self.describir()
