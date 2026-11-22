"Clase cliente con validaciones robustas y datos encapsulados"

"Los atributos tienen doble guion bajo para que nadie los cambie desde afuera sin pasar por las validaciones"

import re  # Librería de expresiones regulares para revisar el formato de un texto

from entidad import EntidadBase
from excepciones import ClienteInvalidoError, ParametroFaltanteError


class Cliente(EntidadBase):
    def __init__(self, nombre=None, documento=None, correo=None, telefono=None):
        # Ejecuta automáticamente el "setter" de más abajo, que valida el dato. Si algo está mal, da un error y el cliente no se crea.
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono
        # El identificador se asigna al final. Si hubo error, no se gasta un número.
        super().__init__("Cliente")

    # Nombre
    @property
    def nombre(self):
        "Devuelve el nombre"
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        # Si no escribieron nada, falta un dato obligatorio
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError("El nombre es obligatorio")
        # Quita espacios repetidos
        valor = " ".join(str(valor).split())
        # Solo se permiten letras y espacios
        if not re.fullmatch(r"[A-Za-zÁÉÍÓÚÜáéíóúüÑñ ]+", valor):
            raise ClienteInvalidoError(f"Nombre invalido: '{valor}' (solo letras)")
        # Debe tener al menos 2 palabras de 2 letras o más
        palabras = valor.split(" ")
        if len(palabras) < 2 or any(len(p) < 2 for p in palabras):
            raise ClienteInvalidoError(
                f"Debe ingresar el nombre completo (nombre y apellido): '{valor}'")
        self.__nombre = valor  # Si pasó todo, se guarda

    # Documento
    @property
    def documento(self):
        return self.__documento

    @documento.setter
    def documento(self, valor):
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError("El documento es obligatorio")
        valor = str(valor).strip()
        # Solo números entre 6 y 12 dígitos
        if not valor.isdigit() or not 6 <= len(valor) <= 12:
            raise ClienteInvalidoError(f"Documento invalido: '{valor}' (6 a 12 digitos)")
        self.__documento = valor

    # Correo
    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError("El correo es obligatorio")
        valor = str(valor).strip().lower()  # Lo pasa a minúsculas
        # Acepta varios dominios
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
        # Quita espacios, guiones y paréntesis
        limpio = original
        for simbolo in (" ", "-", "(", ")"):
            limpio = limpio.replace(simbolo, "")
        # Si empieza con "+", se ignora solo para contar los dígitos
        digitos = limpio[1:] if limpio.startswith("+") else limpio
        # Debe tener solo números entre 7 y 15 dígitos
        if not digitos.isdigit() or not 7 <= len(digitos) <= 15:
            raise ClienteInvalidoError(
                f"Telefono invalido: '{original}' (debe tener entre 7 y 15 digitos).")
        self.__telefono = limpio

    def describir(self):
        "Versión propia de describir() para el cliente."
        return f"Cliente #{self.id}: {self.nombre} | Doc: {self.documento} | {self.correo}"

