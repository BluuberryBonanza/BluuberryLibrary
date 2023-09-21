"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from bluuberrylibrary.events.event_dispatchers.bb_event_dispatcher import BBEventDispatcher
from bluuberrylibrary.mod_identity import ModIdentity
from bluuberrylibrary.utils.debug.bb_injection_utils import BBInjectionUtils
from event_testing.results import TestResult
from server.client import Client
from zone import Zone


class BBZoneEventDispatcher(BBEventDispatcher):
    """Dispatches event related to Zones"""

    def __init__(self):
        super().__init__()
        self._client_finished_first_load = False
        self._client_is_loading = True

    @property
    def client_is_loading(self) -> bool:
        """True, if the client is currently loading (In a loading screen). False, if not."""
        return self._client_is_loading

    @property
    def client_finished_first_load(self) -> bool:
        """True, if the client has finished loading for the very first time. False, if not."""
        return self._client_finished_first_load

    def on_zone_load_finished(self, zone: Zone, household_id: int, is_build_mode: bool) -> TestResult:
        """on_zone_load_finished(zone, household_id, is_build_mode)

        Dispatch an event when a zone finishes loading.

        :param zone: The zone that finished loading.
        :type zone: Zone
        :param household_id: The id of the household that finished loading.
        :type household_id: int
        :param is_build_mode: True, if the client loaded into Build Mode. False, if the client loaded into Live Mode.
        :type is_build_mode: bool
        :return: The result of dispatching the event. True, if successful. False, if not.
        :rtype: TestResult
        """
        from bluuberrylibrary.events.event_dispatchers.zone.events.bb_on_zone_load_end_event import BBOnZoneLoadEndEvent
        event = BBOnZoneLoadEndEvent(ModIdentity(), zone, household_id, is_build_mode, self.client_finished_first_load)
        result = self.dispatch(event)
        self._client_finished_first_load = True
        self._client_is_loading = False
        return result

    def on_zone_load_started(self, zone: Zone) -> TestResult:
        """on_zone_load_started(zone)

        Dispatch an event when a Zone starts loading.

        :param zone: The zone that started to load.
        :type zone: Zone
        :return: The result of dispatching the event. True, if successful. False, if not.
        :rtype: TestResult
        """
        self._client_is_loading = True
        from bluuberrylibrary.events.event_dispatchers.zone.events.bb_on_zone_load_start_event import \
            BBOnZoneLoadStartEvent
        event = BBOnZoneLoadStartEvent(ModIdentity(), zone, self.client_finished_first_load)
        result = self.dispatch(event)
        return result

    def on_zone_unload_started(self, zone: Zone, client: Client) -> TestResult:
        """on_zone_unload_started(zone, client)

        Dispatch an event when a Zone starts unloading.

        :param zone: The zone that started to unload.
        :type zone: Zone
        :param client: The client being unloaded.
        :type client: Client
        :return: The result of dispatching the event. True, if successful. False, if not.
        :rtype: TestResult
        """
        self._client_is_loading = True
        from bluuberrylibrary.events.event_dispatchers.zone.events.bb_on_zone_unload_start_event import \
            BBOnZoneUnloadStartEvent
        event = BBOnZoneUnloadStartEvent(ModIdentity(), zone, client)
        result = self.dispatch(event)
        return result


@BBInjectionUtils.inject(ModIdentity(), Zone, Zone.load_zone.__name__, log_errors=False)
def _bbl_on_zone_load_start(original, self: Zone, *args, **kwargs):
    result = original(self, *args, **kwargs)
    BBZoneEventDispatcher().on_zone_load_started(self)
    return result


@BBInjectionUtils.inject(ModIdentity(), Zone, Zone.do_zone_spin_up.__name__, log_errors=False)
def _bbl_on_zone_finished_loading(original, self: Zone, household_id: int, *args, **kwargs):
    result = original(self, household_id, *args, **kwargs)
    BBZoneEventDispatcher().on_zone_load_finished(self, household_id, False)
    return result


@BBInjectionUtils.inject(ModIdentity(), Zone, Zone.do_build_mode_zone_spin_up.__name__, log_errors=False)
def _bbl_on_zone_finished_loading_to_build_mode(original, self: Zone, household_id: int, *args, **kwargs):
    result = original(self, household_id, *args, **kwargs)
    BBZoneEventDispatcher().on_zone_load_finished(self, household_id, True)
    return result


@BBInjectionUtils.inject(ModIdentity(), Zone, Zone.on_teardown.__name__, log_errors=False)
def _bbl_on_zone_unload(original, self: Zone, client: Client):
    BBZoneEventDispatcher().on_zone_unload_started(self, client)
    return original(self, client)
