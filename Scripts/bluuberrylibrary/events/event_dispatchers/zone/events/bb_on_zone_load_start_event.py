"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from bluuberrylibrary.events.event_handling.bb_event import BBEvent
from bluuberrylibrary.mod_registration.bb_mod_identity import BBModIdentity
from zone import Zone


class BBOnZoneLoadStartEvent(BBEvent):
    """BBOnZoneLoadStartEvent(mod_identity, zone, is_first_load)
    An event that occurs when a Zone starts loading.

    Usage:
        @BBEventHandlerRegistry.register(ModIdentity(), BBOnZoneLoadStartEvent)
        def _bbl_handle_on_zone_load_start(event: BBOnZoneLoadStartEvent):

    :Example usage:

    .. highlight:: python
    .. code-block:: python

        from bluuberrylibrary.events.event_handling.bb_event_handler_registry import BBEventHandlerRegistry
        from event_testing.results import TestResult

        @BBEventHandlerRegistry.register(ModIdentity(), BBOnZoneLoadStartEvent)
        def _bbl_handle_on_zone_load_start(event: BBOnZoneLoadStartEvent):
            return TestResult.TRUE

    :param mod_identity: The identity of the mod that owns this event.
    :type mod_identity: BBModIdentity
    :param zone: An instance of the Zone that was loaded.
    :type zone: Zone
    :param is_first_load: True, indicates this is the first time the client has loaded into a zone. False, if the client has previously loaded into a zone.
    :type is_first_load: bool
    """
    def __init__(self, mod_identity: BBModIdentity, zone: Zone, is_first_load: bool):
        super().__init__(mod_identity)
        self._zone = zone
        self._is_first_load = is_first_load

    @property
    def zone(self) -> Zone:
        """The Zone that started loading."""
        return self._zone

    @property
    def is_first_load(self) -> bool:
        """True, if this the first load of the game. False, if not."""
        return self._is_first_load
