"Clase Cliente con validaciones robustas y datos encapsulados"
import re

from entidad import EntidadBase
from excepciones import ClienteInvalidoError, ParametroFaltanteError


class Cliente(EntidadBase):
    def __init__(self, nombre=None, documento=None, correo=None, telefono=None):
        super().__init__()
        # Verifican los datos y generan una excepción si hay errores
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono

    # Nombre
    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError("El nombre es obligatorio")
        valor = " ".join(str(valor).split())  # quita espacios repetidos
        if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ ]+", valor):
            raise ClienteInvalidoError(f"Nombre invalido: '{valor}' (solo letras).")
        palabras = valor.split(" ")
        if len(palabras) < 2 or any(len(p) < 2 for p in palabras):
            raise ClienteInvalidoError(
                f"Debe ingresar el nombre completo (nombre y apellido): '{valor}'.")
        self.__nombre = valor

    # Documento
    @property
    def documento(self):
        return self.__documento

    @documento.setter
    def documento(self, valor):
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError("El documento es obligatorio")
        valor = str(valor).strip()
        if not valor.isdigit() or not 6 <= len(valor) <= 12:
            raise ClienteInvalidoError(f"Documento invalido: '{valor}' (6 a 12 digitos).")
        self.__documento = valor

    # Correo
    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError("El correo es obligatorio")
        valor = str(valor).strip().lower()
        # Acepta cualquier dominio: gmail, hotmail, outlook, yahoo, institucionales, etc.
        if not re.fullmatch(r"[a-z0-9._+-]+@[a-z0-9-]+(\.[a-z0-9-]+)*\.[a-z]{2,}", valor):
            raise ClienteInvalidoError(
                f"Correo invalido: '{valor}' (formato esperado: usuario@dominio.com).")
        self.__correo = valor

    # Telefono
    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError("El telefono es obligatorio")
        original = str(valor).strip()
        # Acepta celulares, fijos e internacionales
        # Permite espacios, guiones, parentesis y un "+" inicial
        limpio = original
        for simbolo in (" ", "-", "(", ")"):
            limpio = limpio.replace(simbolo, "")
        digitos = limpio[1:] if limpio.startswith("+") else limpio
        if not digitos.isdigit() or not 7 <= len(digitos) <= 15:
            raise ClienteInvalidoError(
                f"Telefono invalido: '{original}' (debe tener entre 7 y 15 digitos).")
        self.__telefono = limpio

    def describir(self):
        return f"Cliente #{self.id}: {self.nombre} | Doc: {self.documento} | {self.correo}"
