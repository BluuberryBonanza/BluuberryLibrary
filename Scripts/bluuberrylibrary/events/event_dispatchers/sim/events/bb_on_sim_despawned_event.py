"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from bluuberrylibrary.events.event_handling.bb_event import BBEvent
from bluuberrylibrary.mod_registration.bb_mod_identity import BBModIdentity
from sims.sim_info import SimInfo


class BBOnSimDespawnedEvent(BBEvent):
    """BBOnSimDespawnedEvent(mod_identity, sim_info)

    An event that occurs when a Sim is despawned

    Usage:
        @BBEventHandlerRegistry.register(ModIdentity(), BBOnSimDespawnedEvent)
        def _bbl_handle_on_sim_despawned(event: BBOnSimDespawnedEvent):

    :Example usage:

    .. highlight:: python
    .. code-block:: python

        from bluuberrylibrary.events.event_handling.bb_event_handler_registry import BBEventHandlerRegistry
        from bluuberrylibrary.classes.bb_test_result import BBTestResult

        @BBEventHandlerRegistry.register(ModIdentity(), BBOnSimDespawnedEvent)
        def _bbl_handle_on_sim_despawned(event: BBOnSimDespawnedEvent) -> BBRunResult:
            return BBRunResult.TRUE

    :param mod_identity: The identity of the mod that owns this event.
    :type mod_identity: BBModIdentity
    :param sim_info: The info of a Sim.
    :type sim_info: SimInfo
    """
    def __init__(self, mod_identity: BBModIdentity, sim_info: SimInfo):
        super().__init__(mod_identity)
        self._sim_info = sim_info

    @property
    def sim_info(self) -> SimInfo:
        """The Sim that despawned."""
        return self._sim_info
