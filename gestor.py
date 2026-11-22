"Sistema de gestión: administra las listas internas y captura todos los errores"

"Los clientes, servicios y reservas se guardan en listas de Python, que existen solo mientras el programa se ejecute"

from cliente import Cliente
from excepciones import ErrorSoftwareFJ, OperacionNoPermitidaError, ReservaInvalidaError
from logger import log
from reserva import Reserva


class SistemaGestion:
    def __init__(self):
        # Listas internas donde se guardan los objetos creados
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def _ejecutar(self, descripcion, funcion):
        "Ejecuta una operación de forma segura"

        "Si la operación falla, el error se muestra, se anota en el log y el programa sigue funcionando"
        
        print(f"\n>> {descripcion}")
        try:
            # Cada operación muestra el objeto y un mensaje
            objeto, mensaje = funcion()
        except ErrorSoftwareFJ as error:
            # Error que se tuvo en cuenta
            causa = f" (causa: {error.__cause__})" if error.__cause__ else ""
            print(f"   [Error controlado] {type(error).__name__}: {error}{causa}")
            log.error("%s | %s: %s%s", descripcion, type(error).__name__, error, causa)
        except Exception as error:
            # Error que no se tuvo en cuenta
            print(f"   [Error inesperado] {type(error).__name__}: {error}")
            log.critical("%s | Error inesperado %s: %s", descripcion, type(error).__name__, error)
        else:
            # No hubo errores
            print(f"   [OK] {mensaje}")
            log.info("%s | OK | %s", descripcion, mensaje)
            return objeto
        finally:
            # Siempre se ejecuta, con o sin error
            log.info("Fin de operacion: %s", descripcion)
        return None  # Si hubo error, la operación da none

    def _verificar_reserva(self, reserva):
        "Revisa que se haya recibido una reserva real"
        if not isinstance(reserva, Reserva):
            raise ReservaInvalidaError("No hay una reserva valida para esta operacion")

    def registrar_cliente(self, **datos):
        def accion():
            # Revisa que el documento no esté repetido
            documento = str(datos.get("documento", "")).strip()
            for existente in self.clientes:
                if existente.documento == documento:
                    raise OperacionNoPermitidaError(
                        f"Ya existe un cliente con el documento {documento}")
            cliente = Cliente(**datos)   # Aquí se validan todos los datos
            self.clientes.append(cliente)  # Solo se guarda si no hubo error
            return cliente, cliente.describir()
        return self._ejecutar("Registrar cliente", accion)

    def crear_servicio(self, clase, **datos):
        def accion():
            servicio = clase(**datos)  # Puede ser ReservaSala, AlquilerEquipo
            self.servicios.append(servicio)
            return servicio, servicio.describir()
        return self._ejecutar(f"Crear servicio {clase.__name__}", accion)

    def crear_reserva(self, cliente, servicio, horas):
        def accion():
            reserva = Reserva(cliente, servicio, horas)
            reserva.confirmar()  # La dejamos confirmada
            self.reservas.append(reserva)
            return reserva, reserva.describir()
        return self._ejecutar("Crear y confirmar reserva", accion)

    def cancelar_reserva(self, reserva):
        def accion():
            self._verificar_reserva(reserva)
            reserva.cancelar()
            return reserva, reserva.describir()
        return self._ejecutar("Cancelar reserva", accion)

    def procesar_reserva(self, reserva, descuento=0.0):
        def accion():
            self._verificar_reserva(reserva)
            total = reserva.procesar(descuento)
            return reserva, f"Total a pagar: ${total:,.2f}"
        return self._ejecutar("Procesar reserva", accion)

    def resumen(self):
        "Muestra cuántos objetos hay y el estado final de cada reserva"
        print("\n" + "=" * 60)
        print(f"Resumen: {len(self.clientes)} clientes | {len(self.servicios)} servicios | "
              f"{len(self.reservas)} reservas")
        for reserva in self.reservas:
            print("  -", reserva.describir())
        print("=" * 60)
