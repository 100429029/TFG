from enum import Enum

from Creencias import TipoCreencia

import Intenciones


class Deseo:

    def __init__(self):

        self.tipo = None
        self.activo = False
        self.conceptos = None
        self.intenciones = []

    def comprobar_satisfecho(self, creencias):
        for intencion in self.intenciones:
            if not intencion.comprobar_alcanzada(creencias):
                return False
        return True


class TipoDeseo(Enum):

    DEFENDER = 1
    ALL_IN = 2
    MEJORAR_ESTRUCTURAS = 3
    ENTRENAR_TROPAS = 4
    OCUPAR_OBREROS = 5
    IDLE_ALL_IN = 6
    SATURAR_FACTORIAS = 7


class AllIn(Deseo):
    def __init__(self):
        super().__init__()
        self.intenciones = []
        self.conceptos = []
        self.activo = False
        self.tipo = TipoDeseo.ALL_IN

    def comprobaractivar(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.SITUACION_DESESPERADA:
                for creencia_objetivo_prioritario in creencias:
                    if creencia_objetivo_prioritario.tipo == TipoCreencia.OBJETIVO_PRIORITARIO:
                        self.intenciones.append(Intenciones.IntencionAllIn(creencia_objetivo_prioritario.valores[0]))
                    return True
        return False


class IdleAllIn(Deseo):

    def __init__(self):
        super().__init__()
        self.intenciones = []
        self.conceptos = []
        self.activo = False
        self.tipo = TipoDeseo.IDLE_ALL_IN

    def comprobaractivar(self, creencias):
        for c in creencias:
            if c.tipo == TipoCreencia.IDLE_FORCES:
                # Si hay mas de dos unidades pasivas
                if c.valores[0].amount >= 3:
                    for creencia_objetivo_prioritario in creencias:
                        if creencia_objetivo_prioritario.tipo == TipoCreencia.OBJETIVO_PRIORITARIO:
                            self.intenciones.append(
                                Intenciones.IntencionIdleAllIn(creencia_objetivo_prioritario.valores[0]))
                            return True
        return False


class MejorarEstructuras(Deseo):

    def __init__(self):
        super().__init__()
        self.intenciones = []
        self.conceptos = []
        self.activo = False
        self.tipo = TipoDeseo.MEJORAR_ESTRUCTURAS

    def comprobaractivar(self, creencias):
        activar = False
        for c in creencias:
            if c.tipo == TipoCreencia.FACTORIA_DISPONIBLE:
                activar = True
                self.intenciones.append(Intenciones.CrearFactory())
            elif c.tipo == TipoCreencia.REFINERIA_DISPONIBLE:
                activar = True
                self.intenciones.append(Intenciones.CrearRefineriaDeGas())
            elif c.tipo == TipoCreencia.BARRACON_DISPONIBLE:
                activar = True
                self.intenciones.append(Intenciones.CrearBarrack())
            elif c.tipo == TipoCreencia.FALTAN_SUPP_DEPO:
                activar = True
                self.intenciones.append(Intenciones.CrearSupplyDepo())
            elif c.tipo == TipoCreencia.TECHLAB_DISPONIBLE:
                activar = True
                self.intenciones.append(Intenciones.CrearTechlab())
        return activar


class EntrenarTropas(Deseo):

    def __init__(self):
        super().__init__()
        self.intenciones = []
        self.conceptos = []
        self.activo = False
        self.tipo = TipoDeseo.ENTRENAR_TROPAS

    def comprobaractivar(self, creencias):
        activar = False
        for c in creencias:
            if c.tipo == TipoCreencia.CYCLONE_DISPONIBLE:
                self.intenciones.append(Intenciones.EntrenarCyclone())
                activar = True
            elif c.tipo == TipoCreencia.FALTAN_TRABAJADORES:
                self.intenciones.append(Intenciones.EntrenarTrabajadores())
                activar = True
        return activar


class OcuparObreros(Deseo):

    def __init__(self):
        super().__init__()
        self.intenciones = []
        self.conceptos = []
        self.activo = False
        self.tipo = TipoDeseo.OCUPAR_OBREROS

    def comprobaractivar(self, creencias):
        activar = False
        for c in creencias:
            if c.tipo == TipoCreencia.TRABAJADORES_IDLE:
                self.intenciones.append(Intenciones.OcuparTrabajadores())
                activar = True
        return activar


class SaturarFacorias(Deseo):

    def __init__(self):
        super().__init__()
        self.intenciones = []
        self.conceptos = []
        self.activo = False
        self.tipo = TipoDeseo.SATURAR_FACTORIAS

    def comprobaractivar(self, creencias):
        activar = False
        for c in creencias:
            if c.tipo == TipoCreencia.REFINERIA_SIN_SATURAR:
                self.intenciones.append(Intenciones.SaturarGayser())
                activar = True
        return activar

