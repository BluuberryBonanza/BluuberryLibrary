"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from bluuberrylibrary.classes.bb_run_result import BBRunResult
from bluuberrylibrary.classes.bb_singleton import BBSingleton
from bluuberrylibrary.events.event_handling.bb_event import BBEvent
from event_testing.results import TestResult


class BBEventDispatcher(metaclass=BBSingleton):
    """Dispatches events to :class:`.BBEventHandlerRegistry`"""

    # noinspection PyMethodMayBeStatic
    def dispatch(self, event: BBEvent) -> BBRunResult:
        """dispatch(event)

        Dispatch an event to the Event Registry.

        :param event: The event to dispatch.
        :type event: BBEvent
        :return: The result of dispatch.
        :rtype: BBRunResult
        """
        from bluuberrylibrary.events.event_handling.bb_event_handler_registry import BBEventHandlerRegistry
        return BBEventHandlerRegistry().dispatch(event)
