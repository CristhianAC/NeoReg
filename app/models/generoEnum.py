from enum import Enum


class Genero(str, Enum):
    masculino = "Masculino"
    femenino = "Femenino"
    no_binario = "No binario"
    prefiero_no_reportar = "Prefiero no reportar"