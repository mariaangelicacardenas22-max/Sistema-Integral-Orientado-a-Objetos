"Configuración del archivo de logs"

"Archivo de texto donde el programa anota todo lo que pasa con la fecha y la hora"

import logging
import os

# Ruta del archivo
RUTA_LOG = os.path.join("logs", "software_fj.log")


def obtener_logger():
    "Crea y muestra el encargado de registrar en el archivo de log"
    # Crea la carpeta logs si no existe
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger("software_fj")

    # Se configura la primera vez. Si no cada mensaje se escribiría repetido en el archivo.
    if not logger.handlers:
        logger.setLevel(logging.INFO)  # Guarda mensajes desde nivel INFO hacia arriba
        manejador = logging.FileHandler(RUTA_LOG, encoding="utf-8")  # Dónde escribir
        # Formato de cada línea
        formato = logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s")
        manejador.setFormatter(formato)
        logger.addHandler(manejador)
    return logger


# Crea el logger una sola vez. Los demás archivos lo importan
log = obtener_logger()
