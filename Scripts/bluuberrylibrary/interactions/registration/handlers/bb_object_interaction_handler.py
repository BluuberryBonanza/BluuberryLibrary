"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Tuple

from bluuberrylibrary.interactions.registration.handlers.bb_interaction_handler import BBInteractionHandler
from bluuberrylibrary.interactions.registration.handlers.bb_interaction_location import \
    BBInteractionLocation
from objects.game_object import GameObject
from sims.sim import Sim
from sims.sim_info import SimInfo


class BBObjectInteractionHandler(BBInteractionHandler):
    """BBObjectInteractionHandler()

    A handler for registering interactions on Game Objects that are not Sims.

    .. highlight:: python
    .. code-block:: python

        @BBInteractionRegistry.register()
        class _ExampleObjectInteractionRegistration(BBObjectInteractionHandler):

            @property
            def interaction_guids(self) -> Tuple[int]:
                return (
                    12345,
                )

            def should_register(self, game_object: GameObject) -> bool:
                super_result = super().should_register(game_object)
                if not super_result:
                    return super_result
                # If matches specific id.
                return game_object.id == 5678

    """
    @property
    def registration_location(self) -> BBInteractionLocation:
        return BBInteractionLocation.SCRIPT_OBJECT

    @property
    def interaction_guids(self) -> Tuple[int]:
        raise NotImplementedError()

    def should_register(self, game_object: GameObject) -> bool:
        return (isinstance(game_object, GameObject)
                and not isinstance(game_object, Sim)
                and not isinstance(game_object, SimInfo))
