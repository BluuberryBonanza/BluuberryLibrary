"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from bluuberrylibrary.events.event_dispatchers.zone.events.bb_on_zone_load_end_event import BBOnZoneLoadEndEvent
from bluuberrylibrary.events.event_handling.bb_event_handler_registry import BBEventHandlerRegistry
from bluuberrylibrary.logs.bb_log_registry import BBLogRegistry
from bluuberrylibrary.mod_identity import ModIdentity
from event_testing.results import TestResult


@BBEventHandlerRegistry.register(ModIdentity(), BBOnZoneLoadEndEvent)
def _bbl_example_on_zone_load_end_event(event: BBOnZoneLoadEndEvent):
    log = BBLogRegistry().register_log(ModIdentity(), 'bb_example_events')
    log.enable()
    log.debug('Ran load event', is_first_load=event.is_first_load, household_id=event.household_id, is_build_mode=event.is_build_mode)
    log.disable()
    return TestResult.TRUE
