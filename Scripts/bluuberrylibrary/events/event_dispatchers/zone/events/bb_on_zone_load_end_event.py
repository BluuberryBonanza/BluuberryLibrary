"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from bluuberrylibrary.events.event_handling.bb_event import BBEvent
from bluuberrylibrary.mod_registration.bb_mod_identity import BBModIdentity
from zone import Zone


class BBOnZoneLoadEndEvent(BBEvent):
    """BBOnZoneLoadEndEvent(mod_identity, zone, is_first_load)
    An event that occurs when a Zone finishes loading.

    Usage:
        @BBEventHandlerRegistry.register(ModIdentity(), BBOnZoneLoadEndEvent)
        def _bbl_handle_on_zone_load_end(event: BBOnZoneLoadEndEvent):

    :Example usage:

    .. highlight:: python
    .. code-block:: python

        from bluuberrylibrary.events.event_handling.bb_event_handler_registry import BBEventHandlerRegistry
        from event_testing.results import TestResult

        @BBEventHandlerRegistry.register(ModIdentity(), BBOnZoneLoadEndEvent)
        def _bbl_handle_on_zone_load_end(event: BBOnZoneLoadEndEvent):
            return TestResult.TRUE

    :param mod_identity: The identity of the mod that owns this event.
    :type mod_identity: BBModIdentity
    :param zone: An instance of the Zone that was loaded.
    :type zone: Zone
    :param household_id: The id of the household that was loaded.
    :type household_id: int
    :param is_build_mode: True, indicates the client loaded into Build Mode. (No Sims are selected) False, indicates the client loaded into Live Mode.
    :type is_build_mode: bool
    :param is_first_load: True, indicates this is the first time the client has loaded into a zone. False, if the client has previously loaded into a zone.
    :type is_first_load: bool
    """
    def __init__(self, mod_identity: BBModIdentity, zone: Zone, household_id: int, is_build_mode: bool, is_first_load: bool):
        super().__init__(mod_identity)
        self._zone = zone
        self._household_id = household_id
        self._is_build_mode = is_build_mode
        self._is_first_load = is_first_load

    @property
    def zone(self) -> Zone:
        """The zone that finished loading."""
        return self._zone

    @property
    def household_id(self) -> int:
        """The id of the household being loaded."""
        return self._household_id

    @property
    def is_build_mode(self) -> bool:
        """True, if the client loaded into build mode. False, if the client loaded into Live mode."""
        return self._is_build_mode

    @property
    def is_first_load(self) -> bool:
        """True, if this the first load of the game. False, if not."""
        return self._is_first_load
