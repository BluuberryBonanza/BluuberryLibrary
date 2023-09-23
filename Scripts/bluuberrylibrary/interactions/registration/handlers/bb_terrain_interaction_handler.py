"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Tuple, Any

from bluuberrylibrary.interactions.registration.handlers.bb_interaction_handler import BBInteractionHandler
from bluuberrylibrary.interactions.registration.handlers.bb_interaction_location import \
    BBInteractionLocation


class BBTerrainInteractionHandler(BBInteractionHandler):
    """BBTerrainInteractionHandler()

    A handler for registering interactions on the Terrain (Does not include Oceans).

    """
    @property
    def registration_location(self) -> BBInteractionLocation:
        return BBInteractionLocation.TERRAIN

    @property
    def interaction_guids(self) -> Tuple[int]:
        raise NotImplementedError()

    def should_register(self, _: Any) -> bool:
        return True
