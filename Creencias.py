from sc2.units import Units

from enum import Enum


class Creencia:  # clase sin metodos, solo sirve para encapsular datos
    def __init__(self, tipo_creencia):
        self.tipo = tipo_creencia


class TipoCreencia(Enum):
    # Creencia activa si se necesitan más trabajadores
    FALTAN_TRABAJADORES = 1
    # Creencia activa si se necesitan más Supply Depositories (se pueden construir y hay supply escaso)
    FALTAN_SUPP_DEPO = 2
    # Creencia activa durante caso de emergencia (en principio cuando no hay Command Centers)
    SITUACION_DESESPERADA = 3
    # Creencia activa si desconocemos la posicion del enemigo y no se encuentra en su spawn
    ENEMY_MISSING = 4
    # Creencia que indica la unidad enemiga que debe ser atacada prioritariamente
    # valores: Unit
    OBJETIVO_PRIORITARIO = 5
    # Creencia que guarda las fuerzas (CYCLONE) sin ocupar
    # valores: Units
    IDLE_FORCES = 6
    # Creencia activa si se dan las condiciones para construir barracks
    # Y que haya menos de 3
    BARRACON_DISPONIBLE = 7
    # Creencias activa si se dan las condiciones para construir factoria con techlab anexado
    FACTORIA_DISPONIBLE = 8
    TECHLAB_DISPONIBLE = 9
    # Creencia activa si se dan las condiciones para construir reineria de gas
    # y que haya menos de dos y que haya un Barrack (construido o en construccion)
    REFINERIA_DISPONIBLE = 10
    # Creencia activa si se dan las condiciones para entrenar cyclone
    CYCLONE_DISPONIBLE = 11
    # Creencia activa si hay trabajadores sin trabajo
    TRABAJADORES_IDLE = 12
    REFINERIA_SIN_SATURAR = 13


class ObjetivoPrioritario(Creencia):
    def __init__(self, tipo_creencia, unidad):
        super().__init__(tipo_creencia)
        self.valores = [unidad]


class IdleForces(Creencia):
    def __init__(self, tipo_creencia, unidades):
        super().__init__(tipo_creencia)
        if isinstance(unidades, Units):
            self.valores = [unidades]
