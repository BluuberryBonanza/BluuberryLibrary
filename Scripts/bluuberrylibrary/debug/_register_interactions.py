"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Tuple

from bluuberrylibrary.enums.interaction_ids import BBLInteractionId
from bluuberrylibrary.interactions.registration.bb_interaction_registry import BBInteractionRegistry
from bluuberrylibrary.interactions.registration.handlers.bb_object_interaction_handler import BBObjectInteractionHandler
from bluuberrylibrary.interactions.registration.handlers.bb_ocean_interaction_handler import BBOceanInteractionHandler
from bluuberrylibrary.interactions.registration.handlers.bb_sim_interaction_handler import BBSimInteractionHandler
from bluuberrylibrary.interactions.registration.handlers.bb_terrain_interaction_handler import \
    BBTerrainInteractionHandler


@BBInteractionRegistry.register()
class _BBLSimInteractionRegistration(BBSimInteractionHandler):

    @property
    def interaction_guids(self) -> Tuple[int]:
        # noinspection PyTypeChecker
        return (
            BBLInteractionId.BBL_DEBUG_SHOW_INTERACTIONS,
            BBLInteractionId.BBL_DEBUG_SHOW_SITUATIONS,
            BBLInteractionId.BBL_DEBUG_SHOW_TRAITS,
            BBLInteractionId.BBL_DEBUG_CHANGE_OBJECT_STATES
        )


@BBInteractionRegistry.register()
class _BBLObjectInteractionRegistration(BBObjectInteractionHandler):

    @property
    def interaction_guids(self) -> Tuple[int]:
        # noinspection PyTypeChecker
        return (
            BBLInteractionId.BBL_DEBUG_CHANGE_OBJECT_STATES,
        )


@BBInteractionRegistry.register()
class _BBLOceanInteractionRegistration(BBOceanInteractionHandler):

    @property
    def interaction_guids(self) -> Tuple[int]:
        # noinspection PyTypeChecker
        return (
            BBLInteractionId.BBL_DEBUG_CHANGE_OBJECT_STATES,
        )


@BBInteractionRegistry.register()
class _BBLTerrainInteractionRegistration(BBTerrainInteractionHandler):

    @property
    def interaction_guids(self) -> Tuple[int]:
        # noinspection PyTypeChecker
        return (
            BBLInteractionId.BBL_DEBUG_CHANGE_OBJECT_STATES,
        )
