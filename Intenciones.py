from enum import Enum
import Deseos
from Creencias import TipoCreencia
from sc2.unit import Unit
from sc2.bot_ai import BotAI
from sc2.ids.unit_typeid import UnitTypeId


class Intencion:

    def __init__(self):
        self.conceptos = None
        self.tipo = None
        self.deseo = None
        self.coste = 0
        self.urgencia = 0
        self.prioridad = 0

    # ------------------ "async" necesario para "await" --------------
    """async def ejecuta(self):
        """

    def calcular_prioridad(self, creencias, estado_del_mundo: BotAI):
        self.prioridad = self.urgencia - self.coste
        return True

    def comprobar_alcanzada(self, creencias):
        return False


class TipoIntencion(Enum):

    ALL_IN = 1
    ATACAR_OBJETIVO_TROPLA_IDLE = 2
    CREAR_TRABAJADORES = 3
    CREAR_SUPPLY_DEPO = 4
    CREAR_BARRACK = 5
    CREAR_REFINERIA_DE_GAS = 6
    CREAR_FACTORY = 7
    ENTRENAR_CYCLON = 8
    SATURAR_GEYSER = 9
    OCUPAR_TRABAJADORES = 10
    ESPERAR = 11
    CREAR_TECHLAB = 12


class IntencionAllIn(Intencion):

    def __init__(self, target: Unit):
        super().__init__()
        self.conceptos = target
        self.tipo = TipoIntencion.ALL_IN
        self.deseo = Deseos.AllIn()
        self.coste = 0
        self.urgencia = 0
        self.posteriores = []
        self.prioridad = 0


class IntencionIdleAllIn(Intencion):

    def __init__(self, target: Unit):
        super().__init__()
        self.conceptos = target
        self.tipo = TipoIntencion.ATACAR_OBJETIVO_TROPLA_IDLE
        self.deseo = Deseos.IdleAllIn()

    def comprobar_alcanzada(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.IDLE_FORCES:
                return False
        return True

class CrearBarrack(Intencion):

    def __init__(self):
        super().__init__()
        self.tipo = TipoIntencion.CREAR_BARRACK
        self.deseo = Deseos.MejorarEstructuras()
        self.urgencia = 1

    def comprobar_alcanzada(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.BARRACON_DISPONIBLE:
                return False
        return True


class CrearSupplyDepo(Intencion):

    def __init__(self):
        super().__init__()
        self.tipo = TipoIntencion.CREAR_SUPPLY_DEPO
        self.deseo = Deseos.MejorarEstructuras()

    def comprobar_alcanzada(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.FALTAN_SUPP_DEPO:
                return False
        return True


class IntencionCrearEdificio(Intencion):

    def __init__(self, tipointencion):
        super().__init__()
        self.tipo = tipointencion
        self.deseo = Deseos.MejorarEstructuras()

class CrearRefineriaDeGas(IntencionCrearEdificio):

    def __init__(self):
        super().__init__(TipoIntencion.CREAR_REFINERIA_DE_GAS)

    def comprobar_alcanzada(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.REFINERIA_DISPONIBLE:
                return False
        return True


class CrearFactory(IntencionCrearEdificio):

    def __init__(self):
        super().__init__(TipoIntencion.CREAR_FACTORY)

    def comprobar_alcanzada(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.FACTORIA_DISPONIBLE:
                return False
        return True

    # Prioridad negativa mientras haya otra factoria sin techlab
    def calcular_prioridad(self, creencias, estado_del_mundo):
        for refineria in estado_del_mundo.structures(UnitTypeId.FACTORY).ready:
            if not refineria.has_add_on:
                self.urgencia = -1
        self.prioridad = self.urgencia - self.coste
        return True

class CrearTechlab(IntencionCrearEdificio):
    def __init__(self):
        super().__init__(TipoIntencion.CREAR_TECHLAB)

    def comprobar_alcanzada(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.TECHLAB_DISPONIBLE:
                return False
        return True

class EntrenarCyclone(IntencionCrearEdificio):

    def __init__(self):
        super().__init__(TipoIntencion.ENTRENAR_CYCLON)
        self.urgencia = 1

    def comprobar_alcanzada(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.CYCLONE_DISPONIBLE:
                return False
        return True


class EntrenarTrabajadores(Intencion):

    def __init__(self):
        super().__init__()
        self.tipo = TipoIntencion.CREAR_TRABAJADORES
        self.deseo = Deseos.EntrenarTropas()

    def comprobar_alcanzada(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.FALTAN_TRABAJADORES:
                return False
        return True


class OcuparTrabajadores(Intencion):

    def __init__(self):
        super().__init__()
        self.tipo = TipoIntencion.OCUPAR_TRABAJADORES
        self.deseo = Deseos.OcuparObreros()

    def comprobar_alcanzada(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.TRABAJADORES_IDLE:
                return False
        return True


class SaturarGayser(Intencion):

    def __init__(self):
        super().__init__()
        self.tipo = TipoIntencion.SATURAR_GEYSER
        self.deseo = Deseos.SaturarFacorias()

    def comprobar_alcanzada(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.REFINERIA_SIN_SATURAR:
                return False
        return True


class Esperar(Intencion):

    def __init__(self):
        super().__init__()
        self.tipo = TipoIntencion.ESPERAR
        self.deseo = Deseos.OcuparObreros()
        self.urgencia = -1
        self.prioridad = -1
