"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Type, Callable

from bluuberrylibrary.events.event_handling.bb_event import BBEvent
from bluuberrylibrary.mod_registration.bb_mod_identity import BBModIdentity

# noinspection PyBroadException
try:
    from event_testing.results import TestResult
except:
    class TestResult:
        pass


class BBEventHandler:
    """BBEventHandler(mod_identity, event_type, handler)

    Handles events when they occur.

    :param mod_identity: The identity of the mod that owns this handler.
    :type mod_identity: Union[str, BBModIdentity]
    :param event_type: The type of event being handled.
    :type event_type: Type[BBEvent]
    :param handler: The function that handles events.
    :type handler: Callable[[BBEvent], Any]
    :exception RuntimeError: When event_function is None.
    :exception TypeError: When event_function is not a callable function.
    :exception AssertionError: When the event_function is missing the event_data argument, when the event_function contains a self or cls argument, or when more than one argument is found.
    """
    def __init__(
        self,
        mod_identity: BBModIdentity,
        event_type: Type[BBEvent],
        handler: Callable[[BBEvent], TestResult]
    ):
        self._mod_identity = mod_identity
        self._event_type = event_type
        self._handler = handler

    @property
    def mod_identity(self) -> BBModIdentity:
        """The identity of the mod that owns this handler.

        :return: A mod identity.
        :rtype: BBModIdentity
        """
        return self._mod_identity

    @property
    def handler(self) -> Callable[[BBEvent], TestResult]:
        """The function invoked when the handler handles an event.

        :return: A function invoked upon handling events.
        :rtype: Callable[[BBEvent], TestResult]
        """
        return self._handler

    @property
    def event_type(self) -> Type[BBEvent]:
        """The type of events this handler waits for.

        :return: An event type.
        :rtype: Type[BBEvent]
        """
        return self._event_type

    def can_handle(self, event: BBEvent) -> bool:
        return isinstance(event, self.event_type)

    def handle(self, event: BBEvent) -> TestResult:
        return self._handler(event)
