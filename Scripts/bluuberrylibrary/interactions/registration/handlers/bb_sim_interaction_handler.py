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
from sims.sim import Sim


class BBSimInteractionHandler(BBInteractionHandler):
    """BBSimInteractionHandler()

    A handler for registering interactions on Sims.

    .. highlight:: python
    .. code-block:: python

        @BBInteractionRegistry.register()
        class _ExampleSimInteractionRegistration(BBSimInteractionHandler):

            @property
            def interaction_guids(self) -> Tuple[int]:
                return (
                    12345,
                )

            def should_register(self, sim: Sim) -> bool:
                super_result = super().should_register(sim)
                if not super_result:
                    return super_result
                # Only register these interactions to Young Adult Sims.
                return sim.age == Age.YOUNGADULT

    """
    @property
    def registration_location(self) -> BBInteractionLocation:
        return BBInteractionLocation.SCRIPT_OBJECT

    @property
    def interaction_guids(self) -> Tuple[int]:
        raise NotImplementedError()

    def should_register(self, sim: Sim) -> bool:
        return isinstance(sim, Sim) or (hasattr(sim, 'is_sim') and sim.is_sim)
