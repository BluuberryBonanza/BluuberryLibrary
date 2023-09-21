from typing import Any, Type, List, Callable

from bluuberrylibrary.events.event_handling.bb_event import BBEvent
from bluuberrylibrary.events.event_handling.bb_event_handler import BBEventHandler
from bluuberrylibrary.mod_registration.bb_mod_identity import BBModIdentity
from bluuberrylibrary.classes.bb_singleton import BBSingleton

# noinspection PyBroadException
try:
    from event_testing.results import TestResult
except:
    class TestResult:
        pass


class BBEventHandlerRegistry(metaclass=BBSingleton):
    """Register event handlers and dispatch events to those handlers.
    Usage:
    @BBEventHandlerRegistry().register(ModIdentity(), BBEvent())
    def _bbl_handle_on_zone_load_event(event: BBEvent):

    """
    def __init__(self):
        self._event_handlers: List[BBEventHandler] = []

    def dispatch(self, event: BBEvent) -> TestResult:
        """dispatch(event)

        Dispatch an event to all listening handlers.

        :param event: An event to dispatch.
        :type event: BBEvent
        :return: The result of dispatching the event.
        :rtype: TestResult
        """
        all_success = TestResult.TRUE
        for event_handler in self._event_handlers:
            if event_handler.can_handle(event):
                try:
                    result = event_handler.handle(event)
                    if not result:
                        all_success = result
                except Exception as ex:
                    from bluuberrylibrary.logs.bb_log_registry import BBLogRegistry
                    _log = BBLogRegistry().register_log(event_handler.mod_identity, 'bb_event_dispatcher')
                    _log.error(f'An error occurred in {event_handler.handler.__name__} while handling event {event}.', exception=ex, event=event, event_handler=event_handler, handling_function=event_handler.handler)
        return all_success

    @staticmethod
    def register(mod_identity: BBModIdentity, event_type: Type[BBEvent]) -> Callable[[Callable[[BBEvent], TestResult]], Callable[[BBEvent], TestResult]]:
        """register(mod_identity, event_type)

        Register a function as a handler of events.

        :param mod_identity: The identity of the mod that owns the handler.
        :type mod_identity: BBModIdentity
        :param event_type: The type of event being handled.
        :type event_type: Type[BBEvent]
        :return: A function that will handle events.
        :rtype: Callable[[Callable[[BBEvent], TestResult]], Callable[[BBEvent], TestResult]]
        """
        def _wrapped(handler: Callable[[BBEvent], TestResult]) -> Callable[..., Any]:
            BBEventHandlerRegistry().register_handler(mod_identity, event_type, handler)
            return handler
        return _wrapped

    def register_handler(self, mod_identity: BBModIdentity, event_type: Type[BBEvent], handler: Callable[[BBEvent], TestResult]) -> BBEventHandler:
        """register_handler(mod_identity, event_type, handler)

        Register a handler of events.

        :param mod_identity: The identity of the mod that owns the handler.
        :type mod_identity: BBModIdentity
        :param event_type: The type of events to be handled.
        :type event_type: Type[BBEvent]
        :param handler: A function listening for events.
        :type handler: Callable[[BBEvent], TestResult]
        :return: An event handler that will receive events.
        :rtype: BBEventHandler
        """
        event_handler = BBEventHandler(mod_identity, event_type, handler)
        self._event_handlers.append(event_handler)
        return event_handler

    def unregister_handler(self, event_handler: BBEventHandler):
        """unregister_handler(event_handler)

        Unregister a handler manually from receiving events.

        :param event_handler: The event handler being unregistered.
        :type event_handler: BBEventHandler
        """
        if event_handler in self._event_handlers:
            self._event_handlers.remove(event_handler)
