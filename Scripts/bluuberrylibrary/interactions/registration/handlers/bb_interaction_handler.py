"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Tuple, Iterator

from bluuberrylibrary.interactions.registration.handlers.bb_interaction_location import BBInteractionLocation
from bluuberrylibrary.utils.instances.bb_interaction_utils import BBInteractionUtils
from interactions.base.interaction import Interaction
from objects.script_object import ScriptObject


class BBInteractionHandler:
    """BBInteractionHandler()

    A handler for registering interactions on script objects.

    """

    def __init__(self) -> None:
        self._interactions = None

    @property
    def registration_location(self) -> BBInteractionLocation:
        """The location for which interactions will be registered."""
        raise NotImplementedError()

    @property
    def interaction_guids(self) -> Tuple[int]:
        """A collection of interaction GUIDs to register."""
        raise NotImplementedError()

    def _get_interactions_gen(self) -> Iterator[Interaction]:
        if self._interactions is not None:
            yield from self._interactions
        else:
            import services
            from sims4.resources import Types
            affordance_manager = services.get_instance_manager(Types.INTERACTION)
            interactions = list()
            for interaction_guid in self.interaction_guids:
                interaction = affordance_manager.get(interaction_guid)
                if interaction is None:
                    raise Exception(f'No interaction found with id {interaction_guid} with {interaction}')
                yield interaction
                interactions.append(interaction)
            self._interactions = tuple(interactions)

    def should_register(self, script_object: ScriptObject) -> bool:
        """should_register(script_object)

        Determine if the interactions should be registered to the specified script object.

        :param script_object: The object to check.
        :type script_object: ScriptObject
        :return: True, if the interactions should register to the object. False, if not.
        :rtype: bool
        """
        raise NotImplementedError()
