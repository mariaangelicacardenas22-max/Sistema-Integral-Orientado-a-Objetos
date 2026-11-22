"Programa principal: Simula las operaciones del sistema (válidas e inválidas)"

"Para ejecutarlo:   python main.py"

from gestor import SistemaGestion
from logger import log
from servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala


def main():
    log.info("Inicio")
    s = SistemaGestion()  # Crea el sistema con sus listas vacias

    # Clientes
    ana = s.registrar_cliente(nombre="Ana Sofia Torres Carreño", documento="1098765432",
                              correo="ana.torres@gmail.com", telefono="3101234567")   # Válido
    luis = s.registrar_cliente(nombre="Luis Andres Perez Trujillo", documento="52345678",
                               correo="luis.perez@gmail.com", telefono="3209876543")  # Válido
    s.registrar_cliente(nombre="Carlos Ruiz", documento="99887766")                   # Inválido: faltan correo y teléfono

    # Servicios 
    # Cada método entrega el objeto creado o None si ocurre un error
    sala = s.crear_servicio(ReservaSala, nombre="Sala Innovacion", tarifa_hora=50000, capacidad=12)                  # Válido
    equipo = s.crear_servicio(AlquilerEquipo, nombre="Portatil Pro", tarifa_hora=15000, tipo_equipo="Computador")    # Válido
    asesoria = s.crear_servicio(AsesoriaEspecializada, nombre="Asesoria Python", tarifa_hora=80000, nivel="Senior")  # Válido
    s.crear_servicio(AsesoriaEspecializada, nombre="Asesoria X", tarifa_hora="Gratis")                               # Inválido: tarifa no numérica

    # Reservas
    r1 = s.crear_reserva(ana, sala, 3)         # Exitosa
    r2 = s.crear_reserva(luis, asesoria, 2)    # Exitosa
    s.crear_reserva(luis, asesoria, 20)        # Falla: asesoría de más de 8 horas
    equipo.disponible = False                  # Dejamos el equipo "no disponible"
    s.crear_reserva(luis, equipo, 2)           # Falla: servicio no disponible

    # Procesar y cancelar
    s.procesar_reserva(r1)                     # Exitosa: total con IVA
    s.procesar_reserva(r2, descuento=1.5)      # Falla: cálculo incorrecto
    s.cancelar_reserva(r2)                     # Exitosa: cancelación correcta
    s.cancelar_reserva(r1)                     # Falla: ya estaba procesada

    s.resumen()
    log.info("Fin")
    print("\nEl programa termino sin interrupciones. Revisa logs/software_fj.log")


# Hace que main() se ejecute solo solo al abrir directamente el archivo
if __name__ == "__main__":
    main()

