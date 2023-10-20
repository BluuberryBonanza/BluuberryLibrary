"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from bluuberrylibrary.events.event_handling.bb_event import BBEvent
from bluuberrylibrary.mod_registration.bb_mod_identity import BBModIdentity
from server.client import Client
from zone import Zone


class BBOnZoneUnloadStartEvent(BBEvent):
    """BBOnZoneUnloadStartEvent(mod_identity, zone)
    An event that occurs when a Zone starts unloading.

    Usage:
        @BBEventHandlerRegistry.register(ModIdentity(), BBOnZoneUnloadStartEvent)
        def _bbl_handle_on_zone_unload_start(event: BBOnZoneUnloadStartEvent):

    :Example usage:

    .. highlight:: python
    .. code-block:: python

        from bluuberrylibrary.events.event_handling.bb_event_handler_registry import BBEventHandlerRegistry
        from bluuberrylibrary.classes.bb_test_result import BBTestResult

        @BBEventHandlerRegistry.register(ModIdentity(), BBOnZoneUnloadStartEvent)
        def _bbl_handle_on_zone_unload_start(event: BBOnZoneUnloadStartEvent):
            return BBTestResult.TRUE

    :param mod_identity: The identity of the mod that owns this event.
    :type mod_identity: BBModIdentity
    :param zone: An instance of the Zone that was loaded.
    :type zone: Zone
    :param client: The client performing the action.
    :type client: Client
    """
    def __init__(self, mod_identity: BBModIdentity, zone: Zone, client: Client):
        super().__init__(mod_identity)
        self._zone = zone
        self._client = client

    @property
    def zone(self) -> Zone:
        """The zone that finished loading."""
        return self._zone

    @property
    def client(self) -> Client:
        """The client performing the action."""
        return self._client
