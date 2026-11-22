"Simulacion de 12 operaciones del sistema (validas e invalidas)."
from gestor import SistemaGestion
from logger import log
from servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala


def main():
    log.info("Inicio")
    s = SistemaGestion()

    # Clientes (2 validos, 2 invalidos)
    ana = s.registrar_cliente(nombre="Ana Sofia Torres Carreño", documento="1098765432", correo="ana.torres@gmail.com", telefono="3101234567")
    luis = s.registrar_cliente(nombre="Luis Andres Perez Trujillo", documento="52345678", correo="luis.perez@gmail.com", telefono="3209876543")
    s.registrar_cliente(nombre="Pedro", documento="256", correo="pedro@hotmail.com", telefono="3001234567")  # invalido
    s.registrar_cliente(nombre="Carlos Ruiz", documento="99887766")                           # faltan datos 

    # Servicios (3 validos, varios invalidos)
    s.crear_servicio(ReservaSala, nombre="Sala Innovacion", tarifa_hora=50000, capacidad=12)
    s.crear_servicio(AlquilerEquipo, nombre="Portatil Pro", tarifa_hora=15000, tipo_equipo="Computador")
    s.crear_servicio(AsesoriaEspecializada, nombre="Asesoria Python", tarifa_hora=80000, nivel="senior")
    s.crear_servicio(ReservaSala, nombre="Sala Rota", tarifa_hora=-5, capacidad=10)            # invalido
    s.crear_servicio(AsesoriaEspecializada, nombre="Asesoria X", tarifa_hora="gratis")        # invalido

    sala, equipo, asesoria = s.servicios[0], s.servicios[1], s.servicios[2]

    # Reservas exitosas y fallidas
    r1 = s.crear_reserva(ana, sala, 3)                  # exitosa
    s.crear_reserva(luis, asesoria, 20)                 # falla: asesoria > 8 horas
    s.crear_reserva("no soy cliente", equipo, 2)        # falla: cliente invalido
    equipo.disponible = False
    s.crear_reserva(luis, equipo, 2)                    # falla: servicio no disponible
    equipo.disponible = True
    r2 = s.crear_reserva(luis, asesoria, 2)             # exitosa

    s.procesar_reserva(r1)                              # exitosa con IVA
    s.procesar_reserva(r1)                              # falla: ya procesada
    s.procesar_reserva(r2, descuento=0.10)              # exitosa con descuento
    s.cancelar_reserva(r2)                              # falla: ya procesada

    s.resumen()
    log.info("Fin")
    print("\nEl programa termino sin interrupciones. Revisa logs/software_fj.log")


if __name__ == "__main__":
    main()
