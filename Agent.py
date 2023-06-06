from sc2.bot_ai import BotAI
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId
from sc2.position import Point2
from sc2.unit import Unit
from sc2.units import Units

import Intenciones
from Creencias import Creencia
from Creencias import TipoCreencia
import Creencias

from Intenciones import Intencion
from Intenciones import TipoIntencion

from Deseos import Deseo
import Deseos


class JugadorAgent(BotAI):

    def __init__(self):
        self.misCreencias = []
        self.misDeseos: [Deseo] = [Deseos.OcuparObreros(), Deseos.EntrenarTropas(), Deseos.IdleAllIn(),
                                   Deseos.MejorarEstructuras(), Deseos.AllIn(), Deseos.SaturarFacorias()]
        self.misIntenciones: [Intencion] = [Intenciones.Esperar()]

    def actualiza_creencias(self):
        self.misCreencias.clear()

        if self.townhalls(UnitTypeId.COMMANDCENTER):
            if (
                self.can_afford(UnitTypeId.SCV)
                and self.supply_workers + self.already_pending(UnitTypeId.SCV) < 22
                and self.townhalls(UnitTypeId.COMMANDCENTER).first.is_idle
            ):
                self.misCreencias.append(Creencia(TipoCreencia.FALTAN_TRABAJADORES))

        # No hay Command Centre aliado
        if (
               not self.townhalls(UnitTypeId.COMMANDCENTER)
        ):
            self.misCreencias.append(Creencia(TipoCreencia.SITUACION_DESESPERADA))
        unidades_enemigas = self.enemy_units
        estructuras_enemigas = self.enemy_structures

        # Si hay estructuras enemigas a la vista, escoger una aleatoria
        if (
                estructuras_enemigas
        ):
            self.misCreencias.append(Creencias.ObjetivoPrioritario(TipoCreencia.OBJETIVO_PRIORITARIO,
                                                                   estructuras_enemigas.random))

        # Si no hay estructuras pero sí hay unidades enemigas a la vista, escoger una aleatoria
        elif (
                unidades_enemigas
        ):
            self.misCreencias.append(Creencias.ObjetivoPrioritario(TipoCreencia.OBJETIVO_PRIORITARIO,
                                                                   unidades_enemigas.random))

        # No hay unidades ni estructuras enemigas a la vista y hay alguna unidad junto al Start Location enemigo
        # Objetivo: un campo aleatorio de minerales
        elif (
                min((unit.distance_to(self.enemy_start_locations[0]) for unit in self.units)) <= 5
        ):
            self.misCreencias.append(Creencia(TipoCreencia.ENEMY_MISSING))
            self.misCreencias.append(Creencias.ObjetivoPrioritario(TipoCreencia.OBJETIVO_PRIORITARIO,
                                                                   self.mineral_field.random.position))

        # No hay unidades ni estructuras enemigas a la vista y NO hay alguna unidad junto al Start Location enemigo
        # Objetivo: Start Location enemigo
        else:
            self.misCreencias.append(Creencias.ObjetivoPrioritario(TipoCreencia.OBJETIVO_PRIORITARIO,
                                                                   self.enemy_start_locations[0]))

        # Si hay algun CYCLONE libre
        if self.units(UnitTypeId.CYCLONE).idle:
            self.misCreencias.append(Creencias.IdleForces(TipoCreencia.IDLE_FORCES,
                                                          self.units(UnitTypeId.CYCLONE).idle))

        # Estamos escasos de supply, nos lo podemos permitir y no hay supply depos en cola
        if self.supply_left < 3:
            if self.can_afford(UnitTypeId.SUPPLYDEPOT) and self.already_pending(UnitTypeId.SUPPLYDEPOT) < 2:
                self.misCreencias.append(Creencia(TipoCreencia.FALTAN_SUPP_DEPO))

        for refineria in self.gas_buildings:
            if refineria.ideal_harvesters > refineria.assigned_harvesters:
                self.misCreencias.append(Creencia(TipoCreencia.REFINERIA_SIN_SATURAR))

        # Si tenemos supply depots., no tenemos barracones y podemos permitirnoslos
        if self.structures(UnitTypeId.SUPPLYDEPOT):
            if not self.structures(UnitTypeId.BARRACKS) and self.can_afford(UnitTypeId.BARRACKS):
                self.misCreencias.append(Creencia(TipoCreencia.BARRACON_DISPONIBLE))

            # Si tenemos barracones y menos de 2 refinerias
            elif(
                    self.structures(UnitTypeId.BARRACKS)
                    and self.gas_buildings.amount < 2
                    and self.can_afford(UnitTypeId.REFINERY)
            ):
                self.misCreencias.append(Creencia(TipoCreencia.REFINERIA_DISPONIBLE))

            if (
                    self.structures(UnitTypeId.BARRACKS).ready  # Tenemos un barracon
                    and self.structures(UnitTypeId.FACTORY).amount < 2  # Menos de 3 facorias
                    and not self.already_pending(UnitTypeId.FACTORY)
                    and self.can_afford(UnitTypeId.FACTORY)  # Podemos permitirnoslo
            ):
                self.misCreencias.append(Creencia(TipoCreencia.FACTORIA_DISPONIBLE))

            for factoria in self.structures(UnitTypeId.FACTORY).ready:
                if (
                        not factoria.has_add_on  # Si hay alguna factoria sin techlab
                        and self.can_afford(UnitTypeId.TECHLAB)  # Podemos permitirnos un techlab
                ):
                    self.misCreencias.append(Creencia(TipoCreencia.TECHLAB_DISPONIBLE))

        # Si hay una factoria disponible y desocupada y tenemos recursos, CYCLONE disponible
        for factoria in self.structures(UnitTypeId.FACTORY).ready.idle:
            if self.can_afford(UnitTypeId.CYCLONE) and factoria.has_techlab:
                self.misCreencias.append(Creencia(TipoCreencia.CYCLONE_DISPONIBLE))

        if self.workers.idle:
            self.misCreencias.append(Creencia(TipoCreencia.TRABAJADORES_IDLE))

        if len(self.misCreencias) > 1:
            print("creenacias: ", end='')
            for c in self.misCreencias:
                if c.tipo != TipoCreencia.OBJETIVO_PRIORITARIO:
                    print(c.tipo, end=' ')
            print("")

    def actualiza_deseos(self):
        for d in self.misDeseos:
            if d.activo:
                if d.comprobar_satisfecho(self.misCreencias):
                    d.activo = False
                    d.intenciones = []
                pass
            elif d.comprobaractivar(self.misCreencias):
                for nuevaIntencion in d.intenciones:
                    self.misIntenciones.append(nuevaIntencion)
                d.activo = True

    def actualiza_intenciones(self):
        for i in self.misIntenciones:
            if i.comprobar_alcanzada(self.misCreencias):
                # quita la intencion actual de la lista de intenciones del agente
                self.misIntenciones.remove(i)
            if i.comprobar_anulada(self.misCreencias):
                self.misIntenciones.remove(i)

    def calcula_prioridades(self):
        for i in self.misIntenciones:
            i.calcularprioridad(self.misCreencias, self)
        pass

    def elige_intencion(self) -> Intencion:
        maximaprioridad = -2
        intencion_a_ejecutar = self.misIntenciones[0]
        for i in self.misIntenciones:
            if i.tipo != TipoIntencion.ESPERAR:
                print(i.tipo, " prioridad: ", i.prioridad, " ")
            if i.prioridad > maximaprioridad and i.comprobar_posible(self.misCreencias):
                maximaprioridad = i.prioridad
                intencion_a_ejecutar = i
        return intencion_a_ejecutar

    async def on_step(self, iteration):
        self.actualiza_creencias()
        self.actualiza_deseos()  # con las creencias cambiadas en el paso anterior
        # con las creencias cambiadas en el paso primero, incluidas las intenciones añadidas en el paso anterior
        self.actualiza_intenciones()
        self.calcula_prioridades()  # de las intenciones
        await self.ejecuta_intencion(self.elige_intencion())  # ejecuta la de mayor prioridad

    async def ejecuta_intencion(self, intencion):

        if intencion.tipo != TipoIntencion.ESPERAR:
            print("intencion a ejecutar: ", intencion.tipo)

        if intencion.tipo == TipoIntencion.ALL_IN:
            target = intencion.conceptos.position
            for unit in self.workers | self.units(UnitTypeId.CYCLONE):
                unit.attack(target)

        elif intencion.tipo == TipoIntencion.ATACAR_OBJETIVO_TROPLA_IDLE:
            target = intencion.conceptos.position
            for unit in self.units(UnitTypeId.CYCLONE).idle:
                unit.attack(target)

        if self.townhalls(UnitTypeId.COMMANDCENTER):
            cc = self.townhalls(UnitTypeId.COMMANDCENTER).first
        else:
            cc = None
            print("NO CC")

        if intencion.tipo == TipoIntencion.CREAR_REFINERIA_DE_GAS and cc:
            gaysers = self.vespene_geyser.closer_than(10, cc)
            for gayser in gaysers:
                if self.gas_buildings.filter(lambda unidad: unidad.distance_to(gayser) < 1):
                    continue  # Ignorar gayser con refineria encima
                # Seleccionamos el trabajador mas cercano al gayser
                trabajador: Unit = self.select_build_worker(gayser)
                # trabajador puede ser none en caso de que esten todos muertos
                if trabajador is None:
                    continue
                trabajador.build_gas(gayser)

        if intencion.tipo == TipoIntencion.SATURAR_GEYSER:
            for refinery in self.gas_buildings:
                if refinery.ideal_harvesters - refinery.assigned_harvesters > 0:
                    workers: Units = self.workers.closer_than(20, refinery)
                    if workers:
                        workers.random.gather(refinery)
                    else:
                        print("no workers")

        elif intencion.tipo == TipoIntencion.CREAR_BARRACK and cc:
            print("creando barrac¿?: ", end=" ")
            print(self.can_afford(UnitTypeId.BARRACKS))
            print(await self.build(UnitTypeId.BARRACKS, near=cc.position.towards(self.game_info.map_center, 12)))

        elif intencion.tipo == TipoIntencion.CREAR_FACTORY and cc:
            position: Point2 = cc.position.towards_with_random_angle(self.game_info.map_center, 16)
            await self.build(UnitTypeId.FACTORY, near=position)

        elif intencion.tipo == TipoIntencion.CREAR_TECHLAB and cc:
            for factoria in self.structures(UnitTypeId.FACTORY).ready:
                if not factoria.has_add_on and self.can_afford(UnitTypeId.TECHLAB):
                    factoria(AbilityId.BUILD_TECHLAB_FACTORY)

        elif intencion.tipo == TipoIntencion.CREAR_SUPPLY_DEPO and cc:
            await self.build(UnitTypeId.SUPPLYDEPOT, near=cc.position.towards(self.game_info.map_center, 8))

        elif intencion.tipo == TipoIntencion.ENTRENAR_CYCLON:
            for factory in self.structures(UnitTypeId.FACTORY).ready.idle:
                if self.can_afford(UnitTypeId.CYCLONE) and factory.has_techlab:
                    factory.train(UnitTypeId.CYCLONE)

        elif intencion.tipo == TipoIntencion.CREAR_TRABAJADORES and cc:
            cc.train(UnitTypeId.SCV)

        elif intencion.tipo == TipoIntencion.OCUPAR_TRABAJADORES and cc:
            # Los obreros que sobran minan minerales
            for scv in self.workers.idle:
                scv.gather(self.mineral_field.closest_to(cc))
