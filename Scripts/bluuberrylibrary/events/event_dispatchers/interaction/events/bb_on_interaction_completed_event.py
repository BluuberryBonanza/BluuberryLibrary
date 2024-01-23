"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Union

from bluuberrylibrary.events.event_handling.bb_event import BBEvent
from bluuberrylibrary.mod_registration.bb_mod_identity import BBModIdentity
from interactions.base.interaction import Interaction
from objects.game_object import GameObject
from sims.sim import Sim
from sims.sim_info import SimInfo


class BBOnInteractionCompletedEvent(BBEvent):
    """BBOnInteractionCompletedEvent(\
        mod_identity,\
        sim_info,\
        interaction,\
        target\
    )

    An event that occurs when a Sim finished performing an interaction.

    Usage:
        @BBEventHandlerRegistry.register(ModIdentity(), BBOnInteractionCompletedEvent)
        def _bbl_handle_on_interaction_completed(event: BBOnInteractionCompletedEvent):

    :Example usage:

    .. highlight:: python
    .. code-block:: python

        from bluuberrylibrary.events.event_handling.bb_event_handler_registry import BBEventHandlerRegistry
        from bluuberrylibrary.classes.bb_test_result import BBTestResult

        @BBEventHandlerRegistry.register(ModIdentity(), BBOnInteractionCompletedEvent)
        def _bbl_handle_on_interaction_completed(event: BBOnInteractionCompletedEvent) -> BBRunResult:
            return BBRunResult.TRUE

    :param mod_identity: The identity of the mod that owns this event.
    :type mod_identity: BBModIdentity
    :param sim_info: The info of a Sim.
    :type sim_info: SimInfo
    :param interaction: The interaction that was completed.
    :type interaction: Interaction
    :param target: The target of the interaction.
    :type target: GameObject or Sim
    """
    def __init__(self, mod_identity: BBModIdentity, sim_info: SimInfo, interaction: Interaction, target: Union[GameObject, Sim]):
        super().__init__(mod_identity)
        self._sim_info = sim_info
        self._interaction = interaction
        if target is not None and isinstance(target, Sim):
            from bluuberrylibrary.utils.sims.bb_sim_utils import BBSimUtils
            target = BBSimUtils.to_sim_info(target)
        self._target = target

    @property
    def sim_info(self) -> SimInfo:
        """The Sim that performed the interaction."""
        return self._sim_info

    @property
    def interaction(self) -> Interaction:
        """The interaction that was completed."""
        return self._interaction

    @property
    def target(self) -> Union[GameObject, Sim]:
        """The target of the interaction."""
        return self._target

    @property
    def was_user_cancelled(self) -> bool:
        """True, if the interaction was cancelled by the Player. False, if the interaction was not cancelled by the Player."""
        return self.interaction.has_been_user_canceled

    @property
    def finished_naturally(self) -> bool:
        """True, if the interaction exited on its own. False, if the interaction did not exit on its own, for example, being cancelled by the Player."""
        return self.interaction.is_finishing_naturally
