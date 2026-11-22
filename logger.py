"Configuracion del archivo de logs"
import logging
import os

RUTA_LOG = os.path.join("logs", "software_fj.log")


def obtener_logger():
    "Devuelve el logger del sistema. Crea la carpeta y el archivo si no existen"
    os.makedirs("logs", exist_ok=True)
    logger = logging.getLogger("software_fj")
    if not logger.handlers:  # Evita repetir funciones que gestionan acciones
        logger.setLevel(logging.INFO)
        manejador = logging.FileHandler(RUTA_LOG, encoding="utf-8")
        formato = logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s")
        manejador.setFormatter(formato)
        logger.addHandler(manejador)
    return logger


log = obtener_logger()
