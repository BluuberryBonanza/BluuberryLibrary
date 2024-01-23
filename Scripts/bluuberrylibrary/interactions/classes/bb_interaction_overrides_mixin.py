"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Any

from bluuberrylibrary.classes.bb_run_result import BBRunResult
from bluuberrylibrary.classes.bb_test_result import BBTestResult
from interactions.context import InteractionContext
from interactions.interaction_finisher import FinishingType
from scheduling import Timeline
from sims.sim_info import SimInfo


class BBInteractionOverridesMixin:
    """An interaction that occurs immediately when the player selects it. The Sim will not queue it."""
    # noinspection PyUnusedLocal
    @classmethod
    def bbl_test(cls, interaction_sim_info: SimInfo, interaction_target: Any, interaction_context: InteractionContext, *args, **kwargs) -> BBTestResult:
        """bbl_test(interaction_sim_info, interaction_target, interaction_context, *args, **kwargs)

        Occurs when testing the interaction.

        :param interaction_sim_info: The source Sim of the interaction.
        :type interaction_sim_info: SimInfo
        :param interaction_target: The target Object of the interaction.
        :type interaction_target: Any
        :param interaction_context: The context of the interaction.
        :type interaction_context: InteractionContext
        :return: The outcome of testing the availability of the interaction
        :rtype: BBTestResult
        """
        return BBTestResult.TRUE

    # noinspection PyUnusedLocal
    def bbl_started(self, interaction_sim_info: SimInfo, interaction_target: Any) -> BBRunResult:
        """bbl_started(interaction_sim_info, interaction_target)

        Occurs when starting the interaction.

        :param interaction_sim_info: The source Sim of the interaction.
        :type interaction_sim_info: SimInfo
        :param interaction_target: The target Object of the interaction.
        :type interaction_target: Any
        :return: The result of running the start function. True, if the interaction hook was executed successfully. False, if the interaction hook was not executed successfully.
        :rtype: BBRunResult
        """
        return BBRunResult.TRUE

    def bbl_run(self, interaction_sim_info: SimInfo, interaction_target: Any, timeline: Timeline) -> BBRunResult:
        """bbl_run(interaction_sim_info, interaction_target, timeline)

        Occurs when the interaction runs.

        :param interaction_sim_info: The source Sim of the interaction.
        :type interaction_sim_info: SimInfo
        :param interaction_target: The target Object of the interaction.
        :type interaction_target: Any
        :param timeline: The timeline.
        :type timeline: Timeline
        :return: The result of running function. True, if the interaction hook was executed successfully. False, if the interaction hook was not executed successfully.
        :rtype: BBRunResult
        """
        return BBRunResult.TRUE

    def bbl_cancelled(self, interaction_sim_info: SimInfo, interaction_target: Any, interaction_context: InteractionContext, finishing_type: FinishingType, cancel_reason: str, **kwargs) -> BBRunResult:
        """bbl_cancelled(interaction_sim_info, interaction_target, interaction_context, finishing_type, cancel_reason, **kwargs)

        Occurs when the interaction is cancelled.

        :param interaction_sim_info: The source Sim of the interaction.
        :type interaction_sim_info: SimInfo
        :param interaction_target: The target Object of the interaction.
        :type interaction_target: Any
        :param interaction_context: The context of the interaction.
        :type interaction_context: InteractionContext
        :param finishing_type: The type of cancel.
        :type finishing_type: FinishingType
        :param cancel_reason: The reason for cancellation.
        :type cancel_reason: str
        :return: The result of running the function. True, if the interaction hook was executed successfully. False, if the interaction hook was not executed successfully.
        :rtype: BBRunResult
        """
        return BBRunResult.TRUE
