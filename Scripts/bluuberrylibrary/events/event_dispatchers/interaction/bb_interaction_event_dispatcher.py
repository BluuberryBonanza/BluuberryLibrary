"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
import services
from bluuberrylibrary.classes.bb_run_result import BBRunResult
from bluuberrylibrary.events.event_dispatchers.bb_event_dispatcher import BBEventDispatcher
from bluuberrylibrary.events.event_dispatchers.interaction.events.bb_on_interaction_completed_event import \
    BBOnInteractionCompletedEvent
from bluuberrylibrary.events.event_dispatchers.zone.events.bb_on_zone_load_end_event import BBOnZoneLoadEndEvent
from bluuberrylibrary.events.event_handling.bb_event_handler_registry import BBEventHandlerRegistry
from bluuberrylibrary.mod_identity import ModIdentity
from event_testing.test_events import TestEvent
from interactions import ParticipantType


class BBInteractionEventDispatcher(BBEventDispatcher):
    """Dispatches event related to Interactions"""

    def __init__(self):
        super().__init__()
        services.get_event_manager().register_single_event(self, TestEvent.InteractionComplete)

    def handle_event(self, sim_info, event, resolver):
        if event == TestEvent.InteractionComplete:
            interaction = resolver.interaction
            target_object = resolver.get_participant(ParticipantType.Object)
            self.dispatch(BBOnInteractionCompletedEvent(ModIdentity(), sim_info, interaction, target_object))


@BBEventHandlerRegistry.register(ModIdentity(), BBOnZoneLoadEndEvent)
def _bbl_example_on_zone_load_end_event(event: BBOnZoneLoadEndEvent):
    BBInteractionEventDispatcher()
    return BBRunResult.TRUE
