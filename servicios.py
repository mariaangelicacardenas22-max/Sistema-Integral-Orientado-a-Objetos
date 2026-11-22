"Clase abstracta servicio y tres servicios especializados."
from abc import abstractmethod

from entidad import EntidadBase
from excepciones import (CalculoInconsistenteError, ParametroFaltanteError,
                          ServicioInvalidoError)

IVA = 0.19


class Servicio(EntidadBase):
    "Define lo que debe cumplir cada servicio"

    def __init__(self, nombre=None, tarifa_hora=None):
        super().__init__()
        if nombre is None or str(nombre).strip() == "":
            raise ParametroFaltanteError("El nombre del servicio es obligatorio")
        try:
            tarifa_hora = float(tarifa_hora)
        except (TypeError, ValueError) as error:
            # Encadenamiento de excepciones: Se mantiene el motivo original del error
            raise ServicioInvalidoError("La tarifa debe ser un numero") from error
        if tarifa_hora <= 0:
            raise ServicioInvalidoError("La tarifa por hora debe ser mayor que 0")
        self._nombre = str(nombre).strip()
        self._tarifa_hora = tarifa_hora
        self._disponible = True

    @property
    def nombre(self):
        return self._nombre

    @property
    def disponible(self):
        return self._disponible

    @disponible.setter
    def disponible(self, valor):
        self._disponible = bool(valor)

    # Metodos abstractos (En cada hijo)
    @abstractmethod
    def calcular_costo(self, horas):
        "Costo base (sin impuestos ni descuentos)"

    @abstractmethod
    def validar_parametros(self, horas):
        "ServicioInvalidoError si los parametros no son validos"

    @abstractmethod
    def describir(self):
        "Descripcion del servicio"

      # Metodo sobrecargado mediante parametros opcionales
    def calcular_costo_total(self, horas, impuesto=None, descuento=0.0):
        """
        Variantes de uso (sobrecarga en Python con parametros opcionales):
          calcular_costo_total(2)                    -> costo base + IVA 19%
          calcular_costo_total(2, 0.0)               -> costo sin impuesto
          calcular_costo_total(2, 0.19, 0.10)        -> con IVA y 10% de descuento
        """
        self.validar_parametros(horas)
        if impuesto is None:
            impuesto = IVA
        if not 0 <= impuesto <= 1 or not 0 <= descuento < 1:
            raise CalculoInconsistenteError("Impuesto o descuento fuera de rango")
        base = self.calcular_costo(horas)
        total = base * (1 - descuento) * (1 + impuesto)
        if total < 0:
            raise CalculoInconsistenteError("El costo total no puede ser negativo")
        return round(total, 2)

def _validar_horas(horas):
    "Funcion auxiliar de validacion de la duracion"
    if isinstance(horas, bool) or not isinstance(horas, (int, float)):
        raise ServicioInvalidoError(f"Duracion invalida: {horas!r}.")
    if horas <= 0 or horas > 24:
        raise ServicioInvalidoError("La duracion debe estar entre 1 y 24 horas")


class ReservaSala(Servicio):
    def __init__(self, nombre=None, tarifa_hora=None, capacidad=None):
        super().__init__(nombre, tarifa_hora)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ServicioInvalidoError("La capacidad de la sala debe ser un entero positivo")
        self._capacidad = capacidad

    def calcular_costo(self, horas):
        return self._tarifa_hora * horas

    def validar_parametros(self, horas):
        _validar_horas(horas)

    def describir(self):
        return f"Sala '{self.nombre}' (capacidad {self._capacidad}) - ${self._tarifa_hora:,.0f}/hora"


class AlquilerEquipo(Servicio):
    FIANZA = 20000  # Costo fijo de garantia

    def __init__(self, nombre=None, tarifa_hora=None, tipo_equipo=None):
        super().__init__(nombre, tarifa_hora)
        if tipo_equipo is None or str(tipo_equipo).strip() == "":
            raise ParametroFaltanteError("El tipo de equipo es obligatorio")
        self._tipo_equipo = str(tipo_equipo).strip()

    def calcular_costo(self, horas):
        return self._tarifa_hora * horas + self.FIANZA

    def validar_parametros(self, horas):
        _validar_horas(horas)
        if horas > 12:
            raise ServicioInvalidoError("Un equipo no se puede alquilar mas de 12 horas")

    def describir(self):
        return f"Equipo '{self.nombre}' ({self._tipo_equipo}) - ${self._tarifa_hora:,.0f}/hora + fianza"


class AsesoriaEspecializada(Servicio):
    RECARGO = {"junior": 1.0, "senior": 1.5}

    def __init__(self, nombre=None, tarifa_hora=None, nivel="junior"):
        super().__init__(nombre, tarifa_hora)
        nivel = str(nivel).lower()
        if nivel not in self.RECARGO:
            raise ServicioInvalidoError(f"Nivel de asesor invalido: '{nivel}'.")
        self._nivel = nivel

    def calcular_costo(self, horas):
        return self._tarifa_hora * horas * self.RECARGO[self._nivel]

    def validar_parametros(self, horas):
        _validar_horas(horas)
        if horas > 8:
            raise ServicioInvalidoError("Una asesoria no puede superar las 8 horas")

    def describir(self):
        return f"Asesoria '{self.nombre}' (nivel {self._nivel}) - ${self._tarifa_hora:,.0f}/hora"
