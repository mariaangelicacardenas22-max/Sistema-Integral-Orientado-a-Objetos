"Sistema de gestion que administra listas internas y captura todos los errores"
from cliente import Cliente
from excepciones import ErrorSoftwareFJ
from logger import log
from reserva import Reserva


class SistemaGestion:
    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def _ejecutar(self, descripcion, funcion):
        "Ejecuta una operacion. Si falla, registra el error y el programa sigue"
        print(f"\n>> {descripcion}")
        try:
            objeto, mensaje = funcion()   # Cada acción entrega un objeto y un mensaje.
        except ErrorSoftwareFJ as error:
            causa = f" (causa: {error.__cause__})" if error.__cause__ else ""
            print(f"   [ERROR CONTROLADO] {type(error).__name__}: {error}{causa}")
            log.error("%s | %s: %s%s", descripcion, type(error).__name__, error, causa)
        except Exception as error:  # Error inesperado que no detiene el sistema
            print(f"   [ERROR INESPERADO] {type(error).__name__}: {error}")
            log.critical("%s | Error inesperado %s: %s", descripcion, type(error).__name__, error)
        else:
            print(f"   [OK] {mensaje}")
            log.info("%s | OK | %s", descripcion, mensaje)
            return objeto
        finally:
            log.info("Fin de operacion: %s", descripcion)
        return None

    def registrar_cliente(self, **datos):
        def accion():
            cliente = Cliente(**datos)
            self.clientes.append(cliente)
            return cliente, cliente.describir()
        return self._ejecutar("Registrar cliente", accion)

    def crear_servicio(self, clase, **datos):
        def accion():
            servicio = clase(**datos)
            self.servicios.append(servicio)
            return servicio, servicio.describir()
        return self._ejecutar(f"Crear servicio {clase.__name__}", accion)

    def crear_reserva(self, cliente, servicio, horas):
        def accion():
            reserva = Reserva(cliente, servicio, horas)
            reserva.confirmar()
            self.reservas.append(reserva)
            return reserva, reserva.describir()
        return self._ejecutar("Crear y confirmar reserva", accion)

    def cancelar_reserva(self, reserva):
        return self._ejecutar("Cancelar reserva", lambda: (reserva, (reserva.cancelar(), reserva.describir())[1]))

    def procesar_reserva(self, reserva, descuento=0.0):
        return self._ejecutar("Procesar reserva", lambda: (reserva, f"Total a pagar: ${reserva.procesar(descuento):,.2f}"))

    def resumen(self):
        print("\n" + "=" * 60)
        print(f"RESUMEN: {len(self.clientes)} clientes | {len(self.servicios)} servicios | "
              f"{len(self.reservas)} reservas")
        for reserva in self.reservas:
            print("  -", reserva.describir())
        print("=" * 60)
