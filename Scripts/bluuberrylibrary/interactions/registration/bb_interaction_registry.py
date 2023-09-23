"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Callable, Any, Dict, List

from bluuberrylibrary.classes.bb_singleton import BBSingleton
from bluuberrylibrary.interactions.registration.handlers.bb_interaction_handler import BBInteractionHandler
from bluuberrylibrary.interactions.registration.handlers.bb_interaction_location import \
    BBInteractionLocation
from bluuberrylibrary.logs.bb_log import BBLog
from bluuberrylibrary.mod_identity import ModIdentity
from bluuberrylibrary.utils.debug.bb_injection_utils import BBInjectionUtils
from objects.script_object import ScriptObject
from services.terrain_service import TerrainService
from sims.sim import Sim


class BBInteractionRegistry(metaclass=BBSingleton):
    """A registry for putting interactions onto Sims, Objects, Terrain, and other places.

    """

    def get_log(self) -> BBLog:
        from bluuberrylibrary.logs.bb_log_registry import BBLogRegistry
        return BBLogRegistry().register_log(ModIdentity(), 'bb_interaction_registry')

    def __init__(self) -> None:
        super().__init__()
        self._interaction_handlers: Dict[BBInteractionLocation, List[BBInteractionHandler]] = {
            BBInteractionLocation.TERRAIN: list(),
            BBInteractionLocation.OCEAN: list(),
            BBInteractionLocation.SCRIPT_OBJECT: list(),
            BBInteractionLocation.RELATIONSHIP_PANEL: list(),
            BBInteractionLocation.PHONE: list()
        }

    def register_interaction_handler(self, interaction_handler: BBInteractionHandler):
        """register_interaction_handler(interaction_handler)

        Manually register a handler for interactions.

        :param interaction_handler: The handler being registered.
        :type interaction_handler: BBInteractionHandler
        """
        interaction_location = interaction_handler.registration_location
        if interaction_location not in self._interaction_handlers:
            self._interaction_handlers[interaction_location] = list()
        self._interaction_handlers[interaction_location].append(interaction_handler)

    @classmethod
    def register(cls) -> Callable[..., BBInteractionHandler]:
        """register()

        Make the registry know about your handler.

        Usage:
        @BBInteractionRegistry.register()
        class BBExampleSimHandler(BBSimInteractionHandler):

        :return: A callable that creates an instance.
        :rtype: Callable[[Type[BBInteractionHandler]], BBInteractionHandler]
        """
        def _wrapper(interaction_handler) -> BBInteractionHandler:
            BBInteractionRegistry().register_interaction_handler(interaction_handler())
            return interaction_handler
        return _wrapper

    def _on_script_object_add(self, script_object: ScriptObject):
        log = self.get_log()
        try:
            script_object_type = type(script_object)
            log.debug('Adding interactions for type', script_object_type=script_object_type)
            if not hasattr(script_object_type, '_super_affordances'):
                log.debug('Object did not have super affordances.', script_object=script_object_type)
                return
            new_interactions = list()
            for interaction_handler in self._interaction_handlers[BBInteractionLocation.SCRIPT_OBJECT]:
                log.debug('Running with interaction handler', interaction_handler=interaction_handler)
                if not interaction_handler.should_register(script_object):
                    log.debug('Interaction not being added to object.', script_object=script_object, script_object_type=script_object_type)
                    continue
                for interaction_instance in interaction_handler._get_interactions_gen():
                    if interaction_instance in new_interactions or interaction_instance in script_object_type._super_affordances:
                        log.debug('Interaction was already found in the interactions list.', script_object_type=script_object_type, interaction_instance=interaction_instance)
                        continue
                    new_interactions.append(interaction_instance)
            log.debug('Adding super affordances to object.', script_object=script_object, script_object_type=script_object_type, new_interactions=new_interactions)
            script_object_type._super_affordances += tuple(new_interactions)
            new_object_interactions = list()
            for new_super_affordance in new_interactions:
                if new_super_affordance in script_object._super_affordances:
                    continue
                new_object_interactions.append(new_super_affordance)
            script_object._super_affordances += tuple(new_object_interactions)
        except Exception as ex:
            log.error('Failed to register interactions. Error occurred. 257', exception=ex)

    def _on_sim_relationship_panel_load(self, sim: Sim):
        log = self.get_log()
        try:
            sim_class = type(sim)
            if not hasattr(sim_class, '_relation_panel_affordances'):
                return
            new_interactions = list()
            for interaction_handler in self._interaction_handlers[BBInteractionLocation.RELATIONSHIP_PANEL]:
                if not interaction_handler.should_register(sim):
                    continue
                for interaction_instance in interaction_handler._get_interactions_gen():
                    if interaction_instance in new_interactions or interaction_instance in sim_class._relation_panel_affordances:
                        continue
                    new_interactions.append(interaction_instance)
            sim_class._relation_panel_affordances += tuple(new_interactions)
        except Exception as ex:
            log.error('Failed to register interactions. Error occurred.765', exception=ex)

    def _on_sim_phone_load(self, sim: Sim):
        log = self.get_log()
        try:
            sim_class = type(sim)
            if not hasattr(sim_class, '_phone_affordances'):
                return
            new_interactions = list()
            for interaction_handler in self._interaction_handlers[BBInteractionLocation.PHONE]:
                if not interaction_handler.should_register(sim):
                    continue
                for interaction_instance in interaction_handler._get_interactions_gen():
                    if interaction_instance in new_interactions or interaction_instance in sim_class._phone_affordances:
                        continue
                    new_interactions.append(interaction_instance)
            sim_class._phone_affordances += tuple(new_interactions)
        except Exception as ex:
            log.error('Failed to register interactions. Error occurred.8765', exception=ex)

    def _on_terrain_load(self, terrain_service: TerrainService):
        log = self.get_log()
        try:
            new_interactions = list()
            for interaction_handler in self._interaction_handlers[BBInteractionLocation.TERRAIN]:
                for interaction_instance in interaction_handler._get_interactions_gen():
                    if interaction_instance in new_interactions or interaction_instance in terrain_service.TERRAIN_DEFINITION.cls._super_affordances:
                        continue
                    new_interactions.append(interaction_instance)
            new_terrain_definition_class = terrain_service.TERRAIN_DEFINITION.cls
            new_terrain_definition_class._super_affordances += tuple(new_interactions)
            terrain_service.TERRAIN_DEFINITION.set_class(new_terrain_definition_class)
        except Exception as ex:
            log.error('Failed to register interactions. Error occurred. 898867', exception=ex)

    def _on_ocean_load(self, terrain_service: TerrainService):
        log = self.get_log()
        try:
            new_interactions = list()
            for interaction_handler in self._interaction_handlers[BBInteractionLocation.OCEAN]:
                for interaction_instance in interaction_handler._get_interactions_gen():
                    if interaction_instance in new_interactions or interaction_instance in terrain_service.OCEAN_DEFINITION.cls._super_affordances:
                        continue
                    new_interactions.append(interaction_instance)
            new_ocean_definition_class = terrain_service.OCEAN_DEFINITION.cls
            new_ocean_definition_class._super_affordances += tuple(new_interactions)
            terrain_service.OCEAN_DEFINITION.set_class(new_ocean_definition_class)
        except Exception as ex:
            log.error('Failed to register interactions. Error occurred.98569875', exception=ex)


@BBInjectionUtils.inject(ModIdentity(), ScriptObject, ScriptObject.on_add.__name__, log_errors=False)
def _bbl_on_script_object_load(original, self, *args, **kwargs) -> Any:
    try:
        result = original(self, *args, **kwargs)
        BBInteractionRegistry()._on_script_object_add(self)
        if isinstance(self, Sim):
            BBInteractionRegistry()._on_sim_relationship_panel_load(self)
            BBInteractionRegistry()._on_sim_phone_load(self)
    except Exception as ex:
        from bluuberrylibrary.logs.bb_log_registry import BBLogRegistry
        log = BBLogRegistry().register_log(ModIdentity(), 'bb_interaction_registry')
        log.error('Failed to register interactions 24. Error occurred.', exception=ex)
        return original(self, *args, **kwargs)
    return result


@BBInjectionUtils.inject(ModIdentity(), TerrainService, TerrainService.start.__name__, log_errors=False)
def _bbl_on_terrain_load(original, self, *args, **kwargs) -> Any:
    try:
        result = original(self, *args, **kwargs)
        BBInteractionRegistry()._on_terrain_load(self)
    except Exception as ex:
        from bluuberrylibrary.logs.bb_log_registry import BBLogRegistry
        log = BBLogRegistry().register_log(ModIdentity(), 'bb_interaction_registry')
        log.error('Failed to register interactions 52353. Error occurred.', exception=ex)
        return original(self, *args, **kwargs)
    return result


@BBInjectionUtils.inject(ModIdentity(), TerrainService, TerrainService.on_zone_load.__name__, log_errors=False)
def _bbl_on_ocean_load(original, self, *args, **kwargs) -> Any:
    try:
        result = original(self, *args, **kwargs)
        BBInteractionRegistry()._on_ocean_load(self)
    except Exception as ex:
        from bluuberrylibrary.logs.bb_log_registry import BBLogRegistry
        log = BBLogRegistry().register_log(ModIdentity(), 'bb_interaction_registry')
        log.error('Failed to register interactions. Error occurred 765.', exception=ex)
        return original(self, *args, **kwargs)
    return result
