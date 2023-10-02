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


class BBRelationshipPanelInteractionHandler(BBInteractionHandler):
    """BBRelationshipPanelInteractionHandler()

    A handler for registering interactions on the Relationship Panel.

    .. highlight:: python
    .. code-block:: python

        @BBInteractionRegistry.register()
        class _ExampleRelationshipPanelInteractionRegistration(BBRelationshipPanelInteractionHandler):

            @property
            def interaction_guids(self) -> Tuple[int]:
                return (
                    12345,
                )

    """
    @property
    def registration_location(self) -> BBInteractionLocation:
        return BBInteractionLocation.RELATIONSHIP_PANEL

    @property
    def interaction_guids(self) -> Tuple[int]:
        raise NotImplementedError()

    def should_register(self, _: Any) -> bool:
        return True
