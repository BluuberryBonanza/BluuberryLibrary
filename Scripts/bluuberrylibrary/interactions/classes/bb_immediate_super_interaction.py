"""
This mod is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) BLUUBERRYBONANZA
"""
from typing import Any

from bluuberrylibrary.logs.bb_log import BBLog
from bluuberrylibrary.logs.bb_log_registry import BBLogRegistry
from bluuberrylibrary.mod_registration.bb_mod_identity import BBModIdentity
from bluuberrylibrary.utils.sims.bb_sim_utils import BBSimUtils
from event_testing.results import TestResult
from interactions.base.immediate_interaction import ImmediateSuperInteraction
from interactions.context import InteractionContext
from interactions.interaction_finisher import FinishingType
from sims.sim import Sim
from sims.sim_info import SimInfo


class BBImmediateSuperInteraction(ImmediateSuperInteraction):
    @classmethod
    def get_mod_identity(cls) -> BBModIdentity:
        """The identity of the mod that owns this class."""
        raise NotImplementedError()

    @classmethod
    def get_log_name(cls) -> str:
        """The name of the log used within the class."""
        raise NotImplementedError()

    @classmethod
    def get_log(cls) -> BBLog:
        return BBLogRegistry().register_log(cls.get_mod_identity(), cls.get_log_name())

    # noinspection PyUnusedLocal
    @classmethod
    def bbl_test(cls, interaction_sim_info: SimInfo, interaction_target: Any, interaction_context: InteractionContext, *args, **kwargs) -> TestResult:
        """bbl_test(interaction_sim_info, interaction_target, interaction_context, *args, **kwargs)

        Occurs when testing the interaction.

        :param interaction_sim_info: The source Sim of the interaction.
        :type interaction_sim_info: SimInfo
        :param interaction_target: The target Object of the interaction.
        :type interaction_target: Any
        :param interaction_context: The context of the interaction.
        :type interaction_context: InteractionContext
        :return: The outcome of testing the availability of the interaction
        :rtype: TestResult
        """
        return TestResult.TRUE

    # noinspection PyUnusedLocal
    def bbl_started(self, interaction_sim_info: SimInfo, interaction_target: Any) -> TestResult:
        """bbl_started(interaction_sim_info, interaction_target)

        Occurs when starting the interaction.

        :param interaction_sim_info: The source Sim of the interaction.
        :type interaction_sim_info: SimInfo
        :param interaction_target: The target Object of the interaction.
        :type interaction_target: Any
        :return: The result of running the start function. True, if the interaction hook was executed successfully. False, if the interaction hook was not executed successfully.
        :rtype: TestResult
        """
        return TestResult.TRUE

    @classmethod
    def _test(cls, target: Any, context: InteractionContext, **kwargs) -> TestResult:
        from event_testing.results import TestResult
        log = cls.get_log()
        try:
            sim_info = BBSimUtils.to_sim_info(context.sim)
            target_sim_info = target
            if target_sim_info is not None and isinstance(target_sim_info, Sim):
                target_sim_info = BBSimUtils.to_sim_info(target_sim_info)
            test_result = cls.bbl_test(sim_info, target_sim_info, context, **kwargs)
            if not test_result:
                return test_result
        except Exception as ex:
            log.error(f'Error happened while running bbl_test of \'{cls.__name__}\'.', exception=ex)
            return TestResult(False, f'An error happened {ex} running bbl_test.')

        try:
            return super()._test(target, context, **kwargs)
        except Exception as ex:
            log.error(f'Error happened while running _test of \'{cls.__name__}\'.', exception=ex)
            return TestResult(False, f'An error happened {ex} running _test.')

    def _trigger_interaction_start_event(self: 'BBImmediateSuperInteraction'):
        log = self.get_log()
        try:
            sim_info = BBSimUtils.to_sim_info(self.sim)
            target = self.target
            if target is not None and isinstance(target, Sim):
                target = BBSimUtils.to_sim_info(self.target)
            result = self.bbl_started(sim_info, target)
            if result is not None and result.result:
                self.cancel(FinishingType.CONDITIONAL_EXIT, str(result))
                return
        except Exception as ex:
            log.error(f'Error happened when running bbl_started \'{self.__class__.__name__}\'.', exception=ex)

        try:
            return super()._trigger_interaction_start_event()
        except Exception as ex:
            log.error(f'Error happened while running _trigger_interaction_start_event of \'{self.__class__.__name__}\'.', exception=ex)
