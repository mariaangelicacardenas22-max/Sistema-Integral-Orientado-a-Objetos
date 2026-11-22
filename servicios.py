"Clase abstracta servicio y tres servicios especializados"

"Reciben todo lo que servicio ya tiene"

"Los tres tienen los mismos métodos pero cada uno los hace a su manera"

from abc import abstractmethod

from entidad import EntidadBase
from excepciones import (CalculoInconsistenteError, ParametroFaltanteError,
                         ServicioInvalidoError)

IVA = 0.19  # Impuesto del 19%


class Servicio(EntidadBase):
    "Define lo que TODO servicio debe tener y hacer"

    def __init__(self, nombre=None, tarifa_hora=None):
        # S validan los datos.
        if nombre is None or str(nombre).strip() == "":
            raise ParametroFaltanteError("El nombre del servicio es obligatorio")
        try:
            tarifa_hora = float(tarifa_hora)  # Intenta convertir a número
        except (TypeError, ValueError) as error:
            # Encadenamiento de excepciones, guarda el error original
            raise ServicioInvalidoError("La tarifa debe ser un numero") from error
        if tarifa_hora <= 0:
            raise ServicioInvalidoError("La tarifa por hora debe ser mayor que 0")

        # Si todo está bien, se guardan los datos.
        # Un solo guion bajo  indica que son atributos protegidos
        self._nombre = str(nombre).strip()
        self._tarifa_hora = tarifa_hora
        self._disponible = True
        # El identidicador se asigna al final.
        # Si hubo error antes, no se gasta un número.
        super().__init__("Servicio")

    @property
    def nombre(self):
        return self._nombre

    @property
    def disponible(self):
        return self._disponible

    @disponible.setter
    def disponible(self, valor):
        self._disponible = bool(valor)  # Siempre guarda True o False

    # Cada servicio hijo debe escribir los suyos
    @abstractmethod
    def calcular_costo(self, horas):
        "Costo base (sin impuestos ni descuentos)"

    @abstractmethod
    def validar_parametros(self, horas):
        "Invalido si las horas no son válidas"

    @abstractmethod
    def describir(self):
        "Descripción del servicio en texto"

    # Metodo sobrecargado
    def calcular_costo_total(self, horas, impuesto=None, descuento=0.0):
        self.validar_parametros(horas)  # Cada hijo valida a su manera 
        if impuesto is None:  # Si no mandaron impuesto, usamos el IVA normal
            impuesto = IVA
        # El impuesto va de 0 a 1 (0% a 100%) y el descuento de 0 a menos de 1
        if not 0 <= impuesto <= 1 or not 0 <= descuento < 1:
            raise CalculoInconsistenteError("Impuesto o descuento fuera de rango")
        base = self.calcular_costo(horas)  # Cada hijo calcula su costo base
        total = base * (1 - descuento) * (1 + impuesto)
        if total < 0:
            raise CalculoInconsistenteError("El costo total no puede ser negativo")
        return round(total, 2)


def _validar_horas(horas):
    "Revisa reglas de las horas que sirven para todos los servicios"
    # bool se excluye porque en Python True cuenta como número (True == 1)
    if isinstance(horas, bool) or not isinstance(horas, (int, float)):
        raise ServicioInvalidoError(f"Duracion invalida: {horas!r}.")
    if horas <= 0 or horas > 24:
        raise ServicioInvalidoError("La duracion debe ser mayor que 0 y maximo 24 horas")


class ReservaSala(Servicio):
    "Reserva de salas. Se cobra solo por hora"

    def __init__(self, nombre=None, tarifa_hora=None, capacidad=None):
        # Se valida el dato propio de la sala antes para no gastar un identificador si hay un error
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ServicioInvalidoError("La capacidad de la sala debe ser un entero positivo")
        super().__init__(nombre, tarifa_hora)  # Valida y guarda nombre y tarifa
        self._capacidad = capacidad

    def calcular_costo(self, horas):
        return self._tarifa_hora * horas

    def validar_parametros(self, horas):
        _validar_horas(horas)

    def describir(self):
        return f"Sala '{self.nombre}' (capacidad {self._capacidad}) - ${self._tarifa_hora:,.0f}/hora"


class AlquilerEquipo(Servicio):
    "Alquiler de equipos. Se cobra por hora más una fianza fija"

    FIANZA = 20000  # Costo fijo de garantía

    def __init__(self, nombre=None, tarifa_hora=None, tipo_equipo=None):
        if tipo_equipo is None or str(tipo_equipo).strip() == "":
            raise ParametroFaltanteError("El tipo de equipo es obligatorio")
        super().__init__(nombre, tarifa_hora)
        self._tipo_equipo = str(tipo_equipo).strip()

    def calcular_costo(self, horas):
        return self._tarifa_hora * horas + self.FIANZA

    def validar_parametros(self, horas):
        _validar_horas(horas)  # Reglas generales
        if horas > 12:         # Regla propia del equipo
            raise ServicioInvalidoError("Un equipo no se puede alquilar mas de 12 horas")

    def describir(self):
        return f"Equipo '{self.nombre}' ({self._tipo_equipo}) - ${self._tarifa_hora:,.0f}/hora + fianza"


class AsesoriaEspecializada(Servicio):
    "Asesorías. El asesor senior cobra 50% más que el junior."

    RECARGO = {"junior": 1.0, "senior": 1.5}  # Multiplicador según el nivel

    def __init__(self, nombre=None, tarifa_hora=None, nivel="junior"):
        nivel = str(nivel).lower()
        if nivel not in self.RECARGO:
            raise ServicioInvalidoError(f"Nivel de asesor invalido: '{nivel}'.")
        super().__init__(nombre, tarifa_hora)
        self._nivel = nivel

    def calcular_costo(self, horas):
        return self._tarifa_hora * horas * self.RECARGO[self._nivel]

    def validar_parametros(self, horas):
        _validar_horas(horas)  # Reglas generales
        if horas > 8:          # Regla propia de la asesoría
            raise ServicioInvalidoError("Una asesoria no puede superar las 8 horas")

    def describir(self):
        return f"Asesoria '{self.nombre}' (nivel {self._nivel}) - ${self._tarifa_hora:,.0f}/hora"

