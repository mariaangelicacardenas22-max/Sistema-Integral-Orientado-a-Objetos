"Clase abstracta de las entidades generales del sistema"

"No se puede crear un objeto directamente con ella, solo sirve para que otras clases la hereden y cumplan lo que ella exige"

from abc import ABC, abstractmethod


class EntidadBase(ABC):
    "Las entidades tienen un número de identificador y descripcion"

    # Diccionario compartido que cuenta cuántos objetos de cada tipo existen
    # Cada tipo tiene su propia numeración
    _contadores = {}

    def __init__(self, tipo):
        # Suma 1 al contador de este tipo 
        # Si no existe todavía,  empieza en 0
        self._contadores[tipo] = self._contadores.get(tipo, 0) + 1
        self._id = self._contadores[tipo]

    @property
    def id(self):
        "Permite leer el identificador pero no cambiarlo desde afuera"
        return self._id

    @abstractmethod
    def describir(self):
        "Cada clase hija debe escribir su propia versión"

    def __str__(self):
        # Muestra la descripción
        return self.describir()
